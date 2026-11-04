#!/usr/bin/env python3
"""Build the tracked Claude Code and Codex cane-wiki plugin bundles."""

import argparse
import json
import shutil
import tempfile
from pathlib import Path

from render_platform_skill import render


ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "plugins"
SKILL = ROOT / "skills/cane-wiki-init"


def build(destination: Path) -> None:
    version = (ROOT / "agents/cane-wiki/VERSION").read_text().strip()
    for platform, folder in (("claude-code", "claude"), ("codex", "codex")):
        plugin = destination / folder / "cane-wiki"
        skill = plugin / "skills/cane-wiki-init"
        shutil.copytree(SKILL, skill, ignore=shutil.ignore_patterns(".DS_Store", "*.swp"))
        render(SKILL / "SKILL.md", skill / "SKILL.md", platform)
        if platform == "claude-code":
            agents = plugin / "agents"
            agents.mkdir()
            for name in ("cane-wiki", "cane-wiki-critic"):
                shutil.copy2(ROOT / "agents" / name / f"{name}.md", agents / f"{name}.md")
            manifest = {
                "name": "cane-wiki",
                "version": version,
                "description": "Obsidian wiki agents and vault setup skill",
                "author": {"name": "webcane"},
                "repository": "https://github.com/webcane/skills",
                "license": "MIT",
            }
            path = plugin / ".claude-plugin/plugin.json"
        else:
            manifest = {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                "name": "cane-wiki",
                "version": version,
                "description": "Obsidian wiki setup skill for the cane-wiki Codex agents",
            }
            path = plugin / "plugin.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def identical(left: Path, right: Path) -> bool:
    left_files = {path.relative_to(left): path.read_bytes() for path in left.rglob("*") if path.is_file()}
    right_files = {path.relative_to(right): path.read_bytes() for path in right.rglob("*") if path.is_file()}
    return left_files == right_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when tracked plugin bundles are stale")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        expected = Path(directory) / "plugins"
        build(expected)
        for folder in ("claude", "codex"):
            target = PLUGINS / folder / "cane-wiki"
            source = expected / folder / "cane-wiki"
            if args.check:
                if not target.is_dir() or not identical(source, target):
                    parser.exit(1, f"Stale plugin bundle: {target}\nRun python3 scripts/build-cane-wiki-plugins.py\n")
            else:
                if target.exists():
                    shutil.rmtree(target)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, target)
        print("✓ cane-wiki plugin bundles match source" if args.check else "✓ Built cane-wiki plugin bundles")
