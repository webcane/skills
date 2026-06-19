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
/ `ace`) via `layers.<layer>.<group>` in `references/CONFIG.md`. Each cell is
`"false"` (layer off), `"true"` (layer on, no addition), or any other text (layer on,
that text is this group's addition, appended after the layer's own pattern/preset
text):

- **Background** — base cardstock color/texture, plus this group's addition if the
  cell is custom text. On for every group by default.
- **Decor** — background pattern / accent colors beyond the suit's own color, plus
  this group's addition if the cell is custom text.
- **Ornaments** — vignettes, corner flourishes, decorative elements that aren't the
  frame itself, plus this group's addition if the cell is custom text.
- **Highlights** — gilding, lacquer, glow, shine — accents that can sit over the
  figure/pips, plus this group's addition if the cell is custom text.
- **Frame** — the border/architectural framing (`[FRAME_LINE]`), its text drawn from
  the chosen `frame` preset in `assets/frame/`, plus this group's addition if the cell
  is custom text.
- **Figure** — the figure type for this group's center motif. The cell value is
  the figure TYPE: `"false"` = no figure; `"character"` / `"building"` / `"animal"` /
  `"custom"` = figure on + that type. The type selects which
  `assets/figure-type/<type>.md` text is pulled into `[STYLE_BLOCK]`, and determines
  whether character-only sources (Face Style, character_framing) apply. Default:
  `"character"` for `court` and `joker` (the portrait); `"false"` for `pip`/`ace`
  (no figure) — set to a type value for `pip`/`ace` only for transformation-style
  decks where number/ace cards carry small figures.
- **Mood** — whether `[MOOD_LINE]` (the deck's overall atmosphere, from the `mood`
  setting) and this group's addition (a per-group mood addition, when the cell is
  custom text) apply to this group. On for every group by default; both are empty
  (and dropped) unless `mood` and/or this group's addition are set.
- **Technique** — the rendering technique/medium applied to whatever sits in the
  center (portrait, pip layout, or suit symbol alike) — linework, tonal/area-fill
  rendering, painterly treatment, collage, and so on — plus this group's addition if
  the cell is custom text. Also gates the pattern's "Finish" lines (the print-quality/
  final-rendering descriptor for the whole card) — Technique and Finish both describe
  *how* the card is rendered, so they share one on/off switch. On for every group by
  default. Distinct from **Figure** — Technique (+ Finish) is *how* the card is
  rendered regardless of what it shows; Figure is *whether* the center motif is a
  portrait at all.

Each `assets/pattern/<style>.md` provides the text for Background, Decor, Ornaments,
Highlights, "Technique" (the linework/medium descriptor applied to whatever sits in
the center — portrait, pip layout, or suit symbol alike), "Finish" (the print-quality/
final-rendering descriptor for the whole card), "Figure detail" (additional rendering
detail that only makes sense for a portrait, e.g. skin tones — or `(none)`), and "Face
Style" (how a figure's face reads in this pattern — typage, expression, degree of
stylization). The pattern file itself never references `layers.*` or any other config;
whether "Technique" and "Finish" are folded into `[STYLE_BLOCK]` for a given group is
decided here via a single `layers.technique.<group>` gate (see steps 5 and 7 below),
and whether "Figure detail" and "Face Style" are folded in is decided here via
`layers.figure.<group>` (and only for the `character` type) — independently of
`layers.technique.<group>`.

### Resolving `[STYLE_BLOCK]` for a card group

For the group `g` (`court`, `pip`, `ace`, `joker`, `back`, or `special`), each `layers.<layer>.g` cell resolves to
**off** (cell is `"false"`), **on, no addition** (cell is `"true"`), or **on, with
addition** (cell is any other text — that text is the addition). Build `[STYLE_BLOCK]`
by concatenating, in this order, only the layers that are on:

1. **Background** — the pattern's Background lines, then `layers.background.g`'s
   addition (free text, own comma phrase) if the cell is custom text.
2. **Decor** — the pattern's Decor lines, then `layers.decor.g`'s addition (free
   text, own comma phrase) if the cell is custom text.
