#!/usr/bin/env python3
"""Manage config.json for the playing-card-prompt skill.

A small, dependency-free CLI for reading, writing, and validating the
persistent settings the wizard loads at startup. config.json holds one or
more named *profiles* — each a full bundle of persistent settings (deck,
style, layers, mood, theme, ...) — plus an `active_profile` pointer. Allowed
values for `deck` and `style` are discovered from the skill's assets/ folder
so the tool stays in sync with what is actually on disk.

Usage:
  manage_config.py show [--profile <name>]      # effective + saved settings
  manage_config.py get <key> [--profile <name>] # print one value (e.g. deck, index.size)
  manage_config.py set <key> <value> [--profile <name>]  # validate + persist
  manage_config.py unset <key> [--profile <name>]        # remove one field
  manage_config.py reset [--yes]        # delete config.json (ALL profiles)
  manage_config.py validate             # check config.json against the schema
  manage_config.py path                 # print the config.json path
  manage_config.py options [key]        # list allowed values
  manage_config.py migrate <figure-true-to-character|seamless-true-to-alias> --yes
                                         # one-off/manual: upgrade a stale "true"
                                         # layers.<figure|seamless>.<group> cell to a
                                         # concrete alias (not run automatically)

  manage_config.py profile list                       # list profiles, mark active
  manage_config.py profile show [<name>]              # show one profile
  manage_config.py profile create <name> [--from <existing>]
  manage_config.py profile switch <name>              # change active profile
  manage_config.py profile rename <old> <new>
  manage_config.py profile delete <name>
  manage_config.py profile reset <name> --yes         # clear a profile's overrides

Keys (within a profile): deck, lettering, style, frame, aspect_ratio, image_generator,
      structure, index.size, index.count, index.layout, index.symbol, index.type,
      layers.<background|decor|ornaments|highlights|frame|figure|mood|technique|split|seamless>.<court|pip|ace|joker|back|special>,
      theme, figure_scale, character_framing

Every `layers.<layer>.<group>` cell (figure included) shares one unified contract:
"false" (layer off), "true" (layer on; the alias/custom text is asked fresh per-card
at generation time — not resolved here), or any other text (an alias or custom
addition, used verbatim as that group's contribution). `layers.mood.<group>` follows
this same schema and is the ONLY mood setting — there is no separate deck-wide
`mood` field; the mood line, when on, is the cell's own value. `layers.figure.<group>`
no longer has a strict type enum — "character"/"building"/"animal"/"custom" remain
valid aliases, but any other custom figure description is also accepted.
`layers.split.<group>` accepts "false", "true", "none", "horizontal-mirrored",
"angled-mirrored", or any custom free-text split description.

`title` and the `back_purpose`/`back_design`/`back_pattern`/`back_palette`/
`back_symmetry` fields are NOT persistent settings — title and card-back design are
asked fresh per-card in the wizard and never written to config.json.

A pre-4.0 config.json may still have `figure_proportion` — it is migrated automatically
to `character_framing` on load (figure_proportion value → character_framing; figure_scale
defaults to "inscribed-in-frame"; layers.figure.<group>="true" → "character").

A pre-MOOD-01 config.json may still have a root `mood` field — it is migrated
automatically on load: the root value replaces any `layers.mood.<group>` cell that
is exactly "true" (custom per-group text already present is left untouched), then
the root key is removed.

A pre-3.6 config.json may still have the old per-layer `ornaments_extra.<group>`,
`highlights_extra.<group>`, and `frame_extra.<group>` fields, and a pre-3.13
config.json may still have a separate `extras.<layer>.<group>` namespace — both are
migrated automatically into the merged `layers.<layer>.<group>` cells the first time
the file is loaded.

A pre-Phase-5 config.json may still have a `title` key or any `back_*` field — both
are dropped automatically on load (they are no longer persistent; see above).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
ASSETS = SKILL_DIR / "assets"

DEFAULT_PROFILE_NAME = "default"

# Enumerations that do not depend on disk contents.
LETTERING = ["anglo-american", "french", "german", "russian", "dutch", "scandinavian"]
INDEX_SIZE = ["standard", "jumbo", "magnum"]
INDEX_COUNT = ["4-index", "2-index", "top-only", "none"]
INDEX_LAYOUT = ["stacked", "side-by-side", "peek", "none"]
INDEX_SYMBOL = ["star-in-circle", "star", "Jkr", "J", "crown", "jester-face", "none"]
INDEX_TYPE = ["standard", "joker"]
ASPECT_PRESETS = ["5:7", "9:14", "14:25", "7:12"]
BOOL_VALUES = ["true", "false"]
STRUCTURE = ["full", "illustration"]

GROUPS = ("court", "pip", "ace", "joker", "back", "special")
LAYERS = ("background", "decor", "ornaments", "highlights", "frame", "figure", "mood", "technique", "split", "seamless")

FIGURE_TYPE = ["character", "building", "animal", "custom"]
SPLIT_VALUES = ["false", "none", "horizontal-mirrored", "angled-mirrored"]
FIGURE_SCALE = ["full-bleed", "inscribed-in-frame", "small-centered", "cross-a-frame"]

BACK_PATTERN_GEOMETRIC = ["diamond", "cross-hatch", "hexgrid", "wave"]
BACK_PATTERN_BOTANICAL = ["vine", "floral", "leaf", "branch"]
BACK_PATTERN_ABSTRACT = ["interlacing", "color-field", "paint-stroke", "fractal"]
BACK_PATTERN_ILLUSTRATED = ["thematic", "portrait", "landscape", "heraldic"]

# Pre-3.6 field names that are migrated into extras.<layer>.<group> (and from there,
# on a later load, into layers.<layer>.<group> — see _migrate_layers_extras) on load.
LEGACY_EXTRA_KEYS = {
    "ornaments_extra": "ornaments",
    "highlights_extra": "highlights",
    "frame_extra": "frame",
}

# LAYER_DEFAULTS is the fallback for blank profiles (profile_create with no --from).
# config.json ships these same values as the 'default' profile — keep both in sync with
# the Defaults table in references/REFERENCE.md, which is the authoritative spec.
LAYER_DEFAULTS = {
    "background": {"court": "true",      "pip": "true",  "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
    "decor":      {"court": "true",      "pip": "false", "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
    "ornaments":  {"court": "true",      "pip": "false", "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
    "highlights": {"court": "false",     "pip": "false", "ace": "false", "joker": "false",     "back": "false", "special": "false"},
    "frame":      {"court": "true",      "pip": "false", "ace": "true",  "joker": "true",      "back": "true",  "special": "false"},
    "figure":     {"court": "character", "pip": "false", "ace": "false", "joker": "character", "back": "false", "special": "false"},
    "mood":       {"court": "true",      "pip": "true",  "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
    "technique":  {"court": "true",      "pip": "true",  "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
    "split":      {"court": "false",     "pip": "false", "ace": "false", "joker": "false",     "back": "false", "special": "false"},
    "seamless":   {"court": "false",     "pip": "false", "ace": "false", "joker": "false",     "back": "false", "special": "false"},
}

DEFAULTS = {
    "deck": "french",
    "lettering": "anglo-american",
    "style": "austrian",
    "frame": "boxed-index",
    "aspect_ratio": "9:14",
    "image_generator": "nanobanana",
    "structure": "full",
    "index": {"size": "standard", "count": "4-index", "layout": "stacked", "symbol": "star-in-circle", "type": "standard"},
    "layers": {layer: dict(groups) for layer, groups in LAYER_DEFAULTS.items()},
    "theme": "",
    "figure_scale": "inscribed-in-frame",
    "character_framing": "",
}

# Top-level field names of a profile — used to detect a pre-3.0 flat config.json
# (one that has no "profiles" wrapper) for migration.
PROFILE_FIELD_KEYS = set(DEFAULTS.keys())

BUILTIN_CONFIG = {
    "active_profile": DEFAULT_PROFILE_NAME,
    "profiles": {DEFAULT_PROFILE_NAME: DEFAULTS},
}

PERSISTENT_KEYS = {"deck", "lettering", "style", "frame", "aspect_ratio", "image_generator",
                   "structure", "index.size", "index.count", "index.layout", "index.symbol",
                   "index.type", "theme", "figure_scale", "character_framing"}
PERSISTENT_KEYS |= {f"layers.{layer}.{g}" for layer in LAYERS for g in GROUPS}


def _discover(subdir: str) -> list[str]:
    """List asset stems (drop .md, ignore names starting with '_')."""
    d = ASSETS / subdir
    if not d.is_dir():
        return []
    return sorted(p.stem for p in d.glob("*.md") if not p.name.startswith("_"))


def allowed_decks() -> list[str]:
    return _discover("decks") or ["french", "german", "swiss", "latin"]


def allowed_styles() -> list[str]:
    # Styles may be custom; this is the on-disk set used for suggestions.
    return _discover("pattern") or ["austrian", "french", "english"]


def allowed_frames() -> list[str]:
    # Frames may be custom; this is the on-disk set used for suggestions.
    return _discover("frame") or ["boxed-index"]


def allowed_figure_proportions() -> list[str]:
    # Figure proportions may be custom; this is the on-disk set used for suggestions.
    return _discover("figure-proportion") or ["waist-up"]


def allowed_figure_types() -> list[str]:
    # Figure types are discovered from assets/figure-type/; fall back to enum.
    return _discover("figure-type") or FIGURE_TYPE


def allowed_figure_scales() -> list[str]:
    # Figure scales are discovered from assets/figure-scale/; fall back to enum.
    return _discover("figure-scale") or FIGURE_SCALE


def allowed_character_framings() -> list[str]:
    # Character framings may be custom; this is the on-disk set used for suggestions.
    return _discover("character-framing") or ["waist-up"]


def allowed_back_patterns(category: str) -> list[str]:
    # back_pattern's valid aliases depend on the current profile's back_design
    # category. Falls back to "geometric" for unknown/custom categories (D-21),
    # mirroring B3's wizard-side fallback in SKILL.md.
    return {
        "geometric": BACK_PATTERN_GEOMETRIC,
        "botanical": BACK_PATTERN_BOTANICAL,
        "abstract": BACK_PATTERN_ABSTRACT,
        "illustrated": BACK_PATTERN_ILLUSTRATED,
    }.get(category, BACK_PATTERN_GEOMETRIC)


def allowed_splits() -> list[str]:
    # Split values are the on-disk stems plus "false" and "none" (which have no file).
    on_disk = _discover("split")
    known = [v for v in SPLIT_VALUES if v not in ("false", "none")]
    merged = list(dict.fromkeys(["false", "none"] + on_disk + known))
    return merged


def allowed_seamless() -> list[str]:
    # Seamless values are the on-disk assets/seamless/ stems plus "false" (off).
    # Unlike split, there is no "none" sibling (D-04) — only false | true | <alias> |
    # <custom_text>; "true" resolves to a default alias at the cmd_set write path.
    merged = list(dict.fromkeys(["false"] + _discover("seamless")))
    return merged


def allowed_engines() -> list[str]:
    # Engines may be custom; this is the on-disk set used for suggestions.
    return _discover("engines") or ["nanobanana", "stable-diffusion", "midjourney", "dalle", "kaze"]


def options_for(key: str, profile: dict | None = None):
    # NOTE (BACK-EPH-01): back_pattern (and the other back_* fields) are no
    # longer persistent keys, so they intentionally do NOT resolve here —
    # options_for/PERSISTENT_KEYS only cover persisted config schema. A
    # per-card wizard step can still call allowed_back_patterns(category)
    # directly (kept below) to list category-gated pattern aliases; it is
    # just no longer wired through this persistent-config choke point.
    fixed = {
        "deck": (allowed_decks(), True),
        "lettering": (LETTERING, True),
        "style": (allowed_styles(), False),          # custom allowed
        "frame": (allowed_frames(), False),          # custom allowed
        "aspect_ratio": (ASPECT_PRESETS, False),     # custom N:M allowed
        "image_generator": (allowed_engines(), False),  # custom allowed
        "structure": (STRUCTURE, True),
        "index.size": (INDEX_SIZE, True),
        "index.count": (INDEX_COUNT, True),
        "index.layout": (INDEX_LAYOUT, True),
        "index.symbol": (INDEX_SYMBOL, False),   # custom glyph/text allowed
        "index.type": (INDEX_TYPE, True),
        "theme": (None, False),   # free text deck-wide theme/symbolism
        "figure_scale": (allowed_figure_scales(), False),  # custom crop text allowed
        "character_framing": (allowed_character_framings(), False),  # custom allowed; "" = not set
    }.get(key)
    if fixed is not None:
        return fixed
    if key.startswith("layers.") and key.count(".") == 2:
        _, layer, group = key.split(".")
        if layer not in LAYERS or group not in GROUPS:
            return None
        # Unified false|true|alias|custom contract (D-06/D-07): every layer is
        # non-strict. "true" means "layer active for this group" — the actual
        # alias/custom text is asked fresh per-card at generation time, not
        # resolved here or at cmd_set write time. A literal custom string is
        # always a valid cell value.
        if layer == "split":
            # allowed_splits() already contributes "false" (and "none") — don't double up.
            return (["true"] + allowed_splits(), False)
        if layer == "figure":
            return (["false", "true"] + allowed_figure_types(), False)
        if layer == "seamless":
            return (list(dict.fromkeys(["false", "true"] + allowed_seamless())), False)
        # All other layers: "true"/"false" toggle; any other text enables + adds.
        return (BOOL_VALUES, False)
    return None


# --- validation ------------------------------------------------------------

def validate_value(key: str, value: str, profile: dict | None = None) -> tuple[bool, str]:
    opt = options_for(key, profile)
    if opt is None:
        return False, f"unknown key '{key}' (valid: {', '.join(sorted(PERSISTENT_KEYS))})"
    allowed, strict = opt
    if allowed is None:  # free text
        return True, ""
    if value == "":  # empty string = "not set" — always valid, no suggestions
        return True, ""
    if key == "aspect_ratio":
        if value in allowed or re.fullmatch(r"\d+:\d+", value):
            return True, ""
        return False, f"aspect_ratio must be a preset ({', '.join(allowed)}) or N:M"
    if value in allowed:
        if key.startswith("layers.figure.") and value == "custom":
            return True, (f"note: '{value}' is the discovered figure-type alias "
                           f"'custom' (resolves to assets/figure-type/custom.md's "
                           f"generic placeholder line), NOT a marker for free-text "
                           f"custom description — to use your own description, set "
                           f"{key} to that description text directly")
        return True, ""
    if strict:
        return False, f"{key} must be one of: {', '.join(allowed)}"
    if key.startswith("layers."):
        return True, (f"note: '{value}' enables this layer (if it wasn't already) "
                       f"and is used as its group-wide addition")
    return True, f"note: '{value}' is a custom {key} (not in {', '.join(allowed)})"


def _flatten(d: dict, prefix: str = "") -> dict:
    flat = {}
    for k, v in d.items():
        full = f"{prefix}{k}"
        if isinstance(v, dict):
            flat.update(_flatten(v, f"{full}."))
        else:
            flat[full] = v
    return flat


# --- config io ---------------------------------------------------------------

def _migrate_extras(profile: dict) -> bool:
    """Move pre-3.6 `*_extra.<group>` fields into `extras.<layer>.<group>`, in place.

    Returns True if anything was migrated. An existing `extras.<layer>.<group>`
    value (if already set) wins over the legacy value for the same slot.
    """
    migrated = False
    for old_key, layer in LEGACY_EXTRA_KEYS.items():
        old = profile.pop(old_key, None)
        if not isinstance(old, dict):
            continue
        migrated = True
        target = profile.setdefault("extras", {}).setdefault(layer, {})
        for g, v in old.items():
            target.setdefault(g, v)
    return migrated


def _migrate_layers_extras(profile: dict) -> bool:
    """Fold a pre-3.13 `extras.<layer>.<group>` namespace into `layers.<layer>.<group>`.

    `layers.<layer>.<group>` becomes a free-text cell: "false" (layer off), "true"
    (layer on, no addition), or any other text (layer on, used as its group-wide
    addition). A layer that was "false" drops its extras text (it was never applied,
    so dropping it preserves the old resolved output); a layer that was "true" (or
    unset, defaulting to "true") becomes its extras text if that text is non-empty.

    Returns True only if a `layers.*` cell was actually mutated (WR-05) — an `extras`
    key that is `{}` or contains only falsy/empty group values is still removed from
    the profile (it's stale data) but does not by itself count as a migration, so
    callers don't print a misleading "migrated" note or write the file unnecessarily.
    """
    extras = profile.pop("extras", None)
    if not isinstance(extras, dict):
        return False
    changed = False
    layers = profile.setdefault("layers", {})
    for layer, groups in extras.items():
        if not isinstance(groups, dict):
            continue
        for group, extra in groups.items():
            if not extra:
                continue
            current = layers.get(layer, {}).get(group, LAYER_DEFAULTS.get(layer, {}).get(group, "true"))
            if current != "false":
                layers.setdefault(layer, {})[group] = extra
                changed = True
    return changed


def _migrate_figure_proportion(profile: dict) -> bool:
    """Migrate a pre-4.0 profile that has `figure_proportion` to the new schema.

    Mapping (D-06/D-07):
    - figure_proportion → character_framing (if character_framing not already set)
    - figure_scale defaults to "inscribed-in-frame" if not already set
    - figure_proportion key is removed from the profile

    Does NOT touch `layers.figure.<group>` cells — like
    `_migrate_figure_true_to_character`/`_migrate_seamless_true_to_alias`, eagerly
    rewriting a stored literal "true" to "character" would silently discard data
    and fight the unified D-06/D-07 contract (a literal "true" is now a valid,
    intentionally preserved cell value, T-05-03). Resolution of "true" to a
    concrete figure type is deferred to per-card wizard steps.

    Returns True if anything was changed.
    """
    if "figure_proportion" not in profile:
        return False
    old_val = profile.pop("figure_proportion")
    changed = True
    if old_val and not profile.get("character_framing"):
        profile["character_framing"] = old_val
    profile.setdefault("figure_scale", "inscribed-in-frame")
    return changed


def _migrate_figure_true_to_character(profile: dict) -> bool:
    """Upgrade pre-4.0 layers.figure.<group>='true' → 'character'. Runs unconditionally.

    A config written by pre-4.0 code (or by a user running `set layers.figure.X true`
    before that cmd_set was made strict) may have 'true' stored for a figure cell.
    'true' is no longer a valid value: STYLE_BLOCK assembly would attempt to load
    assets/figure-type/true.md (which does not exist). Promoting it to 'character'
    restores the pre-4.0 intent (portraits enabled, character type).

    This migration is intentionally separate from _migrate_figure_proportion so it
    runs on every profile regardless of whether figure_proportion is present.

    Returns True if any cell was changed.
    """
    changed = False
    fig = profile.get("layers", {}).get("figure", {})
    for group in GROUPS:
        if fig.get(group) == "true":
            fig[group] = "character"
            changed = True
    return changed


def _migrate_seamless_true_to_alias(profile: dict) -> bool:
    """Upgrade a stale literal layers.seamless.<group>='true' to a concrete alias.

    Mirrors _migrate_figure_true_to_character: 'true' is accepted as cmd_set input
    for convenience but should never be the value actually stored. Runs unconditionally
    so it also catches values written by any path other than this CLI's cmd_set (e.g.
    a hand-edited config.json).

    Returns True if any cell was changed.
    """
    changed = False
    seamless = profile.get("layers", {}).get("seamless", {})
    presets = [v for v in allowed_seamless() if v != "false"]
    default_alias = presets[0] if presets else "false"
    for group in GROUPS:
        if seamless.get(group) == "true":
            seamless[group] = default_alias
            changed = True
    return changed


MANUAL_MIGRATIONS = {
    "figure-true-to-character": _migrate_figure_true_to_character,
    "seamless-true-to-alias": _migrate_seamless_true_to_alias,
}


def cmd_migrate(args):
    """One-off/manual migrations not run automatically by load_raw() (IN-01).

    These two migrations were deliberately disconnected from the automatic
    load_raw() chain once the unified false|true|alias|custom contract made a
    stored literal "true" a valid, intentionally preserved value (T-05-03).
    They remain available here for a user/script that explicitly wants to
    upgrade a truly pre-4.0 config's lingering "true" cells to a concrete
    alias.
    """
    args, profile = _pop_profile_flag(args)
    if not args or args[0] not in MANUAL_MIGRATIONS:
        sys.exit(f"usage: migrate <{'|'.join(MANUAL_MIGRATIONS)}> [--profile <name>] [--yes]")
    name = args[0]
    if "--yes" not in args and "-y" not in args:
        sys.exit(f"refusing to run migration '{name}' without --yes (it rewrites config.json)")
    cfg = load_raw()
    prof_name = profile or active_profile_name(cfg)
    if prof_name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{prof_name}' (see: profile list)")
    changed = MANUAL_MIGRATIONS[name](cfg["profiles"][prof_name])
    if changed:
        save_raw(cfg)
        print(f"✓ migration '{name}' applied to profile '{prof_name}'.")
    else:
        print(f"no change — migration '{name}' found nothing to migrate in profile '{prof_name}'.")


def _migrate_root_mood(profile: dict) -> bool:
    """Migrate a pre-MOOD-01 profile that has a root `mood` field into the unified
    `layers.mood.<group>` schema.

    The old two-level model was: a deck-wide root `mood` (free text) plus a
    per-group `layers.mood.<group>` on/off/addition cell. MOOD-01 collapses
    this into one level: `layers.mood.<group>` alone is `"false"` (no mood),
    `"true"` (on, no specific line), or `<mood_line>` text (the atmosphere
    phrase itself).

    Mapping: pop the root `mood` value. If it is non-empty, for each group
    whose `layers.mood.<group>` cell is exactly `"true"`, replace that cell
    with the old root `mood` text (custom text already in the cell wins —
    it is left untouched; `"false"` cells stay `"false"`). If the root
    `mood` was empty, the pop still removes the dead key.

    Returns True if anything was changed (the root key is always removed
    when present, so this always returns True when called on a profile that
    has the key).
    """
    if "mood" not in profile:
        return False
    old = profile.pop("mood")
    if old:
        layers = profile.get("layers", {})
        mood = layers.get("mood", {})
        for group in GROUPS:
            if mood.get(group) == "true":
                mood[group] = old
    return True


def _migrate_drop_phase5_persistent(profile: dict) -> bool:
    """Drop the now-removed `title` and `back_*` persistent fields (TITLE-01/BACK-EPH-01).

    Title and the five back_* fields (back_purpose/back_design/back_pattern/
    back_palette/back_symmetry) moved from deck-wide persistent config fields
    to per-card ephemeral wizard steps (D-01/D-04) — they are no longer valid
    PERSISTENT_KEYS. A stale profile (hand-edited, or written by pre-Phase-5
    code) may still carry these keys; this migration silently drops them so
    `cmd_validate` never rejects an upgraded profile.

    Unlike `_migrate_figure_true_to_character`/`_migrate_seamless_true_to_alias`,
    this migration does NOT touch `layers.*` cells — a literal stored "true" is
    now a valid value under the unified contract (D-07) and is intentionally
    left untouched.

    Returns True if anything was removed.
    """
    changed = False
    if profile.pop("title", None) is not None:
        changed = True
    for key in ("back_purpose", "back_design", "back_pattern", "back_palette", "back_symmetry"):
        if profile.pop(key, None) is not None:
            changed = True
    return changed


def load_raw() -> dict:
    """Load config.json, migrating a pre-3.0 flat file, pre-3.6 *_extra fields, a
    pre-3.13 extras.<layer>.<group> namespace, a pre-4.0 figure_proportion field, a
    pre-MOOD-01 root mood field, and pre-Phase-5 title/back_* persistent fields."""
    if not CONFIG_PATH.exists():
        return json.loads(json.dumps(BUILTIN_CONFIG))
    try:
        cfg = json.loads(CONFIG_PATH.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"error: config.json is not valid JSON: {e}")
    if "profiles" not in cfg and (PROFILE_FIELD_KEYS & cfg.keys()):
        cfg = {"active_profile": DEFAULT_PROFILE_NAME, "profiles": {DEFAULT_PROFILE_NAME: cfg}}
        save_raw(cfg)
        print(f"note: migrated legacy config.json into profile '{DEFAULT_PROFILE_NAME}'", file=sys.stderr)
    cfg.setdefault("active_profile", DEFAULT_PROFILE_NAME)
    cfg.setdefault("profiles", {})
    cfg["profiles"].setdefault(DEFAULT_PROFILE_NAME, {})
    migrated = False
    # NOTE: each `_migrate_*` call below must visit every profile even after an earlier
    # profile already triggered a change — `any(gen for prof in ...)` short-circuits on
    # the first truthy result and silently skips the migration's side effect (it mutates
    # `prof` in place) for the remaining profiles. Using a list comprehension forces full
    # evaluation before `any()` runs, so every profile is always visited.
    if any([_migrate_extras(prof) for prof in cfg["profiles"].values()]):
        migrated = True
        print("note: migrated ornaments_extra/highlights_extra/frame_extra into extras.*", file=sys.stderr)
    if any([_migrate_layers_extras(prof) for prof in cfg["profiles"].values()]):
        migrated = True
        print("note: merged extras.<layer>.<group> into layers.<layer>.<group>", file=sys.stderr)
    if any([_migrate_figure_proportion(prof) for prof in cfg["profiles"].values()]):
        migrated = True
        print("note: migrated figure_proportion to figure_scale + character_framing", file=sys.stderr)
    # _migrate_figure_true_to_character / _migrate_seamless_true_to_alias are PRESERVED
    # below (unchanged) but are no longer called unconditionally from this chain: under
    # the unified D-06/D-07 contract a literal "true" is now a valid, intentionally
    # preserved cell value (T-05-03) — eagerly rewriting it on every load would silently
    # discard data and fight the new contract. They remain reachable for one-off/manual
    # use against truly pre-4.0 configs via `manage_config.py migrate <name> --yes`
    # (see MANUAL_MIGRATIONS/cmd_migrate, IN-01) but are not part of the automatic
    # migration chain.
    if any([_migrate_root_mood(prof) for prof in cfg["profiles"].values()]):
        migrated = True
        print("note: migrated root mood into layers.mood.<group>", file=sys.stderr)
    if any([_migrate_drop_phase5_persistent(prof) for prof in cfg["profiles"].values()]):
        migrated = True
        print("note: dropped removed persistent fields title/back_* (now per-card ephemeral)", file=sys.stderr)
    if migrated:
        save_raw(cfg)
    return cfg


def save_raw(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n")


def _deep_merge(base: dict, overlay: dict) -> None:
    """Recursively merge overlay into base (overlay wins), in place."""
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def active_profile_name(cfg: dict) -> str:
    return cfg.get("active_profile", DEFAULT_PROFILE_NAME)


def effective(cfg: dict | None = None, profile: str | None = None) -> dict:
    """Built-in defaults overlaid with the given (or active) profile's overrides."""
    if cfg is None:
        cfg = load_raw()
    name = profile or active_profile_name(cfg)
    out = json.loads(json.dumps(DEFAULTS))  # deep copy
    _deep_merge(out, cfg.get("profiles", {}).get(name, {}))
    return out


