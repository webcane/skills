# Engine: kaze.ai

1. **Negative handling** — remove the trailing `[NEGATIVE_LIST]` line from the main
   prompt body and present it as a separate trailing block labeled `Negative:`:

   ```
   Negative: no watermark, no cannon, no winter landscape, ...
   ```

2. **Aspect ratio syntax** — drop the `[ASPECT_RATIO] aspect ratio,` lead-in phrase
   and instead place an inline `--ar [ASPECT_RATIO]` tag right before the
   `Negative:` block.

3. **Extra parameters** — none.
