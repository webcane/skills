# Back Card Wizard

Steps B1–B7, run by `SKILL.md`'s Step 3 instead of Steps 4.1–4.2 when the chosen rank is Back. Read it when the user is generating a Back card.

### Steps B1–B7 — Back card only (run instead of Steps 4.1–4.2 when rank is Back)

Steps B1–B6 are **persistent** (deck-wide): each step checks if the config field is
already set; if so, silently skip it (no per-step value display, no consolidated
settings summary — go straight to the next unset step or to B7). Step B7 is
**per-card** and always runs.

**Step B1 — Back purpose · _persistent_**

_Skipped if `back_purpose` is already set in config._ Ask: "What is this deck back
designed for?" Options (4):
- **Classic** — load `assets/back/purpose/classic.md` → save `back_purpose = "classic"`
- **Designer** — load `assets/back/purpose/designer.md` → save `back_purpose = "designer"`
- **Casino** — load `assets/back/purpose/casino.md` → save `back_purpose = "casino"`
- **Custom text** — ask for free text → save `back_purpose = "<user text>"`

**Step B2 — Back design category · _persistent_**

_Skipped if `back_design` is already set in config._ Ask: "What type of back design?"
Options (4): Geometric | Botanical | Abstract | Illustrated.
Save `back_design = "<choice>"`. No asset loaded at this step — choice determines B3
options.

**Step B3 — Back pattern · _persistent_**

_Skipped if `back_pattern` is already set in config._ Ask: "Choose a specific pattern:"
— show all 4 named options from `assets/back/design/<back_design>/` based on B2 (the
`AskUserQuestion` 4-option limit is fully consumed by these 4 named presets; the tool's
automatic "Other" slot covers freeform input, matching the pattern used in Step 7's
mood options):

- **Geometric** → Diamond / Cross-hatch / Hexgrid / Wave
- **Botanical** → Vine / Floral / Leaf / Branch
- **Abstract** → Interlacing / Color-field / Paint-stroke / Fractal
- **Illustrated** → Thematic / Portrait / Landscape / Heraldic

Load `assets/back/design/<back_design>/<choice>.md` → save `back_pattern = "<choice>"`.
"Other" → ask for freeform description → save `back_pattern = "<user text>"`.

> **D-21 fallback:** If `back_design` is custom text (not a known category alias —
> `geometric`, `botanical`, `abstract`, `illustrated`), B3 defaults to showing the
> `geometric` category's 4 named options. The custom `back_design` value is still
> saved; only the B3 option list falls back to geometric.

**Step B4 — Back palette · _persistent_**

_Skipped if `back_palette` is already set in config._ Ask: "Color palette for the
back?" Options (4):
- **Classic red** — load `assets/back/palette/classic-red.md` → save `back_palette = "classic-red"`
- **Classic blue** — load `assets/back/palette/classic-blue.md` → save `back_palette = "classic-blue"`
- **Dark** — load `assets/back/palette/dark.md` → save `back_palette = "dark"`
- **Gold** — load `assets/back/palette/gold.md` → save `back_palette = "gold"`

Custom palette: if user wants a different palette, accept free text → save `back_palette = "<user text>"`.

**Step B5 — Back symmetry · _persistent_**

_Skipped if `back_symmetry` is already set in config._ Ask: "Symmetry type?"
Options (4):
- **180° rotational** — load `assets/back/symmetry/rotational-180.md` → save `back_symmetry = "rotational-180"`
- **Bilateral** — load `assets/back/symmetry/bilateral.md` → save `back_symmetry = "bilateral"`
- **Asymmetric** — load `assets/back/symmetry/asymmetric.md` → save `back_symmetry = "asymmetric"`
- **Custom text** — ask for free text → save `back_symmetry = "<user text>"`

This value is used in STYLE_BLOCK step 10 (see `references/REFERENCE.md` — back-group
symmetry is always appended from `assets/back/symmetry/<back_symmetry>.md`).

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
Concatenate in order, dropping any empty/unset field:
1. Purpose line from `assets/back/purpose/<back_purpose>.md` (or custom text verbatim)
2. Pattern line from `assets/back/design/<back_design>/<back_pattern>.md` (or custom text verbatim)
3. Palette line from `assets/back/palette/<back_palette>.md` (or custom text verbatim)

Symmetry is NOT included in `[BACK_DESIGN]` — it is added by STYLE_BLOCK step 10 (see
`references/REFERENCE.md`). Frame is NOT included in `[BACK_DESIGN]` — it is included
in `[FRAME_LINE]` via `layers.frame.back`.
