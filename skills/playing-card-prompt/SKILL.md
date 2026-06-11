---
name: playing-card-prompt
description: Interactive wizard that builds image-generation prompts for stylized playing cards across multiple deck systems (French/International, German, Swiss, Italo-Spanish) and regional court-lettering systems, with auto-loaded traditional attributes for court cards (King/Queen/Jack) plus pip and ace cards. Use this skill whenever the user wants to create, design, or generate a playing card, a court card, a deck card with a custom character, or asks for a "playing card prompt" or "card generator", or to turn a person/character/reference image into a playing card. Trigger it even if the user only says they want to "make a card" — walk them through the wizard (deck, lettering, rank, suit, style, attributes, reference transfers, aspect ratio) and output a finished prompt.
color: emerald
metadata:
  author: webcane
  version: 1.0.0
---

# Playing Card Prompt Wizard

Runs an interactive wizard that collects choices and assembles a finished
image-generation prompt for a stylized playing card. The deliverable is the completed
prompt text in a code block for the user to copy. **Do not generate the image yourself.**

---

## Subcommands

The user may invoke the skill in three modes. Detect which one from their message:

| Trigger                                               | Mode        | What to do                                         |
|-------------------------------------------------------|-------------|----------------------------------------------------|
| `--init`, `--config`, `init`, `config`, "configure"   | **Config**  | Run config wizard only; save `config.json`; stop.  |
| `--reset`                                             | **Reset**   | Delete `config.json`; confirm; stop.               |
| _(anything else, or no flag)_                         | **Generate**| Load config → run card wizard → output prompt.     |

---

## Startup: loading saved settings

Before asking any wizard questions, load persistent settings. See `references/CONFIG.md`
for the full schema, lookup order, and field reference.

Manage `config.json` with the bundled CLI rather than hand-editing it — it validates
every value against the on-disk decks/patterns:

```bash
python3 scripts/manage_config.py show              # effective config + saved config.json
python3 scripts/manage_config.py set deck german   # validate + persist one field
python3 scripts/manage_config.py options [key]     # list allowed values
python3 scripts/manage_config.py validate          # check config.json against the schema
python3 scripts/manage_config.py reset --yes       # delete config.json (restore defaults)
```

Keys: `deck`, `lettering`, `style`, `aspect_ratio`, `index.size`, `index.count`,
`index.layout`. Use `get`/`set`/`unset` for single fields.

**Lookup order** (first found wins per field):
1. `config.json` in the skill directory
2. `$AGENT_SKILLS_SETTINGS` → global `settings.json` (read the
   `"playing-card-prompt"` namespace if present, else top-level keys)
3. Built-in defaults

**Persistent fields** (saved in config — rarely change between cards):
`deck`, `lettering`, `style`, `aspect_ratio`, `index.*`

**Per-card fields** (always asked — never saved):
`rank`, `suit`, `character_name`, `character_features`, `extra_attributes`,
`reference_transfers`, `exclusions`

---

## Mode: Config (`--init` / `--config`)

Walk the user through **only the persistent settings** (Steps 1, 2, 5, 9 and
optionally index). Show current values if `config.json` already exists so the user
can accept or change each one. At the end, persist each value with
`python3 scripts/manage_config.py set <key> <value>` (it validates and writes
`config.json`), then confirm. Do **not** proceed to card generation.

Steps to ask in config mode:
1. Deck type
2. Court lettering system
3. Visual style / pattern
4. Aspect ratio
5. (Optional, only if user asks) Index settings

## Mode: Reset (`--reset`)

Run `python3 scripts/manage_config.py reset --yes` to delete `config.json`, confirm to
the user that defaults are restored, and stop.

## Mode: Generate (default)

Load config. Then run the card wizard with this logic:

