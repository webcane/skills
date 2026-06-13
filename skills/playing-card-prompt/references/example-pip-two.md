# Example target prompt — PIP card

A fully assembled PIP prompt (Two of Spades, French deck, Austrian style, 9:14). Use
it as a reference for how `[STYLE_BLOCK]` and `[FRAME_LINE]` resolve for the `pip`
group per "Layers and `[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`, and as a
sanity check after assembly.

## Default — all `layers.*.pip` false except `background` (plain pip)

Compared to the Austrian `[STYLE_BLOCK]` used on COURT cards:
- **Background** stays (`aged ivory playing-card stock, subtle paper grain,`) — on for
  every group by default.
- **Decor** is dropped (`layers.decor.pip = false`) — no extra accent colors beyond
  the suit's own color.
- **Ornaments** and **Highlights** are off and empty for Austrian anyway, so nothing
  to drop.
- **Center motif style** keeps its linework/illustration lines but drops the
  figure-only line (`warm ochre skin tones,`) — there's no portrait.
- **Finish** stays, followed by the plain fallback line
  `plain card face, no additional ornament beyond the pip symbols,` (appended because
  both `layers.decor.pip` and `layers.ornaments.pip` are false).
- `[FRAME_LINE]` (`layers.frame.pip = false`) is omitted entirely.
- There is no center dividing line — that's COURT-only (reversible two-headed layout).

```
9:14 aspect ratio, full card visible, transparent background outside the card,
Two of Spades playing card,
aged ivory playing-card stock, subtle paper grain,
sharp crisp black outlines, fine engraved linework with dense cross-hatching on all illustrated elements and ornamental details,
vintage chromolithographic playing-card illustration,
matte finish,
slight vintage printing imperfections,
highly detailed Austrian-style playing card,
plain card face, no additional ornament beyond the pip symbols,
four corner indices, each with rank 2 stacked above suit symbol ♠, standard small index size, upper indices upright, lower indices rotated 180 degrees,
2 black spade pip symbols arranged in the traditional symmetrical layout for the Two, upper-half pips upright, lower-half pips rotated 180 degrees,
black spade suit symbols,
no watermark
```

## Decorated — `layers.decor.pip`, `layers.ornaments.pip`, `layers.frame.pip` all true

Same card, with the wizard's "Decorated" option chosen and
`extras.ornaments.pip = "small ornamental corner flourishes around each index"`.

- **Background** stays, as always.
- **Decor** is kept (`rich crimson red, royal cobalt blue, burnished gold accents,`).
- **Ornaments** is on: Austrian's Ornaments section is empty, so only
  `extras.ornaments.pip` contributes, as its own phrase.
- **Highlights** stays off (not set).
- **Center motif style** drops the figure-only line as always; **Finish** stays. No
  "plain card face..." line in this branch — decor and ornaments are both on.
- `[FRAME_LINE]` is included (`layers.frame.pip = true`).

```
9:14 aspect ratio, full card visible, transparent background outside the card,
Two of Spades playing card,
aged ivory playing-card stock, subtle paper grain,
rich crimson red, royal cobalt blue, burnished gold accents,
small ornamental corner flourishes around each index,
sharp crisp black outlines, fine engraved linework with dense cross-hatching on all illustrated elements and ornamental details,
vintage chromolithographic playing-card illustration,
matte finish,
slight vintage printing imperfections,
highly detailed Austrian-style playing card,
thin single black border with stepped corner cut-ins framing the index areas,
four corner indices, each with rank 2 stacked above suit symbol ♠, standard small index size, upper indices upright, lower indices rotated 180 degrees,
2 black spade pip symbols arranged in the traditional symmetrical layout for the Two, upper-half pips upright, lower-half pips rotated 180 degrees,
black spade suit symbols,
no watermark
```