3. **Ornaments** — the pattern's Ornaments lines (if any), then `layers.ornaments.g`'s
   addition (free text, own comma phrase) if the cell is custom text — see
   "Theme-derived ornaments/highlights/frame" below if the cell is exactly `"true"`
   and `theme` is set.
4. **Highlights** — the pattern's Highlights lines (if any), then
   `layers.highlights.g`'s addition (free text, own comma phrase) if the cell is
   custom text — same theme fallback as Ornaments.
5. **Technique** — the pattern's "Technique" lines, then `layers.technique.g`'s
   addition (free text, own comma phrase) if the cell is custom text. These describe
   the rendering technique/medium applied to whatever sits in the center (portrait,
   pip layout, or suit symbol alike) and don't depend on `layers.figure.g`. Dropped
   entirely if `layers.technique.g` is `"false"`.

Then:

6. **Figure block** — only if `layers.figure.g` is a type value (not `"false"`).
   Read the type from `layers.figure.g` and append, in this exact order (D-15):

   a. **Figure-type text** — the text from `assets/figure-type/<type>.md`, where
      `<type>` is the `layers.figure.g` value (`character`, `building`, `animal`, or
      `custom`). Applied to ALL figure types.

   b. **Character-only sources** — ONLY when `layers.figure.g` is `"character"`:
      append the pattern's "Figure detail" lines (skip entirely if that section is
      `(none)`), then the pattern's "Face Style" line (how a figure's face reads in
      this pattern — typage, expression, degree of stylization), then
      `layers.figure.g`'s addition (free text, own comma phrase) if the cell is
      custom text beyond the type keyword — a group-wide figure trait for every card
      in this group (e.g. "all court figures shown with a slight hunch"). Then, if
      `character_framing` is non-empty, append it as its own comma phrase (the
      deck-wide character framing from `assets/character-framing/`, e.g.
      `waist-up portrait, torso and arms visible, hands free to hold attributes,`).
      **For `building`, `animal`, and `custom` figure types: skip the pattern's
      "Figure detail" lines, Face Style line, the group-wide addition, and
      `character_framing` entirely** (FIG-08, D-16). These types receive only items
      a, c, and d.

   c. **Figure scale** — the deck-wide `figure_scale` setting (values: `full-bleed`,
      `inscribed-in-frame`, `small-centered`, or custom free text; set in Step 8a).
      Append the `figure_scale` value as its own comma phrase. Applied to ALL figure
      types. If `figure_scale` is empty or not set, omit this phrase.

   d. **Split** — if `layers.split.g` is `"horizontal-mirrored"` or
      `"angled-mirrored"`, append the text from
      `assets/split/<layers.split.g value>.md` as its own comma phrase — the outer
      compositional wrapper (SPLT-03). If `layers.split.g` is `"none"` or `"false"`,
      no split text is added.

   The entire figure block (a–d) is skipped when `layers.figure.g` is `"false"`.
   This is independent of `layers.technique.g` — a card can have Technique on with
   Figure off (e.g. plain pip with the pattern's linework but no portrait detail), or
   vice versa.
7. **Finish** — the pattern's Finish lines, included under the same gate as step 5:
   present if `layers.technique.g` is on, dropped entirely if `layers.technique.g` is
   `"false"`. Finish is the print-quality/final-rendering descriptor for the whole
   card — describing *how* the card is rendered, like Technique, so the two share one
   gate even though Finish sits later in `[STYLE_BLOCK]` (after Figure detail/Face
   Style). `layers.technique.g`'s addition (if any) was already appended in step 5 —
   Finish doesn't get its own addition slot.

8. **Mood** — if `layers.mood.g` is on: if `mood` is non-empty, append `[MOOD_LINE]`
   — the `mood` text as its own comma phrase (e.g. `gothic and brooding atmosphere,`);
   then, if `layers.mood.g`'s addition is non-empty (the cell is custom text), append
   it as its own comma phrase too — a per-group mood addition layered on top of (or in
   place of) the deck-wide `mood`. If both `mood` and `layers.mood.g`'s addition are
   empty, no mood line is added for this group, regardless of `layers.mood.g`.

9. **Plain fallback** — if `g` is `pip` and `layers.decor.pip`, `layers.ornaments.pip`,
   and `layers.highlights.pip` are all `"false"`, append the line `plain card face, no
   additional ornament beyond the pip symbols,` after Mood (a pip card with nothing
   else added should read as a plain number card).

10. **Back-group symmetry** — only for the `back` group: append the "Symmetry line" text
    from `assets/back/symmetry/<back_symmetry>.md` as its own comma phrase after all
    other layers (including Mood and Plain fallback). `back_symmetry` defaults to
    `rotational-180` if not set. This applies regardless of which layers are on or off
    for the back group — it is always present.

`[FRAME_LINE]` is built from the chosen `frame` preset's "Frame line" in
`assets/frame/<frame>.md` (default `boxed-index`: `thin single black border around the
card perimeter, plus a separate thin black border individually framing each of the four
corner index areas,`), with `layers.frame.g`'s addition appended as its own comma
phrase if the cell is custom text — see "Theme-derived ornaments/highlights/frame"
below if the cell is exactly `"true"` and `theme` is set. Included verbatim if
`layers.frame.g` is on and dropped entirely otherwise — it sits in its own template
slot, not inside `[STYLE_BLOCK]`. The same resolved `[FRAME_LINE]` is reused across all
cards of the same group/deck, like `[STYLE_BLOCK]`.

### Figure type, face style, framing & scale (within `[STYLE_BLOCK]`)

There is no separate `[FACE_STYLE_LINE]` template slot and no `face_style` setting —
how a figure's face reads is part of the pattern itself (step 6 above), so it stays
consistent with that pattern's overall look without an extra per-deck choice. Each
`assets/pattern/<style>.md` keeps three sections distinct: "Technique" (the
linework/rendering medium applied to whatever sits in the center — portrait, pips, or
suit symbol alike — gated by `layers.technique.<group>`, step 5 above), "Figure
detail" (additional rendering detail that only makes sense for a portrait, e.g. skin
tones, or `(none)`), and "Face Style" (typage/expression/degree of stylization for a
face). The pattern file never says when "Figure detail" or "Face Style" apply —
`references/REFERENCE.md` alone decides that, via `layers.figure.<group>` and its type
value. Keep these three as separate sections when adding or editing a pattern — don't
fold Figure detail or Face Style into Technique or vice versa.

