# Configuration

The skill ships with `config.json` at the skill root, pre-populated with a `default`
profile holding every setting's factory value — this file *is* the source of truth
for defaults (the field reference below documents allowed values and the factory
values, but the canonical copy lives in `config.json`). Settings can also be
inherited from a global `settings.json` (path given by the `AGENT_SKILLS_SETTINGS`
environment variable), which sits below profile overrides and above built-in
defaults.

## Profiles

`config.json` holds one or more named **profiles** — each a full bundle of the
persistent settings below (deck, style, layers, mood, theme, ...) — plus an
`active_profile` pointer saying which one is currently in use. Profiles let a user
keep multiple saved "looks" (e.g. one profile for an Austrian gothic deck, another
for a Japanese ukiyo-e deck) and switch between them without re-running the whole
config wizard. A profile's stored overrides only need to contain the fields that
differ from the built-in defaults — anything missing falls back to `DEFAULTS` in
`scripts/manage_config.py` (which mirrors the shipped `profiles.default`).

## Managing config.json (`scripts/manage_config.py`)

Use the bundled CLI instead of hand-editing the file — it validates `deck`/`style`
against the actual files in `assets/`, enforces the index enums, and accepts custom
`style`/`aspect_ratio` values with a note.

```bash
python3 scripts/manage_config.py show              # effective + saved settings for the active profile
python3 scripts/manage_config.py get <key>         # e.g. deck, index.size
python3 scripts/manage_config.py set <key> <value> # validate + persist
python3 scripts/manage_config.py unset <key>       # remove a field (falls back to default)
python3 scripts/manage_config.py options [key]     # list allowed values
python3 scripts/manage_config.py validate          # check config.json against the schema
python3 scripts/manage_config.py reset --yes       # delete config.json (ALL profiles)
python3 scripts/manage_config.py path              # print the config.json path
```

`show`, `get`, `set`, and `unset` operate on the **active** profile by default; pass
`--profile <name>` to target a different one without switching, e.g.
`manage_config.py get theme --profile gothic-deck`.

### Profile commands

```bash
python3 scripts/manage_config.py profile list                  # list profiles, * marks active
python3 scripts/manage_config.py profile show [<name>]         # show a profile (default: active)
python3 scripts/manage_config.py profile create <name> [--from <existing>]
python3 scripts/manage_config.py profile switch <name>         # change the active profile
python3 scripts/manage_config.py profile rename <old> <new>
python3 scripts/manage_config.py profile delete <name>         # refuses the active or last profile
python3 scripts/manage_config.py profile reset <name> --yes    # clear one profile's overrides
```

`profile create <name>` with no `--from` starts blank (inherits every built-in
default); `--from <existing>` clones that profile's full *effective* settings, so the
new profile is a self-contained copy a user can then tweak independently.

Dotted keys address nested groups: `index.size`, `index.count`, `index.layout`, and the
two-level `layers.<layer>.<group>` (e.g. `layers.frame.pip`, `layers.highlights.ace`,
`layers.figure.pip`, `layers.mood.court`) and `extras.<layer>.<group>` (e.g.
`extras.ornaments.pip`, `extras.frame.court`, `extras.mood.ace`), where `<layer>` is
one of `background`, `decor`, `ornaments`, `highlights`, `frame`, `mood`. `mood`,
`theme`, and `frame` are flat fields (no `<group>`).

## Lookup order

1. The active profile's overrides in `config.json` (highest priority)
2. `$AGENT_SKILLS_SETTINGS` → path to global `settings.json`
3. Built-in defaults (lowest priority) — mirrored in `config.json`'s `default` profile

## Schema

`config.json` is an `active_profile` pointer plus a map of named profiles. Each
profile holds the fields below:

```json
{
  "active_profile": "default",
  "profiles": {
    "default": {
      "deck": "french",
      "lettering": "anglo-american",
      "style": "austrian",
      "frame": "boxed-index",
      "aspect_ratio": "9:14",
      "image_generator": "nanobanana",
      "index": {
        "size": "standard",
        "count": "4-index",
        "layout": "stacked"
      },
      "layers": {
        "background": {"court": "true",  "pip": "true",  "ace": "true"},
        "decor":      {"court": "true",  "pip": "false", "ace": "true"},
        "ornaments":  {"court": "true",  "pip": "false", "ace": "true"},
        "highlights": {"court": "false", "pip": "false", "ace": "false"},
        "frame":      {"court": "true",  "pip": "false", "ace": "true"},
        "figure":     {"court": "true",  "pip": "false", "ace": "false"},
        "mood":       {"court": "true",  "pip": "true",  "ace": "true"}
      },
      "extras": {
        "background": {"court": "", "pip": "", "ace": ""},
        "decor":      {"court": "", "pip": "", "ace": ""},
        "ornaments":  {"court": "", "pip": "", "ace": ""},
        "highlights": {"court": "", "pip": "", "ace": ""},
        "frame":      {"court": "", "pip": "", "ace": ""},
        "mood":       {"court": "", "pip": "", "ace": ""}
      },
      "mood": "",
      "theme": ""
    }
  }
}
```

Within a profile, all fields are optional. Any missing field falls back to the next
source in the lookup order, ultimately to the built-in default (the field reference
below).

### Field reference

