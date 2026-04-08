#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


PANEL_TAGS = {
    "Panel",
    "Label",
    "Image",
    "DOTAScenePanel",
    "DOTAAbilityImage",
    "DOTAItemImage",
    "DOTAAvatarImage",
    "Movie",
    "Snippet",
}

RESOURCE_INCLUDE_RE = re.compile(r"^file://\{resources\}/(.+)$")


def find_repo_root(start: Path) -> Path | None:
    for current in [start, *start.parents]:
        if (current / "content").exists() and (current / "game").exists():
            return current
    return None


def normalize_resource_path(resource_path: str) -> Path:
    return Path(*resource_path.replace("\\", "/").split("/"))


def find_panorama_root(path: Path) -> Path | None:
    for current in [path.parent, *path.parents]:
        if current.name.lower() == "panorama":
            return current
    return None


def resolve_include(path_str: str, panorama_root: Path) -> Path | None:
    match = RESOURCE_INCLUDE_RE.match(path_str.strip())
    if not match:
        return None
    rel = normalize_resource_path(match.group(1))
    return panorama_root / rel


def first_actual_child(root: ET.Element) -> ET.Element | None:
    for child in list(root):
        if child.tag in {"styles", "scripts"}:
            continue
        return child
    return None


def line_number(text: str, needle: str) -> int | None:
    idx = text.find(needle)
    if idx < 0:
        return None
    return text[:idx].count("\n") + 1


def check_xml_file(path: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_text(encoding="utf-8")
    panorama_root = find_panorama_root(path)
    if panorama_root is None:
        return [f"{path}: could not resolve addon panorama root"]
    try:
        tree = ET.fromstring(raw)
    except ET.ParseError as exc:
        return [f"{path}: XML parse error: {exc}"]

    if tree.tag != "root":
        errors.append(f"{path}: root tag must be <root>")
        return errors

    actual = first_actual_child(tree)
    if actual is None:
        errors.append(f"{path}: missing actual panel tree under <root>")
        return errors

    if actual.attrib.get("id"):
        line = line_number(raw, f'<{actual.tag} id="{actual.attrib.get("id")}"')
        location = f":{line}" if line else ""
        errors.append(
            f"{path}{location}: first actual root panel must not have an id attribute"
        )

    if "worldpanels" in {part.lower() for part in path.parts} and actual.tag not in PANEL_TAGS:
        errors.append(
            f"{path}: first actual node in a worldpanel should be a panel-type tag, got <{actual.tag}>"
        )

    for container_tag in ("styles", "scripts"):
        for container in tree.findall(container_tag):
            for include in container.findall("include"):
                src = include.attrib.get("src", "")
                if not src:
                    errors.append(f"{path}: <include> inside <{container_tag}> is missing src")
                    continue
                resolved = resolve_include(src, panorama_root)
                if resolved is None:
                    continue
                if not resolved.exists():
                    errors.append(
                        f"{path}: include target does not exist: {src} -> {resolved}"
                    )

    return errors


def expand_inputs(paths: list[str]) -> list[Path]:
    expanded: list[Path] = []
    for raw in paths:
        p = Path(raw).resolve()
        if p.is_dir():
            expanded.extend(sorted(x for x in p.rglob("*") if x.is_file()))
        elif p.exists():
            expanded.append(p)
        else:
            expanded.append(p)
    return expanded


def main() -> int:
    parser = argparse.ArgumentParser(description="Lightweight syntax guard for Dota 2 Panorama files.")
    parser.add_argument("--paths", nargs="+", required=True, help="Files or directories to validate.")
    args = parser.parse_args()

    files = expand_inputs(args.paths)
    if not files:
        print("No files to validate.", file=sys.stderr)
        return 1

    repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        print("Could not locate repo root containing content/ and game/.", file=sys.stderr)
        return 1

    errors: list[str] = []
    checked = 0
    for path in files:
        if not path.exists():
            errors.append(f"{path}: path does not exist")
            continue
        if path.suffix.lower() != ".xml":
            continue
        checked += 1
        errors.extend(check_xml_file(path, repo_root))

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        print(f"Panorama syntax guard failed. Checked {checked} xml file(s).", file=sys.stderr)
        return 1

    print(f"Panorama syntax guard passed. Checked {checked} xml file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
