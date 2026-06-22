#!/usr/bin/env python3
import argparse
import os
import platform
import re
import stat
import sys
from pathlib import Path
from typing import Optional


ENV_NAME = "TOKENX24_API_KEY"
MARKER_START = "# >>> TOKENX24_API_KEY managed by gpt-image2 >>>"
MARKER_END = "# <<< TOKENX24_API_KEY managed by gpt-image2 <<<"


def shell_name(shell: Optional[str] = None) -> str:
    shell = shell or os.environ.get("SHELL") or ""
    name = Path(shell).name.lower()
    return name or "sh"


def default_profile_path(
    shell: Optional[str] = None,
    system: Optional[str] = None,
    home: Optional[str] = None,
) -> Path:
    name = shell_name(shell)
    system = system or platform.system()
    home_path = Path(home or os.path.expanduser("~"))

    if name == "zsh":
        return home_path / ".zshrc"
    if name == "bash":
        if system == "Darwin":
            return home_path / ".bash_profile"
        return home_path / ".bashrc"
    if name == "fish":
        return home_path / ".config" / "fish" / "config.fish"
    if system == "Darwin":
        return home_path / ".zshrc"
    return home_path / ".profile"


def quote_posix(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def quote_fish(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def render_export_line(api_key: str, shell: Optional[str] = None) -> str:
    name = shell_name(shell)
    if name == "fish":
        return f"set -gx {ENV_NAME} {quote_fish(api_key)}"
    return f"export {ENV_NAME}={quote_posix(api_key)}"


def render_block(api_key: str, shell: Optional[str] = None) -> str:
    return "\n".join([MARKER_START, render_export_line(api_key, shell), MARKER_END])


def validate_api_key(api_key: str) -> str:
    api_key = api_key.strip()
    if not api_key:
        raise ValueError("API key is empty.")
    if "\n" in api_key or "\r" in api_key:
        raise ValueError("API key must be a single line.")
    if re.search(r"\s", api_key):
        raise ValueError("API key must not contain whitespace.")
    return api_key


def remove_unmanaged_exports(text: str) -> str:
    lines = []
    unmanaged_posix = re.compile(r"^\s*(?:export\s+)?TOKENX24_API_KEY\s*=.*$")
    unmanaged_fish = re.compile(r"^\s*set\s+-gx\s+TOKENX24_API_KEY\s+.*$")

    for line in text.splitlines():
        if unmanaged_posix.match(line) or unmanaged_fish.match(line):
            continue
        lines.append(line)

    return "\n".join(lines)


def upsert_api_key(text: str, api_key: str, shell: Optional[str] = None) -> str:
    api_key = validate_api_key(api_key)
    block = render_block(api_key, shell)
    managed_block = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        flags=re.DOTALL,
    )

    if managed_block.search(text):
        updated = managed_block.sub(block, text, count=1)
    else:
        updated = remove_unmanaged_exports(text)
        updated = updated.rstrip("\n")
        if updated:
            updated += "\n\n"
        updated += block

    return updated.rstrip("\n") + "\n"


def write_api_key(profile_path: Path, api_key: str, shell: Optional[str] = None) -> Path:
    profile_path = profile_path.expanduser()
    profile_path.parent.mkdir(parents=True, exist_ok=True)

    original = ""
    if profile_path.exists():
        original = profile_path.read_text(encoding="utf-8")

    profile_path.write_text(upsert_api_key(original, api_key, shell), encoding="utf-8")
    os.chmod(profile_path, stat.S_IRUSR | stat.S_IWUSR)
    return profile_path


def read_api_key_from_stdin() -> str:
    return validate_api_key(sys.stdin.read())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Configure TOKENX24_API_KEY in the current user's shell profile."
    )
    parser.add_argument(
        "--api-key",
        help="API key value explicitly provided by the agent.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read the API key explicitly passed on stdin.",
    )
    parser.add_argument(
        "--profile",
        help="Shell profile to update. Defaults to the detected macOS/Linux shell profile.",
    )
    parser.add_argument(
        "--shell",
        help="Shell name or path used to render the export line. Defaults to $SHELL.",
    )
    parser.add_argument(
        "--print-target",
        action="store_true",
        help="Only print the default profile path and exit.",
    )
    args = parser.parse_args()

    target_shell = args.shell or os.environ.get("SHELL")
    profile_path = Path(args.profile).expanduser() if args.profile else default_profile_path(target_shell)

    if args.print_target:
        print(profile_path)
        return 0

    if args.api_key and args.stdin:
        print("Use either --api-key or --stdin, not both.", file=sys.stderr)
        return 2
    if not args.api_key and not args.stdin:
        print("--api-key or --stdin is required.", file=sys.stderr)
        return 2

    try:
        if args.stdin:
            api_key = read_api_key_from_stdin()
        elif args.api_key:
            api_key = validate_api_key(args.api_key)

        written_path = write_api_key(profile_path, api_key, target_shell)
    except (OSError, ValueError) as exc:
        print(f"error={exc}", file=sys.stderr)
        return 1

    print(f"configured_env={ENV_NAME}")
    print(f"profile={written_path}")
    print("reload_hint=source the profile file or open a new terminal session")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