def get_path(cfg: dict, key: str):
    node = cfg
    for part in key.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def _pop_profile_flag(args: list[str]) -> tuple[list[str], str | None]:
    if "--profile" in args:
        i = args.index("--profile")
        if i + 1 >= len(args):
            sys.exit("error: --profile requires a value")
        return args[:i] + args[i + 2:], args[i + 1]
    return args, None


# --- commands ----------------------------------------------------------------

def cmd_show(args):
    args, profile = _pop_profile_flag(args)
    cfg = load_raw()
    active = active_profile_name(cfg)
    target = profile or active
    if target not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{target}' (see: profile list)")
    print(f"config file: {CONFIG_PATH}"
          f" ({'exists' if CONFIG_PATH.exists() else 'not created — using built-in defaults'})")
    names = ", ".join(
        f"{n}{' (active)' if n == active else ''}" for n in sorted(cfg["profiles"])
    )
    print(f"profiles: {names}")
    print(f"\neffective settings for profile '{target}':")
    print(json.dumps(effective(cfg, target), indent=2))
    print(f"\nsaved overrides for profile '{target}':")
    print(json.dumps(cfg["profiles"][target], indent=2))


def cmd_get(args):
    args, profile = _pop_profile_flag(args)
    if not args:
        sys.exit("usage: get <key> [--profile <name>]")
    cfg = load_raw()
    name = profile or active_profile_name(cfg)
    if name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{name}' (see: profile list)")
    val = get_path(effective(cfg, name), args[0])
    if val is None:
        sys.exit(f"error: no value for '{args[0]}'")
    print(val if not isinstance(val, dict) else json.dumps(val, indent=2))


