#!/bin/bash
# Package a skill directory into a Claude.ai-compatible .zip file
# Usage: ./scripts/package-skill-claudeai.sh <skill-name> [version]
#
# Claude.ai's skill upload has different requirements than the .skill
# (tar.gz) format produced by package-skill.sh for Claude Code / agentskills.io:
#   - the skill definition file must be named lowercase `skill.md`, not `SKILL.md`
#   - the frontmatter `description` must be <= 200 chars, not 1024
#   - the zip must contain a top-level folder named after the skill (not
#     loose files at the zip root)
#
# To provide a Claude.ai-specific short description, add
# `metadata.description_claudeai` (<= 200 chars) to the skill's SKILL.md
# frontmatter. If absent, the main `description` is truncated to fit, with a
# warning — see scripts/build_claudeai_skill_md.py.

set -e

SKILL_NAME="${1:-}"
VERSION="${2:-}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$REPO_ROOT/skills/$SKILL_NAME"
DIST_DIR="$REPO_ROOT/dist"
STAGE_ROOT="$DIST_DIR/claudeai-stage"
STAGE_DIR="$STAGE_ROOT/$SKILL_NAME"

[ -z "$SKILL_NAME" ] && echo "Usage: $0 <skill-name> [version]" && exit 1
[ ! -f "$SKILL_DIR/SKILL.md" ] && echo "Error: $SKILL_DIR/SKILL.md not found" && exit 1

# Derive version from frontmatter (metadata.version) when not passed explicitly.
if [ -z "$VERSION" ]; then
  VERSION="$(grep -E '^[[:space:]]*version:[[:space:]]*' "$SKILL_DIR/SKILL.md" \
    | head -1 | sed -E 's/^[[:space:]]*version:[[:space:]]*//; s/[[:space:]]*$//')"
fi
[ -z "$VERSION" ] && echo "Error: no version given and none found in $SKILL_NAME/SKILL.md (metadata.version)" && exit 1

mkdir -p "$DIST_DIR"
rm -rf "$STAGE_ROOT"
mkdir -p "$STAGE_DIR"

# Copy skill contents into a folder named after the skill, excluding dev-only files
( cd "$SKILL_DIR" && tar -cf - \
    --exclude='.DS_Store' --exclude='*.swp' --exclude='config.json.bak*' --exclude='TODO.md' . ) \
  | ( cd "$STAGE_DIR" && tar -xf - )

# SKILL.md -> skill.md, with description rewritten to fit Claude.ai's 200-char limit.
# Write to a distinctly-named temp file first: on case-insensitive filesystems
# (default on macOS), "SKILL.md" and "skill.md" are the same file, so writing
# directly to "skill.md" and then `rm`-ing "SKILL.md" would delete both.
python3 "$REPO_ROOT/scripts/build_claudeai_skill_md.py" "$STAGE_DIR/SKILL.md" "$STAGE_DIR/.skill.md.tmp"
rm "$STAGE_DIR/SKILL.md"
mv "$STAGE_DIR/.skill.md.tmp" "$STAGE_DIR/skill.md"

# Zip with the skill folder at the root of the archive
ZIP_FILE="$DIST_DIR/${SKILL_NAME}-claudeai.zip"
rm -f "$ZIP_FILE"
( cd "$STAGE_ROOT" && zip -rq "$ZIP_FILE" "$SKILL_NAME" )

cp "$ZIP_FILE" "$DIST_DIR/${SKILL_NAME}-claudeai-${VERSION}.zip"
rm -rf "$STAGE_ROOT"

echo "✓ dist/${SKILL_NAME}-claudeai.zip"
echo "✓ dist/${SKILL_NAME}-claudeai-${VERSION}.zip (v${VERSION})"
