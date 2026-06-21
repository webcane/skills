#!/usr/bin/env python3
"""One-off assertion script verifying the SYNC-01 LAYER_DEFAULTS cell corrections
(03-04 SYNC-01 verification).

Asserts the seven corrected cells in LAYER_DEFAULTS, the matching cells in the
shipped config.json's default profile, and that the default profile carries no
root `mood` key (MOOD-01 carried through the regeneration). Prints `sync-ok` on
success. Not a shipped feature — safe to delete after the SUMMARY records it
passed, or keep as a lightweight regression check.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manage_config as m

EXPECTED = {
    ("decor", "ace"): "true",
    ("ornaments", "ace"): "true",
    ("technique", "pip"): "true",
    ("technique", "ace"): "true",
    ("mood", "pip"): "true",
    ("mood", "ace"): "true",
    ("frame", "pip"): "false",
}

# 1. LAYER_DEFAULTS cells.
for (layer, group), expected in EXPECTED.items():
    actual = m.LAYER_DEFAULTS[layer][group]
    assert actual == expected, (
        f"LAYER_DEFAULTS[{layer!r}][{group!r}] = {actual!r}, expected {expected!r}"
    )

# 2. config.json's default profile mirrors the corrected cells.
cfg = json.loads(m.CONFIG_PATH.read_text())
default_profile = cfg["profiles"]["default"]
for (layer, group), expected in EXPECTED.items():
    actual = default_profile["layers"][layer][group]
    assert actual == expected, (
        f"config.json profiles.default.layers[{layer!r}][{group!r}] = {actual!r}, "
        f"expected {expected!r}"
    )

# 3. No root mood key (MOOD-01 carried through the regeneration).
assert "mood" not in default_profile, "config.json default profile still has a root 'mood' key"

print("sync-ok")
