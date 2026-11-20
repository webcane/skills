#!/bin/bash
# Build all packages and install into Codex, OpenCode, and Claude Code by default.
# Usage: ./scripts/install-local.sh [skill-name] [--target all|codex|opencode|claude-code]
# INSTALL_DIR restricts installation to that directory; --target selects its format.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
SKILL_NAME=""
INSTALL_TARGET=""
usage() {
  echo "Usage: $0 [skill-name] [--target all|codex|opencode|claude-code]"
  echo "Default: install all three. INSTALL_DIR: install only there (format inferred or --target)."
}
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      [ "$#" -ge 2 ] || { usage >&2; exit 1; }
      INSTALL_TARGET="$2"; shift 2 ;;
    --target=*) INSTALL_TARGET="${1#*=}"; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
    *)
      [ -z "$SKILL_NAME" ] || { echo "Unexpected argument: $1" >&2; exit 1; }
      SKILL_NAME="$1"; shift ;;
  esac
done
case "$INSTALL_TARGET" in
  ''|all|codex|opencode|claude-code) ;;
  claude) INSTALL_TARGET="claude-code" ;;
  *) echo "Unknown target: $INSTALL_TARGET" >&2; exit 1 ;;
esac

# Preserve INSTALL_DIR as a single-destination override, including old callers.
if [ -n "${INSTALL_DIR:-}" ]; then
  [ "$INSTALL_TARGET" != all ] || {
    echo "INSTALL_DIR cannot be combined with --target all; choose one target or unset INSTALL_DIR." >&2
    exit 1
  }
  if [ -z "$INSTALL_TARGET" ]; then
    case "${INSTALL_DIR%/}" in
      */.agents/skills|*/.codex/skills) INSTALL_TARGET="codex" ;;
      */.config/opencode/skills|*/.opencode/skills) INSTALL_TARGET="opencode" ;;
      */.claude/skills) INSTALL_TARGET="claude-code" ;;
      *) INSTALL_TARGET="generic" ;;
    esac
  fi
else
  INSTALL_TARGET="${INSTALL_TARGET:-all}"
fi

# Build the list of available skills by locating every SKILL.md, so nested
# family dirs (skills/mm-wiki/mm-wiki-ingest) are found and non-skill dirs
# (skills/mm-wiki, the family home) are excluded. The name offered is the
# path relative to skills/ (e.g. mm-wiki/mm-wiki-ingest).
if [ -z "$SKILL_NAME" ]; then
  SKILL_NAMES=()
  while IFS= read -r f; do
    # Strip both the skills/ prefix and the trailing /SKILL.md so the
    # offered name is the skill's directory relative to skills/
    # (e.g. mm-wiki/mm-wiki-import), not the file path.
    rel="${f#$SKILLS_DIR/}"
    SKILL_NAMES+=("${rel%/SKILL.md}")
  done < <(find "$SKILLS_DIR" -name SKILL.md | sort)

  echo "Choose available skills:"
  select choice in "${SKILL_NAMES[@]}"; do
    if [ -n "$choice" ]; then
      SKILL_NAME="$choice"
      break
    fi
    echo "Invalid choice."
  done
fi

case "$SKILL_NAME" in
  ''|/*|*..*) echo "Error: invalid skill path '$SKILL_NAME'" >&2; exit 1 ;;
esac
[ -f "$SKILLS_DIR/$SKILL_NAME/SKILL.md" ] || {
  echo "Error: $SKILLS_DIR/$SKILL_NAME/SKILL.md not found" >&2; exit 1
}
bash "$REPO_ROOT/scripts/package-skill.sh" "$SKILL_NAME"
ARTIFACT_NAME="$(basename "$SKILL_NAME")"

install_target() {
  local harness="$1" directory="$2" stage destination
  mkdir -p "$directory"
  # Extract before replacing an existing installation, using the correct host format.
  stage="$(mktemp -d "$directory/.${ARTIFACT_NAME}.XXXXXX")"
  case "$harness" in
    codex|claude-code)
      if ! unzip -q "$REPO_ROOT/dist/$ARTIFACT_NAME-$harness.zip" -d "$stage"; then
        rm -rf "$stage"; return 1
      fi ;;
    opencode|generic)
      mkdir -p "$stage/$ARTIFACT_NAME"
      if ! tar -xzf "$REPO_ROOT/dist/$ARTIFACT_NAME.skill" -C "$stage/$ARTIFACT_NAME"; then
        rm -rf "$stage"; return 1
      fi ;;
  esac
  if [ ! -f "$stage/$ARTIFACT_NAME/SKILL.md" ]; then
    echo "Error: SKILL.md missing for $harness" >&2
    rm -rf "$stage"; return 1
  fi
  destination="$directory/$ARTIFACT_NAME"
  rm -rf "$destination"
  mv "$stage/$ARTIFACT_NAME" "$destination"
  rmdir "$stage"
  echo "✓ Installed $SKILL_NAME for $harness to $destination"
}

if [ -n "${INSTALL_DIR:-}" ]; then
  install_target "$INSTALL_TARGET" "$INSTALL_DIR"
else
  case "$INSTALL_TARGET" in
    all)
      install_target codex "$HOME/.agents/skills"
      install_target opencode "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills"
      install_target claude-code "$HOME/.claude/skills" ;;
    codex) install_target codex "$HOME/.agents/skills" ;;
    opencode) install_target opencode "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills" ;;
    claude-code) install_target claude-code "$HOME/.claude/skills" ;;
  esac
fi
