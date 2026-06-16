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

  manage_config.py profile list                       # list profiles, mark active
  manage_config.py profile show [<name>]              # show one profile
  manage_config.py profile create <name> [--from <existing>]
  manage_config.py profile switch <name>              # change active profile
  manage_config.py profile rename <old> <new>
  manage_config.py profile delete <name>
  manage_config.py profile reset <name> --yes         # clear a profile's overrides

Keys (within a profile): deck, lettering, style, frame, aspect_ratio, image_generator,
      structure, index.size, index.count, index.layout,
      layers.<background|decor|ornaments|highlights|frame|figure|mood|technique>.<court|pip|ace>,
      mood, theme, figure_proportion

Each `layers.<layer>.<group>` cell is a free-text string with three meanings:
"false" (layer off), "true" (layer on, no addition), or any other text (layer on,
used as that group's addition on top of the layer's own pattern/preset text).

A pre-3.6 config.json may still have the old per-layer `ornaments_extra.<group>`,
`highlights_extra.<group>`, and `frame_extra.<group>` fields, and a pre-3.13
config.json may still have a separate `extras.<layer>.<group>` namespace — both are
migrated automatically into the merged `layers.<layer>.<group>` cells the first time
the file is loaded.
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
INDEX_COUNT = ["2-index", "4-index"]
INDEX_LAYOUT = ["stacked", "side-by-side", "peek", "none"]
ASPECT_PRESETS = ["5:7", "9:14", "14:25", "7:12"]
BOOL_VALUES = ["true", "false"]
STRUCTURE = ["full", "illustration"]

GROUPS = ("court", "pip", "ace")
LAYERS = ("background", "decor", "ornaments", "highlights", "frame", "figure", "mood", "technique")

# Pre-3.6 field names that are migrated into extras.<layer>.<group> (and from there,
# on a later load, into layers.<layer>.<group> — see _migrate_layers_extras) on load.
LEGACY_EXTRA_KEYS = {
    "ornaments_extra": "ornaments",
    "highlights_extra": "highlights",
    "frame_extra": "frame",
}

# Defaults reproduce the traditional look: courts get every layer including a
# portrait, plain pips get only background + center motif + finish, aces keep their
# ornamental flourish but no figure. `mood` is on everywhere (but inert until the
# free-text `mood` field is set). This dict mirrors the `profiles.default` entry
# shipped in config.json — that file is the human-readable copy; this dict is what
# every profile falls back to for fields it doesn't override.
LAYER_DEFAULTS = {
    "background": {"court": "true", "pip": "true", "ace": "true"},
    "decor": {"court": "true", "pip": "false", "ace": "true"},
    "ornaments": {"court": "true", "pip": "false", "ace": "true"},
    "highlights": {"court": "false", "pip": "false", "ace": "false"},
    "frame": {"court": "true", "pip": "false", "ace": "true"},
    "figure": {"court": "true", "pip": "false", "ace": "false"},
    "mood": {"court": "true", "pip": "true", "ace": "true"},
    "technique": {"court": "true", "pip": "true", "ace": "true"},
}

DEFAULTS = {
    "deck": "french",
    "lettering": "anglo-american",
    "style": "austrian",
    "frame": "boxed-index",
    "aspect_ratio": "9:14",
    "image_generator": "nanobanana",
    "structure": "full",
    "index": {"size": "standard", "count": "4-index", "layout": "stacked"},
    "layers": {layer: dict(groups) for layer, groups in LAYER_DEFAULTS.items()},
    "mood": "",
    "theme": "",
    "figure_proportion": "",
}

# Top-level field names of a profile — used to detect a pre-3.0 flat config.json
# (one that has no "profiles" wrapper) for migration.
PROFILE_FIELD_KEYS = set(DEFAULTS.keys())

BUILTIN_CONFIG = {
    "active_profile": DEFAULT_PROFILE_NAME,
    "profiles": {DEFAULT_PROFILE_NAME: DEFAULTS},
}

PERSISTENT_KEYS = {"deck", "lettering", "style", "frame", "aspect_ratio", "image_generator",
                   "structure", "index.size", "index.count", "index.layout", "mood", "theme",
                   "figure_proportion"}
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


def allowed_engines() -> list[str]:
    # Engines may be custom; this is the on-disk set used for suggestions.
    return _discover("engines") or ["nanobanana", "stable-diffusion", "midjourney", "dalle", "kaze"]


def options_for(key: str):
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
        "mood": (None, False),    # free text deck-wide atmosphere
        "theme": (None, False),   # free text deck-wide theme/symbolism
        "figure_proportion": (allowed_figure_proportions(), False),  # custom allowed
    }.get(key)
    if fixed is not None:
        return fixed
    if key.startswith("layers.") and key.count(".") == 2:
        _, layer, group = key.split(".")
        if layer in LAYERS and group in GROUPS:
            # "true"/"false" toggle the layer; any other text both enables it
            # and becomes its group-wide addition (see validate_value).
            return (BOOL_VALUES, False)
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

    Returns True if an `extras` namespace was found and removed.
    """
    extras = profile.pop("extras", None)
    if not isinstance(extras, dict):
        return False
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
    return True


def load_raw() -> dict:
    """Load config.json, migrating a pre-3.0 flat file, pre-3.6 *_extra fields, and a
    pre-3.13 extras.<layer>.<group> namespace."""
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
    if any(_migrate_extras(prof) for prof in cfg["profiles"].values()):
        migrated = True
        print("note: migrated ornaments_extra/highlights_extra/frame_extra into extras.*", file=sys.stderr)
    if any(_migrate_layers_extras(prof) for prof in cfg["profiles"].values()):
        migrated = True
        print("note: merged extras.<layer>.<group> into layers.<layer>.<group>", file=sys.stderr)
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
    ok, msg = validate_value(key, value)
    if not ok:
        sys.exit(f"error: {msg}")
    cfg = load_raw()
    name = profile or active_profile_name(cfg)
    if name not in cfg["profiles"]:
        sys.exit(f"error: unknown profile '{name}' (see: profile list)")
    node = cfg["profiles"][name]
    parts = key.split(".")
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
        for k, v in _flatten(prof).items():
            if k not in PERSISTENT_KEYS:
                errors.append(f"profile '{name}': unknown key '{k}'")
                continue
            ok, msg = validate_value(k, str(v))
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
    "profile": cmd_profile,
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
