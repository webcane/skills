---
name: hr-answer-coach
description: Interactive wizard that analyzes a draft answer to an HR/interview question, flags red-flags an HR person would actually notice (victim framing, disloyalty signals, arrogance, clichés, oversharing), and helps rewrite the answer using a Past-Present-Future structure. Use whenever the user pastes an HR question plus their draft answer, asks "как лучше ответить HR на вопрос", wants feedback on an interview answer, or asks to check a response for red flags before a job interview.
metadata:
  author: webcane
  version: 1.0.0
---

# HR Answer Coach

Analyzes a candidate's draft answer to an HR/interview question from two
angles at once: **how an HR person would actually read it** (red flags,
hidden signals) and **how to fix it** (career-coach rewrite). The skill
exists because candidates usually can't hear their own red flags — phrases
that feel honest to them ("меня сократили", "хочу стабильности") land as
warning signs to the person evaluating them.

Default language for the whole interaction is Russian, since the primary
use case is the Russian job market (RF companies, emigration/sanctions
subtext, loyalty signaling). If the user writes in another language, match
theirs instead.

Do not skip straight to a rewrite. The value of this skill is the
**diagnosis** — showing the user *why* each phrase reads badly — before
proposing a fix. A rewrite with no diagnosis is just a better answer the
user can't reproduce next time.

## Workflow

### Step 1 — Collect the question + draft answer

Ask the user to paste, in one message:
- the HR question being asked (any question — this skill is not limited to
  a fixed list: "почему ищете работу", "расскажите о себе", "слабые
  стороны", "почему именно к нам", "ожидания по зарплате", "как разрешали
  конфликт" — all fair game)
- their current draft answer (even a rough/unfinished one)

If the user already pasted both in their first message (as in this skill's
own trigger example), skip straight to Step 2 instead of asking again.

### Step 2 — Context (one AskUserQuestion round, max 4 options each)

Ask two short questions before analyzing:

**A. Тип компании** — affects what reads as a red flag and what tone to
recommend:
- Российская корпорация / госкомпания
- Стартап
- Международная компания / международная команда
- Не уверен(а) / не указано

**B. Чувствительный контекст** (multiSelect) — only ask if not obvious from
the draft itself:
- Уход из/в международную компанию, релокация, ограничения по работе из РФ
- Сокращение или увольнение с предыдущего места
- Конфликт с руководством/командой на предыдущем месте
- Ничего из этого

Use the answers to calibrate Step 3 — e.g. "ограничения на работу из РФ" is
a sharper red flag when the target is a Russian-only company than when the
target itself is international.

### Step 3 — Red-flag diagnosis

Read `references/RED-FLAGS.md` for the pattern catalog. Go phrase by phrase
through the user's draft (not the whole answer at once) and for each
flagged phrase produce:

1. The quoted phrase
2. **Почему плохо** — what the HR person concludes about the candidate (not
   just "звучит плохо" — name the inference: victim framing, disloyalty,
   arrogance, passive cliché, oversharing, mercenary motivation, etc.)
3. Severity — call out critical (signals disloyalty, conflict-proneness,
   or victim framing) vs. minor (clichés that just dilute impact) so the
   user knows what to fix first

Don't invent red flags that aren't there — if a draft is clean, say so
plainly rather than padding the response with weak nitpicks.

### Step 4 — Rewrite

Read `references/ANSWER-STRUCTURE.md` for the rewrite frameworks. Default
to the **Past (factual, neutral) → Present (skill/motivation) → Future
(value to them)** structure for "why are you looking" / "why us" type
questions; use the STAR variant instead for behavioral/conflict questions
("расскажите о ситуации, когда...").

Produce one rewritten answer, calibrated to the company type from Step 2.
Keep it in the user's own voice/vocabulary where possible — don't make it
sound like a template.

### Step 5 — Iterate

Ask if the user wants it shorter, more confident, less formal, or wants a
second version for a different company type. Loop on this until they're
satisfied — don't re-run the full diagnosis on every iteration, just adjust
the rewrite.

## References

- `references/RED-FLAGS.md` — catalog of common red-flag patterns (RU job
  market specifics included) with the HR inference each one triggers
- `references/ANSWER-STRUCTURE.md` — Past-Present-Future and STAR rewrite
  frameworks, plus tone calibration by company type
