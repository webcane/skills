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

Dotted keys address the index group: `index.size`, `index.count`, `index.layout`.

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
  }
}
```

All fields are optional. Any missing field falls back to the next source in the
lookup order, ultimately to the built-in default.

### Field reference

| Field              | Values                                                        | Default            |
|--------------------|---------------------------------------------------------------|--------------------|
| `deck`             | `french`, `german`, `swiss`, `latin`                          | `french`           |
| `lettering`        | `anglo-american`, `french`, `german`, `russian`, `dutch`, `scandinavian` | per deck default   |
| `style`            | `austrian`, `french`, `english` (or any custom pattern name)  | `austrian`         |
| `aspect_ratio`     | `5:7`, `9:14`, `14:25`, `7:12`, or custom                    | `9:14`             |
| `image_generator`  | `nanobanana`, `stable-diffusion`, `midjourney`, `dalle`, `kaze`, or custom | `nanobanana` |
| `index.size`       | `standard`, `jumbo`, `magnum`                                 | `standard`         |
| `index.count`      | `2-index`, `4-index`                                          | `4-index`          |
| `index.layout`     | `stacked`, `side-by-side`, `peek`, `none`                     | `stacked`          |

`image_generator` controls how the assembled prompt is adapted (negative-list
placement, aspect-ratio syntax, extra parameters) — see `assets/engines/`.

### Which settings are "session" vs "persistent"

**Persistent** (saved in config — rarely change between cards):
`deck`, `lettering`, `style`, `aspect_ratio`, `image_generator`, `index.*`

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
