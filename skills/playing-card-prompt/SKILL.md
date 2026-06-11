---
name: playing-card-prompt
description: Interactive wizard that builds image-generation prompts for stylized playing cards across multiple deck systems (French/International, German, Swiss, Italo-Spanish) and regional court-lettering systems, with auto-loaded traditional attributes for court cards (King/Queen/Jack) plus pip and ace cards. Use this skill whenever the user wants to create, design, or generate a playing card, a court card, a deck card with a custom character, or asks for a "playing card prompt" or "card generator", or to turn a person/character/reference image into a playing card. Trigger it even if the user only says they want to "make a card" — walk them through the wizard (deck, lettering, rank, suit, style, attributes, reference transfers, aspect ratio) and output a finished prompt.
color: emerald
metadata:
  author: webcane
  version: 1.2.0
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

Before asking any wizard questions, load persistent settings (`deck`, `lettering`,
`style`, `aspect_ratio`, `image_generator`, `index.*`) via
`python3 scripts/manage_config.py show`.
Everything else — schema, lookup order, field reference, and the full CLI — is in
`references/CONFIG.md`; read it whenever you need to inspect, change, or validate
`config.json`. Per-card fields (`rank`, `suit`, `character_name`,
`character_features`, `extra_attributes`, `reference_transfers`, `exclusions`) are
always asked fresh and never saved.

---

## Mode: Config (`--init` / `--config`)

Walk the user through **only the persistent settings** (Steps 1, 2, 5, 8, 9 and
optionally index). Show current values if `config.json` already exists so the user
can accept or change each one. At the end, persist each value with
`python3 scripts/manage_config.py set <key> <value>` (it validates and writes
`config.json`), then confirm. Do **not** proceed to card generation.

Steps to ask in config mode:
1. Deck type
2. Court lettering system
3. Visual style / pattern
4. Aspect ratio
5. Image generator (optional — see Step 9)
6. (Optional, only if user asks) Index settings

## Mode: Reset (`--reset`)

Run `python3 scripts/manage_config.py reset --yes` to delete `config.json`, confirm to
the user that defaults are restored, and stop.

## Mode: Generate (default)

Load config. Then run the card wizard with this logic:

- **Config exists** → skip persistent-setting steps; show a one-line summary of the
  loaded settings (e.g. "Using: French deck, Anglo-American letters, Austrian style,
  9:14, NanoBanana") and go straight to per-card steps (rank → suit → court details
  if applicable). Mention the user can run `--config` to change defaults.
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
- `assets/engines/` — one file per image-generation engine, describing how to adapt
  the assembled prompt (negative-list placement, aspect-ratio syntax, extra
  parameters); `_config.md` documents the `image_generator` setting itself

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
not on disk, improvise a block following `assets/pattern/_adding-a-pattern.md`, then
save that improvised block (e.g. note it in the conversation) so later cards in the
same deck reuse the identical wording — every card should carry the SAME `[STYLE_BLOCK]`
text verbatim so the whole deck looks like one consistent set.

---

**If the rank is A or a number 2–10, jump to Step 8 (Aspect ratio). Steps 5b–7 are court-only.**

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
with a telescope", "add a laurel wreath"). Note each as an addition or a replacement —
a replacement will remove the traditional item it replaces when attributes are merged
during assembly (see "Assembling the prompt"). If none, skip this.

### Step 6 — Transfer from reference image (court only) · _per-card_

Ask what to carry over from the user's reference image (face, hairstyle, a specific
weapon, an order/medal, etc.). These **take priority over traditional attributes and
over Step 5c** when merged during assembly. If the user has no reference image, skip this.

### Step 7 — Exclude from reference image (court only) · _per-card_

Ask what must NOT carry over (background, decorative elements, props, landscape). Phrase
each as "no <thing>" — these get merged into the single `[NEGATIVE_LIST]` at the end of
the prompt during assembly. If nothing, no extra exclusions are added.

---

### Step 8 — Card type / aspect ratio · _persistent_

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

### Step 9 — Image generator (optional) · _persistent_

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

1. Pick the template (COURT / PIP / ACE) from `references/REFERENCE.md`.
2. Build `[INDEX_LINE]` from `assets/index/options.md` using the silent defaults (Standard size,
   4-Index, rank stacked above suit) — unless the user explicitly asked for a different
   index, in which case combine the chosen fragments.
3. For courts, fill `[CHARACTER_NAME]`/`[CHARACTER_FEATURES]` (required), then build
   `[RESOLVED_ATTRIBUTES]` and `[NEGATIVE_LIST]` by following the merge rules in
   `references/REFERENCE.md` (resolve conflicts down to one final, deduplicated,
   contradiction-free state — do not list "traditional" and "override" side by side).
