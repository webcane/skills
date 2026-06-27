# Wizard Step Map

## Wizard steps: components × layers × placeholders × assets

Maps each wizard step (see `SKILL.md`) to the style components from
`STYLE-COMPONENTS.md` (by number), the `layers.*` it configures (see
`REFERENCE.md`), the prompt placeholders it feeds, and the `assets/` files it
loads.

| # | Step | Components (STYLE-COMPONENTS.md) | Layers (`layers.*`) | Placeholders | Assets |
|---|---|---|---|---|---|
| **1** | Deck type | #12 Pip/suit symbol design (deck's suits) | — | — (loads the suit/rank table) | `assets/decks/<deck>.md` |
| **1b** | Structure *(full vs. illustration-only, persistent)* | — *(structural — gates index/frame/title/seamless deck-wide)* | — | — (no placeholder of its own; gates `[INDEX_LINE]`/`[FRAME_LINE]`/title/seamless downstream) | — |
| **2** | Court lettering | #13 Typography / indices | Index *(structural — rank letters)* | `RANK_LETTER` (for court/ace) | `assets/lettering/systems.md` |
| **3** | Rank | — *(template choice, not a style component)* | Center motif *(structural — selects COURT/PIP/ACE/JOKER)*; sets this card's group (`court`/`pip`/`ace`/`joker`), which determines the `layers.figure.<group>` default checked after Step 7 | `RANK_NAME`, `RANK_LETTER` | `references/REFERENCE.md` (rank table), `assets/courts/<rank>.md` if court or joker |
| **4** | Suit *(skipped for Joker)* | #12 Pip/suit symbol design | Center motif *(structural)* | `SUIT_NAME_TITLE`, `SUIT_NAME`, `SUIT_SYMBOL`, `SUIT_COLOR` | `assets/decks/<deck>.md` |
| **4.1** | Joker role *(Joker only, per-card)* | #2 Color palette | Center motif *(structural)* | `JOKER_ROLE` | — |
| **4.2** | Joker index glyph *(Joker only, persistent)* | #13 Typography / indices | Index *(structural)* | `JOKER_INDEX` → feeds `[INDEX_LINE]` | — |
| **B1** | Back purpose *(Back only, per-card)* | #5 Composition/rhythm | — | contributes to `BACK_DESIGN` | `assets/back/purpose/<choice>.md` |
| **B2** | Back design category *(Back only, per-card)* | #5 Composition/rhythm | — | this card's category answer (filter for B3) | — |
| **B3** | Back pattern *(Back only, per-card)* | #5 Composition/rhythm, #14 Decoration | — | contributes to `BACK_DESIGN` | `assets/back/design/<back_design>/<choice>.md` |
| **B4** | Back palette *(Back only, per-card)* | #2 Color palette | — | contributes to `BACK_DESIGN` | `assets/back/palette/<choice>.md` |
| **B5** | Back symmetry *(Back only, per-card)* | #5 Composition/rhythm | — | feeds STYLE_BLOCK step 10 via this card's symmetry answer | `assets/back/symmetry/<choice>.md` |
| **B6** | Back frame *(Back only, persistent)* | — | Frame (`layers.frame.back`) | — (sets `layers.frame.back`) | — |
| **B7** | Back exclusions *(Back only, per-card, optional)* | — *(negative constraints)* | — | `NEGATIVE_LIST` | — |
| **S1** | Card title *(Special only, per-card)* | — *(structural)* | — | `CARD_NAME` | — |
| **S2** | Special card type *(Special only, per-card)* | #5 Composition/rhythm | — | `SPECIAL_TYPE_LINE` | `assets/special/*.md` (excluding `_*`) |
| **S3** | Visual content description *(Special only, per-card, optional for prospect)* | #9 Poses/gestures, #10 Costume/accessories | Center motif | `FIGURE_DESCRIPTION` (partial), `SPECIAL_ATTRIBUTES` | — |
| **S4** | Named figure *(Special+Prospect only, per-card)* | #9 Poses/gestures | Center motif | `FIGURE_DESCRIPTION` (named figure + S3 description) | `assets/special/prospect.md` (type line only; figure name is per-card user input) |
| **S5** | Special card exclusions *(Special only, per-card, optional)* | — *(negative constraints)* | — | `NEGATIVE_LIST` | — |
| **5** | Visual style/pattern | #1 Medium/technique, #2 Color palette, #3 Era/cultural context, #6 Line character, #7 Degree of stylization *(partial)*, #11 Typage/facial expression | Background, Decor, Ornaments, Highlights, Technique, Finish, Figure detail, Face Style — supplies the TEXT for all of them | feeds `[STYLE_BLOCK]` (layer text, incl. Technique and Finish — sharing one gate — when `layers.technique.<group>` is on, and Figure detail/Face Style when `layers.figure.<group>` is on) | `assets/pattern/<style>.md`, `assets/pattern/_adding-a-pattern.md` (if custom) |
| **6** | Card decoration & theme | #14 Decoration/ornamentation, #15 Deck-wide theme/symbolism, #5 Composition/rhythm *(partial)* | Decor.pip, Ornaments.pip, Frame.pip, Highlights.\* (each toggled and given a per-group addition via `layers.<layer>.<group>`, incl. theme-derived for ornaments/highlights/frame); `layers.background`/`layers.decor` additions (config-only) | feeds `[STYLE_BLOCK]` (layer additions), `[FRAME_LINE]` (preset text + `layers.frame.<group>`'s addition) | `assets/frame/<frame>.md`, `assets/frame/_adding-a-frame.md` (if custom), `references/REFERENCE.md` ("Theme-derived ornaments/highlights/frame") |
| **7** | Mood / atmosphere | #4 Mood/atmosphere | Mood.\* (per-group toggle via `layers.mood.<group>`); `mood` (preset or custom text); `layers.mood.<group>`'s addition (config-only per-group addition) | feeds `[STYLE_BLOCK]` (`[MOOD_LINE]` + per-group addition) | `assets/mood/<name>.md`, `assets/mood/_adding-a-mood.md` (if custom) |
| **8a** | Figure scale | #5 Composition/rhythm *(figure framing/cropping — scale)* | Figure *(deck-wide `figure_scale`)* | feeds `[STYLE_BLOCK]` (figure_scale phrase, appended after character framing / non-character figure-type text) | — *(config value phrase, no asset file lookup)* |
| **8b** | Split layout | #5 Composition/rhythm *(split compositional wrapper)* | Split *(per-group `layers.split.<group>`)* | feeds `[STYLE_BLOCK]` (split phrase as outer wrapper, appended after figure_scale) | `assets/split/horizontal-mirrored.md`, `assets/split/angled-mirrored.md` |
| **8c** | Figure type (`figure_type`) — gate for pattern Face Style folds into this step's own paragraph, no separate step | #5 Composition/rhythm *(figure classification)*, #11 Typage / facial expression *(character-only Face Style gate)*, #9 Poses/gestures *(partial — type preamble)* | Figure *(per-group `layers.figure.<group>` encoded value: `character`/`building`/`animal`/`custom`)* | feeds `[STYLE_BLOCK]` (figure-type preamble text; pattern's Face Style line and Figure detail when type is `character`, before character framing) | `assets/figure-type/<type>.md` (character.md, building.md, animal.md, custom.md), `assets/pattern/<style>.md` "Face Style" section |
| **8e** | Character framing *(character only)* | #5 Composition/rhythm *(character framing/cropping)* | Figure *(deck-wide `character_framing`, gated on `layers.figure.<group> = "character"`)* | feeds `[STYLE_BLOCK]` (character_framing phrase, appended after the pattern's Face Style line) | `assets/character-framing/<name>.md` |
| **8f** | Seamless design *(per-group)* | #5 Composition/rhythm *(seamless/connecting design across cards)* | Seamless *(per-group `layers.seamless.<group>`)* | feeds `[STYLE_BLOCK]` (seamless phrase, appended last in the figure block, after split) | `assets/seamless/continuous-border.md`, `assets/seamless/interlocking-motif.md` |
| **9** | Character / figure description | #9 Poses/gestures (figure cards), #10 Costume/accessories (figure cards) | Center motif (portrait) | `[CHARACTER_NAME]`, `[CHARACTER_FEATURES]` | — |
| **10** | Additional/replaced attributes | #9, #10 *(figure cards only)* | Center motif (figure cards) | contributes to `[RESOLVED_ATTRIBUTES]` | `assets/courts/<rank>.md` (shows traditional attrs, court only) |
| **11** | Transfer from reference image | #9, #10, #11 *(figure cards only)* | Center motif (figure cards), Figure | overrides `[RESOLVED_ATTRIBUTES]` | — |
| **12** | Exclude from reference image | — *(negative constraints, not a style component)* | — | `[NEGATIVE_LIST]` | — |
| **T** | Title overlay *(per-card, all six groups — not part of the figure block)* | #5 Composition/rhythm *(per-card title placement)* | — *(no layers.\* cell — title is per-card ephemeral, never persisted)* | feeds the title named element (no position/font/styling); per-card title text and placement alias are ephemeral, never saved | `assets/title/<alias>.md` (e.g. `below-figure`, `side-running`) — Joker suggests `below-figure`, Court suggests `side-running`, pip/ace/back/special suggest none |
| **13** | Aspect ratio | — *(format)* | — | `[ASPECT_RATIO]` | `references/REFERENCE.md` (aspect ratio table) |
| **14** | Image generator | — *(output post-processing)* | — *(touches all layers indirectly — reformatting)* | adapts `[NEGATIVE_LIST]`, `[ASPECT_RATIO]`, extra suffix params | `assets/engines/<engine>.md`, `assets/engines/_config.md` |

