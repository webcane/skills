#!/usr/bin/env bash
# Install a repository agent into a project's OpenCode agent directory.
# Usage: bash scripts/install-opencode-agent.sh [--force] <agent-name> <project-dir>
set -euo pipefail

FORCE=0
if [ "${1:-}" = "--force" ]; then
  FORCE=1
  shift
fi

if [ "${1:-}" = "--help" ]; then
  echo "Usage: $0 [--force] <agent-name> <project-dir>"
  exit 0
fi

AGENT_NAME="${1:-}"
PROJECT_DIR="${2:-}"
if [ "$#" -ne 2 ] || [[ ! "$AGENT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]] || [ -z "$PROJECT_DIR" ]; then
  echo "Usage: $0 [--force] <agent-name> <project-dir>" >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$REPO_ROOT/agents/$AGENT_NAME/$AGENT_NAME.md"
[ -f "$SOURCE" ] || { echo "Agent not found: $SOURCE" >&2; exit 1; }
[ -d "$PROJECT_DIR" ] || { echo "Project directory not found: $PROJECT_DIR" >&2; exit 1; }

PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd -P)"
TARGET_DIR="$PROJECT_DIR/.opencode/agents"
TARGET="$TARGET_DIR/$AGENT_NAME.md"
RUNTIME_DIR="$PROJECT_DIR/agents/cane-learning"
SKILL_SOURCE="$REPO_ROOT/skills/cane-wiki-init"
SKILL_TARGET="$PROJECT_DIR/.opencode/skills/cane-wiki-init"
RUNTIME_STAGE=""
SKILL_STAGE=""
TEMP_AGENT=""
VERIFY_OUTPUT=""
trap 'if [ -n "$TEMP_AGENT" ]; then rm -f "$TEMP_AGENT"; fi; if [ -n "$VERIFY_OUTPUT" ]; then rm -f "$VERIFY_OUTPUT"; fi; if [ -n "$RUNTIME_STAGE" ] && [ -d "$RUNTIME_STAGE" ]; then rm -rf "$RUNTIME_STAGE"; fi; if [ -n "$SKILL_STAGE" ] && [ -d "$SKILL_STAGE" ]; then rm -rf "$SKILL_STAGE"; fi' EXIT

if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
  [ ! -L "$TARGET" ] && [ -f "$TARGET" ] || {
    echo "Agent destination is not a regular file: $TARGET" >&2
    exit 1
  }
  if [ "$FORCE" -ne 1 ]; then
    echo "Agent already exists: $TARGET (use --force to back it up and replace it)" >&2
    exit 1
  fi
fi

python3 -c 'import yaml' >/dev/null 2>&1 || {
  echo "PyYAML is required to convert agent frontmatter (python3 -m pip install PyYAML)." >&2
  exit 1
}

if [ "$AGENT_NAME" = "cane-learning" ]; then
  RUNTIME_SOURCE="$REPO_ROOT/agents/cane-learning"
  RUNTIME_ITEMS=(methodology.md pipeline.toml validate_run.py cane_learning.py stages schemas)
  RUNTIME_REQUIRED=(
    methodology.md pipeline.toml validate_run.py cane_learning.py
    stages/analyst.md stages/designer.md stages/writer.md stages/reviewer.md
    schemas/ConceptModel.json schemas/LearningSpec.json
    schemas/ArticleDraft.json schemas/QualityReport.json
  )
  for item in "${RUNTIME_REQUIRED[@]}"; do
    [ -e "$RUNTIME_SOURCE/$item" ] || {
      echo "Incomplete cane-learning source: missing $RUNTIME_SOURCE/$item" >&2
      exit 1
    }
  done
  if [ -e "$RUNTIME_DIR" ] || [ -L "$RUNTIME_DIR" ]; then
    [ -d "$RUNTIME_DIR" ] || { echo "cane-learning runtime is not a directory: $RUNTIME_DIR" >&2; exit 1; }
    for item in "${RUNTIME_REQUIRED[@]}"; do
      [ -e "$RUNTIME_DIR/$item" ] || {
        echo "Incomplete cane-learning runtime: missing $RUNTIME_DIR/$item" >&2
        echo "Move it aside or complete it before installing the agent." >&2
        exit 1
      }
    done
  else
    mkdir -p "$PROJECT_DIR/agents"
    RUNTIME_STAGE="$(mktemp -d "$PROJECT_DIR/agents/.cane-learning.XXXXXX")"
    for item in "${RUNTIME_ITEMS[@]}"; do
      cp -R "$RUNTIME_SOURCE/$item" "$RUNTIME_STAGE/"
    done
    mv "$RUNTIME_STAGE" "$RUNTIME_DIR"
    RUNTIME_STAGE=""
  fi
fi

if [ "$AGENT_NAME" = "cane-wiki" ]; then
  [ -f "$SKILL_SOURCE/SKILL.md" ] || {
    echo "cane-wiki-init skill not found: $SKILL_SOURCE/SKILL.md" >&2
    exit 1
  }
  if [ -e "$SKILL_TARGET" ] || [ -L "$SKILL_TARGET" ]; then
    [ -d "$SKILL_TARGET" ] && [ -f "$SKILL_TARGET/SKILL.md" ] || {
      echo "Incomplete cane-wiki-init skill at $SKILL_TARGET" >&2
      exit 1
    }
  else
    mkdir -p "$PROJECT_DIR/.opencode/skills"
    SKILL_STAGE="$(mktemp -d "$PROJECT_DIR/.opencode/skills/.cane-wiki-init.XXXXXX")"
    cp -R "$SKILL_SOURCE/." "$SKILL_STAGE/"
    mv "$SKILL_STAGE" "$SKILL_TARGET"
    SKILL_STAGE=""
  fi
fi

mkdir -p "$TARGET_DIR"
TEMP_AGENT="$TARGET.tmp.$$"
python3 - "$SOURCE" "$TEMP_AGENT" "$AGENT_NAME" <<'PY'
from pathlib import Path
import sys

import yaml

source = Path(sys.argv[1])
target = Path(sys.argv[2])
expected_name = sys.argv[3]
parts = source.read_text(encoding="utf-8").split("---", 2)
if len(parts) != 3:
    raise SystemExit(f"Invalid agent frontmatter: {source}")

frontmatter = yaml.safe_load(parts[1])
if (
    not isinstance(frontmatter, dict)
    or frontmatter.get("name") != expected_name
    or not frontmatter.get("description")
):
    raise SystemExit(f"Agent needs matching name and a description: {source}")

opencode_frontmatter = {
    "description": frontmatter["description"],
    "mode": "primary",
}
content = (
    "---\n"
    + yaml.safe_dump(opencode_frontmatter, allow_unicode=True, sort_keys=False).rstrip()
    + "\n---\n"
    + parts[2].lstrip()
)
target.write_text(content, encoding="utf-8")
PY

if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
  BACKUP="$TARGET.bak.$(date +%Y%m%d%H%M%S)"
  BACKUP_SUFFIX=0
  while [ -e "$BACKUP" ] || [ -L "$BACKUP" ]; do
    BACKUP_SUFFIX=$((BACKUP_SUFFIX + 1))
    BACKUP="$TARGET.bak.$(date +%Y%m%d%H%M%S).$$.$BACKUP_SUFFIX"
  done
  cp -p "$TARGET" "$BACKUP"
  echo "Backed up existing agent to $BACKUP"
fi

mv "$TEMP_AGENT" "$TARGET"
TEMP_AGENT=""
echo "Installed $AGENT_NAME to $TARGET"

if command -v opencode >/dev/null 2>&1; then
  VERIFY_OUTPUT="$(mktemp "${TMPDIR:-/tmp}/opencode-agents.XXXXXX")"
  if (cd "$PROJECT_DIR" && opencode debug agents >"$VERIFY_OUTPUT" 2>/dev/null) \
    && grep -Fq "\"id\": \"$AGENT_NAME\"" "$VERIFY_OUTPUT"; then
    echo "Verified: OpenCode discovers $AGENT_NAME"
  else
    echo "Warning: OpenCode did not confirm discovery; start a new session and check the project path." >&2
  fi
else
  echo "OpenCode CLI not found; skipped discovery verification."
fi
