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
#
# Before tagging: promotes [Unreleased] → [version] - date in the skill's
# CHANGELOG and pushes to master, so CI's promotion step is always a no-op.

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

# Guard 1: local master must not be behind origin
git fetch origin master --quiet
git merge-base --is-ancestor origin/master HEAD \
  || { echo "Error: local master is behind origin/master — run 'git pull --rebase' first"; exit 1; }

if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "Error: tag $TAG already exists" && exit 1
fi

# Extract release notes from [Unreleased] before promotion
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

# Guard 2: warn if [Unreleased] has no content
if [ ! -s "$NOTES_FILE" ]; then
  echo "Warning: [Unreleased] section is empty — release notes will be title-only."
  echo "Release ${SKILL_NAME} v${VERSION}" > "$NOTES_FILE"
fi

echo "Releasing $SKILL_NAME v$VERSION as tag $TAG"

# Promote [Unreleased] → [version] - date locally before tagging so CI is a no-op
if [ -f "$CHANGELOG" ] && grep -q "^## \[Unreleased\]" "$CHANGELOG"; then
  DATE="$(date -u +%Y-%m-%d)"
  # BSD sed (macOS) requires -i ''; GNU sed (Linux) accepts -i '' too
  sed -i '' "s/^## \[Unreleased\]/## [${VERSION}] - ${DATE}/" "$CHANGELOG" 2>/dev/null \
    || sed -i "s/^## \[Unreleased\]/## [${VERSION}] - ${DATE}/" "$CHANGELOG"
  git add "$CHANGELOG"
  git diff --cached --quiet || git commit -m "chore: promote ${SKILL_NAME} CHANGELOG for v${VERSION}"
  git push origin master
  echo "✓ Promoted CHANGELOG and pushed to master"
fi

# Package the skill so artifacts are ready to upload with the release
bash "$REPO_ROOT/scripts/package-skill.sh" "$SKILL_NAME" "$VERSION"

git tag -a "$TAG" -m "$SKILL_NAME v$VERSION"
git push origin "$TAG"

# Guard 3: upload .skill + versioned .skill + .json metadata
gh release create "$TAG" \
  --title "$SKILL_NAME v$VERSION" \
  --notes-file "$NOTES_FILE" \
  "dist/${SKILL_NAME}.skill" \
  "dist/${SKILL_NAME}-${VERSION}.skill" \
  "dist/${SKILL_NAME}-${VERSION}.json"

echo "✓ Released $TAG"
