# Post-validation Checklist

Run this checklist against the assembled prompt before presenting it (see
"Assembling the prompt" step 8 in `SKILL.md`). If any check fails, correct the
relevant field in place and re-run the checklist — don't ask the user to fix it
unless the failure stems from missing/ambiguous information only they can resolve
(e.g. no character name given at all).

- [ ] **No raw placeholders** — no literal `[PLACEHOLDER]`-style token remains anywhere.
- [ ] **Lettering consistency** — `RANK_LETTER` matches the lettering system from Step 2
  (e.g. Russian → К/Д/В, not K/Q/J), and the rank/suit pairing matches Step 3–4.
- [ ] **Suit consistency** — `SUIT_NAME`, `SUIT_SYMBOL`, `SUIT_COLOR` belong to the same
  suit and to the deck chosen in Step 1 (no mixing, e.g. Spades symbol with Acorns name).
- [ ] **Attribute resolution** — `[RESOLVED_ATTRIBUTES]` is deduplicated and
  contradiction-free; replacements from Step 9/10 fully replace (not coexist with) the
  traditional item they replace, and reference-transfer attributes (Step 10) outrank
  Step 9, which outranks the traditional defaults.
- [ ] **Style block integrity** — `[STYLE_BLOCK]` follows "Layers and `[STYLE_BLOCK]`
  assembly" in `references/REFERENCE.md` for this card's group: background/decor/
  ornaments/highlights lines appear only when `layers.<layer>.<group>` is `true` (with
  `extras.background`/`extras.decor`/`extras.ornaments`/`extras.highlights` appended
  when their layer is on), followed by the center-motif style (figure-only line
  included only if `layers.figure.<group>` is `true`), then the pattern's Face Style
  line (also only if `layers.figure.<group>` is `true`), then finish lines, then
  `[MOOD_LINE]`/`extras.mood.<group>` if applicable, and the `plain card face, no
  additional ornament beyond the pip symbols,` fallback is present for PIP when decor,
  ornaments, and highlights are all off. Nothing from an enabled layer is summarized,
  reordered, or dropped. The resolved text is identical across all cards of the same
  group generated for the same deck/session.
- [ ] **Frame line** — `[FRAME_LINE]` matches the chosen `frame` preset's "Frame line"
  in `assets/frame/<frame>.md` (default `stepped-corners`: `thin single black border
  with stepped corner cut-ins framing the index areas,`) verbatim, plus
  `extras.frame.<group>` appended if set, and is present only if
  `layers.frame.<group>` is `true` for this card's group; otherwise the line is absent
  entirely (not an empty placeholder). The resolved text is identical across all cards
  of the same group generated for the same deck/session.
- [ ] **Mood line** — `[MOOD_LINE]` and any `extras.mood.<group>` addition are present
  only if `layers.mood.<group>` is `true` for this card's group, and only if the
  respective `mood`/`extras.mood.<group>` setting is non-empty; the text matches those
  settings verbatim; otherwise the corresponding line is absent entirely.
- [ ] **Face style line** — the chosen pattern's "Face Style" line appears within
  `[STYLE_BLOCK]` (right after the center-motif style) if and only if
  `layers.figure.<group>` is `true` for this card's group, and its text matches that
  pattern's `assets/pattern/<style>.md` "Face Style" section verbatim. If that line
  describes an obscured or mask-like treatment, `[CHARACTER_FEATURES]` contains no
  separate facial description. Otherwise (figure off) the line is absent entirely.
- [ ] **Theme-derived ornaments/highlights/frame** — if `theme` is set and an
  `extras.ornaments`/`extras.highlights`/`extras.frame` slot was empty for an enabled
  layer, the derived phrase reflects `theme` and is reused identically across all
  cards of the same group/deck; an explicit `extras.ornaments`/`extras.highlights`/
  `extras.frame` value was never overridden by a derived one. `extras.background`/
  `extras.decor`/`extras.mood` have no theme fallback — left empty if unset.
- [ ] **Character description (figure cards)** — `[CHARACTER_NAME]` and
  `[CHARACTER_FEATURES]` are both present and non-empty; if derived from a reference
  image (Step 8-A), the description reflects what was actually returned, not a
  generic placeholder.
- [ ] **Negative list** — the negative content (from Step 11) contains only "no …"
  exclusion phrases (or the engine's equivalent), deduplicated, with no positive
  attributes leaking in.
- [ ] **Aspect ratio** — the aspect ratio is a concrete `W:H` ratio (from Step 12 or
  the user's custom value) or its engine-specific equivalent (pixel size, `--ar`,
  fixed size), not descriptive text.
- [ ] **Template match** — the COURT/PIP/ACE template matches the resolved rank, and no
  figure-only fields (character, attributes, negatives) appear in a PIP/ACE prompt
  whose group has `layers.figure.<group>` set to `false`.
- [ ] **Engine formatting** — the chosen `image_generator` (Step 13)'s negative
  handling, aspect-ratio syntax, and extra parameters from
  `assets/engines/<engine>.md` are all applied; for `nanobanana` the prompt matches
  the base template unchanged.
