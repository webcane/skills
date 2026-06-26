#!/bin/bash
# Phase 5 (structural-cleanup) verification gate for playing-card-prompt.
# Usage: bash skills/playing-card-prompt/scripts/verify_phase5_gate.sh
#
# Runs the four required verification commands plus the archive-exclusion
# check, exiting non-zero on any failure (VERIFY-5).
#
# NOTE: test_phase5_schema.py is a one-off contract/migration-fixture test
# (mirrors the Phase 3 precedent of deleting such scripts post-pass so they
# are not shipped in the packaged skill). If it still exists on disk when
# this gate runs, it is executed as part of the gate; if it has already
# been deleted (the expected end state after Plan 07's Task 1), this gate
# skips straight to validate/package/install and the archive-exclusion
# check, which is what actually proves it was not shipped.

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
SKILL_NAME="playing-card-prompt"
TEST_SCRIPT="$SKILL_DIR/scripts/test_phase5_schema.py"

echo "== Phase 5 verification gate: $SKILL_NAME =="

if [ -f "$TEST_SCRIPT" ]; then
  echo "-- [1/5] python3 scripts/test_phase5_schema.py --"
  python3 "$TEST_SCRIPT"
else
  echo "-- [1/5] test_phase5_schema.py already removed (post-pass deletion) — skipping --"
fi

echo "-- [2/5] python3 scripts/manage_config.py validate --"
python3 "$SKILL_DIR/scripts/manage_config.py" validate

echo "-- [3/5] bash scripts/package-skill.sh $SKILL_NAME --"
bash "$REPO_ROOT/scripts/package-skill.sh" "$SKILL_NAME"

echo "-- [4/5] bash scripts/install-local.sh $SKILL_NAME --"
bash "$REPO_ROOT/scripts/install-local.sh" "$SKILL_NAME"

echo "-- [5/5] archive-exclusion check: test_phase5_schema.py must not be shipped --"
COUNT="$(tar -tzf "$REPO_ROOT/dist/${SKILL_NAME}.skill" | grep -c test_phase5_schema || true)"
if [ "$COUNT" -ne 0 ]; then
  echo "FAIL: test_phase5_schema.py found in dist/${SKILL_NAME}.skill ($COUNT occurrence(s))" >&2
  exit 1
fi
echo "✓ test_phase5_schema.py is not present in the packaged archive"

echo ""
echo "✓ Phase 5 verification gate PASSED"
