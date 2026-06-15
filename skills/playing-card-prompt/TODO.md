# TODO

- [ ] Card back: support generating a prompt for the deck's card back design
- [ ] Joker card: support the Joker as a card type/rank in the wizard
- [ ] Special card: support custom/special cards outside the standard rank set
- [ ] Title: support adding a title/text overlay to the card
- [ ] Split: control whether the card is split into mirrored halves (and how — horizontal edge-to-edge vs. angled around the figures) or shows full-body figures without a split
- [ ] Seamless design: support a connecting/seamless design across the card (or across the deck)
- [ ] Config mode: add a "layers overview" sub-step near Step 6 that prints the full 7-layer x 3-group (court/pip/ace) matrix for the active profile (via `manage_config.py show`/`profile show <name>`), and lets the user edit it with free-text targeting (e.g. "highlights включи везде", "figure у pip тоже") translated into `manage_config.py set layers.<layer>.<group> true/false` calls — acts as a fast path before/instead of the guided 6.1-6.4 questions