def cmd_set(args):
    args, profile = _pop_profile_flag(args)
    if len(args) < 2:
        sys.exit("usage: set <key> <value> [--profile <name>]")
    key, value = args[0], args[1]
    cfg = load_raw()
    name = profile or active_profile_name(cfg)
    if name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{name}' (see: profile list)")
    # Use the effective (defaults + overrides) profile so any category-aware
    # validation sees active values even when they were never explicitly set (WR-01).
    ok, msg = validate_value(key, value, effective(cfg, name))
    if not ok:
        sys.exit(f"error: {msg}")
    parts = key.split(".")
    # D-07: a literal "true" is persisted verbatim for every layer — no eager
    # write-path resolution. "true" means "layer active for this group"; the
    # concrete alias/custom text is asked fresh per-card at generation time.
    node = cfg["profiles"][name]
    for part in parts[:-1]:
        if not isinstance(node.get(part), dict):
            node[part] = {}
        node = node[part]
    node[parts[-1]] = value
    save_raw(cfg)
    if msg:
        print(msg)
    print(f"✓ {key} = {value}  → profile '{name}' in {CONFIG_PATH}")


def cmd_unset(args):
    args, profile = _pop_profile_flag(args)
    if not args:
        sys.exit("usage: unset <key> [--profile <name>]")
    key = args[0]
    cfg = load_raw()
    name = profile or active_profile_name(cfg)
    if name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{name}' (see: profile list)")
    parts = key.split(".")
    node = cfg["profiles"][name]
    parents = [node]
    for part in parts[:-1]:
        if not isinstance(node.get(part), dict):
            sys.exit(f"error: '{key}' is not set in profile '{name}'")
        node = node[part]
        parents.append(node)
    if parts[-1] not in node:
        sys.exit(f"error: '{key}' is not set in profile '{name}'")
    del node[parts[-1]]
    # Prune now-empty parent dicts, from deepest to shallowest.
    for i in range(len(parts) - 1, 0, -1):
        if not parents[i]:
            del parents[i - 1][parts[i - 1]]
        else:
            break
    save_raw(cfg)
    print(f"✓ unset {key} in profile '{name}' "
          f"(now falls back to default '{get_path(effective(cfg, name), key)}')")


