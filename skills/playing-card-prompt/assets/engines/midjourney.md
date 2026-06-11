# Engine: Midjourney

1. **Negative handling** — remove the trailing `[NEGATIVE_LIST]` line from the main
   prompt body and convert it into a `--no` parameter at the very end of the
   prompt, stripping the leading `no ` from each item (`--no` already implies it):

   `--no watermark, cannon, winter landscape, fortress, table with documents, background objects`

2. **Aspect ratio syntax** — drop the `[ASPECT_RATIO] aspect ratio,` lead-in phrase
   and instead append `--ar [ASPECT_RATIO]` as a parameter at the end of the
   prompt.

3. **Extra parameters** — append `--v 7 --style raw` for a more literal,
   less Midjourney-default-stylized render. Final parameter order:

   `--ar [ASPECT_RATIO] --v 7 --style raw --no [comma-separated negatives]`