**Step 7 (Mood) always runs**, regardless of whether this card's group has a figure —
it's a persistent, deck-wide setting like Steps 1–2 and 5–6.

**Steps 8a–12 (the figure block) only run for a card whose group has
`layers.figure.<group>` set to a non-`"false"` value** (any of `character`,
`building`, `animal`, `custom`, or a custom free-text entry) — `court` and `joker`
default to `"character"`, or `pip`/`ace` can be enabled via `--config`. Otherwise
the wizard goes straight from Step 7 to Step 13. Step 8a (figure scale) is a
deck-wide persistent setting, skipped if `figure_scale` is already set in config.
Steps 8b (split layout) and 8c (figure type) are per-group persistent but always
run when this group's figure layer is active, since a stored `"true"` still defers
its concrete value to per-card resolution at these steps (UNIFY-01/02/03) — they
are not skipped just because the cell already holds a value. Step 8c's Face Style gate
(folded into 8c's own paragraph, no separate step) and Step 8e (character framing)
additionally require `layers.figure.<group> = "character"` — building/animal/custom
types skip both. Steps 9–12 are per-card.

**`structure` setting** (`full`/`illustration`, asked early as Step 1b — right after
Deck type — and config mode item 2, persistent, WIZ-03/D-12) — when `illustration`,
alters the opening line used in step 1's template, drops `[INDEX_LINE]` (step 2's
placeholder, normally fed by the "not covered" item below), drops `[FRAME_LINE]` (fed
by step 6) regardless of `layers.frame.<group>`, appends a fixed block to
`[NEGATIVE_LIST]` (step 12), and drops the Title step, the Split step, and the
Seamless step entirely — under `illustration`, the per-card Title step (T) is skipped
outright (never asked, not asked-then-discarded), the per-group Split step (8b) is
skipped the same way and the split phrase is not added to any STYLE_BLOCK regardless
of `layers.split.<group>`, and the seamless phrase is not added to any STYLE_BLOCK
regardless of `layers.seamless.<group>` (TITL-05/SEAM-05, one shared structure==
illustration gate that Split now also follows). Asking this early means its
downstream consequences are explained once at Step 1b;
later steps (the figure-check, Step 8b, Step 8f, Step T, and assembly) simply refer
back to "the structure setting chosen earlier." See "`structure` setting" in
`REFERENCE.md`. All other steps/components are unaffected.

