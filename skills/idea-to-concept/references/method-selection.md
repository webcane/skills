# Method Selection — Routing Table

Choose a method by the *symptom* the problem exhibits, not by the problem's domain.

## Method Roles

The methods fall into three roles:

- **Analysis** — clarify, simplify, and root-cause a problem into a well-formed concept
  or hypothesis.
- **Generation** — shift perspective and produce alternative hypotheses.
- **Validation** — prioritize and test a formed hypothesis (offer after a hypothesis
  exists).

## Routing Table

| Role | Symptom in the problem | Method | What it does | Typical trigger phrases |
|---|---|---|---|---|
| Analysis | Ambiguous terms, unstated assumptions, possible hidden contradictions | socratic | Disciplined questioning to expose contradictions and force precise definitions | "it should work", "obviously", undefined terms, edge cases ignored |
| Analysis | Two requirements in tension — both must be satisfied without compromise | triz | Resolve the contradiction by separating concerns; find the abstract solution | "but that conflicts with", "can't have both", "trade-off between X and Y" |
| Analysis | Concept too complex, unclear, or needs to survive long-term use | einstein | Radical simplification — one-sentence explanation, remove one thing, check obviousness | "too complex", "doesn't age well", "hard to explain" |
| Analysis | Unclear value — does this actually solve a real problem? | working-backwards | Start from the desired experience and reason backwards to requirements | "is this useful?", "who benefits?", speculative use case |
| Analysis | Depth of understanding to verify | feynman | Explain in plain language; gaps in the explanation are gaps in understanding | "do I actually understand this?", "everyone knows how this works" |
| Analysis | A conclusion claimed to follow from general rules | deduction | State premises, derive consequences, expose smuggled-in premises | "follows from our principles", "by definition", "if X then necessarily Y" |
| Analysis | A visible symptom whose root cause is unknown | five-whys | Chain "Why?" until a systemic (non-blaming) cause is found | "it keeps breaking", "why does this keep happening", "treating the symptom" |
| Analysis | An emotional or automatic reaction to a problem | three-questions | Pause and analyze from three positions — Why? (motive), What? (facts), How? (response) | "reacting", "people problem", communication breakdown |
| Analysis | A claim that needs testing — is this the simplest way? | scientific-method | Treat the claim as a hypothesis; separate known from assumed; design the minimal experiment | "this is the simplest", "nothing else can do this", "obviously better" |
| Analysis | Fit with existing architecture or stated premises | logical-analysis | State premises, deduce consequences, test for contradiction, find hidden premises | "does this fit?", "consistent with our architecture", "layering" |
| Analysis | An empirically verifiable behavior claim | empirical-analysis | Structural scan + round-trip test against evidence, not intuition | "it will generate correctly", "always works", "no failure mode" |
| Generation | An overconfident claim that needs to face its opposite | dialectic | Build the antithesis, let it conflict, derive the synthesis | "it's either X or Y", polarized debate, overconfident claim |
| Generation | A proposal to review from every side | six-hats | Run the proposal through six fixed modes — facts, emotion, risk, optimism, creativity, process | "let's look at all sides", "review this fully", emotion mixing with logic |
| Generation | A problem framed only as a liability | reframing | Change the frame of interpretation to reveal the asset or the non-obvious solution | "this is a problem", "customers hate this", "unavoidable" |
| Generation | A hypothesis that only considers one direction | inversion | Ask "how to guarantee failure?" to expose the hidden risk and negate it | "more X = better", assumes success, one-directional |
| Generation | A stuck problem needing a fresh angle | analogy | Transfer a solution from a distant domain via structural similarity | "no idea what to do", "need a new angle", "how would X do this?" |
| Generation | A complex hypothesis to decompose and map | mind-map | Radiate the idea into branches and find non-linear connections | "sort this out", "too tangled", "see the whole picture" |
| Validation | A formed hypothesis to test quickly and cheaply | hadi | Hypothesis → Action → Data → Insights in one short loop | "let's test it", "small experiment", "test and see" |
| Validation | Many hypotheses, need to pick the most promising | ice | Score Impact × Confidence × Ease and rank | "which one first?", "too many hypotheses" |
| Validation | One assumption whose failure sinks the whole hypothesis | rat | Test the riskiest assumption first by the cheapest means | "everything depends on this", "big bet on one assumption" |

## Decision Rule

1. If the problem names a tension ("but…", "conflicts with") → **triz**
2. Else if terms are fuzzy or there is a hidden assumption → **socratic**
3. Else if the question is "is this worth it / who benefits" → **working-backwards**
4. Else if it is a complexity / clarity / longevity concern → **einstein**
5. Else if it is a depth-of-understanding check → **feynman**
6. Else if the claim is "this follows from our principles" → **deduction**
7. Else if a visible symptom has no root cause → **five-whys**
8. Else if the situation is an emotional / automatic reaction → **three-questions**
9. Else if the proposal needs review from every side → **six-hats**
10. Else if an obstacle could be an asset → **reframing**
11. Else if an overconfident claim needs its opposite → **dialectic**
12. Else if only one direction is considered → **inversion**
13. Else if the problem is stuck and needs a fresh angle → **analogy**
14. Else if a complex web of ideas needs mapping → **mind-map**
15. Else if a simplicity or capability claim needs testing → **scientific-method**
16. Else if the question is architectural fit → **logical-analysis**
17. Else if behavior can be measured empirically → **empirical-analysis**
18. Ties → prefer **socratic** (it is the lowest-cost probe and surfaces the most)

## After a Hypothesis Is Formed

Analysis and generation methods produce hypotheses. Once one exists, offer the
validation methods:

- Test it fast → **hadi**
- Many hypotheses, pick one → **ice**
- One do-or-die assumption → **rat**
