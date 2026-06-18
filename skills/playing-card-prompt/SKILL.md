---
name: playing-card-prompt
description: Interactive wizard that builds image-generation prompts for stylized playing cards across multiple deck systems (French/International, German, Swiss, Italo-Spanish) and regional court-lettering systems, with auto-loaded traditional attributes for court cards (King/Queen/Jack) plus pip and ace cards. Use this skill whenever the user wants to create, design, or generate a playing card, a court card, a deck card with a custom character, or asks for a "playing card prompt" or "card generator", or to turn a person/character/reference image into a playing card. Trigger it even if the user only says they want to "make a card" — walk them through the wizard (deck, lettering, rank, suit, style, attributes, reference transfers, aspect ratio) and output a finished prompt.
metadata:
  author: webcane
  version: 3.22.3
  description_claudeai: Interactive wizard to build image-gen prompts for stylized playing cards. 4 deck patterns, 6 lettering systems, 3+ styles, court/pip/ace. Trigger on card design requests.
---

# Playing Card Prompt Wizard

Runs an interactive wizard that collects choices and assembles a finished
image-generation prompt for a stylized playing card. The deliverable is the completed
prompt text in a code block for the user to copy. **Do not generate the image yourself.**

---

## Subcommands

The user may invoke the skill in four modes. Detect which one from their message:

| Trigger                                               | Mode        | What to do                                         |
|-------------------------------------------------------|-------------|----------------------------------------------------|
| `--init`, `--config`, `init`, `config`, "configure"   | **Config**  | Run config wizard (profile choice + persistent settings); save to the active profile; stop. |
| `--profile <name>`, "switch/use the `<name>` profile", "list my profiles", "create/rename/delete profile `<name>`" | **Profile** | Manage profiles directly via `python3 scripts/manage_config.py profile ...`; report the result; stop. |
| `--reset`                                             | **Reset**   | Delete `config.json` (all profiles); confirm; stop. |
| _(anything else, or no flag)_                         | **Generate**| Load active profile → run card wizard → output prompt. |

---

## Locating this skill's files

Every `scripts/manage_config.py` command in this document is relative to this
`SKILL.md` file's own directory — call it `<SKILL_DIR>`. Determine `<SKILL_DIR>`
from the path you read this file from (its parent directory), and always invoke
the script as `python3 <SKILL_DIR>/scripts/manage_config.py ...`, regardless of
the shell's current working directory.

---

## Startup: loading saved settings

Before asking any wizard questions, load the active profile's persistent settings
(`deck`, `lettering`, `style`, `frame`, `aspect_ratio`, `image_generator`, `structure`,
`index.symbol`, `index.*`, `layers.*`, `mood`, `theme`, `figure_scale`,
`character_framing`) via `python3 scripts/manage_config.py show`. This also lists
every saved profile and which one is active. `layers.*` includes all card groups:
`court`, `pip`, `ace`, `joker`, `back`, and `special`.
Everything else — schema, profile concept, lookup order, field reference, and the
full CLI — is in `references/CONFIG.md`; read it whenever you need to inspect,
change, or validate `config.json`. Per-card fields (`rank`, `suit`,
`character_name`, `character_features`, `extra_attributes`, `reference_transfers`,
`exclusions`) are always asked fresh and never saved.

---

## Mode: Config (`--init` / `--config`)

