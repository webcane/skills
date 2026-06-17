# TODO

- [ ] Card back: support generating a prompt for the deck's card back design
- [x] Joker card: support the Joker as a card type/rank in the wizard
- [ ] Special card: support custom/special cards outside the standard rank set
- [ ] Title: support adding a title/text overlay to the card
- [ ] Split: control whether the card is split into mirrored halves (and how — horizontal edge-to-edge vs. angled around the figures) or shows full-body figures without a split
- [ ] Seamless design: support a connecting/seamless design across the card (or across the deck)
- [ ] Config mode: add a "layers overview" sub-step near Step 6 that prints the full 7-layer x 3-group (court/pip/ace) matrix for the active profile (via `manage_config.py show`/`profile show <name>`), and lets the user edit it with free-text targeting (e.g. "highlights включи везде", "figure у pip тоже") translated into `manage_config.py set layers.<layer>.<group> true/false` calls — acts as a fast path before/instead of the guided 6.1-6.4 questions
- [ ] Figure types: add a per-card `figure_type` wizard step (character / building / animal / custom) that controls which sub-settings apply. Gate Face Style and `character_framing` on `figure_type == character` only. Add two deck-wide persistent fields: `figure_scale` (full bleed / inscribed in frame / small centered — applies to all figure types) and `character_framing` (head / bust / waist-up / 7/8 / full body — character only, replaces current `figure_proportion`). Update STYLE_BLOCK assembly to apply these gates in the sборщик rather than in pattern files.
