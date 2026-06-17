# Adding a new special card type

Create `assets/special/<name>.md` with a short title, an optional one-line description,
and a "Special type line" fenced block — a single comma-separated phrase (trailing comma
kept) describing the special card's composition and identity. The wizard (Special rank
flow) lists every `*.md` here (except files starting with `_`) as a special card type
option, and uses the "Special type line" text as the type's contribution to the SPECIAL
template.

```markdown
# Special Card Type: <Display Name>

<optional one-line description shown while picking>

## Special type line
```
<composition phrase>, <another phrase>,
```
```

Keep the phrase focused on card composition and identity — per-card name and figure
description are collected separately by the wizard (Steps S3–S4). Custom special types
typed directly by the user bypass the asset lookup and go directly into the SPECIAL
template as free text.
