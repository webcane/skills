#!/usr/bin/env python3
"""Install the two slash commands into a host-specific directory.

Examples:
    scripts/install_commands.py --host opencode --dest .
    scripts/install_commands.py --host claude --dest ~/my-project
    scripts/install_commands.py --list
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import EXIT_OK, EXIT_USAGE, Parser, fail, ok, skill_root

COMMAND_DIRS = {
    "opencode": Path(".opencode") / "command",
    "claude": Path(".claude") / "commands",
    "codex": Path(".codex") / "prompts",
}


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(
        prog="install_commands.py",
        description=(
            "Copy assets/commands/*.md into a host command directory. Commands are thin "
            "wrappers over this skill; the skill itself works without them."
        ),
        epilog=(
            "examples:\n"
            "  scripts/install_commands.py --host opencode --dest .\n"
            "  scripts/install_commands.py --host claude --dest ~/project --dry-run\n"
            "  scripts/install_commands.py --list\n"
            "\n"
            "targets: opencode=.opencode/command, claude=.claude/commands, codex=.codex/prompts\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--host", choices=tuple(COMMAND_DIRS), help="target host")
    parser.add_argument("--dest", default=".", help="project directory (default: current)")
    parser.add_argument("--force", action="store_true", help="overwrite existing command files")
    parser.add_argument("--dry-run", action="store_true", help="show targets, write nothing")
    parser.add_argument("--list", action="store_true", help="list bundled commands and exit")
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    if not argv:
        parser.print_usage(sys.stderr)
        print("  hint: --host is required, e.g. --host opencode --dest .\n  run --help", file=sys.stderr)
        return EXIT_USAGE
    args = parser.parse_args(argv)

    source_dir = skill_root() / "assets" / "commands"
    commands = sorted(source_dir.glob("*.md"))
    if not commands:
        fail(
            "install_commands",
            EXIT_USAGE,
            f"no command templates in {source_dir}",
            "the skill package is incomplete",
            "reinstall the skill or restore assets/commands/",
        )

    if args.list:
        ok(f"Bundled commands ({len(commands)}):")
        for command in commands:
            ok(f"  {command.stem:<12} {command}")
        ok("")
        ok("These are optional wrappers; the skill is fully usable without them.")
        return EXIT_OK

    if not args.host:
        fail(
            "install_commands",
            EXIT_USAGE,
            "--host is required",
            "each host reads commands from a different directory",
            "pass --host opencode, --host claude or --host codex",
        )

    target_dir = Path(args.dest).expanduser().resolve() / COMMAND_DIRS[args.host]
    for command in commands:
        target = target_dir / command.name
        if args.dry_run:
            ok(f"would write {target}")
            continue
        target_dir.mkdir(parents=True, exist_ok=True)
        if target.exists() and not args.force:
            fail(
                "install_commands",
                EXIT_USAGE,
                f"{target} already exists",
                "overwriting would discard local edits",
                "pass --force to replace it",
            )
        shutil.copy2(command, target)
        ok(f"wrote {target}")

    if not args.dry_run:
        ok("")
        ok(f"Restart the host so it picks up {target_dir}.")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
