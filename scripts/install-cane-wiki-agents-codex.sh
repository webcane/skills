#!/usr/bin/env bash
# Install only the Codex cane-wiki agents from this checkout.
# Env: AGENT_INSTALL_DIR (default: ${CODEX_HOME:-~/.codex}/agents)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_DIR="${AGENT_INSTALL_DIR:-${CODEX_HOME:-$HOME/.codex}/agents}"
python3 "$REPO_ROOT/scripts/build-codex-agent.py" --check
mkdir -p "$AGENT_DIR"

for name in cane-wiki cane-wiki-critic; do
  source="$REPO_ROOT/agents/$name/$name.codex.toml"
  target="$AGENT_DIR/$name.toml"
  if [ -f "$target" ] && cmp -s "$source" "$target"; then
    echo "✓ Already installed: $name"
    continue
  fi
  if [ -f "$target" ]; then
    backup="$target.bak.$(date +%Y%m%d%H%M%S)"
    mv "$target" "$backup"
    echo "Backed up $name to $backup"
  fi
  cp "$source" "$target"
  echo "✓ Installed $name to $target"
done
