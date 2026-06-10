---
name: playing-card-prompt
description: "Interactive wizard that builds stylized playing card prompts. Supports French, German, Swiss, and Italo-Spanish decks, regional court-lettering systems, and auto-loads traditional attributes for Kings, Queens, Jacks, pip cards, and Aces.\n **Trigger on:** “create/make/design/generate a playing card”, “court card”, “custom character card”, “playing card prompt”, “card generator”, or turning a person/character/reference image into a card.\n  **Process:** walk user through deck → lettering → rank → suit → style → attributes → reference transfers → aspect ratio → output final prompt."
---

# Playing Card Prompt Wizard

Runs an interactive wizard that collects choices and assembles a finished
image-generation prompt for a stylized playing card. The deliverable is the completed
prompt text in a code block for the user to copy. **Do not generate the image yourself.**

## How to run the wizard

Ask **one logical group at a time**, waiting for each answer. For fixed-choice questions
use `ask_user_input_v0` (tappable options); for open-ended fields ask in plain prose.
Always offer the default so the user can accept with one tap. Read each reference file
as that step comes up — don't preload everything.

Folders:
- `decks/` — one file per deck system (suits + available ranks + default lettering)
- `lettering/systems.md` — court-card index letters per region
- `courts/` — `king.md` / `queen.md` / `jack.md`, auto-loaded by chosen rank
- `pattern/` — one file per visual style; each holds a `[STYLE_BLOCK]`
- `index/options.md` — corner-index settings (advanced; NOT asked in the wizard)
- `references/templates.md` — COURT / PIP / ACE templates, rank table, aspect ratios

---

### Step 1 — Deck type (suit system)

Ask which deck. Options:
- **French / International** (Spades, Clubs, Hearts, Diamonds) — **default**
- **German** (Acorns, Leaves, Hearts, Bells)
- **Swiss** (Acorns, Shields, Roses, Bells)
- **Italo-Spanish / Latin** (Swords, Batons, Cups, Coins)

Load the matching `decks/<deck>.md`. It defines the suit table, the available ranks,
and the deck's default lettering system.

### Step 2 — Court lettering system

Ask which lettering system sets the printed court letters (see `lettering/systems.md`):
- **Anglo-American** (K / Q / J) — default for French & Latin decks
- **French** (R / D / V)
- **German / Austrian** (K / D / B) — default for German & Swiss decks
- **Russian** (К / Д / В)
- **Dutch** (H / V / B)
- **Scandinavian** (K / D / Kn)

Default to the chosen deck's default system. This only affects court cards (and the Ace
letter); for number cards it's unused, but ask it here to keep the flow consistent.

### Step 3 — Rank (branches the flow)

Ask the rank, offering only the ranks listed in the chosen `decks/<deck>.md`
(standard set: A, 2–10, J, Q, K). Resolve via the rank table in `templates.md`:
- **K / Q / J → COURT** → auto-load `courts/<rank>.md` and continue the full flow.
- **A → ACE** → skip court Steps 5b–7; go Suit → Style → Aspect ratio.
- **2–10 → PIP** → same skip as Ace.

Set `RANK_NAME` (English word) and `RANK_LETTER` (localized letter from Step 2 for
courts; the numeral for pips; `A` for Ace unless the user wants `1`).

### Step 4 — Suit

Ask the suit, offering the four suits from the chosen deck (show symbol/shape + name,
e.g. "♠ Spades" or "Acorns"). Fill `SUIT_NAME_TITLE`, `SUIT_NAME`, `SUIT_SYMBOL`,
`SUIT_COLOR` from the deck file.

### Step 5 — Visual style / pattern (REQUIRED — always ask)

Always ask this; never skip it. List the `*.md` files in `pattern/` (ignore names
starting with `_`) as options: **Austrian (default) · French · English**, and note they
can request another style. Load the chosen `pattern/<style>.md` and take its
`[STYLE_BLOCK]`. For a style not on disk, improvise a block following
`pattern/_adding-a-pattern.md`.

---

**If the rank is A or a number 2–10, jump to Step 9 (Aspect ratio). Steps 5b–7 are court-only.**

---

### Step 5b — Character (court only, REQUIRED)

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

### Step 5c — Additional / replaced attributes (court only)

Briefly note the traditional attributes from `courts/<rank>.md` and ask, free text,
for any **additions or replacements** (e.g. "replace scepter with a telescope", "add a
laurel wreath"). **Merge silently** into the final portrait block instead of listing
separately. If none, skip entirely.

### Step 6 — Transfer from reference image (court only)

Ask what to carry over from the user's reference image (face, hairstyle, a specific
weapon, an order/medal, etc.). These **take priority over traditional attributes** — note
that in the prompt. Fill `[REFERENCE_TRANSFERS]`, one item per line prefixed with `- `.
If the user has no reference image, drop this block.