def cmd_reset(args):
    if not CONFIG_PATH.exists():
        print("config.json does not exist; nothing to reset.")
        return
    if "--yes" not in args and "-y" not in args:
        sys.exit("refusing to delete config.json without --yes (this removes ALL profiles)")
    CONFIG_PATH.unlink()
    print("✓ deleted config.json — built-in defaults restored (single 'default' profile).")


def cmd_validate(_args):
    if not CONFIG_PATH.exists():
        print("config.json not found — built-in defaults apply, nothing to validate.")
        return
    cfg = load_raw()
    errors, notes = [], []
    active = cfg.get("active_profile")
    if active not in cfg.get("profiles", {}):
        errors.append(f"active_profile '{active}' is not a defined profile")
    for name, prof in cfg.get("profiles", {}).items():
        eff = effective(cfg, name)
        for k, v in _flatten(prof).items():
            if k not in PERSISTENT_KEYS:
                errors.append(f"profile '{name}': unknown key '{k}'")
                continue
            v_str = "true" if v is True else "false" if v is False else str(v)
            ok, msg = validate_value(k, v_str, eff)
            if not ok:
                errors.append(f"profile '{name}': {msg}")
            elif msg:
                notes.append(f"profile '{name}': {msg}")
    for n in notes:
        print(n)
    if errors:
        print("\n".join(f"✗ {e}" for e in errors))
        sys.exit(1)
    print("✓ config.json is valid.")


