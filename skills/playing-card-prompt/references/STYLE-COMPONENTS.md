# Style Component Coverage

A stylized playing-card deck is defined by a set of style components — medium,
palette, era, mood, and so on. This table maps each component to the config
field / layer / template mechanism that addresses it, so coverage is as explicit
as the layer matrix in `references/REFERENCE.md`.

Card-back design is covered by the `back` card group (rank = Back), added in v3.22.0.
Back cards share all style layers (background, decor, ornaments, mood, technique, frame)
with front-facing cards and are assembled using the same STYLE_BLOCK mechanism.

Special/prospect cards are covered by the `special` card group (rank = Special), which
runs Steps S1-S5 instead of Steps 4.1-4.2 (Step 4 Suit is skipped). Special card types
come from `assets/special/*.md` (e.g. `marketing.md`, `prospect.md`; `_*` files excluded)
via Step S2, addressing #5 Composition/rhythm. The figure block (Steps 8a-12) is skipped
for `special` unless `layers.figure.special` is explicitly set to a non-`"false"` type
value (default `"false"`); when opted in, Steps S3/S4 feed #9 Poses/gestures and #10
Costume/accessories, with Step S4 (named figure) running only for prospect-type special
cards. Like all groups, `special` still enters the mood check (Step 7) and the aspect-ratio
/ generator steps (Steps 13-14), and is assembled using the same STYLE_BLOCK mechanism.

| #  | Component | Status | Mechanism |
|----|-----------|--------|-----------|
| 1  | Medium / technique | Covered | `style` pattern choice → "Technique" + Finish sections of `assets/pattern/<style>.md`, gated by `layers.technique.<group>` |
| 2  | Color palette | Covered | `style` pattern choice → Background/Decor sections, gated by `layers.background.<group>` / `layers.decor.<group>` |
| 3  | Era / cultural context | Covered | `style` pattern presets (austrian, french, english, art-nouveau, japanese), each grounded in an era/culture per `assets/pattern/_adding-a-pattern.md` |
| 4  | Mood / atmosphere | Covered | `mood` (preset from `assets/mood/`, picked or custom in Step 7) → `[MOOD_LINE]`, gated per group by `layers.mood.<group>` (also set in Step 7); a custom-text `layers.mood.<group>` cell adds a config-only per-group addition |
| 5  | Composition / rhythm | Partial | Figure framing/cropping covered via `character_framing` (Step 8e, `assets/character-framing/`, character-type figures only) and `figure_scale` (Step 8a, deck-wide, all figure types — `full-bleed`/`inscribed-in-frame`/`small-centered`/`cross-a-frame` resolve via file-lookup to the matching `assets/figure-scale/<value>.md` phrase, with custom free text used verbatim), both folded into `[STYLE_BLOCK]` when `layers.figure.<group>` is non-`"false"`. Split layout covered via `layers.split.<group>` (Step 8b, `assets/split/`, per-group, all figure types). Seamless/connecting design across cards covered via `layers.seamless.<group>` (Seamless step, per-group, all groups) — named aliases resolve via file-lookup to `assets/seamless/<alias>.md`'s phrase (e.g. `continuous-border`, `interlocking-motif`), custom free text used verbatim. Title placement covered via the per-card Title step (Step T, all six groups) — title text and a placement alias (e.g. `below-figure`, `side-running`, from `assets/title/`) are collected fresh each card, with a group-aware suggested default (Joker → `below-figure`, Court → `side-running`, pip/ace/back/special → none suggested); gated by `structure` (skipped entirely under `illustration`, TITL-05); never persisted to `config.json`. Beyond that, still indirect via `layers.<layer>.<group>` on/off toggles (decor/ornaments/frame density) and `index.layout`; no dedicated "rhythm" control independent of the chosen pattern |
| 6  | Line character / rendering | Covered | `style` pattern choice → "Technique" linework descriptors, gated by `layers.technique.<group>` |
| 7  | Degree of stylization | Partial | Fixed by the `style` choice (e.g. chromolithographic vs. ukiyo-e), including each pattern's Figure detail and Face Style sections for figures; no standalone realistic↔abstract dial |
| 8  | Figure proportions / plasticity | Not covered | No field or template slot addresses body proportions/anatomical exaggeration (distinct from `character_framing`/`figure_scale`, which address framing/cropping, see #5); open gap, not prioritized in this round |
| 9  | Poses / gestures | Covered (court) / Partial (pip, ace) | COURT: traditional attributes (`assets/courts/<rank>.md`) + Step 10 + Step 11, merged into `[RESOLVED_ATTRIBUTES]`. PIP/ACE figures (`layers.figure.<group> = true`) have no templated pose slot |
| 10 | Costume / accessories | Covered (court) / N/A (pip, ace) | Same merge pipeline as #9, court-only |
| 11 | Typage / facial expression | Covered | `style` pattern's "Figure detail" and "Face Style" sections, folded into `[STYLE_BLOCK]`, gated by `layers.figure.<group>` |
| 12 | Pip / suit symbol design | Partial | Symbol/color/shape fixed per `assets/decks/<deck>.md`; pip layout fixed in the PIP template; rendering follows the pattern's Technique section (when `layers.technique.<group>` is on) but there's no field for alternative pip iconography |
| 13 | Typography / indices | Covered | `index.*` (`assets/index/options.md`) → `[INDEX_LINE]`; `lettering` system for rank letters |
| 14 | Decoration / ornamentation | Covered | `layers.ornaments.<group>` / `layers.highlights.<group>` / `layers.frame.<group>` (also `background`/`decor`) — each cell both toggles the layer and, as custom text, supplies that group's addition — with theme-derived fallback for ornaments/highlights/frame; `frame` selects the border preset from `assets/frame/` |
| 15 | Deck-wide theme / symbolism | Covered | `theme` (deck-wide free text) → theme-derived ornaments/highlights; also informs Step 10 character concept suggestions for cards with a figure |

## Technique vs. Functions

Within `assets/pattern/<style>.md`, "Technique"/"Finish" (#1/#6 above) and the
content layers (Decor, Ornaments, Highlights — #14) answer different questions:

- **Technique & Finish** — *how* the card is rendered, sharing a single gate
  (`layers.technique.<group>`): Technique is the medium/linework applied to whatever
  sits in the center (portrait, pip layout, or suit symbol alike), regardless of
  whether that center motif is a figure (`layers.figure.<group>`); Finish is the
  print-quality/final-rendering descriptor for the whole card. Turning
  `layers.technique.<group>` off drops both together (e.g. an unstyled pip face with
  no medium or print-quality descriptor at all).
- **Decor / Ornaments / Highlights** — *what* is added and *where*: extra background
  pattern, vignettes/flourishes, shine/gilding accents — content placed on the card,
  each gated by its own `layers.<layer>.<group>` cell.

When adding or editing a pattern (`assets/pattern/_adding-a-pattern.md`), keep
Technique/Finish-flavored phrasing (medium/linework/rendering/print-quality) out of
Decor/Ornaments/Highlights and vice versa — each section should answer only its own
question.

## Open gaps

- **#8 Figure proportions / plasticity** (anatomical body proportions/exaggeration —
  NOT figure framing/cropping, which is covered by `character_framing`/`figure_scale`, #5) and the
  **partial** items above (#5's remaining non-framing aspects, #7, #9 for pip/ace, #12)
  are known gaps, not yet addressed. They're recorded here so future work can pick them
  up without re-auditing the whole skill.
