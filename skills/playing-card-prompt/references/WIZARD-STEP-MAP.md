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
| **3** | Rank | — *(template choice, not a style component)* | Center motif *(structural — selects COURT/PIP/ACE)*; sets this card's group (`court`/`pip`/`ace`), which determines the `layers.figure.<group>` default checked after Step 6 | `RANK_NAME`, `RANK_LETTER` | `references/REFERENCE.md` (rank table), `assets/courts/<rank>.md` if court |
| **4** | Suit | #12 Pip/suit symbol design | Center motif *(structural)* | `SUIT_NAME_TITLE`, `SUIT_NAME`, `SUIT_SYMBOL`, `SUIT_COLOR` | `assets/decks/<deck>.md` |
| **5** | Visual style/pattern | #1 Medium/technique, #2 Color palette, #3 Era/cultural context, #6 Line character, #7 Degree of stylization *(partial)*, #11 Typage/facial expression | Background, Decor, Ornaments, Highlights, Center motif style, Face Style, Finish — supplies the TEXT for all of them | feeds `[STYLE_BLOCK]` (layer text, incl. Face Style when `layers.figure.<group>` is on) | `assets/pattern/<style>.md`, `assets/pattern/_adding-a-pattern.md` (if custom) |
| **6** | Card decoration, mood, theme | #4 Mood/atmosphere, #14 Decoration/ornamentation, #15 Deck-wide theme/symbolism, #5 Composition/rhythm *(partial)* | Decor.pip, Ornaments.pip, Frame.pip (toggle); Highlights.\* (+extra); Mood.\*; `ornaments_extra`/`highlights_extra` (incl. theme-derived) | feeds `[STYLE_BLOCK]` (extra phrases, `[MOOD_LINE]`), `[FRAME_LINE]` (pip) | `references/REFERENCE.md` ("Theme-derived ornaments/highlights") |
| **7** | Character / figure description | #9 Poses/gestures (figure cards), #10 Costume/accessories (figure cards) | Center motif (portrait) | `[CHARACTER_NAME]`, `[CHARACTER_FEATURES]` | — |
| **8** | Additional/replaced attributes | #9, #10 *(figure cards only)* | Center motif (figure cards) | contributes to `[RESOLVED_ATTRIBUTES]` | `assets/courts/<rank>.md` (shows traditional attrs, court only) |
| **9** | Transfer from reference image | #9, #10, #11 *(figure cards only)* | Center motif (figure cards), Figure | overrides `[RESOLVED_ATTRIBUTES]` | — |
| **10** | Exclude from reference image | — *(negative constraints, not a style component)* | — | `[NEGATIVE_LIST]` | — |
| **11** | Aspect ratio | — *(format)* | — | `[ASPECT_RATIO]` | `references/REFERENCE.md` (aspect ratio table) |
| **12** | Image generator | — *(output post-processing)* | — *(touches all layers indirectly — reformatting)* | adapts `[NEGATIVE_LIST]`, `[ASPECT_RATIO]`, extra suffix params | `assets/engines/<engine>.md`, `assets/engines/_config.md` |

**Steps 7–10 (the figure block) only run for a card whose group has
`layers.figure.<group> = true`** — `court` by default, or `pip`/`ace` for
transformation-style decks where `layers.figure.pip`/`.ace` was turned on via
`--config`. Otherwise the wizard goes straight from Step 6 to Step 11.

**Not covered by a dedicated step (silent / assembly-only):**
- **`[INDEX_LINE]`** — assembled from `assets/index/options.md` via silent defaults in Assembling step 2; not asked in the wizard.
- **Face Style** — folded into `[STYLE_BLOCK]` automatically from the chosen pattern when `layers.figure.<group>` is on; no separate wizard question or config field.
- **#8 Figure proportions/plasticity**, **#5/#7/#9(pip,ace)/#12** — open "Partial/Not covered" gaps from STYLE-COMPONENTS.md, not addressed by any step.
- **Turning on figure for pip/ace** (`layers.figure.pip`/`.ace`) — only available via `--config`; once on, the figure block (Steps 7–10) runs for that group like court.
