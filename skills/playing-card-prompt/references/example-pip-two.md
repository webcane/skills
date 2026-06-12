# Example target prompt — PIP card

A fully assembled PIP prompt (Two of Spades, French deck, Austrian style, 9:14). Use
it as a reference for how `[STYLE_BLOCK_PIP]` and `[FRAME_LINE]` resolve for PIP cards,
and as a sanity check after assembly.

## Default — `content_style.pip = false`, `frame.pip = false` (plain pip)

Compared to the Austrian `[STYLE_BLOCK]` used verbatim on COURT cards:
- The accent line (`rich crimson red, royal cobalt blue, burnished gold accents,`) is
  dropped — no extra decoration beyond the suit's own color.
- The figure-only line (`warm ochre skin tones,`) is dropped — there's no portrait.
- `plain card face, no additional ornament beyond the pip symbols,` is appended after
  the remaining style lines.
- `[FRAME_LINE]` (the bordered-index-area line) is omitted entirely.
- There is no center dividing line — that's COURT-only (reversible two-headed layout).

```
9:14 aspect ratio, full card visible, transparent background outside the card,
Two of Spades playing card,
sharp crisp black outlines, fine engraved linework with dense cross-hatching on all illustrated elements and ornamental details,
vintage chromolithographic playing-card illustration,
aged ivory playing-card stock,
subtle paper grain,
matte finish,
slight vintage printing imperfections,
highly detailed Austrian-style playing card,
plain card face, no additional ornament beyond the pip symbols,
four corner indices, each with rank 2 stacked above suit symbol ♠, standard small index size, upper indices upright, lower indices rotated 180 degrees,
2 black spade pip symbols arranged in the traditional symmetrical layout for the Two, upper-half pips upright, lower-half pips rotated 180 degrees,
black spade suit symbols,
no watermark
```

## Decorated — `content_style.pip = true`, `frame.pip = true`

Same card, with the wizard's "Decorated" option chosen and
`pip_decoration_extra = "small ornamental corner flourishes around each index"`.
The accent line is kept (figure-only line is still dropped), `[FRAME_LINE]` is
included, and the extra decoration is appended as its own phrase — no
"plain card face..." line in this branch.

```
9:14 aspect ratio, full card visible, transparent background outside the card,
Two of Spades playing card,
sharp crisp black outlines, fine engraved linework with dense cross-hatching on all illustrated elements and ornamental details,
vintage chromolithographic playing-card illustration,
rich crimson red, royal cobalt blue, burnished gold accents,
aged ivory playing-card stock,
subtle paper grain,
matte finish,
slight vintage printing imperfections,
highly detailed Austrian-style playing card,
small ornamental corner flourishes around each index,
thin single black border with stepped corner cut-ins framing the index areas,
four corner indices, each with rank 2 stacked above suit symbol ♠, standard small index size, upper indices upright, lower indices rotated 180 degrees,
2 black spade pip symbols arranged in the traditional symmetrical layout for the Two, upper-half pips upright, lower-half pips rotated 180 degrees,
black spade suit symbols,
no watermark
```
