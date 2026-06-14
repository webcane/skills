#!/bin/bash
# Build a skill from source and install/reinstall it locally.
# Usage: ./scripts/install-local.sh [skill-name]
# Env:   INSTALL_DIR (default: ~/.claude/skills)
#
# If [skill-name] is omitted, prompts to choose from skills/ in this repo.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.claude/skills}"

SKILL_NAME="${1:-}"

if [ -z "$SKILL_NAME" ]; then
  SKILL_NAMES=()
  for dir in "$SKILLS_DIR"/*/; do
    SKILL_NAMES+=("$(basename "$dir")")
  done

  echo "Choose available skills:"
  select choice in "${SKILL_NAMES[@]}"; do
    if [ -n "$choice" ]; then
      SKILL_NAME="$choice"
      break
    fi
    echo "Invalid choice."
  done
fi

[ ! -f "$SKILLS_DIR/$SKILL_NAME/SKILL.md" ] && echo "Error: $SKILLS_DIR/$SKILL_NAME/SKILL.md not found" && exit 1

bash "$REPO_ROOT/scripts/package-skill.sh" "$SKILL_NAME"

TARGET="$INSTALL_DIR/$SKILL_NAME"
rm -rf "$TARGET"
mkdir -p "$TARGET"
tar -xzf "$REPO_ROOT/dist/${SKILL_NAME}.skill" -C "$TARGET"

echo "✓ Installed $SKILL_NAME to $TARGET"
