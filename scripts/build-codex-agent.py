#!/usr/bin/env python3
"""Render Codex custom agents from their Claude agent instructions."""

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ("cane-wiki", "cane-wiki-critic", "cane-learning")


def render(name: str) -> str:
    source = ROOT / "agents" / name / f"{name}.md"
    parts = source.read_text().split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Missing frontmatter: {source}")
    front = yaml.safe_load(parts[1])
    if not isinstance(front, dict) or front.get("name") != name or not front.get("description"):
        raise ValueError(f"Agent needs matching name and description: {source}")
    return (
        f"# Generated from agents/{name}/{name}.md; edit that file instead.\n"
        f"name = {json.dumps(front['name'], ensure_ascii=False)}\n"
        f"description = {json.dumps(front['description'], ensure_ascii=False)}\n"
        f"developer_instructions = {json.dumps(parts[2].lstrip(), ensure_ascii=False)}\n"
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    check = "--check" in args
    names = [arg for arg in args if arg != "--check"] or list(AGENTS)
    if args.count("--check") > 1 or any(name not in AGENTS for name in names):
        supported = "|".join(AGENTS)
        sys.exit(f"Usage: {sys.argv[0]} [--check] [{supported} ...]")
    for name in names:
        target = ROOT / "agents" / name / f"{name}.codex.toml"
        try:
            output = render(name)
        except ValueError as exc:
            sys.exit(f"Error: {exc}")
        if check:
            if not target.exists() or target.read_text() != output:
                sys.exit(f"Codex agent differs from Claude source: {name}")
            print(f"✓ Codex agent matches Claude source: {name}")
        else:
            target.write_text(output)
            print(f"✓ Rendered Codex agent: {name}")
