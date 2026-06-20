# File Map

Maps the skill's folder layout — every `assets/`, `scripts/`, and `references/` file and what it backs — for `SKILL.md`. Read it whenever you need to find which file backs an asset/preset.

## File map

Folders under `assets/`:
- `assets/decks/` — one file per deck system (suits + available ranks + default lettering)
- `assets/lettering/systems.md` — court-card index letters per region
- `assets/courts/` — `king.md` / `queen.md` / `jack.md`, auto-loaded by chosen rank
- `assets/pattern/` — one file per visual style; each holds layer-fragment sections
  (Background, Decor, Ornaments, Highlights, Technique, Figure detail, Face
  Style, Finish) that assemble into `[STYLE_BLOCK]` per card group (see
  `references/REFERENCE.md`)
- `assets/mood/` — one file per mood/atmosphere preset, each holding a "Mood line"
  used to fill `[MOOD_LINE]` (see Step 7 and `assets/mood/_adding-a-mood.md`)
- `assets/frame/` — one file per border/frame preset, each holding a "Frame line"
  used to fill `[FRAME_LINE]` (see Step 6 and `assets/frame/_adding-a-frame.md`)
- `assets/figure-type/` — one file per figure type (`character.md`, `building.md`,
  `animal.md`, `custom.md`), each holding the canonical prompt phrase for that figure
  type's contribution to `[STYLE_BLOCK]` (see Steps 8a–8c and
  `assets/figure-type/_adding-a-figure-type.md`)
- `assets/split/` — one file per split mode (`horizontal-mirrored.md`,
  `angled-mirrored.md`), each holding the canonical prompt phrase for that split mode
  appended as the outer compositional wrapper in `[STYLE_BLOCK]` (see Step 8b and
  `assets/split/_adding-a-split.md`); `none`/`false` produce no text
- `assets/character-framing/` — one file per character framing/cropping preset (e.g.
  `waist-up.md`, `full-body.md`), each holding a "Character framing line" folded into
  `[STYLE_BLOCK]` for character-type figures only (see Step 8e and
  `assets/character-framing/_adding-a-character-framing.md`)
- `assets/figure-proportion/` — legacy directory from pre-4.0; content is preserved
  for reference but superseded by `assets/character-framing/` (see migration notes in
  `references/CONFIG.md`)
- `assets/back/` — back card design asset directories:
  - `purpose/` — one file per purpose preset (`classic.md`, `designer.md`, `casino.md`);
    each holds a "Purpose line" loaded in Step B1
  - `design/<category>/` — four pattern files per design category (`geometric/`,
    `botanical/`, `abstract/`, `illustrated/`); each holds a "Pattern line" loaded in
    Step B3 based on B2 category choice
  - `palette/` — one file per palette preset (`classic-red.md`, `classic-blue.md`,
    `dark.md`, `gold.md`); each holds a "Palette line" loaded in Step B4
  - `symmetry/` — one file per symmetry type (`rotational-180.md`, `bilateral.md`,
    `asymmetric.md`); each holds a "Symmetry line" always appended to `[STYLE_BLOCK]`
    for the `back` group (step 10 in "Resolving `[STYLE_BLOCK]`" in
    `references/REFERENCE.md`), selected via `back_symmetry` config field
  - `symmetry.md` — legacy single-file symmetry entry (superseded by `symmetry/`
    subdirectory; kept for reference)
- `assets/special/` — one file per special card type (`prospect.md`, `marketing.md`,
  etc.); each holds a "Special type line" used to fill `[SPECIAL_TYPE_LINE]` in the
  SPECIAL template (see Steps S1–S5 and `assets/special/_adding-a-special.md`)
- `assets/index/options.md` — corner-index settings (advanced; NOT asked in the wizard)
- `assets/engines/` — one file per image-generation engine, describing how to adapt
  the assembled prompt (negative-list placement, aspect-ratio syntax, extra
  parameters); `_config.md` documents the `image_generator` setting itself

Scripts under `scripts/`:
- `scripts/manage_config.py` — CLI to read/write/validate `config.json`
  (`show`, `get`, `set`, `unset`, `validate`, `reset`, `options`, `path`, and
  `profile list|show|create|switch|rename|delete|reset`)

`config.json` ships at the skill root with a `default` profile populated with
factory settings — it's the canonical source of defaults (see
`references/CONFIG.md`). User edits add/switch profiles in the same file.

Reference files under `references/`:
- `references/REFERENCE.md` — COURT / PIP / ACE / JOKER / BACK / SPECIAL templates, rank table, aspect ratios
- `references/CONFIG.md` — config schema, profiles, lookup order, field reference
- `references/example-court-king.md` — a fully assembled COURT example prompt for reference
- `references/example-pip-two.md` — a fully assembled PIP example prompt (plain default and decorated variant)
- `references/STYLE-COMPONENTS.md` — maps the deck's style components (medium,
  palette, era, mood, composition, etc.) to the config field/layer/template that
  addresses each, and flags open gaps
- `references/WIZARD-STEP-MAP.md` — maps each wizard step to the style components,
  `layers.*`, prompt placeholders, and `assets/` files it touches
- `references/POST-VALIDATION.md` — final checklist run before presenting the
  assembled prompt
