# Example target prompts — engine variants

The same King of Spades from `references/example-court-king.md` (French deck,
Anglo-American letters, Austrian style, 9:14), adapted per
`assets/engines/<engine>.md`. Only the **lead-in line** and the **trailing
negative content** change — everything in between (style block, layout, index
line, portrait, attributes) stays identical to the NanoBanana version.

The shared middle (omitted below as `...`) is:

```
Peter the Great as King of Spades playing card,
sharp crisp black outlines, fine engraved linework with dense cross-hatching on face, hair, costume and fabric folds,
vintage chromolithographic playing-card illustration,
rich crimson red, royal cobalt blue, burnished gold accents,
warm ochre skin tones,
aged ivory playing-card stock,
subtle paper grain,
matte finish,
slight vintage printing imperfections,
highly detailed Austrian-style playing card,
thin single black border with stepped corner cut-ins framing the index areas,
four corner indices, each with rank K stacked above suit symbol ♠, standard small index size, upper indices upright, lower indices rotated 180 degrees,
large black spade suit symbols centered in upper and lower card fields,
thin black horizontal dividing line through the exact center of the card,
reversible two-way court card layout, identical upper and lower portraits rotated 180 degrees around the central horizontal axis, symmetrical costume design,
Tall strong-jawed mature man, dark short slightly wavy hair, neat prominent mustache, commanding authoritative pose, direct piercing confident gaze, early-18th-century military dress, royal crown (jeweled, closed imperial or open royal arch), dark green military caftan with gold buttons, light blue Order of Saint Andrew sash and star medallion, rapier held upright in the primary hand, rolled map in the secondary hand, enthroned, broad-shouldered frontal pose,
black spade suit symbols,
```

---

## Midjourney

`--ar` and the `--no` negatives move to the end; lead-in drops the
`9:14 aspect ratio,` phrase.

```
full card visible, transparent background outside the card,
...
--ar 9:14 --v 7 --style raw --no watermark, cannon, winter landscape, fortress, table with documents, background objects
```

---

## Stable Diffusion (SDXL)

The lead-in becomes a pixel size from the resolution table; negatives move to a
separate `Negative prompt:` block.

```
832x1280 px (9:14 aspect ratio), full card visible, transparent background outside the card,
...
```

```
Negative prompt: no watermark, no cannon, no winter landscape, no fortress, no table with documents, no background objects
```

---

## kaze.ai

`--ar` is placed inline before a separate `Negative:` block; lead-in drops the
`9:14 aspect ratio,` phrase.

```
full card visible, transparent background outside the card,
...
black spade suit symbols, --ar 9:14
```

```
Negative: no watermark, no cannon, no winter landscape, no fortress, no table with documents, no background objects
```

---

## DALL·E

Lead-in uses the closest fixed size (portrait); the negative list folds into one
positive-avoidance clause appended to the body instead of a trailing "no ..." list.

```
1024x1792, full card visible, transparent background outside the card,
...
black spade suit symbols,
plain background free of watermarks, weapons, or props beyond those described
```

Note to the user: crop the 1024x1792 output to 9:14 afterward.
