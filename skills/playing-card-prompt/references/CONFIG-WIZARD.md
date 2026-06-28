# Config Wizard

Full 11-step persistent-settings flow run by `SKILL.md`'s Config mode (`--init` / `--config`). Read it when the user enters Config mode.

## Mode: Config (`--init` / `--config`)

**Step 0 — Profile.** Run `python3 scripts/manage_config.py profile list`. If more
than one profile exists, or the user's message implies they want a different "look"
(e.g. "set up a new deck profile"), ask whether to: continue editing the active
profile, switch to an existing one (`profile switch <name>`), or create a new one
(`profile create <name>`, optionally `--from <existing>` to clone the active
profile's settings as a starting point). Otherwise skip straight to Step 1 and edit
the active profile.

Then walk the user through **only the persistent settings** (items 1–8 below, plus
index settings if asked). Show current values for the target profile (from `profile
show`) so the user can accept or change each one. At the end, persist each value with
`python3 scripts/manage_config.py set <key> <value>` (it validates and writes to the
active profile in `config.json`; pass `--profile <name>` if editing a non-active
profile), then confirm.

Steps to ask in config mode (Structure moved to position 2, mirroring `SKILL.md`
Step 1b's resequenced position right after Deck type — WIZ-03/D-12):
1. Deck type
2. Structure — full card (`full`, default) or center-illustration-only
   (`illustration`, for users compositing the artwork into their own SVG/HTML card
   template that already supplies the frame and corner indices). See "`structure`
   setting" in `references/REFERENCE.md` for what changes under `illustration`.
3. Court lettering system
4. Visual style / pattern
5. Card decoration layers and theme (Step 6)
6. Mood / atmosphere (Step 7)
7. Figure block — figure_scale (deck-wide scale), split (per-group split layout),
   figure_type (per-group character/building/animal/custom),
   character_framing (deck-wide framing, character-only), and seamless
   (per-group connecting/seamless design) — from the figure-block steps
   (Steps 8a–8f)
8. Aspect ratio (Step 13)
9. Image generator (optional — see Step 14)
10. Joker index (D2) — `index.count` (placement: `4-index` / `2-index` / `top-only` /
    `none`) and `index.symbol` (glyph: `star-in-circle` / `star` / `Jkr` / `crown` /
    `jester-face` / `none` / custom). Only surface when the user mentions Joker
    settings or asks explicitly.
11. (Optional, only if user asks) Standard index settings, or per-layer overrides via
    `layers.<layer>.<group>` for Court/Pip/Ace (e.g. `layers.ornaments.ace`,
    `layers.figure.pip`, `layers.mood.court`). Turning on `layers.figure.pip` or
    `layers.figure.ace` (transformation decks) makes Steps 8–12 apply to pip/ace
    cards too, the same way they apply to court by default.
