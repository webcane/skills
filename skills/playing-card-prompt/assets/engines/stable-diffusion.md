# Engine: Stable Diffusion (SD 1.5 / SDXL / Flux)

1. **Negative handling** — remove the trailing `[NEGATIVE_LIST]` line from the main
   prompt body and present it as a separate block immediately below the prompt:

   ```
   Negative prompt: no watermark, no cannon, no winter landscape, ...
   ```

2. **Aspect ratio syntax** — drop the `[ASPECT_RATIO] aspect ratio,` lead-in phrase
   and instead state the resolution as `WxH px` at the start of the prompt, using
   the closest match below (SDXL-friendly, multiples of 64):

   | Card aspect ratio           | SD resolution |
   |------------------------------|---------------|
   | 5:7 (Poker / Mini)            | 896x1216      |
   | 9:14 (Bridge / Preferans)      | 832x1280      |
   | 14:25 (European / Skat)       | 768x1344      |
   | 7:12 (Tarot)                  | 768x1344      |
   | custom                        | nearest 64-px multiple matching the ratio |

   Lead with both, e.g. `832x1280 px (9:14 aspect ratio), full card visible, ...`.

3. **Extra parameters** — none required. You may mention that the user's usual
   sampler/steps/CFG settings are applied separately in their tool — this skill
   does not generate them.
