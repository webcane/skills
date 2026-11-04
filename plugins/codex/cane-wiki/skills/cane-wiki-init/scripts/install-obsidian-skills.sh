#!/usr/bin/env bash
# Install missing Obsidian skill dependencies for the current host.
# Usage: INSTALL_DIR=/path/to/skills bash scripts/install-obsidian-skills.sh <codex|claude-code>
# Env: OBSIDIAN_SKILLS_SOURCE may point to a local upstream skills/ directory.
set -euo pipefail

PLATFORM="${1:-}"
case "$PLATFORM" in
  codex) TARGET_DIR="${INSTALL_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}" ;;
  claude-code) TARGET_DIR="${INSTALL_DIR:-$HOME/.claude/skills}" ;;
  *) echo "Usage: $0 <codex|claude-code>" >&2; exit 1 ;;
esac

NAMES=(obsidian-markdown obsidian-cli defuddle)
MISSING=()
for name in "${NAMES[@]}"; do
  [ -f "$TARGET_DIR/$name/SKILL.md" ] || MISSING+=("$name")
done
if [ "${#MISSING[@]}" -eq 0 ]; then
  echo "✓ All Obsidian skills already installed in $TARGET_DIR"
  exit 0
fi

TEMP="$(mktemp -d)"
trap 'rm -rf "$TEMP"' EXIT
if [ -n "${OBSIDIAN_SKILLS_SOURCE:-}" ]; then
  SOURCE_DIR="$OBSIDIAN_SKILLS_SOURCE"
else
  git clone --depth 1 https://github.com/kepano/obsidian-skills.git "$TEMP/upstream" >/dev/null
  SOURCE_DIR="$TEMP/upstream/skills"
fi
for name in "${MISSING[@]}"; do
  [ -f "$SOURCE_DIR/$name/SKILL.md" ] || { echo "Missing skill in source: $name" >&2; exit 1; }
done

mkdir -p "$TARGET_DIR"
for name in "${MISSING[@]}"; do
  cp -R "$SOURCE_DIR/$name" "$TARGET_DIR/$name"
  echo "✓ Installed $name to $TARGET_DIR/$name"
done
