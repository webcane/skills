#!/usr/bin/env bash
# Install a repository agent into Claude Code's user agent directory.
# Usage: INSTALL_DIR=/path/to/agents bash scripts/install-agent-local.sh cane-wiki
set -euo pipefail

AGENT_NAME="${1:-}"
case "$AGENT_NAME" in
  ''|*[!a-zA-Z0-9_-]*) echo "Usage: $0 <agent-name>" >&2; exit 1 ;;
esac

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$REPO_ROOT/agents/$AGENT_NAME/$AGENT_NAME.md"
TARGET_DIR="${INSTALL_DIR:-$HOME/.claude/agents}"
[ -f "$SOURCE" ] || { echo "Agent not found: $SOURCE" >&2; exit 1; }

mkdir -p "$TARGET_DIR"
cp "$SOURCE" "$TARGET_DIR/$AGENT_NAME.md"
echo "✓ Installed $AGENT_NAME to $TARGET_DIR/$AGENT_NAME.md"
