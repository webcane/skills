# Prompt Templates

Three variants by rank: COURT (King/Queen/Jack), PIP (2–10), ACE.
Fill every `[PLACEHOLDER]`. Drop any line whose value is empty rather than leaving a
literal bracket. `[SUIT_SYMBOL]` is a Unicode glyph for French decks (♠♥♦♣) or a short
shape word for other decks (acorn, leaf, sword, cup, coin, shield, rose, hawk-bell).

`[INDEX_LINE]` is built from `assets/index/options.md` (defaults applied silently — the wizard
does not ask). The default expands to:
`four corner indices, each with rank [RANK_LETTER] stacked above suit symbol [SUIT_SYMBOL], standard small index size, upper indices upright, lower indices rotated 180 degrees,`

---

## Layers and `[STYLE_BLOCK]` assembly

Every card is built from layers. Two are **structural** — always present, never
toggled off, because they're what makes the card that card:

- **Index** — the rank/suit corner markers (`[INDEX_LINE]`, from
  `assets/index/options.md`).
- **Center motif** — the card's main subject: the portrait + attributes on Court
  cards, the pip layout on number cards, the large suit symbol on Aces. This is the
  per-rank content built directly into the COURT/PIP/ACE templates below.

The rest are **configurable layers**, each controlled per card group (`court` / `pip`
/ `ace`) via `layers.<layer>.<group>` in `references/CONFIG.md`:

- **Background** — base cardstock color/texture. On for every group by default.
- **Decor** — background pattern / accent colors beyond the suit's own color.
- **Ornaments** — vignettes, corner flourishes, decorative elements that aren't the
  frame itself.
- **Highlights** — gilding, lacquer, glow, shine — accents that can sit over the
  figure/pips.
- **Frame** — the border/architectural framing (`[FRAME_LINE]`).
- **Figure** — whether this group's center motif carries a figure/portrait at all.
  Gates the Center motif style's figure-only line and `[FACE_STYLE_LINE]`. On for
  `court` by default (the portrait); off for `pip`/`ace` (no figure) — turn on for
  `pip`/`ace` only for transformation-style decks where number/ace cards carry small
  figures.
- **Mood** — whether `[MOOD_LINE]` (the deck's overall atmosphere, from the `mood`
  setting) applies to this group. On for every group by default; the line itself is
  empty (and dropped) unless `mood` is set.

Each `assets/pattern/<style>.md` provides the text for Background, Decor, Ornaments,
Highlights, and "Center motif style" (the linework/illustration descriptor applied to
whatever sits in the center — see that file's "Center motif style" section, which also
marks any figure-only line that only makes sense with a portrait).

### Resolving `[STYLE_BLOCK]` for a card group

For the group `g` (`court`, `pip`, or `ace`), build `[STYLE_BLOCK]` by concatenating,
in this order, only the layers where `layers.<layer>.g` is `true`:

1. **Background** — the pattern's Background lines.
2. **Decor** — the pattern's Decor lines.
3. **Ornaments** — the pattern's Ornaments lines (if any), then `ornaments_extra.g`
   (free text, own comma phrase) if set — see "Theme-derived ornaments/highlights"
   below if `ornaments_extra.g` is empty and `theme` is set.
4. **Highlights** — the pattern's Highlights lines (if any), then `highlights_extra.g`
   (free text, own comma phrase) if set — same theme fallback as Ornaments.

Then, always (these aren't gated by layers — they're part of the structural center
motif and finish):

5. **Center motif style** — the pattern's lines, including the figure-only line only
   if `layers.figure.g` is `true` (default: on for `court`, off for `pip`/`ace`).
6. **Finish** — the pattern's Finish lines.

7. **Mood** — if `layers.mood.g` is `true` and `mood` is non-empty, append
   `[MOOD_LINE]` — the `mood` text as its own comma phrase (e.g. `gothic and brooding
   atmosphere,`). Empty `mood` → no line, regardless of `layers.mood.g`.

