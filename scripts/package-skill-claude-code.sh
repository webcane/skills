#!/usr/bin/env bash
# Package a canonical Agent Skill with Claude Code-specific instructions.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec bash "$REPO_ROOT/scripts/package-skill-platform.sh" claude-code "$@"
