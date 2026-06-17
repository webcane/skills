# Wizard Step Map

## Wizard steps: components × layers × placeholders × assets

Maps each wizard step (see `SKILL.md`) to the style components from
`STYLE-COMPONENTS.md` (by number), the `layers.*` it configures (see
`REFERENCE.md`), the prompt placeholders it feeds, and the `assets/` files it
loads.

| # | Step | Components (STYLE-COMPONENTS.md) | Layers (`layers.*`) | Placeholders | Assets |
|---|---|---|---|---|---|
| **1** | Deck type | #12 Pip/suit symbol design (deck's suits) | — | — (loads the suit/rank table) | `assets/decks/<deck>.md` |
| **2** | Court lettering | #13 Typography / indices | Index *(structural — rank letters)* | `RANK_LETTER` (for court/ace) | `assets/lettering/systems.md` |
| **3** | Rank | — *(template choice, not a style component)* | Center motif *(structural — selects COURT/PIP/ACE/JOKER)*; sets this card's group (`court`/`pip`/`ace`/`joker`), which determines the `layers.figure.<group>` default checked after Step 7 | `RANK_NAME`, `RANK_LETTER` | `references/REFERENCE.md` (rank table), `assets/courts/<rank>.md` if court or joker |
| **4** | Suit *(skipped for Joker)* | #12 Pip/suit symbol design | Center motif *(structural)* | `SUIT_NAME_TITLE`, `SUIT_NAME`, `SUIT_SYMBOL`, `SUIT_COLOR` | `assets/decks/<deck>.md` |
| **4.1** | Joker role *(Joker only, per-card)* | #2 Color palette | Center motif *(structural)* | `JOKER_ROLE` | — |
| **4.2** | Joker index glyph *(Joker only, persistent)* | #13 Typography / indices | Index *(structural)* | `JOKER_INDEX` → feeds `[INDEX_LINE]` | — |
| **B1** | Back design path *(Back only, per-card)* | #2 Color palette, #5 Composition/rhythm | — *(design description collected, not a layer toggle)* | `BACK_DESIGN` | — *(suggested: derived from active style+mood; freeform: user text; ref-image: user source + modifications)* |
| **B2** | Suggested back refinement *(Back only, suggested path only, per-card)* | #2 Color palette, #5 Composition/rhythm | — | `BACK_DESIGN` (confirmed or replaced) | — |
| **B3** | Back card exclusions *(Back only, per-card, optional)* | — *(negative constraints)* | — | `NEGATIVE_LIST` | — |
| **5** | Visual style/pattern | #1 Medium/technique, #2 Color palette, #3 Era/cultural context, #6 Line character, #7 Degree of stylization *(partial)*, #11 Typage/facial expression | Background, Decor, Ornaments, Highlights, Technique, Finish, Figure detail, Face Style — supplies the TEXT for all of them | feeds `[STYLE_BLOCK]` (layer text, incl. Technique and Finish — sharing one gate — when `layers.technique.<group>` is on, and Figure detail/Face Style when `layers.figure.<group>` is on) | `assets/pattern/<style>.md`, `assets/pattern/_adding-a-pattern.md` (if custom) |
| **6** | Card decoration & theme | #14 Decoration/ornamentation, #15 Deck-wide theme/symbolism, #5 Composition/rhythm *(partial)* | Decor.pip, Ornaments.pip, Frame.pip, Highlights.\* (each toggled and given a per-group addition via `layers.<layer>.<group>`, incl. theme-derived for ornaments/highlights/frame); `layers.background`/`layers.decor` additions (config-only) | feeds `[STYLE_BLOCK]` (layer additions), `[FRAME_LINE]` (preset text + `layers.frame.<group>`'s addition) | `assets/frame/<frame>.md`, `assets/frame/_adding-a-frame.md` (if custom), `references/REFERENCE.md` ("Theme-derived ornaments/highlights/frame") |
| **7** | Mood / atmosphere | #4 Mood/atmosphere | Mood.\* (per-group toggle via `layers.mood.<group>`); `mood` (preset or custom text); `layers.mood.<group>`'s addition (config-only per-group addition) | feeds `[STYLE_BLOCK]` (`[MOOD_LINE]` + per-group addition) | `assets/mood/<name>.md`, `assets/mood/_adding-a-mood.md` (if custom) |
| **8a** | Figure scale | #5 Composition/rhythm *(figure framing/cropping — scale)* | Figure *(deck-wide `figure_scale`)* | feeds `[STYLE_BLOCK]` (figure_scale phrase, appended after character framing / non-character figure-type text) | — *(config value phrase, no asset file lookup)* |
| **8b** | Split layout | #5 Composition/rhythm *(split compositional wrapper)* | Split *(per-group `layers.split.<group>`)* | feeds `[STYLE_BLOCK]` (split phrase as outer wrapper, appended after figure_scale) | `assets/split/horizontal-mirrored.md`, `assets/split/angled-mirrored.md` |
| **8c** | Figure type (`figure_type`) | #5 Composition/rhythm *(figure classification)*, #9 Poses/gestures *(partial — type preamble)* | Figure *(per-group `layers.figure.<group>` encoded value: `character`/`building`/`animal`/`custom`)* | feeds `[STYLE_BLOCK]` (figure-type preamble text, before face style / character framing) | `assets/figure-type/<type>.md` (character.md, building.md, animal.md, custom.md) |
| **8d** | Face style gate *(character only)* | #11 Typage / facial expression, #7 Degree of stylization *(partial)* | Figure *(pattern face style, gated on `layers.figure.<group> = "character"`)* | feeds `[STYLE_BLOCK]` (pattern's Face Style line and Figure detail — same gate as existing, now narrowed to character type) | `assets/pattern/<style>.md` "Face Style" section |
| **8e** | Character framing *(character only)* | #5 Composition/rhythm *(character framing/cropping)* | Figure *(deck-wide `character_framing`, gated on `layers.figure.<group> = "character"`)* | feeds `[STYLE_BLOCK]` (character_framing phrase, appended after Face Style/`layers.figure.<group>`'s addition) | `assets/character-framing/<name>.md` |
| **9** | Character / figure description | #9 Poses/gestures (figure cards), #10 Costume/accessories (figure cards) | Center motif (portrait) | `[CHARACTER_NAME]`, `[CHARACTER_FEATURES]` | — |
| **10** | Additional/replaced attributes | #9, #10 *(figure cards only)* | Center motif (figure cards) | contributes to `[RESOLVED_ATTRIBUTES]` | `assets/courts/<rank>.md` (shows traditional attrs, court only) |
| **11** | Transfer from reference image | #9, #10, #11 *(figure cards only)* | Center motif (figure cards), Figure | overrides `[RESOLVED_ATTRIBUTES]` | — |
| **12** | Exclude from reference image | — *(negative constraints, not a style component)* | — | `[NEGATIVE_LIST]` | — |
| **13** | Aspect ratio | — *(format)* | — | `[ASPECT_RATIO]` | `references/REFERENCE.md` (aspect ratio table) |
| **14** | Image generator | — *(output post-processing)* | — *(touches all layers indirectly — reformatting)* | adapts `[NEGATIVE_LIST]`, `[ASPECT_RATIO]`, extra suffix params | `assets/engines/<engine>.md`, `assets/engines/_config.md` |

