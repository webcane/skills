# Adding a new pattern

Create `assets/pattern/<name>.md` with the layer sections below, each a fenced block of
short comma-phrases (trailing comma kept on every line). The wizard lists every `*.md`
here (except files starting with `_`) as a style option. See "Layers and `[STYLE_BLOCK]`
assembly" in `references/REFERENCE.md` for how these sections combine per card type
(Court / Pip / Ace) according to the `layers.*` config.

Ground the pattern in a specific era and/or cultural context (e.g. "Art Nouveau,
fin-de-siècle Europe", "ukiyo-e, Edo-period Japan", "Art Deco, 1920s") — this should
shape the color palette, ornament motifs, and "Center motif style" linework
consistently, not just the Finish line's name.

## Background
Base cardstock color/texture for the card (e.g. `aged ivory playing-card stock, subtle
paper grain,`). Always at least one line — this is the only layer that's on for every
group by default.

## Decor (background pattern)
Extra accent colors or background decoration beyond the suit's own color (e.g.
`rich crimson red, royal cobalt blue, burnished gold accents,`). Leave the fenced block
empty (just `(none)`) if the style has nothing here.

## Ornaments
Vignettes, corner flourishes, or decorative elements that are NOT the frame/border
itself. Often empty for a first draft — `extras.ornaments.<group>` (free text from the
wizard or config) is appended after whatever's here.

## Highlights / Overlays
Gilding, lacquer, glow, or shine phrasing that can sit on top of the figure/pips (e.g.
`gold leaf highlights catching the light along raised linework,`). Usually empty —
`extras.highlights.<group>` covers most cases via free text.

## Center motif style
The rendering style applied to whatever sits in the card's center (the portrait on
Court cards, the pip layout on number cards, the large suit symbol on Aces): linework,
illustration descriptor, and so on. Follow this order: linework → illustration
descriptor → (optional figure-only line, e.g. skin tones).

If one line only makes sense with a portrait (skin tones, facial rendering), mark it
explicitly below — it's included only if `layers.figure.<group>` is on for that group
(default: on for court, off for pip/ace):
- Figure-only line (drop unless `layers.figure.<group>` is on): `<line text>` (or "none")

## Face Style
One comma-phrase describing how this pattern renders a figure's face — typage,
expression, degree of stylization (e.g. idealized/archetypal vs. naturalistic vs.
obscured). Like the figure-only line above, this section is included only if
`layers.figure.<group>` is on for that group (default: on for court, off for pip/ace).
Ground it in the same era/culture as the rest of the pattern so a court figure's face
reads consistently with the pattern's overall aesthetic.

## Finish
Print-quality / final descriptor lines, ending with
`highly detailed <Name>-style playing card,`.
