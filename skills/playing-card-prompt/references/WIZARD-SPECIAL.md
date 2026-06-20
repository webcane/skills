# Special Card Wizard

Steps S1–S5, run by `SKILL.md`'s Step 3 instead of Steps 4.1–4.2 when the chosen rank is Special. Read it when the user is generating a Special card.

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

For **Prospect type**: use `AskUserQuestion` to ask how the 12 figures should be
arranged on the card. Offer these options (default first):
- **4 suits × 3 ranks grid (default)** — a grid with each figure as a small portrait,
  grouped by suit in columns. `[SPECIAL_ATTRIBUTES]` = `4 suits × 3 ranks grid, each figure a small portrait`
- **12-row list** — one row per court card slot, each showing the suit symbol, rank, and
  the named figure assigned to that slot (e.g. "♠ King — Peter I"). `[SPECIAL_ATTRIBUTES]` =
  `12-row list, each row: suit symbol · rank · named figure`
- **3 rows grouped by rank** — King / Queen / Jack rows, each spanning all four suits.
  `[SPECIAL_ATTRIBUTES]` = `3 rows grouped by rank (King / Queen / Jack), spanning all suits`
- **Free-form collage** — figures arranged freely without a fixed grid or list structure.
  `[SPECIAL_ATTRIBUTES]` = `free-form collage of all 12 court figures`

"Other" covers any custom layout description — use the user's text verbatim as
`[SPECIAL_ATTRIBUTES]`. This value becomes the layout instruction that wraps the figure
list in the assembled prompt. If the user doesn't specify, default to the grid.

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
`[FIGURE_DESCRIPTION]` for prospect cards is a structured list of all collected figures,
structured to match the Step S3 layout choice so the figure data and the layout
instruction in `[SPECIAL_ATTRIBUTES]` agree:

- **4 suits × 3 ranks grid (default):**
  ```
  suit arrangement (4 suits × 3 ranks):
    ♠ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack)
    ♥ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack)
    ♦ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack)
    ♣ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack)
  ```
- **12-row list:**
  ```
  named figures, one row per slot:
    ♠ King — [King figure], ♠ Queen — [Queen figure], ♠ Jack — [Jack figure],
    ♥ King — [King figure], ♥ Queen — [Queen figure], ♥ Jack — [Jack figure],
    ♦ King — [King figure], ♦ Queen — [Queen figure], ♦ Jack — [Jack figure],
    ♣ King — [King figure], ♣ Queen — [Queen figure], ♣ Jack — [Jack figure]
  ```
- **3 rows grouped by rank:**
  ```
  named figures grouped by rank, spanning all suits:
    King row: ♠ [King figure], ♥ [King figure], ♦ [King figure], ♣ [King figure]
    Queen row: ♠ [Queen figure], ♥ [Queen figure], ♦ [Queen figure], ♣ [Queen figure]
    Jack row: ♠ [Jack figure], ♥ [Jack figure], ♦ [Jack figure], ♣ [Jack figure]
  ```
- **Free-form collage:**
  ```
  named figures (no fixed arrangement):
    ♠ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack)
    ♥ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack)
    ♦ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack)
    ♣ [suit label if any]: [King figure] (King), [Queen figure] (Queen), [Jack figure] (Jack)
  ```

Use the block matching the Step S3 layout selection (or the "Other" custom layout's
nearest structural match) so the resulting text never restates a layout that
contradicts `[SPECIAL_ATTRIBUTES]`. This entire block is `[FIGURE_DESCRIPTION]` in the
SPECIAL template. Output: ONE prompt.

Session only — figures are not persisted to config in v1.

> **Note:** Deciding WHO the 12 figures are (research, thematic grouping, historical
> selection) is a structural/content task — outside this skill's scope. The skill
> expects the user to arrive with the figure assignments already prepared. Do not
> attempt to suggest or fill in figures on behalf of the user.

**Step S5 — Special card exclusions · _per-card (optional)_**

Ask what must NOT appear on the special card (e.g., "no playing card symbols", "no suit
marks"). Phrase each as "no <thing>" — merged into `[NEGATIVE_LIST]`. If nothing, skip.
