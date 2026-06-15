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
itself. Often empty for a first draft — `layers.ornaments.<group>`'s addition (custom
text from the wizard or config) is appended after whatever's here.

## Highlights / Overlays
Gilding, lacquer, glow, or shine phrasing that can sit on top of the figure/pips (e.g.
`gold leaf highlights catching the light along raised linework,`). Usually empty —
`layers.highlights.<group>`'s addition covers most cases via custom text.

## Center motif style
The rendering style applied to whatever sits in the card's center (the portrait on
Court cards, the pip layout on number cards, the large suit symbol on Aces): linework,
illustration descriptor, and so on. These lines apply regardless of whether the center
motif is a portrait, a pip layout, or a suit symbol — don't fold portrait-only details
(skin tones, facial rendering) in here; those belong in "Figure detail" below.

## Figure detail
Any additional rendering detail that only makes sense when the card's center motif is
a portrait — most often skin-tone/complexion treatment (e.g. `warm ochre skin tones,`).
Write `(none)` if this pattern has nothing extra to add for portraits beyond "Center
motif style". Don't write any assembly/config logic here (e.g. don't mention
`layers.*`) — whether this section is used for a given card is decided elsewhere (see
"Layers and `[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`), not by the pattern
file itself.

## Face Style
One comma-phrase describing how this pattern renders a figure's face — typage,
expression, degree of stylization (e.g. idealized/archetypal vs. naturalistic vs.
obscured). Ground it in the same era/culture as the rest of the pattern so a court
figure's face reads consistently with the pattern's overall aesthetic. As with "Figure
detail", whether this section is used for a given card is decided by
`references/REFERENCE.md`, not by this file.

## Finish
Print-quality / final descriptor lines, ending with
`highly detailed <Name>-style playing card,`.
