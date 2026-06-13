# Adding a new mood preset

Create `assets/mood/<name>.md` with a short title, an optional one-line description,
and a "Mood line" fenced block — a single comma-separated phrase (trailing comma kept)
describing the deck's overall atmosphere. The wizard (Step 7) lists every `*.md` here
(except files starting with `_`) as a mood option, and uses the "Mood line" text
verbatim as `[MOOD_LINE]` / the `mood` config value when chosen.

```markdown
# Mood: <Display Name>

<optional one-line description shown while picking>

## Mood line
```
<atmosphere phrase>, <another descriptive phrase>,
```
```

Keep it to one or two short phrases — `[MOOD_LINE]` is appended as its own segment
within `[STYLE_BLOCK]`, after the pattern's Finish lines (see "Layers and
`[STYLE_BLOCK]` assembly" in `references/REFERENCE.md`). Custom moods typed directly by
the user in Step 7 follow the same one-line, comma-terminated convention but aren't
saved as a file.