def cmd_path(_args):
    print(CONFIG_PATH)


def cmd_options(args):
    args, profile = _pop_profile_flag(args)
    keys = [args[0]] if args else sorted(PERSISTENT_KEYS)
    if CONFIG_PATH.exists():
        cfg = load_raw()
        name = profile or active_profile_name(cfg)
        eff = effective(cfg, name)
    else:
        eff = DEFAULTS
    for k in keys:
        opt = options_for(k, eff)
        if opt is None:
            sys.exit(f"error: unknown key '{k}'")
        allowed, strict = opt
        if allowed is None:
            print(f"{k}: <free text>  [default: '{get_path(DEFAULTS, k)}']")
            continue
        suffix = "" if strict else " (or custom)"
        print(f"{k}: {', '.join(allowed)}{suffix}  [default: {get_path(DEFAULTS, k)}]")


# --- profile subcommands -------------------------------------------------------

def profile_list(_args):
    cfg = load_raw()
    active = active_profile_name(cfg)
    for name in sorted(cfg["profiles"]):
        print(f"{'* ' if name == active else '  '}{name}")


def profile_show(args):
    cfg = load_raw()
    name = args[0] if args else active_profile_name(cfg)
    if name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{name}' (see: profile list)")
    suffix = " (active)" if name == active_profile_name(cfg) else ""
    print(f"profile '{name}'{suffix}")
    print("\neffective settings:")
    print(json.dumps(effective(cfg, name), indent=2))
    print("\nsaved overrides:")
    print(json.dumps(cfg["profiles"][name], indent=2))