**Step 7 (Mood) always runs**, regardless of whether this card's group has a figure —
it's a persistent, deck-wide setting like Steps 1–2 and 5–6.

**Steps 8a–12 (the figure block) only run for a card whose group has
`layers.figure.<group>` set to a non-`"false"` value** (any of `character`,
`building`, `animal`, `custom`, or a custom free-text entry) — `court` and `joker`
default to `"character"`, or `pip`/`ace` can be enabled via `--config`. Otherwise
the wizard goes straight from Step 7 to Step 13. Steps 8a–8c are persistent
(asked once per group, skipped if already set in config). Step 8d (Face Style gate)
and Step 8e (character framing) additionally require `layers.figure.<group> =
"character"` — building/animal/custom types skip both. Steps 9–12 are per-card.

**`structure` setting** (`full`/`illustration`, config mode item 9, persistent) — when
`illustration`, alters the opening line used in step 1's template, drops
`[INDEX_LINE]` (step 2's placeholder, normally fed by the "not covered" item below),
drops `[FRAME_LINE]` (fed by step 6) regardless of `layers.frame.<group>`, and appends
a fixed block to `[NEGATIVE_LIST]` (step 12). See "`structure` setting" in
`REFERENCE.md`. All other steps/components are unaffected.

**Not covered by a dedicated step (silent / assembly-only):**
- **`[INDEX_LINE]`** — assembled from `assets/index/options.md` via silent defaults in Assembling step 2; not asked in the wizard.
- **Figure detail & Face Style** — folded into `[STYLE_BLOCK]` automatically from the chosen pattern when `layers.figure.<group>` is on; no separate wizard question or config field.
- **`layers.technique.<group>`** — on for every group by default, contributing the chosen pattern's "Technique" AND "Finish" sections (one shared gate) to `[STYLE_BLOCK]`; toggling it off per group, or setting a per-group addition (Technique only — Finish has no separate addition slot), is config-only (like `layers.background`/`layers.decor` additions), not asked in the wizard.
- **#8 Figure proportions/plasticity** (anatomical body proportions/exaggeration — distinct from the figure block's figure *framing/cropping*, see Steps 8a/8e), **#7/#9(pip,ace)/#12** — open "Partial/Not covered" gaps from STYLE-COMPONENTS.md, not addressed by any step.
- **Turning on figure for pip/ace** (`layers.figure.pip`/`.ace`) — only available via `--config`; once on, the figure block (Steps 8–12) runs for that group like court.
- **Back symmetry line** — the "Symmetry line" from `assets/back/symmetry.md` is appended to `[STYLE_BLOCK]` automatically for the `back` group (step 10 in "Resolving `[STYLE_BLOCK]`" in `REFERENCE.md`); no wizard question.

**Back rank group** (`rank = Back`): Steps B1–B3 run instead of Steps 4.1–4.2. Steps 4 (Suit), 8a–12 (figure block) are skipped unless `layers.figure.back` is explicitly set to a non-false type value in config. The `back` group enters the mood check (Step 7) and the aspect ratio / generator steps (Steps 13–14) like all other groups.
