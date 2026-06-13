# Image generator config

Defines the optional `image_generator` persistent setting and how it is applied
during assembly ("Engine-aware prompt formatting").

## Field

| Field              | Values                                                                      | Default      |
|--------------------|------------------------------------------------------------------------------|--------------|
| `image_generator`  | `nanobanana`, `stable-diffusion`, `midjourney`, `dalle`, `kaze`, or any custom name | `nanobanana` |

`nanobanana` needs no special handling — the base templates in
`references/REFERENCE.md` (inline `[NEGATIVE_LIST]`, `[ASPECT_RATIO] aspect ratio,`
lead-in) already target it. Every other engine has a file in this folder describing
the deltas to apply on top of the base assembled prompt.

## Wizard behavior (Step 12)

- Optional. Skipped entirely if `image_generator` is already saved in `config.json`
  — go straight to a one-line mention of which engine is in use.
- Otherwise ask once, with NanoBanana as the default/first option, and offer to save
  the answer to `config.json` like the other persistent settings (deck, lettering,
  style, aspect ratio).
- For an engine the user names that has no matching `assets/engines/<name>.md`,
  fall back to the NanoBanana format and say no engine-specific adaptation was
  applied.

## Per-engine files

Each `assets/engines/<engine>.md` (besides this one) documents three deltas applied
during assembly:

1. **Negative handling** — inline `[NEGATIVE_LIST]` (default) vs. moved to a
   separate block/field, and that field's exact label.
2. **Aspect ratio syntax** — how `[ASPECT_RATIO]` is expressed: inline phrase,
   `--ar` flag, or a converted pixel size.
3. **Extra parameters** — any engine-specific suffix flags or notes to append.
