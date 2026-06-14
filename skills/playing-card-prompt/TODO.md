# TODO

- [ ] Card back: support generating a prompt for the deck's card back design
- [ ] Joker card: support the Joker as a card type/rank in the wizard
- [ ] Special card: support custom/special cards outside the standard rank set
- [ ] Title: support adding a title/text overlay to the card
- [ ] Split: control whether the card is split into mirrored halves (and how — horizontal edge-to-edge vs. angled around the figures) or shows full-body figures without a split
- [ ] Seamless design: support a connecting/seamless design across the card (or across the deck)
- [ ] Merge layers/extras: fold `extras.<layer>.<group>` into `layers.<layer>.<group>`, turning each cell from a bool into `{enabled, extra}` — drops the `extras` namespace entirely while keeping the `layers` prefix (avoids collision with top-level scalar settings that share a layer name, e.g. `frame`/`mood`). Requires updating `manage_config.py` (`EXTRA_LAYERS`, `_migrate_extras`, path validation/`PERSISTENT_KEYS`) and all `extras.<layer>.<group>` references in `CONFIG.md`/`SKILL.md`/`REFERENCE.md`
