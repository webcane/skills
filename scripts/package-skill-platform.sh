#!/usr/bin/env bash
# Shared packaging engine for Claude Code and Codex platform variants.
# Usage: package-skill-platform.sh <claude-code|codex> <skill-path> [version]
set -euo pipefail

PLATFORM="${1:-}"
SKILL_NAME="${2:-}"
VERSION="${3:-}"
case "$PLATFORM" in
  claude-code|codex) ;;
  *) echo "Usage: $0 <claude-code|codex> <skill-path> [version]" >&2; exit 1 ;;
esac
case "$SKILL_NAME" in
  ''|/*|*..*) echo "Invalid skill path: $SKILL_NAME" >&2; exit 1 ;;
esac

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$REPO_ROOT/skills/$SKILL_NAME"
[ -f "$SKILL_DIR/SKILL.md" ] || { echo "Skill not found: $SKILL_NAME" >&2; exit 1; }
ARTIFACT_NAME="$(basename "$SKILL_NAME")"
if [ -z "$VERSION" ]; then
  VERSION="$(grep -E '^[[:space:]]*version:[[:space:]]*' "$SKILL_DIR/SKILL.md" | head -1 | sed -E 's/^[[:space:]]*version:[[:space:]]*//; s/[[:space:]]*$//')"
fi
[ -n "$VERSION" ] || { echo "Missing skill version: $SKILL_NAME" >&2; exit 1; }

mkdir -p "$REPO_ROOT/dist"
STAGE="$(mktemp -d "$REPO_ROOT/dist/$PLATFORM-stage.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
STAGE_DIR="$STAGE/$ARTIFACT_NAME"
mkdir -p "$STAGE_DIR"
(cd "$SKILL_DIR" && tar -cf - --exclude='.DS_Store' --exclude='*.swp' --exclude='config.json.bak*' --exclude='TODO.md' .) | (cd "$STAGE_DIR" && tar -xf -)
python3 "$REPO_ROOT/scripts/render_platform_skill.py" "$PLATFORM" "$STAGE_DIR/SKILL.md" "$STAGE_DIR/.SKILL.md.tmp"
mv "$STAGE_DIR/.SKILL.md.tmp" "$STAGE_DIR/SKILL.md"

ZIP_FILE="$REPO_ROOT/dist/$ARTIFACT_NAME-$PLATFORM.zip"
rm -f "$ZIP_FILE"
(cd "$STAGE" && zip -rq "$ZIP_FILE" "$ARTIFACT_NAME")
cp "$ZIP_FILE" "$REPO_ROOT/dist/$ARTIFACT_NAME-$PLATFORM-$VERSION.zip"
echo "✓ dist/$ARTIFACT_NAME-$PLATFORM.zip"
echo "✓ dist/$ARTIFACT_NAME-$PLATFORM-$VERSION.zip (v$VERSION)"
