# Style Component Coverage

A stylized playing-card deck is defined by a set of style components — medium,
palette, era, mood, and so on. This table maps each component to the config
field / layer / template mechanism that addresses it, so coverage is as explicit
as the layer matrix in `references/REFERENCE.md`.

**Card-back design is intentionally excluded** — it will be implemented as a
separate card type alongside `court` / `pip` / `ace`, not as a style component of
the front-facing cards covered here.

| #  | Component | Status | Mechanism |
|----|-----------|--------|-----------|
| 1  | Medium / technique | Covered | `style` pattern choice → "Center motif style" + Finish sections of `assets/pattern/<style>.md` |
| 2  | Color palette | Covered | `style` pattern choice → Background/Decor sections, gated by `layers.background.<group>` / `layers.decor.<group>` |
| 3  | Era / cultural context | Covered | `style` pattern presets (austrian, french, english, art-nouveau, japanese), each grounded in an era/culture per `assets/pattern/_adding-a-pattern.md` |
| 4  | Mood / atmosphere | Covered | `mood` (preset from `assets/mood/`, picked or custom in Step 7) → `[MOOD_LINE]`, gated per group by `layers.mood.<group>` (also set in Step 7); a custom-text `layers.mood.<group>` cell adds a config-only per-group addition |
| 5  | Composition / rhythm | Partial | Figure framing/cropping covered via `figure_proportion` (Step 8, `assets/figure-proportion/`), folded into `[STYLE_BLOCK]` when `layers.figure.<group>` is on. Beyond that, still indirect via `layers.<layer>.<group>` on/off toggles (decor/ornaments/frame density) and `index.layout`; no dedicated "rhythm" control independent of the chosen pattern |
| 6  | Line character / rendering | Covered | `style` pattern choice → "Center motif style" linework descriptors |
| 7  | Degree of stylization | Partial | Fixed by the `style` choice (e.g. chromolithographic vs. ukiyo-e), including each pattern's Face Style line for figures; no standalone realistic↔abstract dial |
| 8  | Figure proportions / plasticity | Not covered | No field or template slot addresses body proportions/anatomical exaggeration (distinct from `figure_proportion`, which addresses framing/cropping, see #5); open gap, not prioritized in this round |
| 9  | Poses / gestures | Covered (court) / Partial (pip, ace) | COURT: traditional attributes (`assets/courts/<rank>.md`) + Step 10 + Step 11, merged into `[RESOLVED_ATTRIBUTES]`. PIP/ACE figures (`layers.figure.<group> = true`) have no templated pose slot |
| 10 | Costume / accessories | Covered (court) / N/A (pip, ace) | Same merge pipeline as #9, court-only |
| 11 | Typage / facial expression | Covered | `style` pattern's "Face Style" section, folded into `[STYLE_BLOCK]`, gated by `layers.figure.<group>` |
| 12 | Pip / suit symbol design | Partial | Symbol/color/shape fixed per `assets/decks/<deck>.md`; pip layout fixed in the PIP template; rendering follows the pattern's Center motif style but there's no field for alternative pip iconography |
| 13 | Typography / indices | Covered | `index.*` (`assets/index/options.md`) → `[INDEX_LINE]`; `lettering` system for rank letters |
| 14 | Decoration / ornamentation | Covered | `layers.ornaments.<group>` / `layers.highlights.<group>` / `layers.frame.<group>` (also `background`/`decor`) — each cell both toggles the layer and, as custom text, supplies that group's addition — with theme-derived fallback for ornaments/highlights/frame; `frame` selects the border preset from `assets/frame/` |
| 15 | Deck-wide theme / symbolism | Covered | `theme` (deck-wide free text) → theme-derived ornaments/highlights; also informs Step 10 character concept suggestions for cards with a figure |

## Open gaps

- **#8 Figure proportions / plasticity** (anatomical body proportions/exaggeration —
  NOT figure framing/cropping, which is covered by `figure_proportion`, #5) and the
  **partial** items above (#5's remaining non-framing aspects, #7, #9 for pip/ace, #12)
  are known gaps, not yet addressed. They're recorded here so future work can pick them
  up without re-auditing the whole skill.
