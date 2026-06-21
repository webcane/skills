#!/usr/bin/env python3
"""One-off assertion script exercising `_migrate_root_mood` (03-04 MOOD-01 verification).

Builds an in-memory profile carrying a root `mood` field plus a `layers.mood`
block with one cell of each kind (court="true", pip="false", ace=<custom text>),
runs the migration, and asserts the expected outcome. Prints `migrate-ok` on
success. Not a shipped feature — safe to delete after the SUMMARY records it
passed, or keep as a lightweight regression check.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_config as m

MOOD_LINE = "gothic and brooding atmosphere"

profile = {
    "mood": MOOD_LINE,
    "layers": {
        "mood": {
            "court": "true",
            "pip": "false",
            "ace": "already custom ace mood text",
        }
    },
}

changed = m._migrate_root_mood(profile)

assert changed is True, "expected _migrate_root_mood to report a change"
assert "mood" not in profile, "root 'mood' key should be removed"
assert profile["layers"]["mood"]["court"] == MOOD_LINE, (
    f"expected court cell to be upgraded to the mood line, got {profile['layers']['mood']['court']!r}"
)
assert profile["layers"]["mood"]["pip"] == "false", (
    f"expected pip cell to stay 'false', got {profile['layers']['mood']['pip']!r}"
)
assert profile["layers"]["mood"]["ace"] == "already custom ace mood text", (
    f"expected ace cell's custom text to be preserved, got {profile['layers']['mood']['ace']!r}"
)

# Also verify the no-op path: a profile with no root mood key returns False
# and leaves the profile untouched.
untouched = {"layers": {"mood": {"court": "true"}}}
assert m._migrate_root_mood(untouched) is False
assert untouched == {"layers": {"mood": {"court": "true"}}}

print("migrate-ok")
