#!/bin/bash
# Sync canonical mm-wiki assets into member skill dirs.
# Usage: ./scripts/sync-mm-wiki.sh [--check]
#
# Two canonical pools feed the member skills:
#   skills/mm-wiki/shared/*   → copied into EVERY member's references/
#                                (conventions/docs, e.g. wiki-conventions.md)
#   skills/mm-wiki/scripts/*  → copied only into the scanner members' scripts/
#                                (mm-wiki-lint, mm-wiki-prune, mm-wiki-status)
#                                — a single scanner, not copied to everyone
# Each member skill ships a self-contained copy so the packaging pipeline
# (which packs skills/<name>/ as-is) keeps working unchanged.
#
# Per-skill custom files (e.g. mm-wiki-ingest/references/wiki-conventions.extra.md)
# are hand-maintained and NEVER overwritten — only files that exist in the
# canonical pools are managed.
#
#   no args   → copy canonical files into member skills (idempotent)
#   --check   → verify every managed copy matches its canonical source;
#               exit 1 and list any that drifted (no writes)

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MM="$REPO_ROOT/skills/mm-wiki"
CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

# Members that invoke the family scanner and therefore receive scripts/*.
SCANNER_MEMBERS=(mm-wiki-lint mm-wiki-prune mm-wiki-status)

DRIFT=0

sync_one() { # src dest — copy if different; --check reports drift
  local src="$1" dest="$2"
  if [ "$CHECK" = "1" ]; then
    if ! cmp -s "$src" "$dest"; then
      echo "DRIFT: ${dest#$REPO_ROOT/}"
      return 1
    fi
  else
    if ! cmp -s "$src" "$dest"; then
      mkdir -p "$(dirname "$dest")"
      cp "$src" "$dest"
      echo "synced: ${dest#$REPO_ROOT/}"
    fi
  fi
  return 0
}

# 1) Every nested member skill (a dir containing a SKILL.md) receives every
#    shared file. The family home itself (skills/mm-wiki) has no SKILL.md and
#    is skipped.
MEMBERS=()
while IFS= read -r skill_md; do
  MEMBERS+=("$(dirname "$skill_md")")
done < <(find "$MM" -name SKILL.md | sort)

for member in "${MEMBERS[@]}"; do
  for src in "$MM"/shared/*; do
    [ -f "$src" ] || continue
    sync_one "$src" "$member/references/$(basename "$src")" || DRIFT=1
  done
done

# 2) Family scripts go only to the scanner members (not copied to everyone).
for name in "${SCANNER_MEMBERS[@]}"; do
  member="$MM/$name"
  for src in "$MM"/scripts/*; do
    [ -f "$src" ] || continue
    sync_one "$src" "$member/scripts/$(basename "$src")" || DRIFT=1
  done
done

if [ "$CHECK" = "1" ]; then
  if [ "$DRIFT" = "1" ]; then
    echo "→ run: bash scripts/sync-mm-wiki.sh to restore canonical content"
    exit 1
  fi
  echo "✓ all mm-wiki shared assets in sync"
else
  echo "✓ sync complete"
fi
