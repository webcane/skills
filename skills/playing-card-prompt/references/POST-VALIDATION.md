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
  contradiction-free; replacements from Step 10/11 fully replace (not coexist with) the
  traditional item they replace, and reference-transfer attributes (Step 11) outrank
  Step 10, which outranks the traditional defaults.
- [ ] **Style block integrity** — `[STYLE_BLOCK]` follows "Layers and `[STYLE_BLOCK]`
  assembly" in `references/REFERENCE.md` for this card's group: background/decor/
  ornaments/highlights/technique lines appear only when `layers.<layer>.<group>` is
  not `"false"` (with each layer's addition — its cell's text, if not
  `"true"`/`"false"` — appended when the layer is on), then — only if
  `layers.figure.<group>` is on — the pattern's Figure detail lines (skipped if that
  section is `(none)`) and its Face Style line, then the pattern's Finish lines (only
  if `layers.technique.<group>` is on — same gate as the Technique lines; dropped
  together with Technique if that layer is off), then
  `[MOOD_LINE]`/`layers.mood.<group>`'s addition if applicable, and the `plain card
  face, no additional ornament beyond the pip symbols,` fallback is present for PIP
  when decor, ornaments, and highlights are all off. Nothing from an enabled layer is
  summarized, reordered, or dropped. The resolved text is identical across all cards
  of the same group generated for the same deck/session.
- [ ] **Frame line** — `[FRAME_LINE]` matches the chosen `frame` preset's "Frame line"
  in `assets/frame/<frame>.md` (default `boxed-index`: `thin single black border around
  the card perimeter, plus a separate thin black border individually framing each of the
  four corner index areas,`) verbatim, plus `layers.frame.<group>`'s addition appended
  if its cell is custom text, and is present only if `layers.frame.<group>` is on for
  this card's group; otherwise the line is absent entirely (not an empty placeholder).
  The resolved text is identical across all cards of the same group generated for the
  same deck/session.
- [ ] **Mood line** — `[MOOD_LINE]` and any `layers.mood.<group>` addition are present
  only if `layers.mood.<group>` is on for this card's group, and only if the
  respective `mood`/addition is non-empty; the text matches those settings verbatim;
  otherwise the corresponding line is absent entirely.
- [ ] **Figure detail line** — the chosen pattern's "Figure detail" lines (when that
  section is not `(none)`) appear within `[STYLE_BLOCK]` immediately following the
  Technique lines (or in that position if `layers.technique.<group>` is off) if and
  only if `layers.figure.<group>` is on for this card's group, matching that pattern's
  `assets/pattern/<style>.md` "Figure detail" section verbatim. Otherwise (figure off,
  or the section is `(none)`) no such line appears.
- [ ] **Face style line** — the chosen pattern's "Face Style" line appears within
  `[STYLE_BLOCK]` (right after the Figure detail lines, or in the Technique/Figure
  detail position if Figure detail is `(none)`) if and only if
  `layers.figure.<group>` is on for this card's group, and its text matches that
  pattern's `assets/pattern/<style>.md` "Face Style" section verbatim. If that line
  describes an obscured or mask-like treatment, `[CHARACTER_FEATURES]` contains no
  separate facial description. Otherwise (figure off) the line is absent entirely.
- [ ] **Figure proportion line** — if `figure_proportion` is non-empty and
  `layers.figure.<group>` is on for this card's group, its text (from
  `assets/figure-proportion/<name>.md` or custom) appears within `[STYLE_BLOCK]`
  immediately after the Face Style line / `layers.figure.<group>`'s addition,
  identical across all cards of the same group/deck. If `figure_proportion` is empty
  or `layers.figure.<group>` is `"false"`, no such line appears.
- [ ] **Theme-derived ornaments/highlights/frame** — if `theme` is set and a
  `layers.ornaments`/`layers.highlights`/`layers.frame` cell was exactly `"true"` (on,
  no explicit addition) for an enabled layer, the derived phrase reflects `theme` and
  is reused identically across all cards of the same group/deck; an explicit addition
  on `layers.ornaments`/`layers.highlights`/`layers.frame` was never overridden by a
  derived one. `layers.background`/`layers.decor`/`layers.mood` have no theme fallback
  — a cell of exactly `"true"` simply has no addition.
- [ ] **Character description (figure cards)** — `[CHARACTER_NAME]` and
  `[CHARACTER_FEATURES]` are both present and non-empty; if derived from a reference
  image (Step 9-A), the description reflects what was actually returned, not a
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
