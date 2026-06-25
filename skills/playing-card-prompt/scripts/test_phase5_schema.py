#!/usr/bin/env python3
"""Standalone assertion script proving the Phase 5 schema contract.

No pytest dependency (the repo has no test framework) — bare `assert`
statements, run as `python3 test_phase5_schema.py` from this directory (or
anywhere, since it inserts this directory onto sys.path).

Monkeypatches `manage_config.CONFIG_PATH` to a tempfile-created path so it
never touches the real shipped `config.json`.

Encodes the Phase 5 contract (UNIFY-01/02/03, TITLE-01, BACK-EPH-01):
- Every `layers.<layer>.<group>` cell is non-strict (figure included).
- A literal "true" written via cmd_set is persisted verbatim for
  figure/split/seamless (no eager resolution to an alias/"none").
- `title.enabled` and the five `back_*` fields are no longer valid
  persistent keys (options_for returns None, not in PERSISTENT_KEYS).
- `_migrate_drop_phase5_persistent` drops stale title/back_* keys from an
  existing profile so validation passes cleanly afterward.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import manage_config as m  # noqa: E402


def with_temp_config(fn):
    """Run fn() with manage_config.CONFIG_PATH pointed at a throwaway temp file."""
    real_path = m.CONFIG_PATH
    with tempfile.TemporaryDirectory() as tmp:
        m.CONFIG_PATH = Path(tmp) / "config.json"
        try:
            fn()
        finally:
            m.CONFIG_PATH = real_path


def test_layers_figure_non_strict():
    opt = m.options_for("layers.figure.court")
    assert opt is not None, "layers.figure.court should resolve to options"
    allowed, strict = opt
    assert strict is False, f"layers.figure.court must be strict=False (UNIFY-01), got strict={strict}"


def test_layers_split_non_strict():
    opt = m.options_for("layers.split.court")
    assert opt is not None
    allowed, strict = opt
    assert strict is False, f"layers.split.court must be strict=False, got strict={strict}"


def test_layers_seamless_non_strict():
    opt = m.options_for("layers.seamless.court")
    assert opt is not None
    allowed, strict = opt
    assert strict is False, f"layers.seamless.court must be strict=False, got strict={strict}"


def test_custom_figure_text_validates():
    ok, note = m.validate_value("layers.figure.court", "a weathered stone gargoyle")
    assert ok is True, (
        "custom figure text must validate under the unified non-strict contract "
        f"(UNIFY-01); got ok={ok}, note={note!r}"
    )


def test_title_enabled_removed():
    assert m.options_for("title.enabled") is None, "title.enabled must no longer resolve via options_for (TITLE-01)"
    assert "title.enabled" not in m.PERSISTENT_KEYS, "title.enabled must not be in PERSISTENT_KEYS (TITLE-01)"


def test_back_fields_removed():
    for k in ("back_purpose", "back_design", "back_pattern", "back_palette", "back_symmetry"):
        assert m.options_for(k) is None, f"{k} must no longer resolve via options_for (BACK-EPH-01)"
        assert k not in m.PERSISTENT_KEYS, f"{k} must not be in PERSISTENT_KEYS (BACK-EPH-01)"


def _set_and_read_back(key: str, value: str) -> str:
    cfg = m.load_raw()
    name = m.active_profile_name(cfg)
    m.cmd_set([key, value])
    cfg2 = m.load_raw()
    return m.get_path(cfg2["profiles"][name], key)


def test_split_true_round_trip():
    def run():
        persisted = _set_and_read_back("layers.split.court", "true")
        assert persisted == "true", (
            f"layers.split.court set to 'true' must persist literally (UNIFY-02/03), got {persisted!r}"
        )

    with_temp_config(run)


def test_seamless_true_round_trip():
    def run():
        persisted = _set_and_read_back("layers.seamless.court", "true")
        assert persisted == "true", (
            f"layers.seamless.court set to 'true' must persist literally (UNIFY-02), got {persisted!r}"
        )

    with_temp_config(run)


def test_figure_true_round_trip():
    def run():
        persisted = _set_and_read_back("layers.figure.court", "true")
        assert persisted == "true", (
            f"layers.figure.court set to 'true' must persist literally (UNIFY-02), "
            f"not resolved to LAYER_DEFAULTS['figure']['court'] ({m.LAYER_DEFAULTS['figure']['court']!r}); "
            f"got {persisted!r}"
        )

    with_temp_config(run)


def test_migrate_drop_phase5_persistent():
    profile = {
        "title": {"enabled": "true"},
        "back_purpose": "casino",
        "layers": {"figure": {"pip": "true"}},
    }
    changed = m._migrate_drop_phase5_persistent(profile)
    assert changed is True, "_migrate_drop_phase5_persistent should report it changed the profile"
    assert "title" not in profile, "stale 'title' key must be dropped"
    assert "back_purpose" not in profile, "stale 'back_purpose' key must be dropped"
    # layers.* cells are intentionally untouched (a literal "true" is now valid, D-07).
    assert profile["layers"]["figure"]["pip"] == "true", "layers.* cells must NOT be touched by this migration"
    flat = m._flatten(profile)
    extra = set(flat.keys()) - m.PERSISTENT_KEYS
    assert not extra, f"migrated profile must contain no keys outside PERSISTENT_KEYS, found: {extra}"


TESTS = [
    test_layers_figure_non_strict,
    test_layers_split_non_strict,
    test_layers_seamless_non_strict,
    test_custom_figure_text_validates,
    test_title_enabled_removed,
    test_back_fields_removed,
    test_split_true_round_trip,
    test_seamless_true_round_trip,
    test_figure_true_round_trip,
    test_migrate_drop_phase5_persistent,
]


def main() -> int:
    failures = []
    for test in TESTS:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except AssertionError as e:
            print(f"FAIL: {test.__name__}: {e}")
            failures.append(test.__name__)
        except Exception as e:  # noqa: BLE001 - report unexpected errors as failures too
            print(f"ERROR: {test.__name__}: {type(e).__name__}: {e}")
            failures.append(test.__name__)
    if failures:
        print(f"\n{len(failures)}/{len(TESTS)} FAILED: {', '.join(failures)}")
        return 1
    print(f"\nALL PASS ({len(TESTS)}/{len(TESTS)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
