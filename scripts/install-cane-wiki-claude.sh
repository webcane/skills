#!/usr/bin/env bash
# Install the Claude Code cane-wiki-init skill and cane-wiki subagent.
# Env: INSTALL_DIR (default ~/.claude/skills), AGENT_INSTALL_DIR (default ~/.claude/agents)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${INSTALL_DIR:-$HOME/.claude/skills}"
AGENTS_DIR="${AGENT_INSTALL_DIR:-$HOME/.claude/agents}"
for name in cane-wiki-init; do
  bash "$REPO_ROOT/scripts/package-skill-claude-code.sh" "$name"
  mkdir -p "$SKILLS_DIR"
  unzip -q -o "$REPO_ROOT/dist/$name-claude-code.zip" -d "$SKILLS_DIR"
  echo "✓ Installed $name to $SKILLS_DIR/$name"
done
INSTALL_DIR="$AGENTS_DIR" bash "$REPO_ROOT/scripts/install-agent-local.sh" cane-wiki