8. **Plain fallback** — if `g` is `pip` and `layers.decor.pip`, `layers.ornaments.pip`,
   and `layers.highlights.pip` are all `false`, append the line `plain card face, no
   additional ornament beyond the pip symbols,` after Mood (a pip card with nothing
   else added should read as a plain number card).

`[FRAME_LINE]` is the line `thin single black border with stepped corner cut-ins
framing the index areas,`, included verbatim if `layers.frame.g` is `true` and dropped
entirely otherwise — it sits in its own template slot, not inside `[STYLE_BLOCK]`.

### Figure & face style resolution (`[FACE_STYLE_LINE]`)

`[FACE_STYLE_LINE]` is a separate template slot, placed next to the figure itself
(`[CHARACTER_FEATURES]` on COURT, or the pip/ace symbol line for transformation
decks). It is non-empty only when `layers.figure.g` is `true` AND `face_style.g` is
not `individual` (the default — "individual portrait" is already what
`[CHARACTER_FEATURES]` describes, so it adds nothing extra):

| `face_style.g`          | `[FACE_STYLE_LINE]` text |
|--------------------------|--------------------------|
| `individual` (default)  | _(empty — line dropped)_ |
| `archetypal`             | `archetypal symmetrical mask-like face, idealized features, no individualized expression,` |
| `expressive`             | `expressive individualized facial features, naturalistic emotion,` |
| `faceless`               | `figure depicted with face obscured or abstracted, no facial features,` |

For COURT with `face_style.court = faceless`, also drop any facial description from
`[CHARACTER_FEATURES]` (silhouette/costume only — see SKILL Step 5b).

For `pip`/`ace`, `[FACE_STYLE_LINE]` only matters if `layers.figure.<group> = true`
(transformation decks); otherwise it's empty and the slot is dropped.

### Theme-derived ornaments/highlights