### Step 7 — Exclude from reference image (court only)

Ask what must NOT carry over (background, decorative elements, props, landscape). Phrase
each as "no <thing>" joined by commas (e.g. "no background, no cannon, no table"). Fill
`[EXCLUSIONS_LIST]`. If nothing, use "no extra background objects".

---

### Step 8 — Card type / aspect ratio (all ranks)

Ask the card type (see the aspect-ratio table in `templates.md`):
- **Bridge / Preferans (Narrow)** — 9:14 — **default**
- **Poker (Wide)** — 5:7
- **European / German (Skat)** — 14:25
- **Tarot** — 7:12
- **Mini** — 5:7
- or a custom ratio (free text)

Fill `[ASPECT_RATIO]` with the ratio only.

---

## Assembling the prompt — COMPACT STYLE

**The prompt must be compact and dense** — suitable for image generation models.
Merge related information into 3–4 logical blocks. Avoid verbose descriptions,
redundant attributes, and ALL-CAPS section headers.

**Compact structure:**

1. **First line:** `[CHARACTER_NAME] as [RANK_NAME] of [SUIT_NAME] playing card` (courts)
   or `[RANK_NAME] of [SUIT_NAME] playing card` (pip/ace).
2. **Style & format block:** copy `[INDEX_LINE]` + `[STYLE_BLOCK]` **verbatim** —
   every word of оформление (border, corner indices, index size, index orientation,
   suit symbols, dividing line, reversible layout, portrait rotation, symmetrical costume,
   cross-hatching specifics, linework quality, palette, card stock, paper grain, finish,
   printing imperfections, background) must be preserved exactly as in the original.
   NO shortening of оформление. Only reorganize into a `Layout:` + `Style:` split for
   readability, without dropping a single descriptor.
3. **Portrait / visual block:** merge `[CHARACTER_FEATURES]` + traditional rank attributes
   (prioritized: traditional defaults → additions/replacements → reference transfers)
   into one flowing paragraph. Resolve all overrides silently — never list a traditional
   attribute that is later replaced. Drop attributes not applicable to the composition
   (e.g. "hands with halberd" if portrait is chest-up only).
4. **Exclusions & constraints block:** list all negative constraints (no hands, no
   background, no watermark), plus color palette, as one compact paragraph.

**Key rules:**
- Drop empty blocks entirely; never output `[PLACEHOLDER]` or empty headers.
- Use short block headers: `Layout:`, `Portrait:`, `Style:`, `Exclusions:`.
- Eliminate redundancy: don't repeat attributes across blocks.
- Merge traditional attributes silently into the portrait block; don't list them
  separately unless the user explicitly asks.
- Consistency check: RANK_LETTER matches lettering system, SUIT_SYMBOL/SUIT_NAME/
  SUIT_COLOR match the deck.

## Presenting the result

Output the finished compact prompt in a single fenced code block, with a one-line
lead-in. Then offer to tweak any field or build another card. Never call an image
tool — this skill produces prompt text only.

## Worked example (King of Spades, French deck, Anglo-American letters, Austrian style)

```
Peter the Great as King of Spades playing card.

Layout: Highly detailed Austrian-style playing card, aspect ratio 9:14. Full card visible. Transparent background outside the card. Thin single black border with stepped corner cut-ins framing the index areas. Four corner indices, each with rank K stacked above suit symbol ♠, standard small index size, upper indices upright, lower indices rotated 180 degrees. Large black spade suit symbols centered in upper and lower card fields. Thin black horizontal dividing line through the exact center of the card. Reversible two-way court card layout, identical upper and lower portraits rotated 180 degrees around the central horizontal axis. Symmetrical costume design (upper/lower halves rotationally mirrored).

Portrait: Tall strong-jawed mature man, dark wavy hair, neat mustache, authoritative pose, piercing gaze. Dark green military caftan with gold buttons, rapier. Light blue Order of Saint Andrew sash and star medallion. Early-18th-century military appearance.

Style: Vintage chromolithographic playing-card illustration. Sharp crisp black outlines, fine engraved linework with dense cross-hatching on face, hair, costume and fabric folds. Colors: rich crimson red, royal cobalt blue, burnished gold accents, warm ochre skin tones. Aged ivory playing-card stock, subtle paper grain, matte finish, slight vintage printing imperfections.

Exclusions: No crown, no cannon, no winter landscape, no fortress, no table, no background objects, no watermark.
```