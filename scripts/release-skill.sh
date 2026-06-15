#!/bin/bash
# Tag, push, and create a GitHub release for a skill.
# Usage: ./scripts/release-skill.sh [skill-name]
#
# If [skill-name] is omitted, prompts to choose from skills/ in this repo.
# The version is read from the skill's SKILL.md frontmatter (metadata.version)
# — that frontmatter is the single source of truth. Creates an annotated tag
# <skill-name>/v<version>, pushes it, and runs `gh release create` for it.
#
# Release notes are taken from the skill's CHANGELOG.md "[Unreleased]"
# section if present, otherwise a default title-only message is used so
# `gh release create` never prompts for input.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

SKILL_NAME="${1:-}"

if [ -z "$SKILL_NAME" ]; then
  SKILL_NAMES=()
  for dir in "$SKILLS_DIR"/*/; do
    SKILL_NAMES+=("$(basename "$dir")")
  done

  echo "Choose a skill to release:"
  select choice in "${SKILL_NAMES[@]}"; do
    if [ -n "$choice" ]; then
      SKILL_NAME="$choice"
      break
    fi
    echo "Invalid choice."
  done
fi

SKILL_DIR="$SKILLS_DIR/$SKILL_NAME"
[ ! -f "$SKILL_DIR/SKILL.md" ] && echo "Error: $SKILL_DIR/SKILL.md not found" && exit 1

VERSION="$(grep -E '^[[:space:]]*version:[[:space:]]*' "$SKILL_DIR/SKILL.md" \
  | head -1 | sed -E 's/^[[:space:]]*version:[[:space:]]*//; s/[[:space:]]*$//')"
[ -z "$VERSION" ] && echo "Error: no version found in $SKILL_NAME/SKILL.md (metadata.version)" && exit 1

TAG="${SKILL_NAME}/v${VERSION}"

if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "Error: tag $TAG already exists" && exit 1
fi

# Pull release notes from the "[Unreleased]" section of the skill's
# CHANGELOG.md, if any content is there.
NOTES_FILE="$(mktemp)"
trap 'rm -f "$NOTES_FILE"' EXIT

CHANGELOG="$SKILL_DIR/CHANGELOG.md"
if [ -f "$CHANGELOG" ]; then
  awk '
    /^## \[Unreleased\]/ { found=1; next }
    found && /^## \[/ { exit }
    found { print }
  ' "$CHANGELOG" | sed -e '/./,$!d' -e :a -e '/^\n*$/{$d;N;ba' -e '}' > "$NOTES_FILE"
fi

if [ ! -s "$NOTES_FILE" ]; then
  echo "Release ${SKILL_NAME} v${VERSION}" > "$NOTES_FILE"
fi

echo "Releasing $SKILL_NAME v$VERSION as tag $TAG"

git tag -a "$TAG" -m "$SKILL_NAME v$VERSION"
git push origin "$TAG"
gh release create "$TAG" --title "$SKILL_NAME v$VERSION" --notes-file "$NOTES_FILE"

echo "✓ Released $TAG"
