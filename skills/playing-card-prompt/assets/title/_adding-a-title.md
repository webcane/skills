# Adding a new title preset

Create `assets/title/<name>.md` with a short title, an optional one-line description,
and a fenced block — a single comma-terminated phrase describing the title
placement/style treatment. The file stem becomes a selectable per-card alias offered
in the title wizard step.

```markdown
# Title: <Display Name>

<optional one-line description shown while picking>

## Title phrase
```
<title placement phrase>,
```
```

**Important notes:**

- Title has **no** deck-wide persistent config cell of its own (no `layers.*`-style
  entry under that name). Title is never stored in `config.json` — unlike most other
  layers, title has no persisted value to resolve.
- The file stem is offered as a **per-card suggested default by group**: Joker →
  `below-figure`, Court → `side-running`, pip / ace / back / special → no title
  suggested by default. The user may accept the suggested alias, pick any other alias,
  or enter custom text fresh each time a card is generated — the suggestion is just a
  starting point, not a stored setting.
- The title TEXT itself (the actual words shown on the card) is collected per-card and
  is ephemeral, the same way `extra_attributes`, `reference_transfers`, and
  `exclusions` are — asked fresh every time, never written to `config.json`.
- Per TITL-03, the phrase describes placement/style only — no font family, point size,
  or color. Those are SVG-template concerns, not prompt concerns.

Keep title phrases short and comma-terminated, consistent with the existing asset files.