| Field                       | Values                                                        | Default            |
|-----------------------------|-----------------------------------------------------------------|--------------------|
| `deck`                      | `french`, `german`, `swiss`, `latin`                          | `french`           |
| `lettering`                 | `anglo-american`, `french`, `german`, `russian`, `dutch`, `scandinavian` | per deck default   |
| `style`                     | `austrian`, `french`, `english` (or any custom pattern name)  | `austrian`         |
| `frame`                     | `boxed-index`, `stepped-corners`, `double-rule`, `ornate-scrollwork`, `art-deco-geometric`, `rope-twist` (or any custom frame name/description) | `boxed-index` |
| `aspect_ratio`              | `5:7`, `9:14`, `14:25`, `7:12`, or custom                    | `9:14`             |
| `image_generator`           | `nanobanana`, `stable-diffusion`, `midjourney`, `dalle`, `kaze`, or custom | `nanobanana` |
| `index.size`                | `standard`, `jumbo`, `magnum`                                 | `standard`         |
| `index.count`               | `2-index`, `4-index`                                          | `4-index`          |
| `index.layout`              | `stacked`, `side-by-side`, `peek`, `none`                     | `stacked`          |
| `layers.background.<group>` | `true`, `false`                                               | all `true`         |
| `layers.decor.<group>`      | `true`, `false`                                               | court/ace `true`, pip `false` |
| `layers.ornaments.<group>`  | `true`, `false`                                               | court/ace `true`, pip `false` |
| `layers.highlights.<group>` | `true`, `false`                                               | all `false`        |
| `layers.frame.<group>`      | `true`, `false`                                               | court/ace `true`, pip `false` |
| `layers.figure.<group>`     | `true`, `false`                                               | court `true`, pip/ace `false` |
| `layers.mood.<group>`       | `true`, `false`                                               | all `true`         |
| `extras.background.<group>` | free text                                                     | `""`               |
| `extras.decor.<group>`      | free text                                                      | `""`               |
| `extras.ornaments.<group>`  | free text                                                      | `""`               |
| `extras.highlights.<group>` | free text                                                      | `""`               |
| `extras.frame.<group>`      | free text                                                      | `""`               |
| `extras.mood.<group>`       | free text (per-group mood addition, on top of deck-wide `mood`) | `""`             |
| `mood`                      | free text (deck-wide atmosphere, e.g. `gothic and brooding atmosphere,`); see `assets/mood/` for presets | `""` |
| `theme`                     | free text (deck-wide concept/symbolism, e.g. `celestial mythology`) | `""` |

`<group>` is one of `court`, `pip`, `ace`.

`image_generator` controls how the assembled prompt is adapted (negative-list
placement, aspect-ratio syntax, extra parameters) — see `assets/engines/`.

`layers.*` controls which layers (background, decor, ornaments, highlights, frame,
figure, mood) contribute to `[STYLE_BLOCK]` / `[FRAME_LINE]` / `[MOOD_LINE]` for each
card group — see "Layers and `[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`.
`extras.<layer>.<group>` is the free-text addition appended within that layer when
`layers.<layer>.<group>` is enabled — `extras.background.<group>`,
`extras.decor.<group>`, `extras.ornaments.<group>`, `extras.highlights.<group>`, and
`extras.frame.<group>` are appended after the layer's own text (ornaments, highlights,
and frame may also be auto-derived from `theme` if left empty — see "Theme-derived
ornaments/highlights/frame"); `extras.mood.<group>` is appended after `[MOOD_LINE]`
as a per-group addition on top of the deck-wide `mood`. `frame` picks the preset from
`assets/frame/` whose "Frame line" supplies `[FRAME_LINE]` (any custom string is also
accepted). `mood` is a deck-wide free-text atmosphere description, either picked from
a preset in `assets/mood/` or typed as custom text in Step 7, which also sets
`layers.mood.<group>` per card group. When `layers.figure.<group>` is on, the chosen
pattern's own "Face Style" section is folded into `[STYLE_BLOCK]` automatically —
how a figure's face reads is part of the `style` pattern, not a separate setting.
Court cards default to every layer on except highlights (matching prior behavior) but,
like Pip/Ace, can be tuned per layer via `--config`.

### Which settings are "session" vs "persistent"

**Persistent** (saved per profile — rarely change between cards):
`deck`, `lettering`, `style`, `frame`, `aspect_ratio`, `image_generator`, `index.*`,
`layers.*`, `extras.*`, `mood`, `theme`

**Per-card** (always asked in the wizard — never saved):
`rank`, `suit`, `character_name`, `character_features`, `extra_attributes`,
`reference_transfers`, `exclusions`

## Example `config.json`

A minimal `config.json` with one custom profile that only overrides a few fields
(everything else falls back to the built-in defaults):

```json
{
  "active_profile": "gothic-deck",
  "profiles": {
    "default": {},
    "gothic-deck": {
      "deck": "french",
      "style": "austrian",
      "aspect_ratio": "9:14",
      "mood": "gothic and brooding atmosphere,",
      "theme": "celestial mythology"
    }
  }
}
```

## Example global `settings.json`

Located at the path in `$AGENT_SKILLS_SETTINGS`. Can hold defaults for multiple
skills; this skill reads only the keys listed above from the top level (or from a
`"playing-card-prompt"` namespace if present).

```json
{
  "playing-card-prompt": {
    "deck": "french",
    "style": "austrian",
    "image_generator": "nanobanana"
  }
}
```
