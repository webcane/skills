#!/usr/bin/env python3
"""Install the dialectic entry command into a host command directory.

The command is a thin wrapper over the skill: it selects the orchestrator agent
and passes the mode and goal. The skill and agent work without it.

Examples:
    scripts/install_commands.py --host opencode --dest .
    scripts/install_commands.py --host claude --dest ~/work/api
    scripts/install_commands.py --list
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

COMMAND_SOURCE = Path(__file__).resolve().parent.parent / "assets" / "commands"
HOST_DIRS = {
    "opencode": Path(".opencode") / "commands",
    "claude": Path(".claude") / "commands",
    "codex": Path(".codex") / "prompts",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="install_commands.py",
        description="Copy assets/commands/*.md into a host command directory.",
        epilog=(
            "examples:\n"
            "  scripts/install_commands.py --host opencode --dest .\n"
            "  scripts/install_commands.py --host all --dest ~/work/api --dry-run\n"
            "  scripts/install_commands.py --list"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--host",
        choices=sorted(HOST_DIRS) + ["all"],
        help="Host whose command directory should receive the files.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="Project root; the host command directory is created under it.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing.")
    parser.add_argument("--list", action="store_true", help="List command assets and exit.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing command file that differs.",
    )
    return parser


def command_assets() -> list[Path]:
    if not COMMAND_SOURCE.is_dir():
        return []
    return sorted(COMMAND_SOURCE.glob("*.md"))


def install(host: str, dest: Path, assets: list[Path], dry_run: bool, force: bool) -> int:
    target_dir = (dest.expanduser() / HOST_DIRS[host]).resolve()
    failures = 0
    for asset in assets:
        target = target_dir / asset.name
        if target.exists() and target.read_bytes() != asset.read_bytes() and not force:
            print(f"skip (exists, differs): {target} — re-run with --force", file=sys.stderr)
            failures += 1
            continue
        print(f"{'would copy' if dry_run else 'copy'}: {asset} -> {target}")
        if dry_run:
            continue
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(asset, target)
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    assets = command_assets()

    if args.list:
        for asset in assets:
            print(asset.name)
        return 0
    if not assets:
        print(f"no command assets in {COMMAND_SOURCE}", file=sys.stderr)
        return 1
    if not args.host:
        parser.error("--host is required unless --list is used")
    if not args.dest:
        parser.error("--dest is required unless --list is used")

    hosts = sorted(HOST_DIRS) if args.host == "all" else [args.host]
    failures = sum(
        install(host, args.dest, assets, args.dry_run, args.force) for host in hosts
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
