---
description: Merge validated language studies into the cross-language matrix and run self-review
argument-hint: "[--root studies] [--review-only]"
---

Merge and review the dialectical studies in `$ARGUMENTS` (default root: `./studies`).

Then:

1. If `studies/synthesis/decision.md` does not exist, create the directory and a 7-section
   skeleton (`pl-dialectics/references/decision-template.md`). This is the only summary
   document; per-language `decision.md` files stay untouched.
2. Run `scripts/merge_matrix.py --root <root>` and report the axis cells that are empty or
   disputed.
3. Run `scripts/self_review.py --root <root>` and report the per-criterion verdicts.
4. Fill `studies/synthesis/decision.md` by aggregating the per-language decision records:
   one decision per cluster of languages, each traceable to `(language, ID)` pairs.
   Do not create new IDs. Do not average positions; name the disagreement instead.
5. If `--review-only` was passed, stop after step 3 and do not write the synthesis.

Never edit a per-language `study.md` during merge. A defect found here goes back to that
language's run.
