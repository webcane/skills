#!/usr/bin/env bash
# Install a versioned agent asset from a GitHub Release.
# Usage: INSTALL_DIR=/path/to/agents bash scripts/install-agent.sh cane-wiki 0.1.0
set -euo pipefail

AGENT_NAME="${1:-}"
VERSION="${2:-}"
case "$AGENT_NAME" in
  ''|*[!a-zA-Z0-9_-]*) echo "Usage: $0 <agent-name> <version>" >&2; exit 1 ;;
esac
case "$VERSION" in
  ''|*[!a-zA-Z0-9._-]*) echo "Usage: $0 <agent-name> <version>" >&2; exit 1 ;;
esac

GITHUB_REPO="${GITHUB_REPO:-webcane/skills}"
TARGET_DIR="${INSTALL_DIR:-$HOME/.claude/agents}"
ASSET="$AGENT_NAME-$VERSION.md"
URL="https://github.com/$GITHUB_REPO/releases/download/agents%2F$AGENT_NAME%2Fv$VERSION/$ASSET"
TEMP="$(mktemp -d)"
trap 'rm -rf "$TEMP"' EXIT

curl -L --fail --show-error "$URL" -o "$TEMP/$ASSET"
grep -q "^name: $AGENT_NAME$" "$TEMP/$ASSET" || { echo "Downloaded file is not agent $AGENT_NAME" >&2; exit 1; }
mkdir -p "$TARGET_DIR"
cp "$TEMP/$ASSET" "$TARGET_DIR/$AGENT_NAME.md"
echo "✓ Installed $AGENT_NAME v$VERSION to $TARGET_DIR/$AGENT_NAME.md"