def profile_create(args):
    if not args:
        sys.exit("usage: profile create <name> [--from <existing>]")
    name = args[0]
    cfg = load_raw()
    if name in cfg["profiles"]:
        sys.exit(f"error: profile '{name}' already exists")
    source = None
    if "--from" in args:
        i = args.index("--from")
        if i + 1 >= len(args):
            sys.exit("usage: profile create <name> [--from <existing>]")
        source = args[i + 1]
        if source not in cfg["profiles"]:
            sys.exit(f"error: unknown profile '{source}' to clone from (see: profile list)")
    cfg["profiles"][name] = effective(cfg, source) if source else {}
    save_raw(cfg)
    origin = f"cloned from '{source}'" if source else "blank (inherits built-in defaults)"
    print(f"✓ created profile '{name}' ({origin})")


def profile_switch(args):
    if not args:
        sys.exit("usage: profile switch <name>")
    name = args[0]
    cfg = load_raw()
    if name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{name}' (see: profile list)")
    cfg["active_profile"] = name
    save_raw(cfg)
    print(f"✓ active profile is now '{name}'")


def profile_rename(args):
    if len(args) < 2:
        sys.exit("usage: profile rename <old> <new>")
    old, new = args[0], args[1]
    cfg = load_raw()
    if old not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{old}' (see: profile list)")
    if new in cfg["profiles"]:
        sys.exit(f"error: profile '{new}' already exists")
    cfg["profiles"][new] = cfg["profiles"].pop(old)
    if cfg.get("active_profile") == old:
        cfg["active_profile"] = new
    save_raw(cfg)
    print(f"✓ renamed profile '{old}' → '{new}'")


