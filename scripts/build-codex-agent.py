#!/usr/bin/env python3
"""Render a Codex custom agent from the cane-wiki Claude agent instructions."""

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "agents/cane-wiki/cane-wiki.md"
TARGET = ROOT / "agents/cane-wiki/cane-wiki.codex.toml"


def render() -> str:
    parts = SOURCE.read_text().split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"Missing frontmatter: {SOURCE}")
    front = yaml.safe_load(parts[1])
    if not isinstance(front, dict) or not front.get("name") or not front.get("description"):
        raise ValueError("Agent needs name and description")
    return (
        "# Generated from agents/cane-wiki/cane-wiki.md; edit that file instead.\n"
        f"name = {json.dumps(front['name'], ensure_ascii=False)}\n"
        f"description = {json.dumps(front['description'], ensure_ascii=False)}\n"
        f"developer_instructions = {json.dumps(parts[2].lstrip(), ensure_ascii=False)}\n"
    )


if __name__ == "__main__":
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] != "--check"):
        sys.exit(f"Usage: {sys.argv[0]} [--check]")
    try:
        output = render()
    except ValueError as exc:
        sys.exit(f"Error: {exc}")
    if len(sys.argv) == 2:
        if not TARGET.exists() or TARGET.read_text() != output:
            sys.exit("Codex agent differs from Claude source; run scripts/build-codex-agent.py")
        print("✓ Codex agent matches Claude source")
    else:
        TARGET.write_text(output)
        print("✓ Rendered Codex agent")