**Not covered by a dedicated step (silent / assembly-only):**
- **`[INDEX_LINE]`** — assembled from `assets/index/options.md` via silent defaults in Assembling step 2; not asked in the wizard.
- **Figure detail & Face Style** — folded into `[STYLE_BLOCK]` automatically from the chosen pattern when `layers.figure.<group>` is on; no separate wizard question or config field.
- **`layers.technique.<group>`** — on for every group by default, contributing the chosen pattern's "Technique" AND "Finish" sections (one shared gate) to `[STYLE_BLOCK]`; toggling it off per group, or setting a per-group addition (Technique only — Finish has no separate addition slot), is config-only (like `layers.background`/`layers.decor` additions), not asked in the wizard.
- **#8 Figure proportions/plasticity** (anatomical body proportions/exaggeration — distinct from the figure block's figure *framing/cropping*, see Steps 8a/8e), **#7/#9(pip,ace)/#12** — open "Partial/Not covered" gaps from STYLE-COMPONENTS.md, not addressed by any step.
- **Turning on figure for pip/ace** (`layers.figure.pip`/`.ace`) — only available via `--config`; once on, the figure block (Steps 8–12) runs for that group like court.
- **Back symmetry line** — the "Symmetry line" from `assets/back/symmetry/<back_symmetry>.md` is appended to `[STYLE_BLOCK]` automatically for the `back` group (step 10 in "Resolving `[STYLE_BLOCK]`" in `REFERENCE.md`); chosen via Step B5 (persistent).

**Joker rank group** (`rank = Joker`): Steps 4.1–4.2 (role, index placement + symbol) are documented in references/JOKER-WIZARD.md.

**Back rank group** (`rank = Back`): Steps B1–B7 run instead of Steps 4.1–4.2. B1–B5 are per-card ephemeral (asked fresh every Back card, never persisted); B6 (frame) sets the persistent `layers.frame.back` cell; B7 exclusions are per-card. Steps 4 (Suit) and 8a–12 (figure block) are skipped unless `layers.figure.back` is explicitly set to a non-false type value in config. The `back` group enters the mood check (Step 7) and the aspect ratio / generator steps (Steps 13–14) like all other groups.

**Special rank group** (`rank = Special`): Steps S1–S5 run instead of Steps 4.1–4.2 (and Step 4 suit is skipped). Steps 8a–12 (figure block) are skipped unless `layers.figure.special` is explicitly set to a non-false type value. The `special` group enters the mood check (Step 7) and the aspect ratio / generator steps (Steps 13–14) like all other groups. Step S4 (named figure) only runs for prospect-type special cards.
