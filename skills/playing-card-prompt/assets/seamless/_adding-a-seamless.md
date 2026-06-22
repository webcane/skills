# Adding a new seamless preset

Create `assets/seamless/<name>.md` with a short title, an optional one-line description,
and a fenced block — a single comma-terminated phrase describing the connecting/seamless
design treatment. The file stem becomes an allowed value for `layers.seamless.<group>`.

```markdown
# Seamless: <Display Name>

<optional one-line description shown while picking>

## Seamless phrase
```
<seamless design phrase>,
```
```

**Important notes:**

- `layers.seamless.<group>` is `"false"` (off), `"true"` (on, resolves to a default
  alias — the first/canonical preset on disk), `"<alias>"` (one of the file stems
  here), or `"<custom_text>"` (freeform, used verbatim). There is no `"none"` value —
  only `"false"` means no seamless design.
- `"true"` is never persisted literally: `manage_config.py`'s `cmd_set` resolves it to
  a default alias immediately, the same way `layers.figure.<group>="true"` resolves to
  a group's default figure type.
- `layers.seamless.<group>` is only valid for `court`, `pip`, `ace`, and `joker`. `back`
  and `special` are restricted to `"false"` only — there is no figure-bearing seamless
  use case for those two groups.
- Only add a file for seamless designs that contribute actual prompt text.

Keep seamless phrases short and comma-terminated, consistent with the existing asset files.
