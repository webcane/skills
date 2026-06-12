---
name: playing-card-prompt
description: Interactive wizard that builds image-generation prompts for stylized playing cards across multiple deck systems (French/International, German, Swiss, Italo-Spanish) and regional court-lettering systems, with auto-loaded traditional attributes for court cards (King/Queen/Jack) plus pip and ace cards. Use this skill whenever the user wants to create, design, or generate a playing card, a court card, a deck card with a custom character, or asks for a "playing card prompt" or "card generator", or to turn a person/character/reference image into a playing card. Trigger it even if the user only says they want to "make a card" — walk them through the wizard (deck, lettering, rank, suit, style, attributes, reference transfers, aspect ratio) and output a finished prompt.
metadata:
  author: webcane
  version: 3.0.0
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

## Startup: loading saved settings

Before asking any wizard questions, load the active profile's persistent settings
(`deck`, `lettering`, `style`, `aspect_ratio`, `image_generator`, `index.*`,
`layers.*`, `ornaments_extra.*`, `highlights_extra.*`, `mood`, `theme`,
`face_style.*`) via `python3 scripts/manage_config.py show`. This also lists every
saved profile and which one is active.
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

Then walk the user through **only the persistent settings** (Steps 1, 2, 5, 8, 9 and
optionally index). Show current values for the target profile (from `profile show`)
so the user can accept or change each one. At the end, persist each value with
`python3 scripts/manage_config.py set <key> <value>` (it validates and writes to the
active profile in `config.json`; pass `--profile <name>` if editing a non-active
profile), then confirm. Do **not** proceed to card generation.

