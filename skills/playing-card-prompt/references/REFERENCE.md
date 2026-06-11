# Prompt Templates

Three variants by rank: COURT (King/Queen/Jack), PIP (2–10), ACE.
Fill every `[PLACEHOLDER]`. Drop any line whose value is empty rather than leaving a
literal bracket. `[SUIT_SYMBOL]` is a Unicode glyph for French decks (♠♥♦♣) or a short
shape word for other decks (acorn, leaf, sword, cup, coin, shield, rose, hawk-bell).

`[INDEX_LINE]` is built from `assets/index/options.md` (defaults applied silently — the wizard
does not ask). The default expands to:
`four corner indices, each with rank [RANK_LETTER] stacked above suit symbol [SUIT_SYMBOL], standard small index size, upper indices upright, lower indices rotated 180 degrees,`

---

## COURT template (King / Queen / Jack)

`[CHARACTER_NAME]` and `[CHARACTER_FEATURES]` are REQUIRED (at minimum a name). The
features may be typed by the user or derived from a reference image (see SKILL Step 5b).

Attribute blocks are built in priority order (later overrides earlier):
1. `[TRADITIONAL_ATTRIBUTES]` — auto-loaded from `assets/courts/<rank>.md`
2. `[EXTRA_ATTRIBUTES]` — Step 5c additions/replacements
3. `[REFERENCE_TRANSFERS]` — Step 6, takes priority over traditional
4. `[EXCLUSIONS_LIST]` — Step 7, removes elements

```
[CHARACTER_NAME] as [RANK_NAME] of [SUIT_NAME_TITLE] playing card,
thin single black border with stepped corner cut-ins framing the index areas,
[INDEX_LINE]
large [SUIT_COLOR] [SUIT_NAME] suit symbols centered in upper and lower card fields,
thin black horizontal dividing line through the exact center of the card,
reversible two-way court card layout,
identical upper and lower portraits rotated 180 degrees around the central horizontal axis,
CHARACTER-SPECIFIC FEATURES:
[CHARACTER_FEATURES]
STANDARD [RANK_NAME] RANK ATTRIBUTES (traditional defaults for this rank):
[TRADITIONAL_ATTRIBUTES]
ADDITIONAL / REPLACED ATTRIBUTES (override the traditional set):
[EXTRA_ATTRIBUTES]
TRANSFERRED FROM REFERENCE IMAGE (takes priority over traditional attributes):
[REFERENCE_TRANSFERS]
EXCLUSIONS (elements that must NOT transfer from the reference image):
[EXCLUSIONS_LIST]
symmetrical costume design (upper/lower halves rotationally mirrored),
[STYLE_BLOCK]
[SUIT_COLOR] [SUIT_NAME] suit symbols,
full card visible,
transparent background outside the card,
aspect ratio [ASPECT_RATIO], no watermark
```

---

## PIP template (2 through 10)

No portrait, no character. `[RANK_COUNT]` = the rank number.

```
[RANK_NAME] of [SUIT_NAME_TITLE] playing card,
thin single black border with stepped corner cut-ins framing the index areas,
[INDEX_LINE]
[RANK_COUNT] [SUIT_COLOR] [SUIT_NAME] pip symbols arranged in the traditional symmetrical layout for the [RANK_NAME],
upper-half pips upright, lower-half pips rotated 180 degrees,
thin black horizontal dividing line through the exact center of the card,
[STYLE_BLOCK]
[SUIT_COLOR] [SUIT_NAME] suit symbols,
full card visible,
transparent background outside the card,
aspect ratio [ASPECT_RATIO], no watermark
```

---

## ACE template (A)

```
Ace of [SUIT_NAME_TITLE] playing card,
thin single black border with stepped corner cut-ins framing the index areas,
[INDEX_LINE]
one single large ornamental [SUIT_COLOR] [SUIT_NAME] symbol centered on the card,
decorative flourishes and fine scrollwork framing the central symbol,
[STYLE_BLOCK]
[SUIT_COLOR] [SUIT_NAME] suit symbols,
full card visible,
transparent background outside the card,
aspect ratio [ASPECT_RATIO], no watermark
```

---

## Rank reference table

| Choice | RANK_NAME | RANK_LETTER source                | Template | RANK_COUNT |
|--------|-----------|-----------------------------------|----------|------------|
| A      | Ace       | `A` (or `1`)                      | ACE      | 1          |
| 2      | Two       | `2`                               | PIP      | 2          |
| 3      | Three     | `3`                               | PIP      | 3          |
| 4      | Four      | `4`                               | PIP      | 4          |
| 5      | Five      | `5`                               | PIP      | 5          |
| 6      | Six       | `6`                               | PIP      | 6          |
| 7      | Seven     | `7`                               | PIP      | 7          |
| 8      | Eight     | `8`                               | PIP      | 8          |
| 9      | Nine      | `9`                               | PIP      | 9          |
| 10     | Ten       | `10`                              | PIP      | 10         |
| J      | Jack      | from lettering system (J/V/B/В/Kn)| COURT    | —          |
| Q      | Queen     | from lettering system (Q/D/V/Д)   | COURT    | —          |
| K      | King      | from lettering system (K/R/H/К)   | COURT    | —          |

RANK_NAME is always the English word; RANK_LETTER is the localized printed index per
`assets/lettering/systems.md`.

---

## Aspect ratios / card types (Step 8)

| Card type                    | Aspect ratio (ASPECT_RATIO) | Physical size   |
|------------------------------|-----------------------------|-----------------|
| Poker (Wide)                 | 5:7                         | 63.5 × 88.9 mm  |
| Bridge / Preferans (Narrow)  | 9:14 (default)              | 57.15 × 88.9 mm |
| European / German (Skat)     | 14:25                       | ~56 × 100 mm    |
| Tarot                        | 7:12                        | 70 × 120 mm     |
| Mini                         | 5:7                         | 44 × 63 mm      |

Only the ratio goes into the prompt; size is informational. Custom ratios allowed.
