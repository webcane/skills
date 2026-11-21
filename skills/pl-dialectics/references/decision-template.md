# decision.md — 7-section decision record

One file per language, written after `study.md` passes validation. It answers a single
question: **what should Orthon take from this language, and on what evidence?**

A final cross-language `studies/synthesis/decision.md` merges the per-language records only
after `self_review.py` has run, so the per-language decisions are not contaminated by each
other.

## Skeleton

```markdown
---
schema_version: "1"
language: "{{LANGUAGE}}"
slug: {{slug}}
role: decision-record
created: YYYY-MM-DD
---

# {{LANGUAGE}} — what Orthon should take

## 1. Decision / Решение

## 2. Rationale / Обоснование

## 3. Scope / Границы применимости

## 4. Implementation details / Детали реализации

## 5. Verification plan / План проверки

## 6. Risks and forecast / Риски и прогноз

## 7. Open questions / Открытые вопросы
```

## What each section must contain

1. **Decision** — the chosen option, the merged variant, or the synthesis. Name the mechanism
   Orthon would adopt. Reference `S*`, `T*`, `AX*`. One paragraph, one decision. If several
   decisions follow, number them `1.1`, `1.2` and keep them inside section 1.
2. **Rationale** — why this beats the alternatives *that this study actually examined*.
   Reference `C*` and `J*`. An argument that does not cite a study ID is an opinion.
3. **Scope / Границы** — when the decision holds and when it stops holding. Name the
   conditions: language size, team skill, compile-time budget, platform constraints.
4. **Implementation details / Детали** — modules, interfaces, data, state, errors, permissions,
   security, performance, migration, rollback. This is where the decision becomes actionable.
   Each sub-item is a short labelled block, not prose.
5. **Verification / План проверки** — tests, monitoring, staged rollout, acceptance criteria.
   Acceptance criteria must be measurable; "feels better" is not a criterion.
6. **Risks and forecast / Риски** — short-term risk, medium-term evolution, accumulated debt,
   extension paths. Distinguish risk from uncertainty.
7. **Open questions / Открытые вопросы** — what the user or the team must confirm before
   implementation. An empty section is a validation error: every decision has unknowns.

## Rules

- Body language is English; headings stay bilingual for stable parsing and for readers who
  wrote the request in Russian.
- Every section is non-empty. "None" is allowed only in section 7 with a reason.
- No new IDs. `decision.md` references `study.md`; it never introduces `C*`, `J*`, `S*`, `T*`.
  A genuinely new tension belongs in `study.md` Task E, assigned there, then referenced here.
- Length target: 400–900 words. Below 400 the implementation section is usually hollow; above
  900 the decision has become a second study.