def profile_delete(args):
    if not args:
        sys.exit("usage: profile delete <name>")
    name = args[0]
    cfg = load_raw()
    if name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{name}' (see: profile list)")
    if name == active_profile_name(cfg):
        sys.exit(f"error: '{name}' is the active profile — switch to another profile first")
    if len(cfg["profiles"]) == 1:
        sys.exit("error: cannot delete the only remaining profile")
    del cfg["profiles"][name]
    save_raw(cfg)
    print(f"✓ deleted profile '{name}'")


def profile_reset(args):
    if not args:
        sys.exit("usage: profile reset <name> --yes")
    name = args[0]
    cfg = load_raw()
    if name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{name}' (see: profile list)")
    if "--yes" not in args and "-y" not in args:
        sys.exit(f"refusing to clear profile '{name}' without --yes")
    cfg["profiles"][name] = {}
    save_raw(cfg)
    print(f"✓ profile '{name}' reset to built-in defaults")


PROFILE_COMMANDS = {
    "list": profile_list, "ls": profile_list,
    "show": profile_show,
    "create": profile_create, "new": profile_create,
    "switch": profile_switch, "use": profile_switch,
    "rename": profile_rename, "mv": profile_rename,
    "delete": profile_delete, "rm": profile_delete,
    "reset": profile_reset,
}


def cmd_profile(args):
    if not args:
        sys.exit(f"usage: profile <{'|'.join(['list', 'show', 'create', 'switch', 'rename', 'delete', 'reset'])}> ...")
    sub, rest = args[0], args[1:]
    fn = PROFILE_COMMANDS.get(sub)
    if fn is None:
        sys.exit(f"error: unknown profile command '{sub}' "
                 f"(valid: {', '.join(['list', 'show', 'create', 'switch', 'rename', 'delete', 'reset'])})")
    fn(rest)


COMMANDS = {
    "show": cmd_show, "list": cmd_show,
    "get": cmd_get, "set": cmd_set, "unset": cmd_unset,
    "reset": cmd_reset, "validate": cmd_validate,
    "path": cmd_path, "options": cmd_options,
    "profile": cmd_profile, "migrate": cmd_migrate,
}


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]
    fn = COMMANDS.get(cmd)
    if fn is None:
        sys.exit(f"error: unknown command '{cmd}'\n{__doc__}")
    fn(rest)


if __name__ == "__main__":
    main(sys.argv[1:])
