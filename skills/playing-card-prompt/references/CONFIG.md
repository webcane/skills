# Configuration

The skill stores user defaults in `config.json` at the skill root. Settings can also
be inherited from a global `settings.json` (path given by the `AGENT_SKILLS_SETTINGS`
environment variable). Skill-level `config.json` overrides global settings.

## Managing config.json (`scripts/manage_config.py`)

Use the bundled CLI instead of hand-editing the file — it validates `deck`/`style`
against the actual files in `assets/`, enforces the index enums, and accepts custom
`style`/`aspect_ratio` values with a note.

```bash
python3 scripts/manage_config.py show              # effective config + raw config.json
python3 scripts/manage_config.py get <key>         # e.g. deck, index.size
python3 scripts/manage_config.py set <key> <value> # validate + persist
python3 scripts/manage_config.py unset <key>       # remove a field (falls back to default)
python3 scripts/manage_config.py options [key]     # list allowed values
python3 scripts/manage_config.py validate          # check config.json against the schema
python3 scripts/manage_config.py reset --yes       # delete config.json
python3 scripts/manage_config.py path              # print the config.json path
```

Dotted keys address nested groups: `index.size`, `index.count`, `index.layout`,
`ornaments_extra.<group>`, `highlights_extra.<group>`, `face_style.<group>`, and the
two-level `layers.<layer>.<group>` (e.g. `layers.frame.pip`, `layers.highlights.ace`,
`layers.figure.pip`, `layers.mood.court`). `mood` and `theme` are flat free-text
fields (no `<group>`).

## Lookup order

1. `config.json` in the skill directory (highest priority)
2. `$AGENT_SKILLS_SETTINGS` → path to global `settings.json`
3. Built-in defaults (lowest priority)

## Schema

```json
{
  "deck": "french",
  "lettering": "anglo-american",
  "style": "austrian",
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
  "ornaments_extra": {"court": "", "pip": "", "ace": ""},
  "highlights_extra": {"court": "", "pip": "", "ace": ""},
  "mood": "",
  "theme": "",
  "face_style": {"court": "individual", "pip": "individual", "ace": "individual"}
}
```

All fields are optional. Any missing field falls back to the next source in the
lookup order, ultimately to the built-in default.

### Field reference

| Field                       | Values                                                        | Default            |
|-----------------------------|-----------------------------------------------------------------|--------------------|
| `deck`                      | `french`, `german`, `swiss`, `latin`                          | `french`           |
| `lettering`                 | `anglo-american`, `french`, `german`, `russian`, `dutch`, `scandinavian` | per deck default   |
| `style`                     | `austrian`, `french`, `english` (or any custom pattern name)  | `austrian`         |
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
| `ornaments_extra.<group>`   | free text                                                      | `""`               |
| `highlights_extra.<group>`  | free text                                                      | `""`               |
| `mood`                      | free text (deck-wide atmosphere, e.g. `gothic and brooding atmosphere,`) | `""` |
| `theme`                     | free text (deck-wide concept/symbolism, e.g. `celestial mythology`) | `""` |
| `face_style.<group>`        | `individual`, `archetypal`, `expressive`, `faceless`          | `individual`       |

`<group>` is one of `court`, `pip`, `ace`.

`image_generator` controls how the assembled prompt is adapted (negative-list
placement, aspect-ratio syntax, extra parameters) — see `assets/engines/`.

`layers.*` controls which layers (background, decor, ornaments, highlights, frame,
figure, mood) contribute to `[STYLE_BLOCK]` / `[FRAME_LINE]` / `[FACE_STYLE_LINE]` /
`[MOOD_LINE]` for each card group — see "Layers and `[STYLE_BLOCK]` assembly" in
`references/REFERENCE.md`. `ornaments_extra.<group>` and `highlights_extra.<group>`
are free-text additions appended within those layers when enabled (and may be
auto-derived from `theme` if left empty — see "Theme-derived ornaments/highlights").
`mood` is a deck-wide free-text atmosphere description; `face_style.<group>` controls
how a figure's face reads when `layers.figure.<group>` is on. Court cards default to
every layer on except highlights (matching prior behavior) but, like Pip/Ace, can be
tuned per layer via `--config`.

### Which settings are "session" vs "persistent"

**Persistent** (saved in config — rarely change between cards):
`deck`, `lettering`, `style`, `aspect_ratio`, `image_generator`, `index.*`,
`layers.*`, `ornaments_extra.*`, `highlights_extra.*`, `mood`, `theme`, `face_style.*`

**Per-card** (always asked in the wizard — never saved):
`rank`, `suit`, `character_name`, `character_features`, `extra_attributes`,
`reference_transfers`, `exclusions`

## Example `config.json`

```json
{
  "deck": "french",
  "lettering": "anglo-american",
  "style": "austrian",
  "aspect_ratio": "9:14"
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