4. Splice the chosen `[STYLE_BLOCK]` where `[STYLE_BLOCK]` appears, **copied verbatim and
   in full** (every line, in order, trailing comma kept) — never summarize, reorder, or
   drop lines from it. When generating multiple cards for the same deck, reuse the exact
   same `[STYLE_BLOCK]` text on every card so the set stays visually consistent.
5. **Drop any line whose placeholder is empty** — never output a literal `[PLACEHOLDER]`.
6. Keep phrasing as short, comma-separated visual phrases (general → specific: card
   type/style, then layout, then the portrait, then technical finish, then negatives
   last) — avoid full sentences, section headers, or restating the same detail twice.
7. **Engine-aware prompt formatting** — apply the deltas from the
   `assets/engines/<engine>.md` chosen in Step 9 to the otherwise-finished prompt:
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
8. Run the **Post-validation** checklist below. Fix and re-check until everything
   passes — do not move on to "Presenting the result" with a failing check.

## Post-validation

Before presenting the prompt, verify all of the following against the assembled text:

- [ ] **No raw placeholders** — no literal `[PLACEHOLDER]`-style token remains anywhere.
- [ ] **Lettering consistency** — `RANK_LETTER` matches the lettering system from Step 2
  (e.g. Russian → К/Д/В, not K/Q/J), and the rank/suit pairing matches Step 3–4.
- [ ] **Suit consistency** — `SUIT_NAME`, `SUIT_SYMBOL`, `SUIT_COLOR` belong to the same
  suit and to the deck chosen in Step 1 (no mixing, e.g. Spades symbol with Acorns name).
- [ ] **Attribute resolution** — `[RESOLVED_ATTRIBUTES]` is deduplicated and
  contradiction-free; replacements from Step 5c/6 fully replace (not coexist with) the
  traditional item they replace, and reference-transfer attributes (Step 6) outrank
  Step 5c, which outranks the traditional defaults.
- [ ] **Style block integrity** — `[STYLE_BLOCK]` is the chosen style's block copied
  verbatim and in full (every line, in order, nothing summarized or dropped), and is
  identical across all cards generated for the same deck/session.
- [ ] **Character description (court only)** — `[CHARACTER_NAME]` and
  `[CHARACTER_FEATURES]` are both present and non-empty; if derived from a reference
  image (Step 5b-A), the description reflects what was actually returned, not a
  generic placeholder.
- [ ] **Negative list** — the negative content (from Step 7) contains only "no …"
  exclusion phrases (or the engine's equivalent), deduplicated, with no positive
  attributes leaking in.
- [ ] **Aspect ratio** — the aspect ratio is a concrete `W:H` ratio (from Step 8 or
  the user's custom value) or its engine-specific equivalent (pixel size, `--ar`,
  fixed size), not descriptive text.
- [ ] **Template match** — the COURT/PIP/ACE template matches the resolved rank, and no
  court-only fields (character, attributes, negatives) appear in a PIP/ACE prompt.
- [ ] **Engine formatting** — the chosen `image_generator` (Step 9)'s negative
  handling, aspect-ratio syntax, and extra parameters from
  `assets/engines/<engine>.md` are all applied; for `nanobanana` the prompt matches
  the base template unchanged.

If any check fails, correct the relevant field in place and re-run the checklist —
don't ask the user to fix it unless the failure stems from missing/ambiguous
information only they can resolve (e.g. no character name given at all).

## Presenting the result

Output the finished prompt in a single fenced code block, with a one-line lead-in
naming the target engine (e.g. "For Midjourney:"), already adapted per Step 7's
engine-aware formatting — don't make the user manually move the negative list or
swap in `--ar` themselves. If the assembled prompt feels long or cluttered,
offer a shortened ~50–80 token version that keeps only: card type, character name,
the 3–4 most important resolved attributes, style descriptor, and aspect ratio —
but **never shorten or drop lines from `[STYLE_BLOCK]` itself**, since trimming it
would make the card's visual style diverge from the rest of the deck. Then offer to
tweak any field or build another card. Never call an image tool — this skill produces
prompt text only.

## Worked example

For a fully assembled reference prompt (King of Spades, French deck, Anglo-American
letters, Austrian style, NanoBanana), see `references/example-court-king.md`. Read
it before your first assembly to confirm the expected structure, ordering, and
spacing.

For the same card adapted to other engines (Midjourney, Stable Diffusion, kaze.ai,
DALL·E), see `references/example-engine-variants.md`.
