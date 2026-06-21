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
`layers.figure.pip`, `layers.mood.court`, `layers.technique.pip`,
`layers.figure.joker`, `layers.split.back`), where `<layer>` is one of `background`,
`decor`, `ornaments`, `highlights`, `frame`, `figure`, `mood`, `technique`, `split`.
`theme` and `frame` are flat fields (no `<group>`) — note there is no standalone
`mood` flat field; mood is set entirely per-group via `layers.mood.<group>`.

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
      "structure": "full",
      "index": {
        "size": "standard",
        "count": "4-index",
        "layout": "stacked",
        "symbol": "star-in-circle",
        "type": "standard"
      },
      "layers": {
        "background": {"court": "true",      "pip": "true",  "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
        "decor":      {"court": "true",      "pip": "false", "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
        "ornaments":  {"court": "true",      "pip": "false", "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
        "highlights": {"court": "false",     "pip": "false", "ace": "false", "joker": "false",     "back": "false", "special": "false"},
        "frame":      {"court": "true",      "pip": "false", "ace": "true",  "joker": "true",      "back": "true",  "special": "false"},
        "figure":     {"court": "character", "pip": "false", "ace": "false", "joker": "character", "back": "false", "special": "false"},
        "mood":       {"court": "true",      "pip": "true",  "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
        "technique":  {"court": "true",      "pip": "true",  "ace": "true",  "joker": "true",      "back": "true",  "special": "true"},
        "split":      {"court": "false",     "pip": "false", "ace": "false", "joker": "false",     "back": "false", "special": "false"}
      },
      "theme": "",
      "figure_scale": "inscribed-in-frame",
      "character_framing": "",
      "back_purpose": "classic",
      "back_design": "geometric",
      "back_pattern": "diamond",
      "back_palette": "classic-blue",
      "back_symmetry": "rotational-180"
    }
  }
}
```

Within a profile, all fields are optional. Any missing field falls back to the next
source in the lookup order, ultimately to the built-in default (the field reference
below).

Each `layers.<layer>.<group>` cell is a free-text string with three meanings:
- `"false"` — the layer is off for this group; nothing from it appears.
- `"true"` — the layer is on, contributing only its own pattern/preset text (no
  group-wide addition).
- any other text — the layer is on, and that text is appended as this group's
  addition on top of the layer's own pattern/preset text (e.g.
  `"layers": {"ornaments": {"pip": "small corner flourishes,"}}` turns pip ornaments
  on and adds that phrase).

### Field reference

| Field                       | Values                                                        | Default            |
|-----------------------------|-----------------------------------------------------------------|--------------------|
| `deck`                      | `french`, `german`, `swiss`, `latin`                          | `french`           |
| `lettering`                 | `anglo-american`, `french`, `german`, `russian`, `dutch`, `scandinavian` | per deck default   |
| `style`                     | `austrian`, `french`, `english` (or any custom pattern name)  | `austrian`         |
| `frame`                     | `boxed-index`, `stepped-corners`, `double-rule`, `ornate-scrollwork`, `art-deco-geometric`, `rope-twist` (or any custom frame name/description) | `boxed-index` |
| `aspect_ratio`              | `5:7`, `9:14`, `14:25`, `7:12`, or custom                    | `9:14`             |
| `image_generator`           | `nanobanana`, `stable-diffusion`, `midjourney`, `dalle`, `kaze`, or custom | `nanobanana` |
| `structure`                 | `full`, `illustration`                                        | `full`             |
| `index.size`                | `standard`, `jumbo`, `magnum`                                 | `standard`         |
| `index.count`               | `2-index`, `4-index`                                          | `4-index`          |
| `index.layout`              | `stacked`, `side-by-side`, `peek`, `none`                     | `stacked`          |
| `layers.background.<group>` | `true`, `false`, or custom text (addition)                    | all `true`         |
| `layers.decor.<group>`      | `true`, `false`, or custom text (addition)                    | court/ace `true`, pip `false` |
| `layers.ornaments.<group>`  | `true`, `false`, or custom text (addition)                    | court/ace `true`, pip `false` |
| `layers.highlights.<group>` | `true`, `false`, or custom text (addition)                    | all `false`        |
| `layers.frame.<group>`      | `true`, `false`, or custom text (addition)                    | court/ace `true`, pip `false` |
| `layers.figure.<group>`     | `false` \| `alias` \| `alias addition_text` — `alias` is one of `character`/`building`/`animal`/`custom`; bare `"true"` is still accepted on read for backward compatibility but is migrated to the group's default alias (`"character"`) on load via `_migrate_figure_true_to_character` — do not write `"true"` directly | court/joker `character`, pip/ace `false` |
| `layers.mood.<group>`       | `true` \| `false` \| `mood_line` — the unified mood schema; when the cell holds free text, that text IS the mood line for this group (no separate deck-wide mood field) | all `true` |
| `layers.technique.<group>`  | `true`, `false`, or custom text (addition)                    | all `true`         |
| `layers.split.<group>`      | `false`, `none`, `horizontal-mirrored`, `angled-mirrored`, or custom text | all `false`        |
| `theme`                     | free text (deck-wide concept/symbolism, e.g. `celestial mythology`) | `""` |
| `figure_scale`              | `full-bleed`, `inscribed-in-frame`, `small-centered` (or custom crop text); applies to ALL figure types when `layers.figure.<group>` is on | `inscribed-in-frame` |
| `character_framing`         | `bust`, `waist-up`, `three-quarter`, `seven-eighths`, `full-body` (or any custom framing/crop description); see `assets/character-framing/` for presets — applies ONLY when figure type is `character` | `""` |
| `index.symbol`              | `star-in-circle`, `star`, `Jkr`, `J`, `crown`, `jester-face`, `none` (or custom); the glyph shown in Joker corner indices (see `assets/index/options.md` Symbol table for the phrase each value produces) | `star-in-circle` |
| `index.type`                | `standard` (rank+suit index), `joker` (symbol-only index via Menu D2); auto-derived from card group during assembly — set explicitly only to force joker-style indices on all cards | `standard` |

> **Migration note:** `figure_proportion` is not a current field — a pre-4.0
> `config.json` that still has it is migrated automatically on load
> (`_migrate_figure_proportion` in `manage_config.py`): the old value becomes
> `character_framing` (if not already set), `figure_scale` defaults to
> `inscribed-in-frame`, and any `layers.figure.<group>` cell that was `"true"`
> becomes `"character"`. The legacy `figure-proportion` asset presets
> (`assets/figure-proportion/*.md`) still back this migration path but are no
> longer offered as a live wizard choice — see `figure_scale` /
> `character_framing` above.

`<group>` is one of `court`, `pip`, `ace`, `joker`, `back`, `special`.

**Back group defaults** — `layers.figure.back` = `"false"`, `layers.split.back` = `"false"`;
all other layers default `"true"` except highlights (`"false"`). Back cards always include
the symmetry instruction from `assets/back/symmetry/<back_symmetry>.md` in their
STYLE_BLOCK regardless of layer settings (step 10 in REFERENCE.md).

### Back design criteria fields

Five persistent fields control the structured B1–B6 back card wizard steps. All allow
custom free text in addition to the listed preset aliases:

| Field | Values | Default | Asset path |
|-------|--------|---------|------------|
| `back_purpose` | `classic`, `designer`, `casino` (or custom text) | `classic` | `assets/back/purpose/<back_purpose>.md` |
| `back_design` | `geometric`, `botanical`, `abstract`, `illustrated` (or custom text) | `geometric` | — (filter for B3 options; no asset loaded) |
| `back_pattern` | alias within chosen design category (or custom text) | `diamond` | `assets/back/design/<back_design>/<back_pattern>.md` |
| `back_palette` | `classic-red`, `classic-blue`, `dark`, `gold` (or custom text) | `classic-blue` | `assets/back/palette/<back_palette>.md` |
| `back_symmetry` | `rotational-180`, `bilateral`, `asymmetric` (or custom text) | `rotational-180` | `assets/back/symmetry/<back_symmetry>.md` |

Pattern aliases per design category:
- `geometric`: `diamond`, `cross-hatch`, `hexgrid`, `wave`
- `botanical`: `vine`, `floral`, `leaf`, `branch`
- `abstract`: `interlacing`, `color-field`, `paint-stroke`, `fractal`
- `illustrated`: `thematic`, `portrait`, `landscape`, `heraldic`

`back_purpose`, `back_pattern`, and `back_palette` contribute their asset "Purpose
line", "Pattern line", and "Palette line" (respectively) to `[BACK_DESIGN]` in the BACK
template — concatenated in that order.

`back_symmetry` controls STYLE_BLOCK step 10 for the `back` group — its "Symmetry
line" is always appended to STYLE_BLOCK regardless of `layers.*` cell values.

`back_design` is a category selector only; its value is not loaded as an asset —
instead it determines which pattern aliases are shown in Step B3. If `back_design` is
set to custom text (not a known category alias), B3 falls back to the `geometric`
category's options.

**Special group defaults** — `layers.frame.special` = `"false"` (no standard card border),
`layers.figure.special` = `"false"` (no figure by default), `layers.split.special` = `"false"`.
Special cards have no corner indices — the SPECIAL template hardcodes `no corner indices,
no standard rank letters, no suit symbols,`. All other layers default `"true"` except
highlights (`"false"`).

`image_generator` controls how the assembled prompt is adapted (negative-list
placement, aspect-ratio syntax, extra parameters) — see `assets/engines/`.

`structure` controls whether the assembled prompt describes a complete card (`full`,
the default) or only the center illustration (`illustration`, for users compositing
the artwork into their own card template that already supplies the frame and corner
indices) — see "`structure` setting" in `references/REFERENCE.md` for the exact
assembly changes and scope.

`layers.*` controls which layers (background, decor, ornaments, highlights, frame,
figure, mood, technique) contribute to `[STYLE_BLOCK]` / `[FRAME_LINE]` / `[MOOD_LINE]`
for each card group — see "Layers and `[STYLE_BLOCK]` assembly" in
`references/REFERENCE.md`.
Each `layers.<layer>.<group>` cell both gates the layer (`"false"` = off, anything
else = on) and, when it's not `"false"`/`"true"`, supplies that group's free-text
addition appended after the layer's own pattern/preset text — `layers.background.
<group>`, `layers.decor.<group>`, `layers.ornaments.<group>`, `layers.highlights.
<group>`, `layers.frame.<group>`, and `layers.technique.<group>` work this way
(ornaments, highlights, and frame may also have their addition auto-derived from
`theme` if the cell is exactly `"true"` — see "Theme-derived ornaments/highlights/
frame"); `frame` picks the preset from `assets/frame/` whose "Frame line"
supplies `[FRAME_LINE]` (any custom string is also accepted).
`layers.mood.<group>` is the single, unified mood schema — `"false"` (no mood line
for this group), `"true"` (on, but no specific line), or any other text (that text
IS the `[MOOD_LINE]` for this group). There is no separate deck-wide `mood` field;
a preset can still be picked from `assets/mood/` or typed as custom text in Step 7,
which sets the chosen mood line into every group's `layers.mood.<group>` cell.
`layers.figure.<group>` now carries the figure type — `"false"` (off), or one of
`"character"`/`"building"`/`"animal"`/`"custom"` (on + figure type, D-02). For
`character` type, the chosen pattern's own "Figure detail" and "Face Style" sections
are folded into `[STYLE_BLOCK]` automatically — additional portrait-only rendering
detail (e.g. skin tones) and how a figure's face reads are part of the `style`
pattern, not a separate setting; these are skipped entirely for `building`/`animal`/
`custom` (FIG-08, D-16). `layers.figure.<group>`'s addition (free text appended after
the type keyword) is appended after the pattern's Face Style line for `character`
type — a group-wide figure trait (e.g. "all court figures shown with a slight hunch")
layered on top of the pattern's Face Style for every card in that group, distinct from
the per-card `[CHARACTER_FEATURES]` (Steps 9-12).

`character_framing` is folded into `[STYLE_BLOCK]` right after `layers.figure.<group>`'s
addition, ONLY when figure type is `character` — a deck-wide framing/crop description
(e.g. `waist-up portrait, torso and arms visible, hands free to hold attributes,`)
reused across every character figure so the set reads as consistently framed. Picked
from a preset in `assets/character-framing/` or typed as custom text in Step 8e.

`figure_scale` is folded into `[STYLE_BLOCK]` right after `character_framing` (or
right after the figure-type text for non-character types) — applies to ALL figure
types whenever `layers.figure.<group>` is on. Picked from `full-bleed` /
`inscribed-in-frame` / `small-centered` or typed as custom text in Step 8a. There is
no per-group equivalent for `figure_scale` or `character_framing` — both are single
deck-wide phrases.

**Five scopes of figure content**, from broadest to narrowest (see "Figure type, face
style, framing & scale" in `references/REFERENCE.md` for the full assembly order):
- **Deck-wide (figure type)** — the `assets/figure-type/<type>.md` text for the
  group's configured type: the canonical prompt phrase for that figure type. Applied
  to all types.
- **Deck-wide (pattern, character-only)** — the pattern's Figure detail and Face Style
  lines (from `style`): how ANY character figure's face reads in this pattern (typage,
  expression, degree of stylization). Applied only when figure type is `character`.
- **Deck-wide (character framing, character-only)** — `character_framing`: how much of
  the character figure is shown and how it is cropped. Applied only when figure type
  is `character`.
- **Deck-wide (scale, all types)** — `figure_scale`: how the figure sits in the frame,
  applied to ALL figure types.
- **Group-wide** — `layers.figure.<group>`'s addition (when the cell carries custom
  text beyond the type keyword): an optional trait shared by every figure in one group
  (`court`/`pip`/`ace`/`joker`), layered on top of the pattern's Face Style for that
  group (character-only).
- **Per-card** — `[CHARACTER_NAME]`/`[CHARACTER_FEATURES]` and the Step 10-12
  attributes/transfers/exclusions: who this specific card's figure is, always
  supplied per card (from the user or a reference image).
Court cards default to every layer on except highlights (matching prior behavior) but,
like Pip/Ace, can be tuned per layer via `--config`.

### Which settings are "session" vs "persistent"

**Persistent** (saved per profile — rarely change between cards):
`deck`, `lettering`, `style`, `frame`, `aspect_ratio`, `image_generator`, `structure`,
`index.*` (including `index.symbol` and `index.type`), `layers.*` (including
`layers.mood.<group>`, the only mood setting), `theme`,
`figure_scale`, `character_framing`,
`back_purpose`, `back_design`, `back_pattern`, `back_palette`, `back_symmetry`

**Per-card** (always asked in the wizard — never saved):
`rank`, `suit` (or `joker_color` for Joker cards), `character_name`,
`character_features`, `extra_attributes`, `reference_transfers`, `exclusions`

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
      "layers": {
        "mood": {"court": "gothic and brooding atmosphere,", "pip": "gothic and brooding atmosphere,", "ace": "gothic and brooding atmosphere,", "joker": "gothic and brooding atmosphere,", "back": "gothic and brooding atmosphere,", "special": "gothic and brooding atmosphere,"}
      },
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
