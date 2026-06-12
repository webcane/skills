#!/bin/bash
# Download and install a .skill file from GitHub
# Usage: ./scripts/install-skill.sh <skill-name> [version]
# Env:   INSTALL_DIR (default: .), GITHUB_REPO (default: webcane/skills)

set -e

SKILL_NAME="${1:-}"
VERSION="${2:-latest}"
INSTALL_DIR="${INSTALL_DIR:-.}"
GITHUB_REPO="${GITHUB_REPO:-webcane/skills}"
BRANCH="${BRANCH:-main}"

[ -z "$SKILL_NAME" ] && echo "Usage: $0 <skill-name> [version]" && exit 1

if [ "$VERSION" = "latest" ]; then
  URL="https://raw.githubusercontent.com/$GITHUB_REPO/$BRANCH/dist/${SKILL_NAME}.skill"
else
  URL="https://github.com/$GITHUB_REPO/releases/download/v${VERSION}/${SKILL_NAME}-${VERSION}.skill"
fi

echo "Downloading $SKILL_NAME ($VERSION)..."
TEMP=$(mktemp -d)
curl -L --fail --progress-bar "$URL" -o "$TEMP/${SKILL_NAME}.skill" || {
  echo "Error: download failed from $URL"
  rm -rf "$TEMP"; exit 1
}

mkdir -p "$INSTALL_DIR/$SKILL_NAME"

# Back up an existing config.json (it may hold the user's saved profiles) before
# extraction overwrites it with the skill's shipped factory-default config.json.
EXISTING_CONFIG="$INSTALL_DIR/$SKILL_NAME/config.json"
if [ -f "$EXISTING_CONFIG" ]; then
  BACKUP="$EXISTING_CONFIG.bak.$(date +%Y%m%d%H%M%S)"
  cp "$EXISTING_CONFIG" "$BACKUP"
  echo "Backed up existing config.json to $(basename "$BACKUP")"
fi

tar -xzf "$TEMP/${SKILL_NAME}.skill" -C "$INSTALL_DIR/$SKILL_NAME"
rm -rf "$TEMP"

[ ! -f "$INSTALL_DIR/$SKILL_NAME/SKILL.md" ] && echo "Error: SKILL.md missing after extraction" && exit 1

echo "✓ Installed to $INSTALL_DIR/$SKILL_NAME"