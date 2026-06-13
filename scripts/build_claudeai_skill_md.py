#!/usr/bin/env python3
"""Rewrite a skill's SKILL.md frontmatter for Claude.ai's skill.md requirements.

Claude.ai enforces a 200-character limit on the frontmatter `description`
field (Claude Code / agentskills.io allow up to 1024). If the skill defines
`metadata.description_claudeai` (<= 200 chars), that value is used as the
description in the output file and is removed from `metadata`. Otherwise the
main `description` is truncated to fit at a word boundary, with a warning on
stderr suggesting `metadata.description_claudeai` be added.

Usage: build_claudeai_skill_md.py <input SKILL.md> <output skill.md>
"""
import re
import sys

import yaml

MAX_DESCRIPTION = 200


def main(src, dst):
    text = open(src).read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"Error: {src} has no YAML frontmatter")
    frontmatter, body = m.group(1), m.group(2)

    data = yaml.safe_load(frontmatter)
    metadata = data.get("metadata") or {}
    short_desc = metadata.pop("description_claudeai", None)

    if short_desc:
        if len(short_desc) > MAX_DESCRIPTION:
            sys.exit(
                f"Error: metadata.description_claudeai is {len(short_desc)} "
                f"chars, must be <= {MAX_DESCRIPTION}"
            )
        data["description"] = short_desc
    elif len(data.get("description", "")) > MAX_DESCRIPTION:
        original = data["description"]
        truncated = original[:MAX_DESCRIPTION].rsplit(" ", 1)[0]
        data["description"] = truncated
        print(
            f"Warning: description truncated from {len(original)} to "
            f"{len(truncated)} chars for Claude.ai's {MAX_DESCRIPTION}-char "
            f"limit. Add metadata.description_claudeai to {src} for a "
            f"purpose-written short description instead.",
            file=sys.stderr,
        )

    data["metadata"] = metadata

    out_frontmatter = yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, width=1000
    )
    with open(dst, "w") as f:
        f.write(f"---\n{out_frontmatter}---\n{body}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"Usage: {sys.argv[0]} <input SKILL.md> <output skill.md>")
    main(sys.argv[1], sys.argv[2])