**Step 0 — Profile.** Run `python3 scripts/manage_config.py profile list`. If more
than one profile exists, or the user's message implies they want a different "look"
(e.g. "set up a new deck profile"), ask whether to: continue editing the active
profile, switch to an existing one (`profile switch <name>`), or create a new one
(`profile create <name>`, optionally `--from <existing>` to clone the active
profile's settings as a starting point). Otherwise skip straight to Step 1 and edit
the active profile.

Then walk the user through **only the persistent settings** (items 1–8 below, plus
index settings if asked). Show current values for the target profile (from `profile
show`) so the user can accept or change each one. At the end, persist each value with
`python3 scripts/manage_config.py set <key> <value>` (it validates and writes to the
active profile in `config.json`; pass `--profile <name>` if editing a non-active
profile), then confirm. Do **not** proceed to card generation.

Steps to ask in config mode:
1. Deck type
2. Court lettering system
3. Visual style / pattern
4. Card decoration layers and theme (Step 6)
5. Mood / atmosphere (Step 7)
6. Figure block — figure_scale (deck-wide scale), split (per-group split layout),
   figure_type (per-group character/building/animal/custom), and
   character_framing (deck-wide framing, character-only) — from the figure-block
   steps (Steps 8a–8e)
7. Aspect ratio (Step 13)
8. Image generator (optional — see Step 14)
9. Structure — full card (`full`, default) or center-illustration-only
   (`illustration`, for users compositing the artwork into their own SVG/HTML card
   template that already supplies the frame and corner indices). See "`structure`
   setting" in `references/REFERENCE.md` for what changes under `illustration`.
10. Joker index (D2) — `index.count` (placement: `4-index` / `2-index` / `top-only` /
    `none`) and `index.symbol` (glyph: `star-in-circle` / `star` / `Jkr` / `crown` /
    `jester-face` / `none` / custom). Only surface when the user mentions Joker
    settings or asks explicitly.
11. (Optional, only if user asks) Standard index settings, or per-layer overrides via
    `layers.<layer>.<group>` for Court/Pip/Ace (e.g. `layers.ornaments.ace`,
    `layers.figure.pip`, `layers.mood.court`). Turning on `layers.figure.pip` or
    `layers.figure.ace` (transformation decks) makes Steps 8–12 apply to pip/ace
    cards too, the same way they apply to court by default.

## Mode: Profile (`--profile <name>` or other profile commands)

For direct profile-management requests that don't need the settings wizard, call the
matching `python3 scripts/manage_config.py profile <list|show|create|switch|rename|
delete|reset>` subcommand (see `references/CONFIG.md`) and report the result. E.g.
"switch to my gothic-deck profile" → `profile switch gothic-deck`; "make a new
profile called tarot-set based on my current one" → `profile create tarot-set --from
<active>`. If the requested profile doesn't exist, list the available ones and ask
which to use instead of guessing.

## Mode: Reset (`--reset`)

Run `python3 scripts/manage_config.py reset --yes` to delete `config.json` —
**this removes every saved profile**, restoring the single built-in `default`
profile. Confirm this with the user before running it if they have more than one
profile (check `profile list` first). To clear just the active profile's overrides
without affecting other profiles, use `profile reset <name> --yes` instead.

## Mode: Generate (default)

Load the active profile. Then run the card wizard with this logic:

- **Config exists** → skip persistent-setting steps; show a one-line summary of the
  loaded settings including the active profile's name (e.g. "Using profile 'default':
  French deck, Anglo-American letters, Austrian style, 9:14, NanoBanana") and go
  straight to per-card steps (rank → suit → figure details if this card's group has a
  figure). Mention the user can run `--config` to change settings or switch profiles.
- **No config found** → run the full wizard (all steps), then offer to save the
  persistent settings to the active (`default`) profile in `config.json` for next time.

---

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
- `assets/back/` — one file: `symmetry.md`, holding the "Symmetry line" that is always
  appended to `[STYLE_BLOCK]` for the `back` group (step 10 in "Resolving
  `[STYLE_BLOCK]`" in `references/REFERENCE.md`)
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

---

## Wizard steps

Ask **one logical group at a time**, waiting for each answer. For fixed-choice questions
use the `AskUserQuestion` tool (tappable options); for open-ended fields ask in plain
prose. Always make the recommended/default choice the first option so the user can
accept with one tap. `AskUserQuestion` allows at most 4 options per question (plus an
automatic "Other" for free text) — if a step lists more than 4 fixed choices, surface
the default plus the next ~3 most relevant as explicit options and let "Other" cover
the remaining named choices and any custom value. Read each reference file as that step
comes up — don't preload everything.

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
(standard set: A, 2–10, J, Q, K, Joker). Resolve via the rank table in
`references/REFERENCE.md`:
- **K / Q / J → COURT** → auto-load `assets/courts/<rank>.md`; this card's group is
  `court` (`layers.figure.court` defaults to `"character"`).
- **A → ACE** → this card's group is `ace` (`layers.figure.ace` defaults to `"false"`).
- **2–10 → PIP** → this card's group is `pip` (`layers.figure.pip` defaults to `"false"`).
- **Joker → JOKER** → auto-load `assets/courts/joker.md`; this card's group is
  `joker` (`layers.figure.joker` defaults to `"character"`). Skip Step 4 (no suit); run
  Steps 4.1 and 4.2 below instead.
- **Back → BACK** → this card's group is `back` (`layers.figure.back` defaults to
  `"false"`). Skip Step 4 (no suit); run Steps B1–B3 below instead of Steps 4.1–4.2.
- **Special → SPECIAL** → this card's group is `special` (`layers.figure.special` defaults to
  `"false"`). Skip Step 4 (no suit); run Steps S1–S5 below instead of Steps 4.1–4.2.

> If the deck has more than 4 standard rank groups, surface the 4 most common ranks as
> explicit options; Back, Special, and Joker appear under "Other" unless the user is
> generating one of those card types — in which case offer them prominently.

Whether Steps 9–12 apply to this card depends on `layers.figure.<group>` for the group
just set — see the check after Step 7.

Set `RANK_NAME` (English word: Joker for the Joker; Back for the Back; Special for the Special) and
`RANK_LETTER` (localized letter from Step 2 for courts; numeral for pips; `A` for Ace;
`index.symbol` value for the Joker; none for Back or Special — see Steps 4.1–4.2, B1–B3, and S1–S5).

### Step 4 — Suit · _per-card_ (skipped for Joker — see Steps 4.1–4.2)

Always ask for non-Joker cards. Offer the four suits from the chosen deck (show
symbol/shape + name, e.g. "♠ Spades" or "Acorns"). Fill `SUIT_NAME_TITLE`,
`SUIT_NAME`, `SUIT_SYMBOL`, `SUIT_COLOR` from the deck file.

### Steps 4.1–4.2 — Joker-only (run instead of Step 4 when rank is Joker)

**Step 4.1 — Joker type · _per-card_**

Ask which type of Joker this is. This fills `[JOKER_ROLE]` in the JOKER template.
Options:
- **Big Joker (Full)** — primary Joker; vivid full-color elaborate composition. `[JOKER_ROLE]` = `Big Joker, full-color vivid elaborate palette`
- **Little Joker (Half)** — secondary Joker; simpler, subdued or monochrome. `[JOKER_ROLE]` = `Little Joker, simplified subdued monochrome palette`
- **Wild / Trump Joker** — European tradition (Narr / Fool); unpaired. `[JOKER_ROLE]` = `Wild Joker, European fool-card tradition, unpaired`
- **Custom** — user supplies their own type/color/variant description

**Step 4.2 — Joker index placement + symbol · _persistent_ (skipped if loaded from config)**

Ask two things for the Joker's corner indices (Menu D2 — see `assets/index/options.md`):

**Placement** (`index.count`):
- **4-corner** (default) — all four corners
- **2-corner** — top-left and bottom-right only
- **Top-only** — single top-left index
- **None / Full-bleed** — no corner indices

**Symbol** (`index.symbol`, skipped if placement is None):
- **star-in-circle** (default) — `a star enclosed in a circle glyph`
- **star** — `a five-pointed star`
- **Jkr** — `the text "Jkr"`
- or Other: `J`, `crown`, `jester-face`, any custom glyph/text

Save choices via `python3 scripts/manage_config.py set index.count <value>` and
`python3 scripts/manage_config.py set index.symbol <value>`.

### Steps B1–B3 — Back card only (run instead of Steps 4.1–4.2 when rank is Back)

**Step B1 — Back design path · _per-card_**

Offer three design paths (≤ 4 AskUserQuestion options):

- **Suggested (default)** — derive a suggestion from the active style + mood profile.
  Synthesize a back design phrase at prompt time: combine the style name, mood (if set),
  primary colors/motifs from the active pattern, and the symmetry convention into a
  descriptive sentence (e.g., "a mirrored Baroque foliate pattern in deep crimson and
  gold, with ornate repeating motifs,"). Present the suggestion in a code block, then
  proceed to Step B2.
- **Freeform** — ask the user to describe the back design in free text. Use that text
  verbatim as `[BACK_DESIGN]`. Skip Step B2.
- **Reference image + modifications** — ask the user to describe the reference image
  source (e.g., "a 19th-century French card back I have photographed"), then ask what
  modifications to apply (e.g., "replace the blue with gold, simplify the center
  motif"). Assemble as: `Based on [source description]: [modifications]`. The source
  description fills `[BACK_DESIGN]`; the modifications list fills `[BACK_MODIFICATIONS]`.
  Skip Step B2.

**Step B2 — Suggested path refinement · _per-card (only for suggested path)_**

After presenting the synthesized suggestion in a code block (from Step B1 Suggested
path), offer:

- **Use this** — fold the suggestion as-is into `[BACK_DESIGN]`. Leave
  `[BACK_MODIFICATIONS]` empty (drop that line at assembly).
- **Modify it** — switch to the freeform path: pre-fill the suggestion text as the
  starting draft for the user to edit, then collect their edited version as
  `[BACK_DESIGN]`. Leave `[BACK_MODIFICATIONS]` empty.

**Step B3 — Back card exclusions · _per-card (optional)_**

Ask what must NOT appear on the back (e.g., "no text", "no human figures"). Phrase each
as "no <thing>" — merge into `[NEGATIVE_LIST]`. If nothing, skip.

### Steps S1–S5 — Special card only (run instead of Step 4 when rank is Special)

**Step S1 — Card title · _per-card_**

Ask the user for the title of this special card. This becomes `[CARD_NAME]`.
Examples: "The Oracle", "The Fool's Gambit", "Воронежские деятели культуры". No default — required, always ask.

**Prospect type:** the title is the name of the full prospect sheet (the ONE card depicting
all 12 court figures). Do not ask for individual court card slot names here.

**Step S2 — Special card type · _per-card_**

Ask which type of special card this is. List the `*.md` files in `assets/special/` (ignore
names starting with `_`) as options — same discovery pattern as `assets/frame/`. Offer
(≤ 4 AskUserQuestion options):
- **Prospect** — a named historical or thematic figure assigned to a court card slot.
  Load `assets/special/prospect.md`; use its "Special type line" as `[SPECIAL_TYPE_LINE]`.
- **Marketing** — a promotional or marketing card with custom branding.
  Load `assets/special/marketing.md`; use its "Special type line" as `[SPECIAL_TYPE_LINE]`.
- **Custom text** — user describes the special card type in free text. Use that text
  verbatim as `[SPECIAL_TYPE_LINE]` (bypasses asset lookup).

If a preset is named, load `assets/special/<name>.md` and use its "Special type line"
text as `[SPECIAL_TYPE_LINE]`. If "Custom text", use the user's free text verbatim as
`[SPECIAL_TYPE_LINE]`.

**Step S3 — Visual content / layout description · _per-card_**

For **non-prospect types**: ask the user to describe the visual content. This becomes
the base `[FIGURE_DESCRIPTION]`.

For **Prospect type**: ask how the 12 figures should be arranged on the card (e.g.
"4 columns grouped by suit", "3 rows grouped by rank", "free-form collage"). This becomes
`[SPECIAL_ATTRIBUTES]` — the layout instruction that wraps the figure list. If the user
doesn't specify, default to "4 suits × 3 ranks grid, each figure a small portrait".

**Step S4 — Named figures table · _(Prospect type only)_**

Only runs when the user selected "Prospect" in Step S2.

A prospect card is ONE card showing ALL 12 court figures in a single image. The wizard
collects all 12 assignments before generating ONE prompt — not one prompt per figure.

**Collection:**
1. Present the 12 slots as a table (or accept the table from the user if they provide it
   upfront). Slots: King/Queen/Jack × ♠ ♥ ♦ ♣ (or active deck equivalents).
2. For each slot ask (or accept in bulk): the named figure and an optional short
   description (title, era, role). Accept grouped input (e.g. "♠: Peter I, Catherine II,
   Menshikov") or one-by-one.
3. The user may optionally group suits under a thematic label (e.g. "♣ Music & Folk Art")
   — include these labels in `[FIGURE_DESCRIPTION]` if provided.
4. After all 12 (or user says "done"), confirm the table, then proceed to generate.

**Assembly:**
`[FIGURE_DESCRIPTION]` for prospect cards is a structured list of all collected figures:

```
suit arrangement (4 suits × 3 ranks):
  ♠ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack),
  ♥ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack),
  ♦ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack),
  ♣ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack),
