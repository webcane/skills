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

# Build the list of available skills by locating every SKILL.md, so nested
# family dirs (skills/mm-wiki/mm-wiki-ingest) are found and non-skill dirs
# (skills/mm-wiki, the family home) are excluded. The name offered is the
# path relative to skills/ (e.g. mm-wiki/mm-wiki-ingest).
if [ -z "$SKILL_NAME" ]; then
  SKILL_NAMES=()
  while IFS= read -r f; do
    # Strip both the skills/ prefix and the trailing /SKILL.md so the
    # offered name is the skill's directory relative to skills/
    # (e.g. mm-wiki/mm-wiki-import), not the file path.
    rel="${f#$SKILLS_DIR/}"
    SKILL_NAMES+=("${rel%/SKILL.md}")
  done < <(find "$SKILLS_DIR" -name SKILL.md | sort)

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

# Install dir is the flat basename even for nested skills.
ARTIFACT_NAME="$(basename "$SKILL_NAME")"
TARGET="$INSTALL_DIR/$ARTIFACT_NAME"
rm -rf "$TARGET"
mkdir -p "$TARGET"
tar -xzf "$REPO_ROOT/dist/${ARTIFACT_NAME}.skill" -C "$TARGET"

echo "✓ Installed $SKILL_NAME to $TARGET"
