#!/bin/bash
# Sync canonical shared assets from skills/mm-wiki/ into each member skill dir.
# Usage: ./scripts/sync-mm-wiki.sh [--check]
#
# The mm-wiki family keeps its shared assets in a single logical directory:
#   skills/mm-wiki/shared/    — canonical files (single source of truth)
#   skills/mm-wiki/overrides/ — per-skill variants of shared files
# Each member skill ships a self-contained copy so the packaging pipeline
# (which packs skills/<name>/ as-is) keeps working unchanged. This script
# pushes canonical content into those copies.
#
#   no args   → copy canonical files into member skills (idempotent)
#   --check   → verify every managed copy matches its canonical source;
#               exit 1 and list any that drifted (no writes)
#
# Only the managed files listed below are written. SKILL.md and CHANGELOG.md
# are never touched.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MM="$REPO_ROOT/skills/mm-wiki"
CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

# Mapping: <destination-in-skill>|<canonical-source-relative-to-mm/>
# Entries mirror skills/mm-wiki/MANIFEST.md — keep both in sync.
PAIRS=(
  "mm-wiki-import/references/wiki-conventions.md|shared/wiki-conventions.md"
  "mm-wiki-query/references/wiki-conventions.md|shared/wiki-conventions.md"
  "mm-wiki-lint/references/wiki-conventions.md|shared/wiki-conventions.md"
  "mm-wiki-prune/references/wiki-conventions.md|shared/wiki-conventions.md"
  "mm-wiki-status/references/wiki-conventions.md|shared/wiki-conventions.md"
  "mm-wiki-ingest/references/wiki-conventions.md|overrides/mm-wiki-ingest.wiki-conventions.md"
  "mm-wiki-lint/scripts/wiki_scan.py|shared/wiki_scan.py"
  "mm-wiki-prune/scripts/wiki_scan.py|shared/wiki_scan.py"
  "mm-wiki-status/scripts/wiki_scan.py|shared/wiki_scan.py"
)

DRIFT=0
for pair in "${PAIRS[@]}"; do
  DEST="$MM/${pair%%|*}"
  SRC="$MM/${pair#*|}"

  [ ! -f "$SRC" ] && echo "Error: canonical source missing: $SRC" && exit 1

  if [ "$CHECK" = "1" ]; then
    if ! cmp -s "$SRC" "$DEST"; then
      echo "DRIFT: ${DEST#$REPO_ROOT/}"
      DRIFT=1
    fi
  else
    if ! cmp -s "$SRC" "$DEST"; then
      mkdir -p "$(dirname "$DEST")"
      cp "$SRC" "$DEST"
      echo "synced: ${DEST#$REPO_ROOT/}"
    fi
  fi
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
