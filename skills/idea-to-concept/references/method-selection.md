# Method Selection — Routing Table

Choose a method by the *symptom* the problem exhibits, not by the problem's domain.

## Routing Table

| Symptom in the problem | Method | What it does | Typical trigger phrases |
|---|---|---|---|
| Ambiguous terms, unstated assumptions, possible hidden contradictions | socratic | Disciplined questioning to expose contradictions and force precise definitions | "it should work", "obviously", undefined terms, edge cases ignored |
| Two requirements in tension — both must be satisfied without compromise | triz | Resolve the contradiction by separating concerns; find the abstract solution | "but that conflicts with", "can't have both", "trade-off between X and Y" |
| Concept too complex, unclear, or needs to survive long-term use | einstein | Radical simplification — one-sentence explanation, remove one thing, check obviousness | "too complex", "doesn't age well", "hard to explain" |
| Unclear value — does this actually solve a real problem? | working-backwards | Start from the desired experience and reason backwards to requirements | "is this useful?", "who benefits?", speculative use case |
| A claim that needs testing — is this the simplest way? | scientific-method | Treat the claim as a hypothesis; separate known from assumed; design the minimal experiment | "this is the simplest", "nothing else can do this", "obviously better" |
| Fit with existing architecture or stated premises | logical-analysis | State premises, deduce consequences, test for contradiction, find hidden premises | "does this fit?", "consistent with our architecture", "layering" |
| An empirically verifiable behavior claim | empirical-analysis | Structural scan + round-trip test against evidence, not intuition | "it will generate correctly", "always works", "no failure mode" |

## Decision Rule

1. If the problem names a tension ("but…", "conflicts with") → **triz**
2. Else if terms are fuzzy or there is a hidden assumption → **socratic**
3. Else if the question is "is this worth it / who benefits" → **working-backwards**
4. Else if it is a complexity / clarity / longevity concern → **einstein**
5. Else if a simplicity or capability claim needs testing → **scientific-method**
6. Else if the question is architectural fit → **logical-analysis**
7. Else if behavior can be measured empirically → **empirical-analysis**
8. Ties → prefer **socratic** (it is the lowest-cost probe and surfaces the most)