Steps to ask in config mode:
1. Deck type
2. Court lettering system
3. Visual style / pattern
4. Card decoration layers, mood, and theme (Step 5a)
5. Face style for the court figure (Step 5b's `face_style.court` question)
6. Aspect ratio
7. Image generator (optional — see Step 9)
8. (Optional, only if user asks) Index settings, or per-layer overrides via
   `layers.<layer>.<group>` for Court/Pip/Ace (e.g. `layers.ornaments.ace`,
   `layers.figure.pip`, `layers.mood.court`)

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
  straight to per-card steps (rank → suit → court details if applicable). Mention the
  user can run `--config` to change settings or switch profiles.
- **No config found** → run the full wizard (all steps), then offer to save the
  persistent settings to the active (`default`) profile in `config.json` for next time.

---

## File map

Folders under `assets/`:
- `assets/decks/` — one file per deck system (suits + available ranks + default lettering)
- `assets/lettering/systems.md` — court-card index letters per region
- `assets/courts/` — `king.md` / `queen.md` / `jack.md`, auto-loaded by chosen rank
- `assets/pattern/` — one file per visual style; each holds a `[STYLE_BLOCK]` and marks
  its accent/figure-only lines for PIP/ACE resolution (see `references/REFERENCE.md`)
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
- `references/REFERENCE.md` — COURT / PIP / ACE templates, rank table, aspect ratios
- `references/CONFIG.md` — config schema, profiles, lookup order, field reference
- `references/example-court-king.md` — a fully assembled COURT example prompt for reference
- `references/example-pip-two.md` — a fully assembled PIP example prompt (plain default and decorated variant)

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
**Austrian (default) · French · English · Art Nouveau · Japanese (ukiyo-e)**, and note
they can request another style or era/cultural setting (e.g. "Art Deco", "Mexican
Loteria", "Egyptian").
Load the chosen `assets/pattern/<style>.md` and note its layer sections (Background,
Decor, Ornaments, Highlights, Center motif style, Finish). For a style not on disk,
improvise these sections following `assets/pattern/_adding-a-pattern.md`, then save
the improvised text (e.g. note it in the conversation) so later cards in the same deck
reuse identical wording — every card of the same group should resolve to the SAME
`[STYLE_BLOCK]` text verbatim so the whole deck looks like one consistent set.

### Step 5a — Card decoration, mood, and theme · _persistent_

_Skipped if loaded from config._ Every card is built from layers — background, decor
(background pattern/accents), ornaments, highlights/overlays, frame, figure, and mood,
plus the structural index and center-motif layers that are always present (see "Layers
and `[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`). Defaults reproduce the
traditional look: Court gets every layer including a figure; Ace gets every layer
except figure; plain Pip cards get only background + center motif + finish, no figure.
Ask these here:

1. **Number cards (2–10)** — how should they look:
   - **Plain (default)** — large suit-color pip symbols only: no extra decor, no
     ornaments, no border. Sets `layers.decor.pip = false`,
     `layers.ornaments.pip = false`, `layers.frame.pip = false`.
   - **Decorated** — keeps the style's decor accents and adds ornaments plus a
     border. Sets `layers.decor.pip = true`, `layers.ornaments.pip = true`,
     `layers.frame.pip = true`, then ask, free text, what extra ornament to add (e.g.
     "small corner flourishes", "ornamental pip surrounds") and save it as
     `ornaments_extra.pip`.

2. **Highlights / overlays (optional, all cards)** — ask, free text, whether to add
   any gilding, lacquer, glow, or shine accents (e.g. "gold leaf highlights along the
   raised linework"). If the user gives a description, save it to
   `highlights_extra.court`, `highlights_extra.pip`, and `highlights_extra.ace`, and
   set `layers.highlights.<group> = true` for all three groups. If skipped, leave the
   highlights layer off everywhere (the default).

3. **Mood / atmosphere (optional, deck-wide)** — ask, free text, for the deck's
   overall atmosphere (e.g. "gothic and brooding", "warm and whimsical", "eerie
   nocturnal"). If given, save it verbatim as the `mood` setting — it becomes
   `[MOOD_LINE]`, appended on every card group where `layers.mood.<group>` is true
   (all groups, by default). If skipped, leave `mood` empty (no line is added).

4. **Theme / symbolism (optional, deck-wide)** — ask, free text, for an overarching
   concept tying the deck together (e.g. "celestial mythology", "botanical garden",
   "clockwork/steampunk"). If given, save it as the `theme` setting — when an
   ornaments/highlights layer is on for a group but that group's
   `ornaments_extra`/`highlights_extra` is empty, derive a short thematic phrase from
   `theme` to fill it (see "Theme-derived ornaments/highlights" in
   `references/REFERENCE.md`); explicit `ornaments_extra`/`highlights_extra` values
   always win. If skipped, leave `theme` empty.

Court cards keep every other layer on by default (`layers.<layer>.court` all `true`
except highlights), and Ace keeps every layer on except `figure` and `highlights` —
not asked in the wizard, but tunable per layer via `python3 scripts/manage_config.py
set layers.<layer>.<group> false/true` (e.g. `layers.ornaments.ace false` for a
plainer Ace, `layers.decor.court false` for a stripped-down court, or
`layers.figure.pip true` for a transformation-style deck where number cards carry
small figures).

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

**Face style (persistent, asked once).** _Skipped if loaded from config._ Ask how the
court figure's face should read:
- **Individual (default)** — a normal individualized portrait; no extra line added.
- **Archetypal** — symmetrical, mask-like, idealized — no individual expression.
- **Expressive** — naturalistic, emotionally expressive features.
- **Faceless** — face obscured or abstracted entirely; drop facial description from
  `[CHARACTER_FEATURES]` too.

Save as `face_style.court`. This becomes `[FACE_STYLE_LINE]` (see "Figure & face style
resolution" in `references/REFERENCE.md`); `individual` adds no line. (`face_style.pip`
/ `face_style.ace` only matter if `layers.figure.pip`/`.ace` is turned on for a
transformation-style deck — set those via `--config` if needed, not asked here.)

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
4. Resolve `[STYLE_BLOCK]`, `[FRAME_LINE]`, and `[FACE_STYLE_LINE]` for this card's
   group (court/pip/ace) per "Layers and `[STYLE_BLOCK]` assembly" and "Figure & face
   style resolution" in `references/REFERENCE.md`, using the `layers.*`,
   `ornaments_extra.*`, `highlights_extra.*`, `mood`, `theme`, and `face_style.*`
   settings (deriving thematic ornaments/highlights per "Theme-derived
   ornaments/highlights" where applicable). Splice the result **in full** — never
   summarize, reorder, or drop a line from an enabled layer. When generating multiple
   cards for the same deck, reuse the exact same resolved `[STYLE_BLOCK]`/
   `[FRAME_LINE]`/`[FACE_STYLE_LINE]`/derived theme phrases for every card of the same
   group so the set stays visually consistent.
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
- [ ] **Style block integrity** — `[STYLE_BLOCK]` follows "Layers and `[STYLE_BLOCK]`
  assembly" in `references/REFERENCE.md` for this card's group: background/decor/
  ornaments/highlights lines appear only when `layers.<layer>.<group>` is `true` (with
  `ornaments_extra`/`highlights_extra` appended when their layer is on), followed by
  the center-motif style (figure-only line included only if `layers.figure.<group>` is
  `true`) and finish lines, then `[MOOD_LINE]` if applicable, and the `plain card face,
  no additional ornament beyond the pip symbols,` fallback is present for PIP when
  decor, ornaments, and highlights are all off. Nothing from an enabled layer is
  summarized, reordered, or dropped. The resolved text is identical across all cards
  of the same group generated for the same deck/session.
- [ ] **Frame line** — `[FRAME_LINE]` (`thin single black border with stepped corner
  cut-ins framing the index areas,`) is present only if `layers.frame.<group>` is
  `true` for this card's group; otherwise the line is absent entirely (not an empty
  placeholder).
- [ ] **Mood line** — `[MOOD_LINE]` is present only if `layers.mood.<group>` is `true`
  for this card's group AND `mood` is non-empty, and its text matches the `mood`
  setting verbatim; otherwise the line is absent entirely.
- [ ] **Face style line** — `[FACE_STYLE_LINE]` is present only if
  `layers.figure.<group>` is `true` AND `face_style.<group>` is not `individual`, and
  its text matches the table in "Figure & face style resolution"
  (`references/REFERENCE.md`); for `face_style.court = faceless`,
  `[CHARACTER_FEATURES]` contains no facial description. Otherwise the line is absent
  entirely.
- [ ] **Theme-derived ornaments/highlights** — if `theme` is set and an
  `ornaments_extra`/`highlights_extra` slot was empty for an enabled layer, the derived
  phrase reflects `theme` and is reused identically across all cards of the same
  group/deck; an explicit `ornaments_extra`/`highlights_extra` value was never
  overridden by a derived one.
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