```

This entire block is `[FIGURE_DESCRIPTION]` in the SPECIAL template. Output: ONE prompt.

Session only — figures are not persisted to config in v1.

**Step S5 — Special card exclusions · _per-card (optional)_**

Ask what must NOT appear on the special card (e.g., "no playing card symbols", "no suit
marks"). Phrase each as "no <thing>" — merged into `[NEGATIVE_LIST]`. If nothing, skip.

### Step 5 — Visual style / pattern (REQUIRED) · _persistent_

_Skipped if loaded from config._ Always ask this on first run; never skip it. List the
`*.md` files in `assets/pattern/` (ignore names starting with `_`) as options:
**Austrian (default) · French · English · Art Nouveau · Japanese (ukiyo-e)**, and note
they can request another style or era/cultural setting (e.g. "Art Deco", "Mexican
Loteria", "Egyptian").
Load the chosen `assets/pattern/<style>.md` and note its layer sections (Background,
Decor, Ornaments, Highlights, Technique, Figure detail, Face Style, Finish).
For a style not on disk,
improvise these sections following `assets/pattern/_adding-a-pattern.md`, then save
the improvised text (e.g. note it in the conversation) so later cards in the same deck
reuse identical wording — every card of the same group should resolve to the SAME
`[STYLE_BLOCK]` text verbatim so the whole deck looks like one consistent set.

### Step 6 — Card decoration and theme · _persistent_

_Skipped if loaded from config._ Every card is built from layers — background, decor,
ornaments, highlights, frame, figure, mood, and technique — controlled per card group
via `layers.<layer>.<group>` (defaults and full resolution rules are in "Layers and
`[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`). Ask these here:

1. **Number cards (2–10)** — how should they look:
   - **Plain (default)** — large suit-color pip symbols only: no extra decor, no
     ornaments, no border. Sets `layers.decor.pip = "false"`,
     `layers.ornaments.pip = "false"`, `layers.frame.pip = "false"`.
   - **Decorated** — keeps the style's decor accents and adds ornaments plus a
     border. Sets `layers.decor.pip = "true"`, `layers.frame.pip = "true"`, then ask,
     free text, what extra ornament to add (e.g. "small corner flourishes",
     "ornamental pip surrounds"). If given, set `layers.ornaments.pip` to that text
     (this both turns ornaments on and supplies the addition); if skipped, set
     `layers.ornaments.pip = "true"`.

2. **Frame / border style (optional, deck-wide)** — ask which border style the framed
   groups (`layers.frame.<group>` on — court/ace by default, plus pip if Decorated
   above) should use. List the `*.md` files in `assets/frame/` (ignore names starting
   with `_`) as options, e.g.:
   - **Boxed Index (default)**
   - **Stepped Corners (Classic)**
   - **Double Rule**
   - **Ornate Scrollwork**

   "Other" covers Art Deco Geometric, Rope Twist, and any custom border description. If a preset is named,
   load `assets/frame/<name>.md` and use its "Frame line" verbatim as `frame`. If the
   user gives custom text instead, save it as `frame`, phrased as its own
   comma-terminated phrase. If skipped, leave `frame` at its default
   (`boxed-index`). Per-group additions on top of the chosen frame (e.g. "gold
   foil edging" only on court cards) are config-only, not asked here — set via
   `python3 scripts/manage_config.py set layers.frame.<group> "<text>"` (this also
   turns the frame on for that group if it was off).

3. **Highlights / overlays (optional, all cards)** — ask, free text, whether to add
   any gilding, lacquer, glow, or shine accents (e.g. "gold leaf highlights along the
   raised linework"). If the user gives a description, set
   `layers.highlights.court`, `layers.highlights.pip`, `layers.highlights.ace`, and
   `layers.highlights.joker` to that text (this both turns the highlights layer on and
   supplies the addition for all groups). If skipped, leave the highlights layer off
   everywhere (the default).

   Per-group additions to the background or background pattern/accents (e.g. "faint
   marbling on the court cards only") are likewise config-only, not asked here — set
   via `python3 scripts/manage_config.py set layers.background.<group> "<text>"` /
   `layers.decor.<group> "<text>"` (also turns that layer on for that group if off).

4. **Theme / symbolism (optional, deck-wide)** — ask, free text, for an overarching
   concept tying the deck together (e.g. "celestial mythology", "botanical garden",
   "clockwork/steampunk"). If given, save it as the `theme` setting; any
   `layers.ornaments`/`layers.highlights`/`layers.frame` cell left at exactly `"true"`
   (on, no explicit addition) then falls back to a theme-derived phrase (see
   "Theme-derived ornaments/highlights/frame" in `references/REFERENCE.md`) — explicit
   additions always win. If skipped, leave `theme` empty.

Court and Ace keep their other layers on by default (see the Defaults table in
`references/REFERENCE.md`); tune any layer via `python3 scripts/manage_config.py set
layers.<layer>.<group> false/true` (e.g. `layers.figure.pip true` for a
transformation-style deck where number cards carry small figures).

A group-wide figure trait shared by every figure in a group (e.g. "all court figures
shown with a slight hunch"), layered on top of the chosen pattern's Face Style, is
config-only — not asked here — set via `python3 scripts/manage_config.py set
layers.figure.<group> "<text>"` (see "Figure, face style & proportion" in
`references/REFERENCE.md`). For `pip`/`ace`, this also turns figures on for that group
(transformation-style deck) — the trait only makes sense if the group has a figure.

The chosen pattern's "Technique" lines (its linework/rendering medium — see "Layers
and `[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`) apply to every group by
default, independently of whether that group has a figure. The pattern's "Finish"
lines (print-quality/final-rendering descriptor) share this same gate, so dropping
Technique drops Finish too. Dropping the pattern's illustration technique (and finish)
for one group only (e.g. an unstyled plain pip face) or adding a group-specific
rendering note is config-only — set via `python3 scripts/manage_config.py set
layers.technique.<group> false` (or `"<text>"` for a Technique addition; Finish has no
separate addition slot).

---

### Step 7 — Mood / atmosphere · _persistent_

_Skipped if loaded from config._ Ask for the deck's overall atmosphere — this becomes
`[MOOD_LINE]`, appended within `[STYLE_BLOCK]` for every card group where
`layers.mood.<group>` is `true` (see "Layers and `[STYLE_BLOCK]` assembly" in
`references/REFERENCE.md`).

List the `*.md` files in `assets/mood/` (ignore names starting with `_`) as options.
Offer **None** as the default, plus the 3 most evocative presets as explicit choices —
e.g.:
- **None (default)** — no mood line; `mood` stays empty.
- **Gothic & Brooding**
- **Warm & Whimsical**
- **Eerie Nocturnal**

"Other" covers the remaining presets (Regal & Opulent, Serene Pastoral, Noir &
Mysterious — name one to use it) and any custom free-text atmosphere (e.g. "celestial
and dreamlike, soft starlight glow,").

- If a preset is named, load `assets/mood/<name>.md` and use its "Mood line" text
  verbatim as `mood`.
- If the user gives custom text instead, save it as `mood`, phrased as its own
  comma-separated phrase (ending in a comma) to match `[MOOD_LINE]`'s format.
- If "None" or skipped, leave `mood` empty — `[MOOD_LINE]` is then dropped everywhere
  regardless of `layers.mood.<group>`, so skip the group question below.

If `mood` is non-empty, ask which card groups should carry it — multiSelect (Court,
Pip, Ace, Joker; default: all four selected, matching the current `layers.mood.<group>`
defaults). Set `layers.mood.<group>` to `true` for selected groups and `false` for any
deselected ones.

A per-group mood addition on top of the deck-wide `mood` (e.g. extra atmosphere only
on the court cards) is config-only, not asked here — set via
`python3 scripts/manage_config.py set layers.mood.<group> "<text>"` (see "Resolving
`[STYLE_BLOCK]`" step 8 in `references/REFERENCE.md` for how it's appended).

---

**Check `layers.figure.<group>` for this card's group** (`court`/`pip`/`ace`/`joker`/`back`/`special`).
The value is `"false"` (no figure) or a figure type (`"character"`, `"building"`,
`"animal"`, `"custom"`), defaulting to `"character"` for court and joker, `"false"` for
pip/ace/back/special unless previously configured via `--config`). If it's `"false"`, this card
has no figure — **skip the entire figure block (Steps 8a–8e) and go straight to Step 13**
(Aspect ratio). Otherwise, the figure block (Steps 8a–8e) and Steps 9–12 apply: court
and joker cards by default, plus any pip/ace/back/special card whose `layers.figure.<group>` was
set to a type value. Steps 8a–8c are persistent — skipped if already set or loaded from
config; Steps 8d–8e are character-only persistent (skipped if `layers.figure.<group>` is
not `"character"`); Steps 9–12 are per-card.

---

### Step 8a — Figure scale · _persistent_

_Skipped if already set in config, or if `layers.figure.<group>` is `"false"` for
this card's group (see the check above)._ Ask how the figure should sit in the frame
across the deck — this becomes `figure_scale`, applied to every card with a figure
(all figure types: character, building, animal, custom). This is a deck-wide setting;
the same scale is reused for every figure card so the set reads consistently framed.

Offer (default first, per the AskUserQuestion 4-option limit):
- **Inscribed in frame (default)** — the figure is fully contained within the card
  border. Sets `figure_scale = "inscribed-in-frame"`.
- **Full-bleed** — the figure fills and bleeds to the edges of the frame. Sets
  `figure_scale = "full-bleed"`.
- **Small centered** — a small figure centered with space around it. Sets
  `figure_scale = "small-centered"`.
- **Other** — any custom crop/scale description (free text).

Save via `python3 scripts/manage_config.py set figure_scale <value>`. If custom text,
save it phrased as its own comma-separated phrase (ending in a comma).

### Step 8b — Split layout · _per-group persistent_

_Skipped if already set for this group in config, or if `layers.figure.<group>` is
`"false"` (the whole figure block is skipped when the layer is off — SPLT-04)._ Ask
how the figures on the cards in this group should be split (per-group; asked once for
each group, then reused). Applies to all figure types.

Offer (default first):
- **Full body, no split (default)** — single upright figure, no mirroring. Sets
  `layers.split.<group> = "none"`.
- **Horizontal mirrored** — two mirror-image halves meeting at a horizontal edge
  through the center. Sets `layers.split.<group> = "horizontal-mirrored"`.
- **Angled mirrored** — two mirror-image halves angled around the figure. Sets
  `layers.split.<group> = "angled-mirrored"`.
- **Other** — any custom split/mirror description (free text).

Save via `python3 scripts/manage_config.py set layers.split.<group> <value>` (replace
`<group>` with the actual group: `court`, `pip`, `ace`, or `joker`).

### Step 8c — Figure type · _per-group persistent_

_Skipped if already set for this group in config, or if `layers.figure.<group>` is
`"false"`._ Ask what kind of figure this group carries. This sets the group's figure
layer value — the value IS the figure type, keeping the layer on while recording the
type (D-02). Per-group; asked once, then reused.

Offer (default first, per 4-option AskUserQuestion limit):
- **Character (default)** — a person or humanoid figure. Sets
  `layers.figure.<group> = "character"`.
- **Building** — an architectural structure. Sets
  `layers.figure.<group> = "building"`.
- **Animal** — a creature or beast. Sets `layers.figure.<group> = "animal"`.
- **Custom** — user-described figure type (free text). Sets
  `layers.figure.<group> = "custom"` (or the user's description).

Save via `python3 scripts/manage_config.py set layers.figure.<group> <type>` (replace
`<group>` with the actual group). Note that this both keeps the figure layer on for
this group and records the figure type.

**Steps 8d–8e apply ONLY when the group's figure type is `"character"`.** For
`building`, `animal`, and `custom` figure types, skip Steps 8d–8e and proceed directly
to Steps 9–12 (character description steps, adapted for the figure type). Building,
animal, and custom figures still benefit from figure_scale (Step 8a) and split
(Step 8b) — only the character-specific face_style and character_framing are skipped
(FIG-08).

### Step 8d — Face style (character-only gate)

_Applies ONLY when `layers.figure.<group>` is `"character"`._ For `building`,
`animal`, and `custom` figure types, face_style is not applied — skip this step.

For character type: how a figure's face reads (typage, expression, degree of
stylization) comes from the chosen pattern's own "Face Style" section, folded into
`[STYLE_BLOCK]` automatically whenever the figure type is `character`. There is no
separate question for this — the pattern supplies it. State this gate explicitly so
the user understands: **Face Style from the pattern applies only when figure type is
character**; building/animal/custom figures receive the figure-type text and figure
scale, but not the pattern's Face Style line.

### Step 8e — Character framing · _character-only persistent_

_Applies ONLY when `layers.figure.<group>` is `"character"`. Skipped if already set
in config, or if figure type is not character._ Ask how much of the character figure
is shown across the deck — this becomes `character_framing`, folded into `[STYLE_BLOCK]`
for every character-type card (see "Figure, face style & proportion" in
`references/REFERENCE.md`). This is a deck-wide setting; reused across every card
whose group's figure type is character. Building, animal, and custom figures skip this
step (FIG-08).

List the `*.md` files in `assets/character-framing/` (ignore names starting with `_`)
as options. Offer (default first, per 4-option AskUserQuestion limit):
- **None (default)** — no framing line; `character_framing` stays empty (the
  pattern/template's own framing applies, unconstrained).
- **Waist-up**
- **Three-quarter**
- **Full body**

"Other" covers the remaining presets (Bust, Seven-eighths) and any custom framing/crop
description (e.g. "tightly cropped headshot, shoulders only,").

- If a preset is named, load `assets/character-framing/<name>.md` and use its
  "Character framing line" text verbatim as `character_framing`.
- If the user gives custom text instead, save it as `character_framing`, phrased as
  its own comma-separated phrase (ending in a comma).
- If "None" or skipped, leave `character_framing` empty — no framing line is added for
  character cards.

Save via `python3 scripts/manage_config.py set character_framing <value>`.

### Step 9 — Character / figure description (REQUIRED for cards with a figure) · _per-card_

Every card with a figure must have a figure description — **at minimum a name**. Two paths:

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

How the figure's face should read (typage, expression, degree of stylization) comes
from the chosen pattern's own "Face Style" section — folded into `[STYLE_BLOCK]`
automatically whenever `layers.figure.<group>` is on, so it stays consistent with the
rest of that pattern's look (see "Figure, face style & proportion" in
`references/REFERENCE.md`). There's no separate question for this. If that line
describes an obscured or mask-like treatment, drop any facial description from
`[CHARACTER_FEATURES]` so the two don't contradict each other.

### Step 10 — Additional / replaced attributes (figure cards) · _per-card_

For court cards, show the auto-loaded traditional attributes from `assets/courts/<rank>.md`
and ask, free text, for any **additions or replacements** beyond the traditional set
(e.g. "replace scepter with a telescope", "add a laurel wreath"). Note each as an
addition or a replacement — a replacement will remove the traditional item it replaces
when attributes are merged during assembly (see "Assembling the prompt"). For pip/ace
cards with `layers.figure.<group>` on (transformation decks), there's no traditional
attribute set to load — just ask, free text, for any attributes or props the figure
should carry. If none, skip this.

### Step 11 — Transfer from reference image (figure cards) · _per-card_

Ask what to carry over from the user's reference image (face, hairstyle, a specific
weapon, an order/medal, etc.). These **take priority over traditional attributes and
over Step 10** when merged during assembly. If the user has no reference image, skip this.

### Step 12 — Exclude from reference image (figure cards) · _per-card_

Ask what must NOT carry over (background, decorative elements, props, landscape). Phrase
each as "no <thing>" — these get merged into the single `[NEGATIVE_LIST]` at the end of
the prompt during assembly. If nothing, no extra exclusions are added.

---

### Step 13 — Card type / aspect ratio · _persistent_

_Skipped if loaded from config._ Ask the card type (see the aspect-ratio table in
`references/REFERENCE.md`):
- **Bridge / Preferans (Narrow)** — 9:14 — **default**
- **Poker (Wide)** — 5:7
- **European / German (Skat)** — 14:25
- **Tarot** — 7:12
- **Mini** — 5:7
- or a custom ratio (free text)

Fill `[ASPECT_RATIO]` with the ratio only. If `structure` is `illustration`, this
ratio describes the proportions of the center illustration/clip area in the user's
own card template, not the whole card — see "`structure` setting" in
`references/REFERENCE.md`.

---

### Step 14 — Image generator (optional) · _persistent_

_Skipped if loaded from config — just mention which engine is in use (e.g. "Using:
Midjourney") and that `--config` can change it._ Otherwise ask, optional, with
**NanoBanana as the default**:

- **NanoBanana** — default, no adaptation needed
- **Stable Diffusion** (SD 1.5 / SDXL / Flux)
- **Midjourney**
- **DALL·E**
- **kaze.ai**
- or another engine name (free text)

If the user skips this step, use `nanobanana`. Load the matching
`assets/engines/<engine>.md` (see `assets/engines/_config.md` for the lookup and
fallback rules) — it defines how to adapt the assembled prompt for that engine.
Offer to save the choice to `config.json` like the other persistent settings.

---

## Assembling the prompt

1. Pick the template (COURT / PIP / ACE / JOKER / BACK / SPECIAL) from `references/REFERENCE.md`.
   If rank = Back, use the BACK template. If rank = Special, use the SPECIAL template.
   If `structure` is `illustration`, replace the template's opening line with the
   illustration-only opening line from "`structure` setting" in `references/REFERENCE.md`
   (otherwise use the template's default opening line unchanged).
2. Build `[INDEX_LINE]` from `assets/index/options.md`:
   - **Standard cards** (`index.type = "standard"`): Menus A/B/C — rank+suit, silent
     defaults (4-Index, stacked, standard size).
   - **Joker cards** (`index.type = "joker"`, always for the `joker` group): Menu D2 +
     Symbol table — placement from `index.count`, symbol from `index.symbol`. When
     `index.count = "none"` (or `index.symbol = "none"`), emit only `no corner indices,
     full-bleed illustration,`.
   - **Back cards**: `[INDEX_LINE]` is replaced by the fixed line `no corner indices, no
     rank letters, no suit symbols,` — skip the `assets/index/options.md` lookup entirely.
   - **Special cards**: `[INDEX_LINE]` is replaced by the fixed line `no corner indices,
     no standard rank letters, no suit symbols,` hardcoded in the SPECIAL template —
     skip the `assets/index/options.md` lookup entirely.
   - If `structure` is `illustration`, skip this step entirely for all card types.
3. For cards with a figure, fill `[CHARACTER_NAME]`/`[CHARACTER_FEATURES]` (required), then build
   `[RESOLVED_ATTRIBUTES]` and `[NEGATIVE_LIST]` by following the merge rules in
   `references/REFERENCE.md` (resolve conflicts down to one final, deduplicated,
   contradiction-free state — do not list "traditional" and "override" side by side).
   If `structure` is `illustration`, append the fixed negative block from "`structure`
   setting" in `references/REFERENCE.md` (`no card border, no frame, no corner index
   letters or numbers, no corner suit symbols`) to `[NEGATIVE_LIST]`.
4. Resolve `[STYLE_BLOCK]` and `[FRAME_LINE]` for this card's group
   (court/pip/ace/joker/back/special) per "Layers and `[STYLE_BLOCK]` assembly" and "Figure,
   face style & proportion" in `references/REFERENCE.md`, using the `layers.*`, `frame`,
   `mood`, and `theme` settings (deriving thematic ornaments/highlights/frame additions
   per "Theme-derived ornaments/highlights/frame" where applicable, and including the
   chosen pattern's Face Style line when `layers.figure.<group>` is on). `[FRAME_LINE]`
   is the chosen `frame` preset's "Frame line" from `assets/frame/<frame>.md` plus
   `layers.frame.g`'s addition if its cell is custom text, included only if
   `layers.frame.g` is on. Splice the result **in full** — never summarize, reorder, or
   drop a line from an enabled layer. If `structure` is `illustration`, drop
   `[FRAME_LINE]` from the template entirely regardless of `layers.frame.g` — leave
   `layers.frame.<group>` in `config.json` untouched, just don't emit the line.
   For the `back` group, append the "Symmetry line" from `assets/back/symmetry.md` as
   the final item of `[STYLE_BLOCK]` (step 10 in "Resolving `[STYLE_BLOCK]`" in
   `references/REFERENCE.md`).
   When generating multiple cards for the same deck, reuse the exact same resolved
   `[STYLE_BLOCK]`/`[FRAME_LINE]`/derived theme phrases for every card of the same
   group so the set stays visually consistent.
5. **Drop any line whose placeholder is empty** — never output a literal `[PLACEHOLDER]`.
6. Keep phrasing as short, comma-separated visual phrases (general → specific: card
   type/style, then layout, then the portrait, then technical finish, then negatives
   last) — avoid full sentences, section headers, or restating the same detail twice.
7. **Engine-aware prompt formatting** — apply the deltas from the
   `assets/engines/<engine>.md` chosen in Step 14 to the otherwise-finished prompt:
   - **Negative handling** — if the engine moves negatives out of the main body
     (Stable Diffusion, Midjourney, kaze.ai, DALL·E), remove the trailing
     `[NEGATIVE_LIST]` line from the main prompt and reformat it per that engine's
     file (separate `Negative prompt:`/`Negative:` block, `--no` flags, or folded
     into a positive avoidance clause for DALL·E).
   - **Aspect ratio syntax** — if the engine replaces the
     `[ASPECT_RATIO] aspect ratio,` lead-in (SD pixel size, Midjourney/kaze `--ar`,
     DALL·E fixed size), drop the lead-in phrase and apply that engine's syntax.
   - **Extra parameters** — append any engine-specific suffix flags (e.g.
     Midjourney's `--v 7 --style raw`).
   - For `nanobanana` (default), no changes apply — skip this step.
8. Run the **Post-validation** checklist in `references/POST-VALIDATION.md` against
   the assembled text. Fix and re-check until everything passes — do not move on to
   "Presenting the result" with a failing check.

## Presenting the result

Output the finished prompt in a single fenced code block, with a one-line lead-in
naming the target engine (e.g. "For Midjourney:"), already adapted per the
engine-aware formatting step above — don't make the user manually move the negative list or
swap in `--ar` themselves. If the assembled prompt feels long or cluttered,
offer a shortened ~50–80 token version that keeps only: card type, character name,
the 3–4 most important resolved attributes, style descriptor, and aspect ratio —
but **never shorten or drop lines from `[STYLE_BLOCK]` itself**, since trimming it
would make the card's visual style diverge from the rest of the deck. Then offer to
tweak any field or build another card. Never call an image tool — this skill produces
prompt text only.

## Worked example

For a fully assembled COURT reference prompt (King of Spades, French deck,
Anglo-American letters, Austrian style, NanoBanana), see
`references/example-court-king.md`. Read it before your first assembly to confirm the
expected structure, ordering, and spacing.

For a fully assembled PIP reference prompt (Two of Spades, French deck, Austrian
style, 9:14), including both the default "plain" resolution and the "decorated"
variant, see `references/example-pip-two.md`. Read it before assembling any PIP/ACE
card to confirm how `[STYLE_BLOCK]` and `[FRAME_LINE]` resolve per layer.

For the King of Spades card adapted to other engines (Midjourney, Stable Diffusion,
kaze.ai, DALL·E), see `references/example-engine-variants.md`.