If `theme` (a free-text deck-wide concept, e.g. "celestial mythology", "botanical
garden") is set, and for group `g` a layer is enabled but its `_extra` field is empty:

- `layers.ornaments.g = true` and `ornaments_extra.g == ""` → derive a short ornament
  phrase expressing `theme` (e.g. theme "celestial mythology" → `star and
  constellation motifs in the corner ornaments,`) and use it as that card's
  `ornaments_extra.g` for this generation.
- `layers.highlights.g = true` and `highlights_extra.g == ""` → same derivation for
  highlights (e.g. → `faint star-glow highlights,`).

An explicit `ornaments_extra.g` / `highlights_extra.g` (set by the user or saved in
config) always wins — `theme` only fills empty slots. Reuse the same derived phrase
across all cards of the same group/deck so the set stays consistent. For COURT,
`theme` may also inform the character concept and Step 5c attribute suggestions
(suggest, don't force).

### Defaults

| Layer        | court | pip   | ace   |
|--------------|-------|-------|-------|
| background   | true  | true  | true  |
| decor        | true  | false | true  |
| ornaments    | true  | false | true  |
| highlights   | false | false | false |
| frame        | true  | false | true  |
| figure       | true  | false | false |
| mood         | true  | true  | true  |

These reproduce the traditional look out of the box: Court cards carry the full
pattern including the portrait's figure-only line; plain Pip cards show only
background + center motif + finish (no border, no extra accents, no figure); Aces
keep their ornamental flourish and border but no figure. Highlights is off everywhere
by default. `mood` and `theme` are both empty by default, so `[MOOD_LINE]` and the
theme-derived ornaments/highlights produce nothing unless set. Court layers are
configurable via `--config` (see `references/CONFIG.md`) but default to fully on
(except highlights), matching prior behavior.

When generating multiple cards for the same deck, reuse the exact same resolved
`[STYLE_BLOCK]`, `[FRAME_LINE]`, and `[FACE_STYLE_LINE]` for every card of the same
group so the set stays visually consistent.

---

## COURT template (King / Queen / Jack)

`[CHARACTER_NAME]` and `[CHARACTER_FEATURES]` are REQUIRED (at minimum a name). The
features may be typed by the user or derived from a reference image (see SKILL Step 5b).

Before filling the template, resolve all attribute sources into ONE flowing,
contradiction-free `[RESOLVED_ATTRIBUTES]` list — short comma-separated phrases, no
bullet points, no section labels, no duplicated details:

1. Start from `[TRADITIONAL_ATTRIBUTES]` (auto-loaded from `assets/courts/<rank>.md`).
2. Apply the Step 5c additions/replacements — a replacement REMOVES the traditional
   item it replaces rather than sitting next to it.
3. Apply the Step 6 reference transfers — these win over anything from steps 1–2 that
   describes the same feature (face, pose, hand, prop, etc.).
4. Drop any remaining traditional item that conflicts with `[CHARACTER_FEATURES]` or
   the user's stated intent (e.g. a weapon or full-body pose attribute when the user
   asked for a bust portrait with no hands), even if nothing explicitly replaced it.
5. Make sure each visual detail (face, hair, costume piece, color, prop) appears
   exactly once, in whichever phrase describes the character.

Build `[NEGATIVE_LIST]` as a single comma-separated "no …" sequence: start with
`no watermark`, then append the Step 7 exclusions, each phrased as `no <thing>`.
Never repeat a negative elsewhere in the prompt and never add a separate "exclusions"
label — engines that support a negative-prompt field can take this list verbatim.

```
[ASPECT_RATIO] aspect ratio, full card visible, transparent background outside the card,
[CHARACTER_NAME] as [RANK_NAME] of [SUIT_NAME_TITLE] playing card,
[STYLE_BLOCK]
[FRAME_LINE]
[INDEX_LINE]
large [SUIT_COLOR] [SUIT_NAME] suit symbols centered in upper and lower card fields,
thin black horizontal dividing line through the exact center of the card,
reversible two-way court card layout, identical upper and lower portraits rotated 180 degrees around the central horizontal axis, symmetrical costume design,
[FACE_STYLE_LINE]
[CHARACTER_FEATURES], [RESOLVED_ATTRIBUTES],
[SUIT_COLOR] [SUIT_NAME] suit symbols,
[NEGATIVE_LIST]
```

---

## PIP template (2 through 10)

No portrait, no character — unless `layers.figure.pip` is on (transformation-style
decks), in which case `[FACE_STYLE_LINE]` may apply to the small figure within the pip
layout. `[RANK_COUNT]` = the rank number. `[STYLE_BLOCK]` and `[FRAME_LINE]` are
resolved per "Layers and `[STYLE_BLOCK]` assembly" above for the `pip` group (default:
background + center motif + finish only — plain pip card, no frame, no figure).

```
[ASPECT_RATIO] aspect ratio, full card visible, transparent background outside the card,
[RANK_NAME] of [SUIT_NAME_TITLE] playing card,
[STYLE_BLOCK]
[FRAME_LINE]
[INDEX_LINE]
[RANK_COUNT] [SUIT_COLOR] [SUIT_NAME] pip symbols arranged in the traditional symmetrical layout for the [RANK_NAME], upper-half pips upright, lower-half pips rotated 180 degrees,
[FACE_STYLE_LINE]
[SUIT_COLOR] [SUIT_NAME] suit symbols,
no watermark
```

---

## ACE template (A)

`[STYLE_BLOCK]` and `[FRAME_LINE]` are resolved per "Layers and `[STYLE_BLOCK]`
assembly" above for the `ace` group (default: everything on except figure — matches
the previous unconditional behavior). `[FACE_STYLE_LINE]` only applies if
`layers.figure.ace` is on (transformation-style decks with a figure on the Ace).

```
[ASPECT_RATIO] aspect ratio, full card visible, transparent background outside the card,
Ace of [SUIT_NAME_TITLE] playing card,
[STYLE_BLOCK]
[FRAME_LINE]
[INDEX_LINE]
one single large ornamental [SUIT_COLOR] [SUIT_NAME] symbol centered on the card, decorative flourishes and fine scrollwork framing the central symbol,
[FACE_STYLE_LINE]
[SUIT_COLOR] [SUIT_NAME] suit symbols,
no watermark
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
