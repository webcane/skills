# Engine: DALL·E (3)

1. **Negative handling** — DALL·E has no negative-prompt field. Drop the trailing
   `[NEGATIVE_LIST]` line and fold it into one short positive-avoidance clause in
   the main prompt instead of a per-item "no ..." list, e.g. `no watermark, no
   cannon, no winter landscape` becomes `plain background free of watermarks,
   weapons, or props beyond those described`.

2. **Aspect ratio syntax** — DALL·E 3 only accepts three fixed sizes. Drop
   `[ASPECT_RATIO] aspect ratio,` and instead state the closest fixed size:

   | Card aspect ratio                                  | DALL·E size           |
   |-----------------------------------------------------|-----------------------|
   | All portrait card ratios (5:7, 9:14, 14:25, 7:12)   | 1024x1792 (portrait)  |
   | Any landscape/custom wide ratio                     | 1792x1024 (landscape) |

   Tell the user the output will need to be cropped to the exact card ratio
   afterward, since DALL·E can't match it precisely.

3. **Extra parameters** — none. DALL·E takes plain prose only, no `--` flags.
