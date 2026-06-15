# Adding a new pattern

Create `assets/pattern/<name>.md` with the layer sections below, each a fenced block of
short comma-phrases (trailing comma kept on every line). The wizard lists every `*.md`
here (except files starting with `_`) as a style option. See "Layers and `[STYLE_BLOCK]`
assembly" in `references/REFERENCE.md` for how these sections combine per card type
(Court / Pip / Ace) according to the `layers.*` config.

Ground the pattern in a specific era and/or cultural context (e.g. "Art Nouveau,
fin-de-siècle Europe", "ukiyo-e, Edo-period Japan", "Art Deco, 1920s") — this should
shape the color palette, ornament motifs, and "Technique" linework consistently, not
just the Finish line's name.

## Technique vs. Functions

These sections answer two different questions — see "Technique vs. Functions" in `references/STYLE-COMPONENTS.md`:

- **Technique & Finish** — *how* the card is rendered (medium/linework/rendering, and
  the final print-quality descriptor). Both are gated together by the single
  `layers.technique.<group>` cell.
- **Background, Decor, Ornaments, Highlights** — *what* is added to the card and
  *where* (content placement, not rendering medium), each gated by its own
  `layers.<layer>.<group>` cell.

Don't mix the two: keep medium/linework/print-quality phrasing out of the content
layers, and keep content/placement phrasing out of "Technique" and "Finish".

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

## Technique
The rendering technique/medium applied to whatever sits in the card's center (the
portrait on Court cards, the pip layout on number cards, the large suit symbol on
Aces). These lines apply regardless of whether the center motif is a portrait, a pip
layout, or a suit symbol — don't fold portrait-only details (skin tones, facial
rendering) in here; those belong in "Figure detail" below. Gated by
`layers.technique.<group>` (on for every group by default).

Some example mediums to ground this in (pick and combine whatever fits the pattern's
era/culture — this isn't an exhaustive list):
- **Linework** — outline, hatching, cross-hatching, engraving (e.g. `fine engraved
  linework with dense cross-hatching on all illustrated elements,`).
- **Tonal / area-fill** — flat color shapes, block printing, silhouette work (e.g.
  `bold flat-color block-printed shapes with minimal outlines,`).
- **Painterly** — visible brushwork, watercolor washes, gouache (e.g. `soft watercolor
  washes with loose painterly brushwork,`).
- **Textures** — paper grain, woodblock texture, fabric weave showing through the
  illustration (e.g. `visible woodblock-grain texture throughout the illustration,`).
- **Gradients** — smooth tonal transitions, airbrush-style shading (e.g. `smooth
  airbrushed gradients shading the illustrated forms,`).
- **Collage** — cut-paper, mixed-media, layered composition (e.g. `cut-paper collage
  composition with layered geometric shapes,`).

## Figure detail
Any additional rendering detail that only makes sense when the card's center motif is
a portrait — most often skin-tone/complexion treatment (e.g. `warm ochre skin tones,`).
Write `(none)` if this pattern has nothing extra to add for portraits beyond
"Technique". Don't write any assembly/config logic here (e.g. don't mention
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
`highly detailed <Name>-style playing card,`. Shares "Technique"'s gate —
`layers.technique.<group>` (on for every group by default); dropped together with
"Technique" when that layer is off for a group.
