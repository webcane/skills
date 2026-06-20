# Joker Wizard

Steps 4.1–4.2, run by `SKILL.md`'s Step 3 instead of Step 4 when the chosen rank is Joker. Read it when the user is generating a Joker card.

### Steps 4.1–4.2 — Joker-only (run instead of Step 4 when rank is Joker)

**Step 4.1 — Joker type · _per-card_**

Ask which type of Joker this is. This fills `[JOKER_ROLE]` in the JOKER template.
Options:
- **Big Joker (Full)** — primary Joker; vivid full-color elaborate composition. `[JOKER_ROLE]` = `Big Joker, full-color vivid elaborate palette`
- **Little Joker (Half)** — secondary Joker; simpler, subdued or monochrome. `[JOKER_ROLE]` = `Little Joker, simplified subdued monochrome palette`
- **Wild / Trump Joker** — European tradition (Narr / Fool); unpaired. `[JOKER_ROLE]` = `Wild Joker, European fool-card tradition, unpaired`
- **Custom** — user supplies their own type/color/variant description

**Step 4.2 — Joker index placement + symbol · _persistent_ (skipped if loaded from config)**

Ask two things for the Joker's corner indices (Menu D2 — see `assets/index/options.md`):

**Placement** (`index.count`):
- **4-corner** (default) — all four corners
- **2-corner** — top-left and bottom-right only
- **Top-only** — single top-left index
- **None / Full-bleed** — no corner indices

**Symbol** (`index.symbol`, skipped if placement is None):
- **star-in-circle** (default) — `a star enclosed in a circle glyph`
- **star** — `a five-pointed star`
- **Jkr** — `the text "Jkr"`
- or Other: `J`, `crown`, `jester-face`, any custom glyph/text

Save choices via `python3 scripts/manage_config.py set index.count <value>` and
`python3 scripts/manage_config.py set index.symbol <value>`.