- **Config exists** → skip persistent-setting steps; show a one-line summary of the
  loaded settings (e.g. "Using: French deck, Anglo-American letters, Austrian style,
  9:14") and go straight to per-card steps (rank → suit → court details if applicable).
  Mention the user can run `--config` to change defaults.
- **No config found** → run the full wizard (all steps), then offer to save the
  persistent settings to `config.json` for next time.

---

## File map

Folders under `assets/`:
- `assets/decks/` — one file per deck system (suits + available ranks + default lettering)
- `assets/lettering/systems.md` — court-card index letters per region
- `assets/courts/` — `king.md` / `queen.md` / `jack.md`, auto-loaded by chosen rank
- `assets/pattern/` — one file per visual style; each holds a `[STYLE_BLOCK]`
- `assets/index/options.md` — corner-index settings (advanced; NOT asked in the wizard)

Scripts under `scripts/`:
- `scripts/manage_config.py` — CLI to read/write/validate `config.json`
  (`show`, `get`, `set`, `unset`, `validate`, `reset`, `options`, `path`)

Reference files under `references/`:
- `references/REFERENCE.md` — COURT / PIP / ACE templates, rank table, aspect ratios
- `references/CONFIG.md` — config schema, lookup order, field reference
- `references/example-court-king.md` — a fully assembled example prompt for reference

---

## Wizard steps

Ask **one logical group at a time**, waiting for each answer. For fixed-choice questions
use `ask_user_input_v0` (tappable options); for open-ended fields ask in plain prose.
Always offer the default so the user can accept with one tap. Read each reference file
as that step comes up — don't preload everything.

### Step 1 — Deck type (suit system) · _persistent_

_Skipped if loaded from config._ Ask which deck. Options:
- **French / International** (Spades, Clubs, Hearts, Diamonds) — **default**
- **German** (Acorns, Leaves, Hearts, Bells)
- **Swiss** (Acorns, Shields, Roses, Bells)
- **Italo-Spanish / Latin** (Swords, Batons, Cups, Coins)

Load the matching `assets/decks/<deck>.md`. It defines the suit table, the available ranks,
and the deck's default lettering system.

### Step 2 — Court lettering system · _persistent_

_Skipped if loaded from config._ Ask which lettering system sets the printed court
letters (see `assets/lettering/systems.md`):
- **Anglo-American** (K / Q / J) — default for French & Latin decks
- **French** (R / D / V)
- **German / Austrian** (K / D / B) — default for German & Swiss decks
- **Russian** (К / Д / В)
- **Dutch** (H / V / B)
- **Scandinavian** (K / D / Kn)

Default to the chosen deck's default system. This only affects court cards (and the Ace
letter); for number cards it's unused, but ask it here to keep the flow consistent.

### Step 3 — Rank · _per-card_

Always ask. Offer only the ranks listed in the chosen `assets/decks/<deck>.md`
(standard set: A, 2–10, J, Q, K). Resolve via the rank table in `references/REFERENCE.md`:
- **K / Q / J → COURT** → auto-load `assets/courts/<rank>.md` and continue the full flow.
- **A → ACE** → skip court Steps 5b–7; go Suit → Style → Aspect ratio.
- **2–10 → PIP** → same skip as Ace.

Set `RANK_NAME` (English word) and `RANK_LETTER` (localized letter from Step 2 for
courts; the numeral for pips; `A` for Ace unless the user wants `1`).

### Step 4 — Suit · _per-card_

Always ask. Offer the four suits from the chosen deck (show symbol/shape + name,
e.g. "♠ Spades" or "Acorns"). Fill `SUIT_NAME_TITLE`, `SUIT_NAME`, `SUIT_SYMBOL`,
`SUIT_COLOR` from the deck file.

### Step 5 — Visual style / pattern (REQUIRED) · _persistent_

_Skipped if loaded from config._ Always ask this on first run; never skip it. List the
`*.md` files in `assets/pattern/` (ignore names starting with `_`) as options:
**Austrian (default) · French · English**, and note they can request another style.
Load the chosen `assets/pattern/<style>.md` and take its `[STYLE_BLOCK]`. For a style
not on disk, improvise a block following `assets/pattern/_adding-a-pattern.md`.

---

**If the rank is A or a number 2–10, jump to Step 9 (Aspect ratio). Steps 5b–7 are court-only.**

---

### Step 5b — Character (court only, REQUIRED) · _per-card_

