# Configuration

The skill ships with `config.json` at the skill root, pre-populated with a `default`
profile holding every setting's factory value — this file *is* the source of truth
for defaults (the field reference below documents allowed values and the factory
values, but the canonical copy lives in `config.json`).

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
2. Built-in defaults (lowest priority) — mirrored in `config.json`'s `default` profile

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
        "split":      {"court": "false",     "pip": "false", "ace": "false", "joker": "false",     "back": "false", "special": "false"},
        "seamless":   {"court": "false",     "pip": "false", "ace": "false", "joker": "false",     "back": "false", "special": "false"}
      },
      "theme": "",
      "figure_scale": "inscribed-in-frame",
      "character_framing": ""
    }
  }
}
```

Within a profile, all fields are optional. Any missing field falls back to the next
source in the lookup order, ultimately to the built-in default (the field reference
below).

Every `layers.<layer>.<group>` cell — **figure, split, and seamless included** — is a
free-text string sharing one unified contract, `false | true | alias | custom`:
- `"false"` — the layer is off for this group; nothing from it appears.
- `"true"` — the layer is on, contributing only its own pattern/preset text (no
  group-wide addition). The specific alias/custom value (for layers that have one,
  e.g. figure's type, split's mode, seamless's design) is **resolved fresh per-card**
  at generation time — it is never looked up from a stored default when the cell is
  read.
- a known alias (a preset stem discovered under that layer's `assets/<layer>/`
  directory, e.g. `character` for figure, `horizontal-mirrored` for split,
  `continuous-border` for seamless) — the layer is on with that specific preset.
- any other text — the layer is on, and that text is appended (or, for figure,
  used as the type description) as this group's addition on top of the layer's own
  pattern/preset text (e.g. `"layers": {"ornaments": {"pip": "small corner
  flourishes,"}}` turns pip ornaments on and adds that phrase).

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
| `layers.figure.<group>`     | `false` (off) \| `true` (layer active; the type is resolved fresh per-card, not looked up from a stored default) \| `<alias>` (a known `assets/figure-type/` stem: `character`, `building`, `animal`) \| `<custom_text>` (used verbatim as the figure-type description) — the same unified contract as every other layer | court/joker `character`, pip/ace `false` |
| `layers.mood.<group>`       | `true` \| `false` \| `mood_line` — the unified mood schema; bool-only in the normal wizard flow, raw text is a `manage_config.py set` escape hatch where that text IS the mood line for this group (no separate deck-wide mood field) | all `true` |
| `layers.technique.<group>`  | `true`, `false`, or custom text (addition)                    | all `true`         |
| `layers.split.<group>`      | `false` (off) \| `true` (split active; the mode is resolved fresh per-card, not looked up from a stored default) \| `horizontal-mirrored` \| `angled-mirrored` \| custom free text (used verbatim) | all `false`        |
| `layers.seamless.<group>`   | `false` (off) \| `true` (seamless active; resolved fresh per-card, not looked up from a stored default) \| `<alias>` (from `assets/seamless/*.md`, e.g. `continuous-border`, `interlocking-motif`) \| `<custom_text>` (used verbatim) | all `false` |
| `theme`                     | free text (deck-wide concept/symbolism, e.g. `celestial mythology`) | `""` |
| `figure_scale`              | `full-bleed`, `inscribed-in-frame`, `small-centered`, `cross-a-frame` (or custom crop text); named presets resolve to the phrase in `assets/figure-scale/<name>.md`, custom text is used verbatim; applies to ALL figure types when `layers.figure.<group>` is on | `inscribed-in-frame` |
| `character_framing`         | `bust`, `waist-up`, `three-quarter`, `seven-eighths`, `full-body` (or any custom framing/crop description); see `assets/character-framing/` for presets — applies ONLY when figure type is `character` | `""` |
| `index.symbol`              | `star-in-circle`, `star`, `Jkr`, `J`, `crown`, `jester-face`, `none` (or custom); the glyph shown in Joker corner indices (see `assets/index/options.md` Symbol table for the phrase each value produces) | `star-in-circle` |
| `index.type`                | `standard` (rank+suit index), `joker` (symbol-only index via Menu D2); auto-derived from card group during assembly — set explicitly only to force joker-style indices on all cards | `standard` |

The Default column above gives each field's factory value in isolation; for the full
`(layer, group)` default matrix across every layer and group at once, see the
"Defaults" table in `references/REFERENCE.md` — that table is the single canonical
source for every layer default (WIZ-01); this file's Default column is kept
consistent with it but does not restate it.

> **Migration note:** `figure_proportion` is not a current field — a pre-4.0
> `config.json` that still has it is migrated automatically on load
> (`_migrate_figure_proportion` in `manage_config.py`): the old value becomes
> `character_framing` (if not already set), `figure_scale` defaults to
> `inscribed-in-frame`, and any `layers.figure.<group>` cell that was `"true"`
> becomes `"character"`. The legacy `figure-proportion` asset presets
> (`assets/figure-proportion/*.md`) still back this migration path but are no
> longer offered as a live wizard choice — see `figure_scale` /
> `character_framing` above.
>
> A pre-Phase-5 `config.json` may still carry a `title` key or any `back_*` field
> (`back_purpose`, `back_design`, `back_pattern`, `back_palette`, `back_symmetry`) —
> these are silently dropped on load by `_migrate_drop_phase5_persistent` in
> `manage_config.py`, since none of them are persistent fields anymore (see "Back
> design criteria" below). Separately, a literal `layers.*.<group> = "true"` value
> (for `figure`, `split`, or `seamless`) is now **preserved as-is** on load — it is no
> longer eagerly resolved to a concrete alias. It means "this layer is active for this
> group; ask per-card."

`<group>` is one of `court`, `pip`, `ace`, `joker`, `back`, `special`.

**Back group defaults** — `layers.figure.back` = `"false"`, `layers.split.back` = `"false"`;
all other layers default `"true"` except highlights (`"false"`). Back cards always include
the symmetry instruction from `assets/back/symmetry/<back_symmetry>.md` in their
STYLE_BLOCK regardless of layer settings (step 10 in REFERENCE.md) —
(`back_symmetry` itself is per-card ephemeral — see "Back design criteria" below, not a
config.json field).

### Back design criteria

The back design criteria — purpose, design category, pattern, palette, and symmetry —
are **not** persistent fields. They are collected fresh per-card in the Back wizard
(Steps B1–B5, see `references/WIZARD-BACK.md`) every time a back card is generated,
and are never written to `config.json` (D-04). `back_purpose`/`back_pattern`/
`back_palette` contribute their asset "Purpose line"/"Pattern line"/"Palette line" to
`[BACK_DESIGN]` in the BACK template; `back_symmetry` controls STYLE_BLOCK step 10 for
the `back` group (its "Symmetry line" is always appended regardless of `layers.*`
values); `back_design` is a category selector that filters which pattern aliases Step
B3 offers (falls back to the `geometric` category for custom/unknown values) — see
`references/REFERENCE.md` for the full per-card assembly order.

The category→pattern option dependency (`back_design` → `back_pattern`) is still
available as `allowed_back_patterns(category)` in `manage_config.py` — kept as a
standalone helper the per-card wizard step calls directly to enumerate pattern
options for the chosen category; it is no longer wired through `options_for`/
`PERSISTENT_KEYS` since these fields aren't persisted.

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
`layers.figure.<group>` carries the figure type and follows the same unified
`false|true|alias|custom` contract as every other layer — `"false"` (off), `"true"`
(on, type resolved fresh per-card), a known alias (`"character"`/`"building"`/
`"animal"`), or any other custom text (on, used verbatim as the figure-type
description, D-06). For `character` type, the chosen pattern's own "Figure detail"
and "Face Style" sections are folded into `[STYLE_BLOCK]` automatically — additional
portrait-only rendering detail (e.g. skin tones) and how a figure's face reads are
part of the `style` pattern, not a separate setting; these are skipped entirely for
`building`/`animal`/custom-text types (FIG-08, D-16).

`character_framing` is folded into `[STYLE_BLOCK]` right after the pattern's Face
Style line, ONLY when figure type is `character` — a deck-wide framing/crop
description (e.g. `waist-up portrait, torso and arms visible, hands free to hold
attributes,`) reused across every character figure so the set reads as consistently
framed. Picked from a preset in `assets/character-framing/` or typed as custom text in
Step 8e.

`figure_scale` is folded into `[STYLE_BLOCK]` right after `character_framing` (or
right after the figure-type text for non-character types) — applies to ALL figure
types whenever `layers.figure.<group>` is on. Picked from `full-bleed` /
`inscribed-in-frame` / `small-centered` or typed as custom text in Step 8a. There is
no per-group equivalent for `figure_scale` or `character_framing` — both are single
deck-wide phrases.

**Four scopes of figure content**, from broadest to narrowest (see "Figure type, face
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
`figure_scale`, `character_framing`

**Per-card** (always asked in the wizard — never saved):
`rank`, `suit` (or `joker_color` for Joker cards), `character_name`,
`character_features`, `extra_attributes`, `reference_transfers`, `exclusions`,
`back_purpose`, `back_design`, `back_pattern`, `back_palette`, `back_symmetry`,
title text and title placement alias

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

