#!/usr/bin/env bash
# Tag, push, and publish an independently versioned Claude Code agent.
# Usage: bash scripts/release-agent.sh cane-wiki
set -euo pipefail

AGENT_NAME="${1:-}"
case "$AGENT_NAME" in
  ''|*[!a-zA-Z0-9_-]*) echo "Usage: $0 <agent-name>" >&2; exit 1 ;;
esac

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
AGENT_DIR="agents/$AGENT_NAME"
SOURCE="$AGENT_DIR/$AGENT_NAME.md"
VERSION_FILE="$AGENT_DIR/VERSION"
CHANGELOG="$AGENT_DIR/CHANGELOG.md"
[ -f "$SOURCE" ] && [ -f "$VERSION_FILE" ] || { echo "Agent or VERSION missing in $AGENT_DIR" >&2; exit 1; }
if [ "$AGENT_NAME" = "cane-wiki" ]; then
  python3 "$REPO_ROOT/scripts/build-codex-agent.py" --check
fi
VERSION="$(tr -d '[:space:]' < "$VERSION_FILE")"
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Invalid agent version: $VERSION" >&2; exit 1; }
TAG="agents/$AGENT_NAME/v$VERSION"

[ -z "$(git status --porcelain)" ] || { echo "Working tree must be clean before release" >&2; exit 1; }
[ "$(git branch --show-current)" = "master" ] || { echo "Release from master only" >&2; exit 1; }
git fetch origin master --tags --quiet
git merge-base --is-ancestor origin/master HEAD || { echo "Local branch is behind origin/master" >&2; exit 1; }
if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
  echo "Tag already exists: $TAG" >&2; exit 1
fi

NOTES_FILE="$(mktemp)"
trap 'rm -f "$NOTES_FILE"' EXIT
if [ -f "$CHANGELOG" ]; then
  awk '/^## \[Unreleased\]/{found=1; next} found && /^## \[/{exit} found{print}' "$CHANGELOG" > "$NOTES_FILE"
fi
if ! grep -q '[^[:space:]]' "$NOTES_FILE"; then
  echo "Release $AGENT_NAME v$VERSION" > "$NOTES_FILE"
fi

if [ -f "$CHANGELOG" ] && grep -q '^## \[Unreleased\]' "$CHANGELOG"; then
  DATE="$(date -u +%Y-%m-%d)"
  sed -i '' "s/^## \[Unreleased\]/## [$VERSION] - $DATE/" "$CHANGELOG" 2>/dev/null \
    || sed -i "s/^## \[Unreleased\]/## [$VERSION] - $DATE/" "$CHANGELOG"
  git add "$CHANGELOG"
  git diff --cached --quiet || git commit -m "chore: promote $AGENT_NAME agent CHANGELOG for v$VERSION"
  git push origin HEAD:master
fi

mkdir -p dist
ASSET="dist/$AGENT_NAME-$VERSION.md"
cp "$SOURCE" "$ASSET"
RELEASE_ASSETS=("$ASSET")
if [ "$AGENT_NAME" = "cane-wiki" ]; then
  CODEX_ASSET="dist/$AGENT_NAME-$VERSION.toml"
  cp "$AGENT_DIR/$AGENT_NAME.codex.toml" "$CODEX_ASSET"
  RELEASE_ASSETS+=("$CODEX_ASSET")
fi
git tag -a "$TAG" -m "$AGENT_NAME agent v$VERSION"
git push origin "$TAG"
gh release create "$TAG" --title "$AGENT_NAME agent v$VERSION" --notes-file "$NOTES_FILE" "${RELEASE_ASSETS[@]}"
echo "✓ Released $TAG"
