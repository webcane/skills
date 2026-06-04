#!/bin/bash
# Package a skill directory into a distributable .skill file (tar.gz)
# Usage: ./scripts/package-skill.sh <skill-name> [version]

set -e

SKILL_NAME="${1:-}"
VERSION="${2:-1.0.0}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$REPO_ROOT/skills/$SKILL_NAME"
DIST_DIR="$REPO_ROOT/dist"

[ -z "$SKILL_NAME" ] && echo "Usage: $0 <skill-name> [version]" && exit 1
[ ! -f "$SKILL_DIR/SKILL.md" ] && echo "Error: $SKILL_DIR/SKILL.md not found" && exit 1

mkdir -p "$DIST_DIR"

cd "$SKILL_DIR"
SKILL_FILE="$DIST_DIR/${SKILL_NAME}.skill"
tar -czf "$SKILL_FILE" --exclude='.DS_Store' --exclude='*.swp' .

cp "$SKILL_FILE" "$DIST_DIR/${SKILL_NAME}-${VERSION}.skill"

cat > "$DIST_DIR/${SKILL_NAME}-${VERSION}.json" << JSON
{
  "name": "${SKILL_NAME}",
  "version": "${VERSION}",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON

echo "✓ dist/${SKILL_NAME}.skill"
echo "✓ dist/${SKILL_NAME}-${VERSION}.skill"