**Figure type assembly** — `layers.figure.<group>` now carries the figure type (`"false"` / `"character"` / `"building"` / `"animal"` / `"custom"`):
- For `character` type: figure block = `assets/figure-type/character.md` text + pattern's Figure detail + Face Style + group-wide addition + `character_framing` text (from `assets/character-framing/`) + `figure_scale` text + split text (D-17, FIG-07).
- For `building` / `animal` / `custom`: figure block = `assets/figure-type/<type>.md` text + `figure_scale` text + split text. Pattern's Figure detail, Face Style, group-wide addition, and `character_framing` are all skipped (FIG-08, D-16).

**Five scopes of figure content**, broadest to narrowest:
- **Deck-wide (figure type)** — the `assets/figure-type/<type>.md` text for the group's
  configured type: the canonical prompt phrase for that figure type (e.g. character
  preamble, building description, animal phrase). Applied to all types.
- **Deck-wide (pattern, character-only)** — the pattern's "Figure detail" lines (if not
  `(none)`) plus its Face Style line (from `style`): additional portrait-only rendering
  detail (e.g. skin tones) and how a character figure's face reads in this pattern
  (typage, expression, degree of stylization). No separate setting; baked into the
  chosen pattern. Applied ONLY when figure type is `character`.
- **Deck-wide (character framing, character-only)** — `character_framing` (picked from
  `assets/character-framing/` or free-text in Step 8e): how much of the character
  figure is shown and how it is cropped (e.g. "waist-up portrait, torso and arms
  visible, hands free to hold attributes,"), reused across every card whose group's
  figure type is `character`. Applied ONLY when figure type is `character`; appended
  right after the group-wide addition.
- **Deck-wide (scale, all types)** — `figure_scale` (set in Step 8a, stored as
  `full-bleed` / `inscribed-in-frame` / `small-centered`): how the figure sits in the
  frame, applied to ALL figure types. Appended after `character_framing` (or right
  after figure-type text for non-character types).
- **Deck-wide (split, outer wrapper, all types)** — `layers.split.<group>` (`none`,
  `horizontal-mirrored`, `angled-mirrored`): the compositional split layout from
  `assets/split/<mode>.md`. Applied to all figure types; appended as the outermost
  wrapper after `figure_scale`. No split text for `none`/`false`.
- **Group-wide** — `layers.figure.<group>`'s addition beyond the type keyword, when
  the cell contains custom text in addition to or instead of the type enum value
  (config-only): an optional trait shared by every figure in one group
  (`court`/`pip`/`ace`/`joker`) — e.g. "all court figures shown with a slight hunch"
  — appended right after the pattern's Face Style line for that group (character-only).
- **Per-card** — `[CHARACTER_NAME]`/`[CHARACTER_FEATURES]` plus the Steps 10-12
  attributes/reference-transfers/exclusions: who this specific card's figure is,
  always supplied per card (from the user or a reference image).

These scopes stack together rather than compete — each addresses a different question
("which figure type text" / "how do faces render in this pattern" / "how is the
character framed in this deck" / "how is the figure scaled in the frame" / "what split
layout" / "what's true of every figure in this group" / "who is this card's figure").

**Source resolution — pattern vs. reference image.** The Face Style line governs *how*
a face is rendered (stylization, linework, expression register); `[CHARACTER_FEATURES]`
and any Step 11 reference-image transfers govern *what* the face looks like (identity,
specific features, hairstyle). These are complementary, not competing — both apply
together by default. The only conflict is the one already called out: if a pattern's
Face Style line describes an obscured or mask-like treatment, drop any facial
description from `[CHARACTER_FEATURES]` (silhouette/costume only — see SKILL Step 9) so
the two don't contradict each other. Otherwise, no source-resolution step is needed —
the pattern's Face Style line and the character's own features simply stack.

For `pip`/`ace`, the entire figure block (figure-type text, character-only sources,
figure_scale, and split) only appears if `layers.figure.<group>` is a type value (not
`"false"`; transformation decks); otherwise they're part of step 6 and simply not
appended.

### Theme-derived ornaments/highlights/frame

If `theme` (a free-text deck-wide concept, e.g. "celestial mythology", "botanical
garden") is set, and for group `g` a layer's cell is exactly `"true"` (on, with no
explicit addition):

- `layers.ornaments.g == "true"` → derive a short ornament phrase expressing `theme`
  (e.g. theme "celestial mythology" → `star and constellation motifs in the corner
  ornaments,`) and use it as that card's ornaments addition for this generation.
- `layers.highlights.g == "true"` → same derivation for highlights (e.g. → `faint
  star-glow highlights,`).
- `layers.frame.g == "true"` → same derivation for the frame (e.g. → `star-and-comet
  motifs worked into the corner cut-ins,`), appended after the chosen `frame` preset's
  "Frame line".

This theme-derivation applies only to ornaments, highlights, and frame — for
background, decor, and mood, a cell of exactly `"true"` simply has no addition, with
no `theme` fallback.

An explicit addition (`layers.ornaments.g` / `layers.highlights.g` / `layers.frame.g`
set to custom text, by the user or saved in config) always wins — `theme` only fills
in for cells that are exactly `"true"`. Reuse the same derived phrase across all cards
of the same group/deck so the set stays consistent. For cards with a figure, `theme`
may also inform the character concept and Step 10 attribute suggestions (suggest,
don't force).

### Defaults

`layers.figure.<group>` now stores the figure type, not a boolean. `"false"` = no
figure; `"character"` / `"building"` / `"animal"` / `"custom"` = figure on + that type.

| Layer        | court       | pip    | ace    | joker       | back  | special |
|--------------|-------------|--------|--------|-------------|-------|---------|
| background   | true        | true   | true   | true        | true  | true    |
| decor        | true        | false  | false  | true        | true  | true    |
| ornaments    | true        | false  | false  | true        | true  | true    |
| highlights   | false       | false  | false  | false       | false | false   |
| frame        | true        | true   | true   | true        | true  | false   |
| figure       | "character" | false  | false  | "character" | false | false   |
| split        | false       | false  | false  | false       | false | false   |
| mood         | true        | false  | false  | true        | true  | true    |
| technique    | true        | false  | false  | true        | true  | true    |

The `figure` row uses type enum values: `"character"` = portrait on + character type
(default for court/joker); `false` = no figure (default for pip/ace/back/special). The `split` row
defaults to `false` (not configured) for all groups — `"false"` means the wizard asks
the first time a figure card in that group is generated; `"none"` means configured as
no split; `"horizontal-mirrored"` / `"angled-mirrored"` means that split mode.

These reproduce the traditional look out of the box: Court cards carry the full
pattern including its Figure detail and Face Style sections (character type); plain Pip
cards show only background + frame (no technique, no finish, no extra accents, no
figure); Aces carry background + frame but no figure, decor, ornaments, mood, or
technique; Joker cards carry the full pattern with a figure (like Court cards, character
type) — a fully decorated single-figure card. Back cards are fully decorated
(background, decor, ornaments, mood, technique all on) with frame on but no figure —
designed to carry the pattern's repeat motif and finish.
Highlights is off everywhere by default. `mood` and `theme` are both empty by default,
so `[MOOD_LINE]` and the theme-derived ornaments/highlights produce nothing unless set.
Technique is on for Court, Joker, Back, and Special cards by default; Pip and Ace
cards default to technique off (no linework/medium descriptor, no finish lines). Court
and Joker layers are configurable via `--config` (see `references/CONFIG.md`) but
default to fully on (except highlights), matching prior behavior.

Special cards default `frame` to `false` (no standard card border — special cards typically
have non-standard layouts) and `figure` to `false` (no figure by default; set
`layers.figure.special` to a type value to add a figure). There are no corner indices on
Special cards — see the SPECIAL template.

When generating multiple cards for the same deck, reuse the exact same resolved
`[STYLE_BLOCK]` and `[FRAME_LINE]` for every card of the same group so the set stays
visually consistent.

---

## `structure` setting (`full` vs `illustration`)

`structure` (persistent, deck-wide) controls whether the assembled prompt describes a
complete card or only the center illustration. The `illustration` value is for users
who composite the AI-generated artwork into their own SVG/HTML card template — one
that already supplies the frame, corner indices, fonts, and margins — and so want a
prompt that describes ONLY what goes in the center clip area.

- **`full`** (default) — current behavior, unchanged.
- **`illustration`** — exactly four changes to assembly, all others unchanged:
  1. **Drop `[INDEX_LINE]`** entirely from every template — no corner rank/suit
     markers (the user's own template supplies these).
  2. **Drop `[FRAME_LINE]`** entirely from every template, regardless of
     `layers.frame.<group>`. The `layers.frame.<group>` cells in `config.json` are
     **not modified or cleared** — they're simply ignored at assembly time, so
     switching back to `structure: full` restores the prior frame behavior exactly as
     configured.
  3. **Replace the templates' opening line.** Instead of:
     `[ASPECT_RATIO] aspect ratio, full card visible, transparent background outside
     the card,`
     use:
     `[ASPECT_RATIO] aspect ratio, single self-contained illustration filling the
     entire frame edge-to-edge, no card shape, no border, no background beyond the
     illustration itself,`
     `[ASPECT_RATIO]` (Step 13) is itself unchanged — only its meaning shifts, from the
     proportions of the whole card to the proportions of the illustration/clip area in
     the user's template.
  4. **Append a fixed block to `[NEGATIVE_LIST]`**, after the usual exclusions:
     `no card border, no frame, no corner index letters or numbers, no corner suit
     symbols`

**Scope — everything else is unaffected.** `structure: illustration` touches only the
four items above. The following remain fully AI-generated regardless of `structure`:
- All of `[STYLE_BLOCK]` — background, decor, ornaments, highlights, figure, mood, and
  technique layers (including Finish lines), resolved exactly as for `structure: full`.
- The **Center motif** — the portrait + `[RESOLVED_ATTRIBUTES]` on Court cards, the
  `[RANK_COUNT]` pip layout on Pip cards, and the large suit symbol on Aces.

Rounded or cut corners need no separate handling: that treatment lives in
`[FRAME_LINE]` (e.g. `assets/frame/cut-corner.md`, `assets/frame/rounded-cut-corner.md`),
which is already dropped under `structure: illustration`.

**Reusing one illustration as a style reference.** When generating several cards for
the same deck under `structure: illustration`, it often helps to generate one card
first and then reuse it as a style/composition reference for the rest (e.g.
Midjourney's `--sref`, or a `style_reference`/`image_reference` parameter on other
engines), so the whole set of illustrations reads as one consistent style. This is a
workflow tip for the user — this skill does not inject reference-image parameters into
the generated prompt text itself.

---

## COURT template (King / Queen / Jack)

`[CHARACTER_NAME]` and `[CHARACTER_FEATURES]` are REQUIRED (at minimum a name). The
features may be typed by the user or derived from a reference image (see SKILL Step 9).

Before filling the template, resolve all attribute sources into ONE flowing,
contradiction-free `[RESOLVED_ATTRIBUTES]` list — short comma-separated phrases, no
bullet points, no section labels, no duplicated details:

1. Start from `[TRADITIONAL_ATTRIBUTES]` (auto-loaded from `assets/courts/<rank>.md`).
2. Apply the Step 10 additions/replacements — a replacement REMOVES the traditional
   item it replaces rather than sitting next to it.
3. Apply the Step 11 reference transfers — these win over anything from steps 1–2 that
   describes the same feature (face, pose, hand, prop, etc.).
4. Drop any remaining traditional item that conflicts with `[CHARACTER_FEATURES]` or
   the user's stated intent (e.g. a weapon or full-body pose attribute when the user
   asked for a bust portrait with no hands), even if nothing explicitly replaced it.
5. Make sure each visual detail (face, hair, costume piece, color, prop) appears
   exactly once, in whichever phrase describes the character.

Build `[NEGATIVE_LIST]` as a single comma-separated "no …" sequence: start with
`no watermark`, then append the Step 12 exclusions, each phrased as `no <thing>`.
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
[CHARACTER_FEATURES], [RESOLVED_ATTRIBUTES],
[SUIT_COLOR] [SUIT_NAME] suit symbols,
[NEGATIVE_LIST]
```

---

## PIP template (2 through 10)

No portrait, no character — unless `layers.figure.pip` is on (transformation-style
decks), in which case `[STYLE_BLOCK]` carries the pattern's Figure detail and Face
Style lines (step 6 of "Resolving `[STYLE_BLOCK]`") for the small figure within the pip
layout. `[RANK_COUNT]`
= the rank number. `[STYLE_BLOCK]` and `[FRAME_LINE]` are resolved per "Layers and
`[STYLE_BLOCK]` assembly" above for the `pip` group (default: background + center
motif + finish only — plain pip card, no frame, no figure).

```
[ASPECT_RATIO] aspect ratio, full card visible, transparent background outside the card,
[RANK_NAME] of [SUIT_NAME_TITLE] playing card,
[STYLE_BLOCK]
[FRAME_LINE]
[INDEX_LINE]
[RANK_COUNT] [SUIT_COLOR] [SUIT_NAME] pip symbols arranged in the traditional symmetrical layout for the [RANK_NAME], upper-half pips upright, lower-half pips rotated 180 degrees,
[SUIT_COLOR] [SUIT_NAME] suit symbols,
no watermark
```

---

## JOKER template

`[CHARACTER_NAME]` and `[CHARACTER_FEATURES]` are REQUIRED (at minimum a name).
Resolve attributes the same way as COURT (see "Before filling the template" above).

`[JOKER_ROLE]` is the Joker's role/variant designation plus its palette/tradition hint
(per-card, from Step 4.1). Standard values:
- `Big Joker, full-color vivid elaborate palette`
- `Little Joker, simplified subdued monochrome palette`
- `Wild Joker, European fool-card tradition, unpaired`
- or any custom phrase the user provides.

The Joker is a **non-reversible, full-card single-figure composition** — no central
dividing line, no mirrored halves. `[STYLE_BLOCK]` and `[FRAME_LINE]` are resolved for
the `joker` group (`index.type` is effectively `"joker"` for this card).

`[INDEX_LINE]` is built from `assets/index/options.md` using **Menu D2** (Joker
placement) + the symbol from `index.symbol`. Default (4-corner, standard size,
`index.symbol = "star-in-circle"`):
```
four corner indices, each showing a star enclosed in a circle glyph,
no rank letter, no suit symbol, standard small index size,
upper indices upright, lower indices rotated 180 degrees,
```
When `index.count = "none"` (or `index.symbol = "none"`), replace `[INDEX_LINE]`
entirely with: `no corner indices, full-bleed illustration,`

```
[ASPECT_RATIO] aspect ratio, playing card, Joker card ([JOKER_ROLE]),
[INDEX_LINE]
[FRAME_LINE]
[STYLE_BLOCK]
[CHARACTER_NAME], [CHARACTER_FEATURES], [RESOLVED_ATTRIBUTES],
[NEGATIVE_LIST]
```

---

## ACE template (A)

`[STYLE_BLOCK]` and `[FRAME_LINE]` are resolved per "Layers and `[STYLE_BLOCK]`
assembly" above for the `ace` group (default: everything on except figure — matches
the previous unconditional behavior). `[STYLE_BLOCK]` carries the pattern's Figure
detail and Face Style lines only if `layers.figure.ace` is on (transformation-style
decks with a figure on the Ace).

```
[ASPECT_RATIO] aspect ratio, full card visible, transparent background outside the card,
Ace of [SUIT_NAME_TITLE] playing card,
[STYLE_BLOCK]
[FRAME_LINE]
[INDEX_LINE]
one single large ornamental [SUIT_COLOR] [SUIT_NAME] symbol centered on the card, decorative flourishes and fine scrollwork framing the central symbol,
[SUIT_COLOR] [SUIT_NAME] suit symbols,
no watermark
```

---

## BACK template

Used when rank = Back. No suit, no character attributes, no corner indices (Back cards
have no rank/suit letters — all four index areas are blank or absent). STYLE_BLOCK and
FRAME_LINE are resolved for the `back` group per "Layers and [STYLE_BLOCK] assembly"
above. The symmetry instruction from `assets/back/symmetry/<back_symmetry>.md` is
always appended to STYLE_BLOCK for the back group (step 10, per D-04), after the
standard layer assembly — this is a back-group-specific STYLE_BLOCK addition that
applies regardless of `layers.*` cell values.

`[BACK_DESIGN]` is assembled from three asset lines concatenated in order (drop any
empty/unset field):
1. **Purpose line** from `assets/back/purpose/<back_purpose>.md` (or custom text if `back_purpose` is free text)
2. **Pattern line** from `assets/back/design/<back_design>/<back_pattern>.md` (or custom text if `back_pattern` is free text)
3. **Palette line** from `assets/back/palette/<back_palette>.md` (or custom text if `back_palette` is free text)

Symmetry is NOT in `[BACK_DESIGN]` — it goes through STYLE_BLOCK step 10.
Frame is NOT in `[BACK_DESIGN]` — it goes through `[FRAME_LINE]` via `layers.frame.back`.

Per-card exclusions (Step B7) go to `[NEGATIVE_LIST]` only — there is no
`[BACK_MODIFICATIONS]` placeholder in this template.

```
[ASPECT_RATIO] aspect ratio, full card visible, transparent background outside the card,
playing card back design,
[STYLE_BLOCK]
[FRAME_LINE]
no corner indices, no rank letters, no suit symbols,
[BACK_DESIGN]
[NEGATIVE_LIST]
```

---

## SPECIAL template

Used when rank = Special. No suit, no corner indices, no card frame by default
(`layers.frame.special` defaults to `"false"`). STYLE_BLOCK and FRAME_LINE are resolved
for the `special` group per "Layers and [STYLE_BLOCK] assembly" above. Unlike Back cards,
Special cards have no built-in forced STYLE_BLOCK addition — STYLE_BLOCK assembles
normally from whatever `layers.*.<special>` cells are configured.

`[SPECIAL_TYPE_LINE]` is the "Special type line" text from the selected type's asset
file in `assets/special/` (e.g., `prospect.md` or `marketing.md`), OR free text if the
user chose "Custom text" in the wizard (Step S2). Drop this line if empty.

`[CARD_NAME]` is the display name the user provided for this specific card (e.g.,
"King of Clubs" for a prospect card, or any custom name). Required.

`[FIGURE_DESCRIPTION]` is the figure description:
- For **prospect-type** cards: the named figure assigned to this card slot by the
  wizard (Step S4), e.g., "Peter the Great, Russian Emperor, in imperial regalia,"
- For **other types**: the user's visual content description from Step S3.
Drop this line if empty.

`[SPECIAL_ATTRIBUTES]` is the layout arrangement chosen in Step S3 (for prospect-type
cards, the grid/list/row/collage layout; for other types, any additional attributes or
visual instructions the user provides). Drop if empty.

```
[ASPECT_RATIO] aspect ratio, special playing card,
[CARD_NAME],
[SPECIAL_TYPE_LINE]
[STYLE_BLOCK]
[FRAME_LINE]
no corner indices, no standard rank letters, no suit symbols,
[FIGURE_DESCRIPTION]
[SPECIAL_ATTRIBUTES]
[NEGATIVE_LIST]
```

---

## Rank reference table

| Choice  | RANK_NAME | RANK_LETTER source                      | Template | RANK_COUNT |
|---------|-----------|------------------------------------------|----------|------------|
| A       | Ace       | `A` (or `1`)                            | ACE      | 1          |
| 2       | Two       | `2`                                     | PIP      | 2          |
| 3       | Three     | `3`                                     | PIP      | 3          |
| 4       | Four      | `4`                                     | PIP      | 4          |
| 5       | Five      | `5`                                     | PIP      | 5          |
| 6       | Six       | `6`                                     | PIP      | 6          |
| 7       | Seven     | `7`                                     | PIP      | 7          |
| 8       | Eight     | `8`                                     | PIP      | 8          |
| 9       | Nine      | `9`                                     | PIP      | 9          |
| 10      | Ten       | `10`                                    | PIP      | 10         |
| J       | Jack      | from lettering system (J/V/B/В/Kn)      | COURT    | —          |
| Q       | Queen     | from lettering system (Q/D/V/Д)         | COURT    | —          |
| K       | King      | from lettering system (K/R/H/К)         | COURT    | —          |
| Jkr     | Joker     | `index.symbol` (star-in-circle default) | JOKER    | —          |
| Back    | Back      | — (no index letter)                     | BACK     | —          |
| Special | Special   | — (no index letter)                     | SPECIAL  | —          |

> **Back cards** have no corner indices — `[INDEX_LINE]` is replaced by the literal
> `no corner indices, no rank letters, no suit symbols,` in the BACK template.

> **Special cards** have no corner indices — the SPECIAL template hardcodes
> `no corner indices, no standard rank letters, no suit symbols,` inline (no `[INDEX_LINE]`).

RANK_NAME is always the English word; RANK_LETTER is the localized printed index per
`assets/lettering/systems.md` (for court cards) or the `index.symbol` glyph phrase
(for the Joker — see the JOKER template above).

---

## Aspect ratios / card types (Step 13)

| Card type                    | Aspect ratio (ASPECT_RATIO) | Physical size   |
|------------------------------|-----------------------------|-----------------|
| Poker (Wide)                 | 5:7                         | 63.5 × 88.9 mm  |
| Bridge / Preferans (Narrow)  | 9:14 (default)              | 57.15 × 88.9 mm |
| European / German (Skat)     | 14:25                       | ~56 × 100 mm    |
| Tarot                        | 7:12                        | 70 × 120 mm     |
| Mini                         | 5:7                         | 44 × 63 mm      |

Only the ratio goes into the prompt; size is informational. Custom ratios allowed.
