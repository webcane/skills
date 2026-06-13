# TODO

- [ ] Card back: support generating a prompt for the deck's card back design
- [ ] Joker card: support the Joker as a card type/rank in the wizard
- [ ] Special card: support custom/special cards outside the standard rank set
- [ ] Title: support adding a title/text overlay to the card
- [ ] Court proportion: control figure framing/size consistency across court cards (bust, waist-up, 3/4, 7/8, full body, etc.)
- [ ] Split: control whether the card is split into mirrored halves (and how — horizontal edge-to-edge vs. angled around the figures) or shows full-body figures without a split
- [ ] Seamless design: support a connecting/seamless design across the card (or across the deck)

## Config: `extras.<layer>.<group>` generalization

- [ ] Migrate `ornaments_extra`/`highlights_extra` to `extras.ornaments`/`extras.highlights`
- [ ] Add `extras.background.<group>` free-text addition
- [ ] Add `extras.decor.<group>` free-text addition
- [ ] Add `extras.mood.<group>` per-group mood addition
- [ ] Make frame asset-based (`assets/frames/<name>.md`)
- [ ] Add `extras.frame.<group>` free-text addition (depends on frame asset support)
- [ ] Automate face_style source resolution (pattern vs. reference image)
- [ ] Keep "Center motif style" and "Face Style" as separate pattern sections (doc clarification)
- [ ] Update CONFIG.md schema docs for `extras.<layer>.<group>`
- [ ] Update WIZARD-STEP-MAP.md for `extras.*` and frame asset step
- [ ] Update manage_config.py for `extras.*` dotted keys and migration
