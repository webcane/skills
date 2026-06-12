#!/usr/bin/env python3
"""Manage config.json for the playing-card-prompt skill.

A small, dependency-free CLI for reading, writing, and validating the
persistent settings the wizard loads at startup. Allowed values for
`deck` and `style` are discovered from the skill's assets/ folder so the
tool stays in sync with what is actually on disk.

Usage:
  manage_config.py show                 # effective config + raw config.json
  manage_config.py get <key>            # print one value (e.g. deck, index.size)
  manage_config.py set <key> <value>    # validate + persist one value
  manage_config.py unset <key>          # remove one field
  manage_config.py reset [--yes]        # delete config.json
  manage_config.py validate             # check config.json against the schema
  manage_config.py path                 # print the config.json path
  manage_config.py options [key]        # list allowed values

Keys: deck, lettering, style, aspect_ratio, image_generator,
      index.size, index.count, index.layout,
      layers.<background|decor|ornaments|highlights|frame|figure|mood>.<court|pip|ace>,
      ornaments_extra.<court|pip|ace>, highlights_extra.<court|pip|ace>,
      mood, theme, face_style.<court|pip|ace>
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

# Enumerations that do not depend on disk contents.
LETTERING = ["anglo-american", "french", "german", "russian", "dutch", "scandinavian"]
INDEX_SIZE = ["standard", "jumbo", "magnum"]
INDEX_COUNT = ["2-index", "4-index"]
INDEX_LAYOUT = ["stacked", "side-by-side", "peek", "none"]
ASPECT_PRESETS = ["5:7", "9:14", "14:25", "7:12"]
BOOL_VALUES = ["true", "false"]
FACE_STYLES = ["individual", "archetypal", "expressive", "faceless"]

GROUPS = ("court", "pip", "ace")
LAYERS = ("background", "decor", "ornaments", "highlights", "frame", "figure", "mood")

# Defaults reproduce the traditional look: courts get every layer including a
# portrait, plain pips get only background + center motif + finish, aces keep their
# ornamental flourish but no figure. `mood` is on everywhere (but inert until the
# free-text `mood` field is set).
LAYER_DEFAULTS = {
    "background": {"court": "true", "pip": "true", "ace": "true"},
    "decor": {"court": "true", "pip": "false", "ace": "true"},
    "ornaments": {"court": "true", "pip": "false", "ace": "true"},
    "highlights": {"court": "false", "pip": "false", "ace": "false"},
    "frame": {"court": "true", "pip": "false", "ace": "true"},
    "figure": {"court": "true", "pip": "false", "ace": "false"},
    "mood": {"court": "true", "pip": "true", "ace": "true"},
}

DEFAULTS = {
    "deck": "french",
    "lettering": "anglo-american",
    "style": "austrian",
    "aspect_ratio": "9:14",
    "image_generator": "nanobanana",
    "index": {"size": "standard", "count": "4-index", "layout": "stacked"},
    "layers": {layer: dict(groups) for layer, groups in LAYER_DEFAULTS.items()},
    "ornaments_extra": {g: "" for g in GROUPS},
    "highlights_extra": {g: "" for g in GROUPS},
    "mood": "",
    "theme": "",
    "face_style": {g: "individual" for g in GROUPS},
}

PERSISTENT_KEYS = {"deck", "lettering", "style", "aspect_ratio", "image_generator",
                   "index.size", "index.count", "index.layout", "mood", "theme"}
PERSISTENT_KEYS |= {f"layers.{layer}.{g}" for layer in LAYERS for g in GROUPS}
PERSISTENT_KEYS |= {f"ornaments_extra.{g}" for g in GROUPS}
PERSISTENT_KEYS |= {f"highlights_extra.{g}" for g in GROUPS}
PERSISTENT_KEYS |= {f"face_style.{g}" for g in GROUPS}

# Top-level keys that hold nested dicts (any depth).
NESTED_GROUPS = ("index", "layers", "ornaments_extra", "highlights_extra", "face_style")


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


def allowed_engines() -> list[str]:
    # Engines may be custom; this is the on-disk set used for suggestions.
    return _discover("engines") or ["nanobanana", "stable-diffusion", "midjourney", "dalle", "kaze"]


def options_for(key: str):
    fixed = {
        "deck": (allowed_decks(), True),
        "lettering": (LETTERING, True),
        "style": (allowed_styles(), False),          # custom allowed
        "aspect_ratio": (ASPECT_PRESETS, False),     # custom N:M allowed
        "image_generator": (allowed_engines(), False),  # custom allowed
        "index.size": (INDEX_SIZE, True),
        "index.count": (INDEX_COUNT, True),
        "index.layout": (INDEX_LAYOUT, True),
        "mood": (None, False),    # free text deck-wide atmosphere
        "theme": (None, False),   # free text deck-wide theme/symbolism
    }.get(key)
    if fixed is not None:
        return fixed
    if key.startswith("layers.") and key.count(".") == 2:
        _, layer, group = key.split(".")
        if layer in LAYERS and group in GROUPS:
            return (BOOL_VALUES, True)
        return None
    if key.startswith("ornaments_extra.") or key.startswith("highlights_extra."):
        _, group = key.split(".", 1)
        if group in GROUPS:
            return (None, False)  # free text
        return None
    if key.startswith("face_style.") and key.count(".") == 1:
        _, group = key.split(".")
        if group in GROUPS:
            return (FACE_STYLES, True)
        return None
    return None


# --- validation ------------------------------------------------------------

def validate_value(key: str, value: str) -> tuple[bool, str]:
    opt = options_for(key)
    if opt is None:
        return False, f"unknown key '{key}' (valid: {', '.join(sorted(PERSISTENT_KEYS))})"
    allowed, strict = opt
    if allowed is None:  # free text
        return True, ""
    if key == "aspect_ratio":
        if value in allowed or re.fullmatch(r"\d+:\d+", value):
            return True, ""
        return False, f"aspect_ratio must be a preset ({', '.join(allowed)}) or N:M"
    if value in allowed:
        return True, ""
    if strict:
        return False, f"{key} must be one of: {', '.join(allowed)}"
    return True, f"note: '{value}' is a custom {key} (not in {', '.join(allowed)})"


# --- config io -------------------------------------------------------------

def load_raw() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"error: config.json is not valid JSON: {e}")


def save_raw(cfg: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n")


def _deep_merge(base: dict, overlay: dict) -> None:
    """Recursively merge overlay into base (overlay wins), in place."""
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def effective() -> dict:
    """Defaults overlaid with whatever is saved (config.json wins)."""
    cfg = json.loads(json.dumps(DEFAULTS))  # deep copy
    raw = load_raw()
    for k, v in raw.items():
        if k in NESTED_GROUPS and isinstance(v, dict) and isinstance(cfg.get(k), dict):
            _deep_merge(cfg[k], v)
        else:
            cfg[k] = v
    return cfg


def get_path(cfg: dict, key: str):
    node = cfg
    for part in key.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


# --- commands --------------------------------------------------------------

def cmd_show(_args):
    print(f"config file: {CONFIG_PATH}"
          f" ({'exists' if CONFIG_PATH.exists() else 'not created — using defaults'})")
    print("\neffective settings:")
    print(json.dumps(effective(), indent=2))
    if CONFIG_PATH.exists():
        print("\nsaved config.json:")
        print(json.dumps(load_raw(), indent=2))


def cmd_get(args):
    if not args:
        sys.exit("usage: get <key>")
    val = get_path(effective(), args[0])
    if val is None:
        sys.exit(f"error: no value for '{args[0]}'")
    print(val if not isinstance(val, dict) else json.dumps(val, indent=2))


def cmd_set(args):
    if len(args) < 2:
        sys.exit("usage: set <key> <value>")
    key, value = args[0], args[1]
    ok, msg = validate_value(key, value)
    if not ok:
        sys.exit(f"error: {msg}")
    cfg = load_raw()
    parts = key.split(".")
    node = cfg
    for part in parts[:-1]:
        if not isinstance(node.get(part), dict):
            node[part] = {}
        node = node[part]
    node[parts[-1]] = value
    save_raw(cfg)
    if msg:
        print(msg)
    print(f"✓ {key} = {value}  → {CONFIG_PATH}")


def cmd_unset(args):
    if not args:
        sys.exit("usage: unset <key>")
    key = args[0]
    cfg = load_raw()
    parts = key.split(".")
    parents = [cfg]
    node = cfg
    for part in parts[:-1]:
        if not isinstance(node.get(part), dict):
            sys.exit(f"error: '{key}' is not set in config.json")
        node = node[part]
        parents.append(node)
    if parts[-1] not in node:
        sys.exit(f"error: '{key}' is not set in config.json")
    del node[parts[-1]]
    # Prune now-empty parent dicts, from deepest to shallowest.
    for i in range(len(parts) - 1, 0, -1):
        if not parents[i]:
            del parents[i - 1][parts[i - 1]]
        else:
            break
    save_raw(cfg)
    print(f"✓ unset {key} (now falls back to default '{get_path(effective(), key)}')")


def cmd_reset(args):
    if not CONFIG_PATH.exists():
        print("config.json does not exist; nothing to reset.")
        return
    if "--yes" not in args and "-y" not in args:
        sys.exit("refusing to delete config.json without --yes")
    CONFIG_PATH.unlink()
    print("✓ deleted config.json — built-in defaults restored.")


def cmd_validate(_args):
    if not CONFIG_PATH.exists():
        print("config.json not found — defaults apply, nothing to validate.")
        return
    raw = load_raw()
    errors, notes = [], []

    def _flatten(d: dict, prefix: str = "") -> dict:
        flat = {}
        for k, v in d.items():
            full = f"{prefix}{k}"
            if isinstance(v, dict):
                flat.update(_flatten(v, f"{full}."))
            else:
                flat[full] = v
        return flat

    flat = _flatten(raw)
    for k, v in flat.items():
        if k not in PERSISTENT_KEYS:
            errors.append(f"unknown key '{k}'")
            continue
        ok, msg = validate_value(k, str(v))
        if not ok:
            errors.append(msg)
        elif msg:
            notes.append(msg)
    for n in notes:
        print(n)
    if errors:
        print("\n".join(f"✗ {e}" for e in errors))
        sys.exit(1)
    print("✓ config.json is valid.")


def cmd_path(_args):
    print(CONFIG_PATH)


def cmd_options(args):
    keys = [args[0]] if args else sorted(PERSISTENT_KEYS)
    for k in keys:
        opt = options_for(k)
        if opt is None:
            sys.exit(f"error: unknown key '{k}'")
        allowed, strict = opt
        if allowed is None:
            print(f"{k}: <free text>  [default: '{get_path(DEFAULTS, k)}']")
            continue
        suffix = "" if strict else " (or custom)"
        print(f"{k}: {', '.join(allowed)}{suffix}  [default: {get_path(DEFAULTS, k)}]")


COMMANDS = {
    "show": cmd_show, "list": cmd_show,
    "get": cmd_get, "set": cmd_set, "unset": cmd_unset,
    "reset": cmd_reset, "validate": cmd_validate,
    "path": cmd_path, "options": cmd_options,
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
