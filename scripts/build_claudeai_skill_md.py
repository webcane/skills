#!/usr/bin/env python3
"""Compatibility wrapper for rendering a Claude.ai skill definition."""

import sys
from pathlib import Path

from render_platform_skill import render

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"Usage: {sys.argv[0]} <input SKILL.md> <output skill.md>")
    try:
        render(Path(sys.argv[1]), Path(sys.argv[2]), "claudeai")
    except ValueError as exc:
        sys.exit(f"Error: {exc}")
