#!/usr/bin/env bash
# Install cane-wiki and its three external Obsidian skills for Codex.
# Env: INSTALL_DIR (default: ${CODEX_HOME:-~/.codex}/skills)
#      OBSIDIAN_SKILLS_SOURCE (optional local skills/ directory for offline use)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${INSTALL_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}"
AGENT_DIR="${AGENT_INSTALL_DIR:-${CODEX_HOME:-$HOME/.codex}/agents}"
TEMP="$(mktemp -d)"
trap 'rm -rf "$TEMP"' EXIT

python3 "$REPO_ROOT/scripts/build-codex-agent.py" --check
bash "$REPO_ROOT/scripts/package-skill-codex.sh" cane-wiki-init
unzip -q "$REPO_ROOT/dist/cane-wiki-init-codex.zip" -d "$TEMP/stage"

INSTALL_DIR="$TEMP/stage" bash "$REPO_ROOT/skills/cane-wiki-init/scripts/install-obsidian-skills.sh" codex

mkdir -p "$TARGET_DIR"
for name in cane-wiki-init obsidian-markdown obsidian-cli defuddle; do
  target="$TARGET_DIR/$name"
  if [ -d "$target" ]; then
    if diff -qr "$TEMP/stage/$name" "$target" >/dev/null; then
      echo "✓ Already installed: $name"
      continue
    fi
    backup="$target.bak.$(date +%Y%m%d%H%M%S)"
    mv "$target" "$backup"
    echo "Backed up $name to $backup"
  fi
  cp -R "$TEMP/stage/$name" "$target"
  echo "✓ Installed $name to $target"
done

AGENT_INSTALL_DIR="$AGENT_DIR" bash "$REPO_ROOT/scripts/install-cane-wiki-agents-codex.sh"
