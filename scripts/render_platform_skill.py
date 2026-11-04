#!/usr/bin/env python3
"""Render a canonical Agent Skill for a specific host without editing source."""

import re
import sys
from pathlib import Path

import yaml

REPLACEMENTS = {
    "claude-code": {
        "{{ASK_USER}}": "AskUserQuestion",
        "{{MULTI_SELECT}}": "multiSelect",
    },
    "claudeai": {
        "{{ASK_USER}}": "вопрос в диалоге",
        "{{MULTI_SELECT}}": "выбор нескольких вариантов в ответе",
    },
    "codex": {
        "{{ASK_USER}}": "доступный инструмент запроса ввода или вопрос в чате",
        "{{MULTI_SELECT}}": "множественный выбор или перечисление вариантов в ответе",
    },
}


def render(source: Path, destination: Path, platform: str) -> None:
    if platform not in REPLACEMENTS:
        raise ValueError(f"Unknown platform: {platform}")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", source.read_text(), re.S)
    if not match:
        raise ValueError(f"{source} has no YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict) or not data.get("name") or not data.get("description"):
        raise ValueError(f"{source} needs name and description")
    body = match.group(2)
    for neutral, specific in REPLACEMENTS[platform].items():
        body = body.replace(neutral, specific)
    if re.search(r"\{\{[A-Z_]+\}\}", body):
        raise ValueError(f"Unresolved platform marker in {source}")

    metadata = data.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"metadata must be a map in {source}")
    specific_description = metadata.get(f"description_{platform.replace('-', '_')}")
    if specific_description:
        data["description"] = specific_description
    if platform == "claudeai":
        if len(data["description"]) > 200:
            shortened = data["description"][:200].rsplit(" ", 1)[0] or data["description"][:200]
            print(f"Warning: truncating Claude.ai description in {source}", file=sys.stderr)
            data["description"] = shortened
    for key in list(metadata):
        if key.startswith("description_"):
            metadata.pop(key)
    if len(data["description"]) > (200 if platform == "claudeai" else 1024):
        raise ValueError(f"Description too long in {source}")
    if metadata:
        data["metadata"] = metadata
    else:
        data.pop("metadata", None)
    header = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)
    destination.write_text(f"---\n{header}---\n{body}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(f"Usage: {sys.argv[0]} <claude-code|claudeai|codex> <source> <destination>")
    try:
        render(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[1])
    except ValueError as exc:
        sys.exit(f"Error: {exc}")
