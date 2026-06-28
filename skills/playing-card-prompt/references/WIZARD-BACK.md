# Back Card Wizard

Steps B1–B7, run by `SKILL.md`'s Step 3 instead of Steps 4.1–4.2 when the chosen rank is Back. Read it when the user is generating a Back card.

### Steps B1–B7 — Back card only (run instead of Steps 4.1–4.2 when rank is Back)

Steps B1–B5 are **per-card** (ephemeral): each step is asked fresh every time a Back
card is generated, with no skip-guard checking a stored config value and no
`manage_config.py set` call. The chosen value is held in-session for this card only
and fed into `[BACK_DESIGN]`/STYLE_BLOCK assembly; nothing about B1–B5 is written to
`config.json`. Step B6 (back frame) still sets the real persistent
`layers.frame.back` cell, same as today. Step B7 is **per-card** and always runs.

**Step B1 — Back purpose · _per-card_**

Ask: "What is this deck back designed for?" Options (3):
- **Classic** — load `assets/back/purpose/classic.md`
- **Designer** — load `assets/back/purpose/designer.md`
- **Casino** — load `assets/back/purpose/casino.md`

The chosen value is used for this card's `[BACK_DESIGN]` only — not saved.

**Step B2 — Back design category · _per-card_**

Ask: "What type of back design?" Options (4): Geometric | Botanical | Abstract |
Illustrated. No asset loaded at this step — this card's choice determines B3's
option list (D-05). Not saved.

**Step B3 — Back pattern · _per-card_**

Ask: "Choose a specific pattern:" — show all 4 named options from
`assets/back/design/<back_design>/` based on this card's B2 answer (the
`AskUserQuestion` 4-option limit is fully consumed by these 4 named presets; the tool's
automatic "Other" slot covers freeform input, matching the pattern used in Step 7's
mood options). `allowed_back_patterns(category)` in `manage_config.py` remains
available to enumerate the 4 options per category if a step needs to call it
programmatically (kept as a standalone helper per Plan 02), or the four lists below
can be used directly — both describe the same fixed mapping:

- **Geometric** → Diamond / Cross-hatch / Hexgrid / Wave
- **Botanical** → Vine / Floral / Leaf / Branch
- **Abstract** → Interlacing / Color-field / Paint-stroke / Fractal
- **Illustrated** → Thematic / Portrait / Landscape / Heraldic

Load `assets/back/design/<back_design>/<choice>.md` for this card's `[BACK_DESIGN]`.
"Other" → ask for freeform description, used verbatim. Not saved.

> **D-21 fallback:** If this card's B2 answer is custom text (not a known category
> alias — `geometric`, `botanical`, `abstract`, `illustrated`), B3 defaults to showing
> the `geometric` category's 4 named options. The custom B2 value is still used for
> this card; only the B3 option list falls back to geometric.

**Step B4 — Back palette · _per-card_**

Ask: "Color palette for the back?" Options (4):
- **Classic red** — load `assets/back/palette/classic-red.md`
- **Classic blue** — load `assets/back/palette/classic-blue.md`
- **Dark** — load `assets/back/palette/dark.md`
- **Gold** — load `assets/back/palette/gold.md`

Custom palette: if user wants a different palette, accept free text. Used for this
card's `[BACK_DESIGN]` only — not saved.

**Step B5 — Back symmetry · _per-card_**

Ask: "Symmetry type?" Options (3):
- **180° rotational** — load `assets/back/symmetry/rotational-180.md`
- **Bilateral** — load `assets/back/symmetry/bilateral.md`
- **Asymmetric** — load `assets/back/symmetry/asymmetric.md`

This value is used in STYLE_BLOCK step 10 (see `references/REFERENCE.md` — back-group
symmetry is always appended from this card's B5 answer) for this card only — not
saved.

**Step B6 — Back frame · _persistent_**

_Skipped if `layers.frame.back` is already explicitly set._ Ask: "Include a frame
border on the back card?"
- **Yes, use active frame preset** — confirm `layers.frame.back = "true"` (default; no
  change needed if already `"true"`)
- **No frame** — set `layers.frame.back = "false"`

**Step B7 — Back exclusions · _per-card (optional)_**

Ask: "Anything to exclude from this back design?" Freeform. Phrase each as "no <thing>"
and append to `[NEGATIVE_LIST]`. If nothing, skip.

---

**Assembling `[BACK_DESIGN]`:**
Concatenate in order, dropping any empty/unset field. All three values come from
THIS card's B1–B5 answers (per-card, never read from saved config):
1. Purpose line from `assets/back/purpose/<this card's B1 answer>.md` (or custom text verbatim)
2. Pattern line from `assets/back/design/<this card's B2 answer>/<this card's B3 answer>.md` (or custom text verbatim)
3. Palette line from `assets/back/palette/<this card's B4 answer>.md` (or custom text verbatim)

Symmetry is NOT included in `[BACK_DESIGN]` — it is added by STYLE_BLOCK step 10 (see
`references/REFERENCE.md`), using this card's B5 answer. Frame is NOT included in
`[BACK_DESIGN]` — it is included in `[FRAME_LINE]` via the persistent
`layers.frame.back` cell.
