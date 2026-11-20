#!/bin/bash
# Build the universal .skill plus Codex, Claude Code, and Claude.ai archives.
# Usage: ./scripts/package-skill.sh <skill-name> [version]
#
# If [version] is omitted, it is read from the skill's SKILL.md frontmatter
# (metadata.version) — that frontmatter is the single source of truth for a
# skill's version. Releases are tagged per skill as <skill-name>/v<version>.

set -e

SKILL_NAME="${1:-}"
VERSION="${2:-}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$REPO_ROOT/skills/$SKILL_NAME"
DIST_DIR="$REPO_ROOT/dist"
# Artifact names stay flat even when the skill lives under a family directory
# (e.g. skills/mm-wiki/mm-wiki-ingest → artifact name mm-wiki-ingest).
ARTIFACT_NAME="$(basename "$SKILL_NAME")"

[ -z "$SKILL_NAME" ] && echo "Usage: $0 <skill-name> [version]" && exit 1
case "$SKILL_NAME" in
  /*|*..*) echo "Error: invalid skill path '$SKILL_NAME'" >&2; exit 1 ;;
esac
[ ! -f "$SKILL_DIR/SKILL.md" ] && echo "Error: $SKILL_DIR/SKILL.md not found" && exit 1

# Derive version from frontmatter (metadata.version) when not passed explicitly.
if [ -z "$VERSION" ]; then
  VERSION="$(grep -E '^[[:space:]]*version:[[:space:]]*' "$SKILL_DIR/SKILL.md" \
    | head -1 | sed -E 's/^[[:space:]]*version:[[:space:]]*//; s/[[:space:]]*$//')"
fi
[ -z "$VERSION" ] && echo "Error: no version given and none found in $SKILL_NAME/SKILL.md (metadata.version)" && exit 1

mkdir -p "$DIST_DIR"

cd "$SKILL_DIR"
SKILL_FILE="$DIST_DIR/${ARTIFACT_NAME}.skill"
tar -czf "$SKILL_FILE" --exclude='.DS_Store' --exclude='*.swp' --exclude='config.json' --exclude='config.json.bak*' .

cp "$SKILL_FILE" "$DIST_DIR/${ARTIFACT_NAME}-${VERSION}.skill"

cat > "$DIST_DIR/${ARTIFACT_NAME}-${VERSION}.json" << JSON
{
  "name": "${ARTIFACT_NAME}",
  "version": "${VERSION}",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON

echo "✓ dist/${ARTIFACT_NAME}.skill"
echo "✓ dist/${ARTIFACT_NAME}-${VERSION}.skill (v${VERSION})"

# Platform packagers are leaf commands: none calls this orchestrator.
bash "$REPO_ROOT/scripts/package-skill-codex.sh" "$SKILL_NAME" "$VERSION"
bash "$REPO_ROOT/scripts/package-skill-claude-code.sh" "$SKILL_NAME" "$VERSION"
bash "$REPO_ROOT/scripts/package-skill-claudeai.sh" "$SKILL_NAME" "$VERSION"
