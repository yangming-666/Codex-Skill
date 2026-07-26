#!/usr/bin/env python3
"""Search Dota 2 sound events and resources inside `pak01_dir.vpk`.

This helper supports two entry points:
- search directly from a sound token / event name
- scan Lua / Panorama / KV source files for sound API calls, then resolve them

It is intentionally heuristic-friendly:
- it scans compiled soundevent and sound resource files
- it extracts printable strings from binary assets
- it reports candidate event names, API calls, and resource paths
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

PRINTABLE_RE = re.compile(rb"[ -~]{5,}")
SOUND_FILE_RE = re.compile(r"^(soundevents|sounds)/.+\.(vsndevts_c|vsnd_c)$", re.IGNORECASE)
RESOURCE_RE = re.compile(r"(sounds/[A-Za-z0-9_./\-]+\.vsnd(?:evts)?(?:_c)?)", re.IGNORECASE)
EVENT_HINT_RE = re.compile(r"[A-Za-z0-9_]+\.[A-Za-z0-9_.]+")
SOURCE_FILE_RE = re.compile(r"\.(lua|js|ts|xml|txt|kv|vsndevts)$", re.IGNORECASE)
SOUND_API_RE = re.compile(
    r"\b(?P<api>"
    r"Game\.EmitSound|"
    r"EmitSoundOnLocationWithCaster|"
    r"EmitSoundOn|"
    r"EmitSound|"
    r"StopSoundEvent|"
    r"StopSoundOn|"
    r"StopSound|"
    r"PrecacheSoundScript|"
    r"PrecacheResource"
    r")\s*\(",
    re.IGNORECASE,
)
STRING_ARG_RE = re.compile(r"""['"]([^'"]+)['"]""")
ASSIGNMENT_RE = re.compile(r"^\s*(?:local\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*['\"]([^'\"]+)['\"]")
WRAPPED_IDENTIFIER_RE = re.compile(r"(?:String|tostring)\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)")
VSNDEVTS_EVENT_RE = re.compile(r'^\s*"([^"]+)"\s*=\s*$')
VSNDEVTS_RESOURCE_RE = re.compile(r'vsnd_files\s*=\s*(?:"([^"]+)"|\[(.*?)\])', re.IGNORECASE | re.DOTALL)


@dataclass
class Match:
    path: str
    category: str
    score: int
    matched_strings: list[str]
    resource_strings: list[str]
    source_hints: list[str]


@dataclass
class CodeHit:
    path: str
    line_number: int
    api: str
    argument: str
    line: str
    resource_hints: list[str]


def resolve_vpk_path(explicit: str | None) -> Path:
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    env_path = os.environ.get("DOTA2_VPK_PATH")
    if env_path:
        candidates.append(Path(env_path))
    if os.name == "nt":
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            root = Path(f"{letter}:/")
            if not root.exists():
                continue
            for relative in (
                "Steam/steamapps/common/dota 2 beta/game/dota/pak01_dir.vpk",
                "SteamLibrary/steamapps/common/dota 2 beta/game/dota/pak01_dir.vpk",
                "Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/pak01_dir.vpk",
            ):
                candidates.append(root / relative)
    for path in candidates:
        if path and path.exists():
            return path
    raise FileNotFoundError(
        "Could not find pak01_dir.vpk. Set DOTA2_VPK_PATH or pass --vpk-path."
    )


def printable_strings(blob: bytes) -> list[str]:
    return [s.decode("utf-8", "ignore") for s in PRINTABLE_RE.findall(blob)]


def tokenize(query: str) -> list[str]:
    return [part.lower() for part in re.split(r"[^A-Za-z0-9]+", query) if len(part) >= 3]


def dedupe_terms(raw_terms: Iterable[str]) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()
    for raw in raw_terms:
        term = raw.strip().lower()
        if term and term not in seen:
            seen.add(term)
            terms.append(term)
    return terms


def extract_call_body(line: str, open_index: int) -> str:
    depth = 1
    in_quote: str | None = None
    escape = False
    body_start = open_index + 1
    for index in range(body_start, len(line)):
        char = line[index]
        if in_quote:
            if escape:
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char == in_quote:
                in_quote = None
            continue
        if char in ("'", '"'):
            in_quote = char
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return line[body_start:index]
    return line[body_start:]


def split_top_level_args(arg_text: str) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    in_quote: str | None = None
    escape = False
    for char in arg_text:
        if in_quote:
            current.append(char)
            if escape:
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char == in_quote:
                in_quote = None
            continue
        if char in ("'", '"'):
            in_quote = char
            current.append(char)
            continue
        if char == "(":
            depth += 1
            current.append(char)
            continue
        if char == ")":
            depth = max(depth - 1, 0)
            current.append(char)
            continue
        if char == "," and depth == 0:
            value = "".join(current).strip()
            if value:
                args.append(value)
            current = []
            continue
        current.append(char)
    value = "".join(current).strip()
    if value:
        args.append(value)
    return args


def resolve_argument(raw_argument: str, assignment_map: dict[str, str]) -> str:
    literal_match = STRING_ARG_RE.search(raw_argument)
    if literal_match:
        return literal_match.group(1)

    wrapped_match = WRAPPED_IDENTIFIER_RE.search(raw_argument)
    if wrapped_match:
        candidate = wrapped_match.group(1)
        return assignment_map.get(candidate, candidate)

    identifier_match = re.fullmatch(r"[A-Za-z_][A-Za-z0-9_\.]*", raw_argument)
    if identifier_match:
        candidate = identifier_match.group(0)
        return assignment_map.get(candidate, candidate)

    return raw_argument.strip()


def looks_like_sound_hint(value: str) -> bool:
    lower = value.lower()
    return "." in value or "/" in value or lower.endswith((".vsnd", ".vsnd_c", ".vsndevts", ".vsndevts_c", ".mp3", ".wav"))


def is_api_reference(value: str) -> bool:
    lower = value.lower()
    return any(
        token in lower
        for token in (
            "emitsound",
            "stopsound",
            "precachesoundscript",
            "precacheresource",
        )
    )


def iter_sound_files(archive: vpk.VPK) -> Iterable[str]:
    for path, _meta in archive.items():
        if SOUND_FILE_RE.match(path):
            yield path


def classify(path: str) -> str:
    lower = path.lower()
    if lower.startswith("soundevents/game_sounds_heroes/"):
        return "hero_soundevent"
    if lower.startswith("soundevents/game_sounds"):
        return "shared_soundevent"
    if lower.startswith("soundevents/"):
        return "soundevent"
    if lower.startswith("sounds/"):
        return "resource"
    return "other"


def category_rank(category: str) -> int:
    return {
        "hero_soundevent": 0,
        "shared_soundevent": 1,
        "soundevent": 2,
        "resource": 3,
    }.get(category, 9)


def scan_source_file(path: Path) -> list[CodeHit]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    if path.suffix.lower() == ".vsndevts":
        return scan_soundevent_source_file(path, text)

    assignment_map: dict[str, str] = {}
    for line in text.splitlines():
        assign_match = ASSIGNMENT_RE.match(line)
        if assign_match:
            assignment_map[assign_match.group(1)] = assign_match.group(2)

    hits: list[CodeHit] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in SOUND_API_RE.finditer(line):
            api = match.group("api")
            call_body = extract_call_body(line, match.end() - 1)
            args = split_top_level_args(call_body)
            api_lower = api.lower()
            if api_lower == "precacheresource":
                raw_argument = args[1] if len(args) > 1 else (args[0] if args else "")
            else:
                raw_argument = args[0] if args else ""
            argument = resolve_argument(raw_argument, assignment_map) if raw_argument else ""
            hits.append(
                CodeHit(
                    path=str(path),
                    line_number=line_number,
                    api=api,
                    argument=argument,
                    line=line.strip(),
                    resource_hints=[],
                )
            )
    return hits


def scan_soundevent_source_file(path: Path, text: str) -> list[CodeHit]:
    hits: list[CodeHit] = []
    lines = text.splitlines()
    current_event: str | None = None
    block_lines: list[str] = []
    block_start = 0
    depth = 0

    def flush_block() -> None:
        nonlocal current_event, block_lines, block_start
        if not current_event:
            block_lines = []
            return
        block_text = "\n".join(block_lines)
        resource_hints: list[str] = []
        for match in VSNDEVTS_RESOURCE_RE.finditer(block_text):
            single = match.group(1)
            array_body = match.group(2)
            if single:
                resource_hints.append(single)
            elif array_body:
                resource_hints.extend(
                    item
                    for item in re.findall(r'"([^"]+)"', array_body)
                    if item
                )
        hits.append(
            CodeHit(
                path=str(path),
                line_number=block_start,
                api="vsndevts",
                argument=current_event,
                line=block_lines[0].strip() if block_lines else current_event,
                resource_hints=resource_hints,
            )
        )
        current_event = None
        block_lines = []
        block_start = 0

    for line_number, line in enumerate(lines, start=1):
        if current_event is None:
            event_match = VSNDEVTS_EVENT_RE.match(line)
            if event_match:
                current_event = event_match.group(1)
                block_start = line_number
                block_lines = [line]
                depth = 0
            continue

        block_lines.append(line)
        depth += line.count("{") - line.count("}")
        if depth <= 0 and "}" in line:
            flush_block()

    if current_event:
        flush_block()

    return hits


def scan_sources(inputs: list[str]) -> list[CodeHit]:
    hits: list[CodeHit] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and SOURCE_FILE_RE.search(child.name):
                    hits.extend(scan_source_file(child))
        elif path.is_file() and SOURCE_FILE_RE.search(path.name):
            hits.extend(scan_source_file(path))
    return hits


def score_match(terms: list[str], path: str, strings: list[str]) -> tuple[int, list[str], list[str], list[str]]:
    path_lower = path.lower()
    matched = [s for s in strings if any(term in s.lower() for term in terms)]
    token_matches = []
    for token in terms:
        token_matches.extend([s for s in strings if token in s.lower()])
    resource_matches = [
        s for s in strings if RESOURCE_RE.search(s) and any(term in s.lower() for term in terms)
    ]
    source_hints = [s for s in strings if any(term in s.lower() for term in terms) or EVENT_HINT_RE.search(s)]
    score = 0
    if any(term in path_lower for term in terms):
        score += 10
    score += min(len(matched), 5) * 3
    score += min(len(token_matches), 8)
    score += min(len(resource_matches), 5)
    score += sum(1 for token in terms if token in path_lower) * 2
    if any(EVENT_HINT_RE.search(s) for s in matched):
        score += 2
    if not matched and token_matches:
        matched = token_matches
    return score, matched[:12], resource_matches[:12], source_hints[:12]


def collect_matches(archive: vpk.VPK, terms: list[str]) -> list[Match]:
    matches: list[Match] = []
    for path in iter_sound_files(archive):
        category = classify(path)
        if category == "resource":
            path_lower = path.lower()
            if any(term in path_lower for term in terms):
                matches.append(
                    Match(
                        path=path,
                        category=category,
                        score=10,
                        matched_strings=[path],
                        resource_strings=[path],
                        source_hints=[],
                    )
                )
            continue

        try:
            blob = archive.get_file(path).read()
        except Exception:
            continue

        strings = printable_strings(blob)
        score, matched_strings, resource_strings, source_hints = score_match(terms, path, strings)
        if score <= 0:
            continue
        matches.append(
            Match(
                path=path,
                category=category,
                score=score,
                matched_strings=matched_strings,
                resource_strings=resource_strings,
                source_hints=source_hints,
            )
        )

    matches.sort(key=lambda item: (category_rank(item.category), -item.score, item.path))
    return matches


def print_human(matches: list[Match], limit: int) -> None:
    if not matches:
        print("No soundevent/resource matches found.")
        return

    for match in matches[:limit]:
        print(f"{match.path} [{match.category}] score={match.score}")
        if match.matched_strings:
            print("  matches:")
            for value in match.matched_strings:
                print(f"    - {value}")
        if match.resource_strings:
            print("  resources:")
            for value in match.resource_strings:
                print(f"    - {value}")
        if match.source_hints:
            print("  hints:")
            for value in match.source_hints:
                print(f"    - {value}")


def print_json(matches: list[Match], limit: int) -> None:
    payload = [asdict(item) for item in matches[:limit]]
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


def group_code_hits(hits: list[CodeHit]) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for hit in hits:
        grouped[hit.api].append(asdict(hit))
    return dict(grouped)


def hit_matches_query(hit: CodeHit, query_terms: list[str]) -> bool:
    if not query_terms:
        return True
    haystacks = [hit.argument.lower(), hit.line.lower(), *[item.lower() for item in hit.resource_hints]]
    return all(any(token in haystack for haystack in haystacks) for token in query_terms)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Dota 2 sound events/resources in pak01_dir.vpk")
    parser.add_argument("query", nargs="?", default="", help="Sound event name, alias, or resource hint")
    parser.add_argument("--vpk-path", help="Path to pak01_dir.vpk")
    parser.add_argument("--limit", type=int, default=10, help="Maximum matches to print")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Source file or directory to scan for sound APIs (Lua, JS, XML, KV, vsndevts)",
    )
    args = parser.parse_args()

    try:
        import vpk
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing Python dependency 'vpk'. Install it in the selected Python environment "
            "or use the workspace soundevent finder."
        ) from exc

    vpk_path = resolve_vpk_path(args.vpk_path)
    archive = vpk.open(str(vpk_path))
    code_hits = scan_sources(args.source)
    query_terms = [] if is_api_reference(args.query) else tokenize(args.query)
    display_hits = [hit for hit in code_hits if hit_matches_query(hit, query_terms)]
    source_terms = []
    for hit in display_hits:
        for value in [hit.argument, *hit.resource_hints]:
            if not value or not looks_like_sound_hint(value):
                continue
            if query_terms and all(token in value.lower() for token in query_terms):
                source_terms.append(value)
    terms = dedupe_terms([*query_terms, *source_terms])
    if not terms:
        parser.error("Provide a query or at least one --source file containing a sound API call.")

    matches = collect_matches(archive, terms)

    if args.json:
        json.dump(
            {
                "vpk": str(vpk_path),
                "query": args.query,
                "terms": terms,
                "code_hits": group_code_hits(code_hits),
                "matches": [asdict(item) for item in matches[: args.limit]],
            },
            sys.stdout,
            indent=2,
            ensure_ascii=False,
        )
        sys.stdout.write("\n")
    else:
        print(f"VPK: {vpk_path}")
        print(f"Query: {args.query}")
        if terms:
            print(f"Terms: {', '.join(terms)}")
        if display_hits:
            print("Code hits:")
            for api, hits in group_code_hits(display_hits).items():
                print(f"  {api}:")
                for hit in hits[:10]:
                    print(f"    - {hit['path']}:{hit['line_number']} -> {hit['argument']}")
        print_human(matches, args.limit)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