Every court card must have a character description — **at minimum a name**. Two paths:

**A) A reference image is attached.** Derive the description from it. If subagents are
available, spawn one with this exact English prompt; otherwise do it yourself by looking
at the image with the same prompt:

> Describe the person in the attached image in English: facial features, pose, what they
> are wearing, which era it suggests, and characteristic elements/details of the outfit.

Use the resulting description verbatim as `[CHARACTER_FEATURES]`. Then confirm the
character's **name** with the user (e.g. "Use 'Peter the Great' as the name?") and set
`[CHARACTER_NAME]`.

**B) No reference image.** Ask the user for the character: at minimum a name (required),
plus any physical description / pose / costume they want. Set `[CHARACTER_NAME]` and
`[CHARACTER_FEATURES]`. If they give only a name, you may draft a short feature
description from it and let them edit.

> If the figure is a real, identifiable public figure: keep it a neutral descriptive
> depiction (appearance, costume, pose). Don't fabricate quotes or claims.

### Step 5c — Additional / replaced attributes (court only) · _per-card_

Show the auto-loaded traditional attributes from `assets/courts/<rank>.md` and ask, free text,
for any **additions or replacements** beyond the traditional set (e.g. "replace scepter
with a telescope", "add a laurel wreath"). Fill `[EXTRA_ATTRIBUTES]`, one item per line
prefixed with `- `. If none, drop the ADDITIONAL/REPLACED block entirely.

### Step 6 — Transfer from reference image (court only) · _per-card_

Ask what to carry over from the user's reference image (face, hairstyle, a specific
weapon, an order/medal, etc.). These **take priority over traditional attributes** — note
that in the prompt. Fill `[REFERENCE_TRANSFERS]`, one item per line prefixed with `- `.
If the user has no reference image, drop this block.

### Step 7 — Exclude from reference image (court only) · _per-card_

Ask what must NOT carry over (background, decorative elements, props, landscape). Phrase
each as "no <thing>" joined by commas (e.g. "no background, no cannon, no table"). Fill
`[EXCLUSIONS_LIST]`. If nothing, use "no extra background objects".

---

### Step 9 — Card type / aspect ratio · _persistent_

_Skipped if loaded from config._ Ask the card type (see the aspect-ratio table in
`references/REFERENCE.md`):
- **Bridge / Preferans (Narrow)** — 9:14 — **default**
- **Poker (Wide)** — 5:7
- **European / German (Skat)** — 14:25
- **Tarot** — 7:12
- **Mini** — 5:7
- or a custom ratio (free text)

Fill `[ASPECT_RATIO]` with the ratio only.

---

## Assembling the prompt

1. Pick the template (COURT / PIP / ACE) from `references/REFERENCE.md`.
2. Build `[INDEX_LINE]` from `assets/index/options.md` using the silent defaults (Standard size,
   4-Index, rank stacked above suit) — unless the user explicitly asked for a different
   index, in which case combine the chosen fragments.
3. Substitute every placeholder. For courts, fill `[CHARACTER_NAME]`/`[CHARACTER_FEATURES]`
   (required), then build the attribute blocks in priority order: traditional (from
   `assets/courts/<rank>.md`) → additions/replacements → reference transfers → exclusions.
4. Splice the chosen `[STYLE_BLOCK]` where `[STYLE_BLOCK]` appears.
5. **Drop any block/line whose value is empty** — never output a literal `[PLACEHOLDER]`
   or an empty section header.
6. Consistency check: RANK_LETTER matches the lettering system, SUIT_SYMBOL/SUIT_NAME/
   SUIT_COLOR match the deck, and "STANDARD <RANK_NAME> RANK ATTRIBUTES" matches the rank.

## Presenting the result

Output the finished prompt in a single fenced code block, with a one-line lead-in.
Then offer to tweak any field or build another card. Never call an image tool — this
skill produces prompt text only.

## Worked example

For a fully assembled reference prompt (King of Spades, French deck, Anglo-American
letters, Austrian style), see `references/example-court-king.md`. Read it before
your first assembly to confirm the expected structure, ordering, and spacing.
