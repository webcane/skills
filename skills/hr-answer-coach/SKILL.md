---
name: hr-answer-coach
description: Analyzes a draft HR/interview answer, flags red flags (victim framing, disloyalty, arrogance, oversharing), and rewrites it using Past-Present-Future/STAR. Use for any HR/interview answer review.
metadata:
  author: webcane
  version: 2.1.0
---

# HR Answer Coach

Analyzes a candidate's draft answer to an HR/interview question from two
angles at once: **how an HR person would actually read it** (red flags,
hidden signals) and **how to fix it** (career-coach rewrite). The skill
exists because candidates usually can't hear their own red flags — phrases
that feel honest to them ("I was laid off", "I want stability") land as
warning signs to the person evaluating them.

**Language support:** At the start, you'll be asked to choose Russian (RU) or
English (EN) for the entire interaction. If you provide text on the first
trigger (both question + draft answer together), the skill will auto-detect
the language and use it throughout — no explicit choice needed.

Do not skip straight to a rewrite. The value of this skill is the
**diagnosis** — showing the user *why* each phrase reads badly, and what the
question is actually testing for — before proposing a fix. A rewrite with no
diagnosis is just a better answer the user can't reproduce next time.

## Core Principles

Four principles guide both diagnosis and rewrite:

**1. Emphasize business value** — Concrete results beat vague claims. When a candidate talks about their work, they should connect it to measurable outcomes: money saved, time shortened, problems solved, growth numbers. An HR person reads "I improved processes" as unfocused; they read "cut processing time by 40%" as credible impact. Watch for claims without metrics; rewrite should require numbers or specific results. **This applies equally to developers** ("optimized latency by 40%", "shipped a feature used by 500K users/month") and managers alike.

**2. Be authentic** — Templated confidence and fake-humble phrases tank credibility faster than honest self-reflection. A candidate who says "I used to struggle with delegation, but I'm learning to give my team more ownership" lands better than "I'm too hard on myself." Watch for generic corporate-speak; rewrite should preserve the user's real voice and real experience, not a polished fiction.

**3. Own your outcomes** — Blame-shifting is a kill signal. An HR person sees "my boss didn't understand my idea" and hears conflict-prone. The stronger move: "I explained the idea poorly → changed my approach → found common ground." Watch for environment-blaming, excuse-making, or victim framing in conflict/challenge stories; rewrite should show what the candidate controlled and changed, not what was done to them.

**4. Connect to the role** — A great achievement that's irrelevant to the job description wastes credibility. "I organized company events" is real, but it's off-topic for a backend architect role. Watch for achievements that don't map to the job's actual needs; rewrite should tie each example to specific skills or problems the role will face. If the user doesn't know what the company actually needs, suggest they research the job description before finalizing the answer.

## Workflow

### Step 1 — Language selection + collect the question + draft answer

**Language auto-detection:** If the user triggers the skill with both the HR question and draft answer already in their first message, detect the language from their text and use it for the entire interaction (Russian or English). Skip the language question below.

**If no input text yet** (or only partial input), use AskUserQuestion to ask:

**Язык / Language:**
- Русский (RU) — все вопросы и ответы на русском
- English (EN) — all questions and answers in English

Then ask the user to paste, in one message:
- the HR question being asked (any question — this skill is not limited to
  a fixed list: "why are you looking for a new job", "tell me about
  yourself", "weaknesses", "why us", "salary expectations", "conflict
  resolution" — all fair game)
- their current draft answer (even a rough/unfinished one)

If the user already pasted both in their first message (as in this skill's
own trigger example), use language auto-detection and skip the language
selection question.

### Step 2 — Context (one AskUserQuestion round, max 4 options each)

Ask two short questions before analyzing. **Use the language selected in Step 1
(RU or EN).**

**In Russian (if RU selected):**

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

**In English (if EN selected):**

**A. Company type** — affects what reads as a red flag and what tone to
recommend:
- Large corporation / government company
- Startup
- International company / international team
- Not sure / not specified

**B. Sensitive context** (multiSelect) — only ask if not obvious from
the draft itself:
- Moving to/from an international company, relocation, work restrictions from Russia
- Layoff or termination from previous position
- Conflict with management/team at previous place
- None of the above

Use the answers to calibrate Step 3 — e.g. work restrictions tied to Russia
status is a sharper red flag when the target is a Russian-only company than
when the target itself is international.

### Step 3 — Diagnosis: question framing + red flags

Read `references/RED-FLAGS.md` for the pattern catalog. Structure the
response in two layers — **what the question is testing**, then
**phrase-by-phrase red flags**. Don't skip the first layer: it's what tells
the user *why* a fix matters, not just that one is needed.

**A. Question framing — state these three things explicitly before the
phrase-by-phrase diagnosis:**

1. **Why they ask this** — what the HR person is evaluating with this
   specific question (career logic vs. drama, loyalty risk,
   self-awareness, conflict style, etc.)
2. **What they want to hear** — name the answer model that fits this
   question and say which one you're using: Past→Present→Future (default,
   for motivation/why-us questions), STAR (behavioral/conflict questions),
   PAR (weakness questions), or another model if it fits better. Sketch the
   model's structure in one line so the user sees the shape before the
   rewrite arrives.
3. **What not to say** — the specific phrases/patterns that read as red
   flags for *this particular question* (pull from RED-FLAGS.md, and from
   the matching entry in `references/QUESTION-FORMULAS.md` if the question
   matches one of those patterns).

Check `references/QUESTION-FORMULAS.md` for the question being asked — it
catalogs 8 typical HR questions with "Зачем спрашивают" / "Что хотят
услышать" / "Чего не стоит говорить" already worked out. If the question
matches an entry there, base these three points directly on it. Otherwise,
derive them from RED-FLAGS.md and the general PPF/STAR/PAR logic.

**B. Phrase-by-phrase diagnosis** — go through the user's draft (not the
whole answer at once) and for each flagged phrase produce:

1. The quoted phrase
2. **Why it's bad** — what the HR person concludes about the candidate (not
   just "sounds bad" — name the inference: victim framing, disloyalty,
   arrogance, passive cliché, oversharing, mercenary motivation, lack of
   concrete results, generic corporate-speak, etc.)
3. Severity — call out critical (signals disloyalty, conflict-proneness,
   or victim framing) vs. minor (clichés that just dilute impact) so the
   user knows what to fix first

**Also watch for the four core principles** (see above):
- **Missing business value**: Claims without metrics or measurable outcomes ("I improved things" without saying what changed or by how much)
- **Template language over authenticity**: Generic phrases ("I'm too hard on myself", "ambitious", "good team player") that don't reflect the user's real experience
- **Blame-shifting or victim framing**: "My boss didn't listen", "the team was weak", "circumstances didn't allow it" — these signal the candidate won't take ownership in conflicts
- **Irrelevant achievements**: Great stories that don't connect to what the role actually needs

Don't invent red flags that aren't there — if a draft is clean, say so
plainly rather than padding the response with weak nitpicks.

### Step 4 — Rewrite

Read `references/ANSWER-STRUCTURE.md` for the rewrite frameworks. Default
to the **Past (factual, neutral) → Present (skill/motivation) → Future
(value to them)** structure for "why are you looking" / "why us" type
questions; use the STAR variant instead for behavioral/conflict questions
("tell me about a time you had a conflict..."), or PAR for weakness
questions. Use the same model you named in Step 3A.

**Universal answer formula** (works for most HR questions):
- **Past:** Factual, neutral reason for change — no victim framing, no complaints
- **Present:** What you're skilled at and what motivates you — new challenges, growth areas, types of work
- **Future:** Concrete value you'll bring to *them* — how your interests align with what they need

**Apply the four core principles to your rewrite:**
1. **Add business value language** — If the user claims a skill or achievement, push for measurable results. Instead of "improved processes", ask: "What changed? By how much? Was it faster, cheaper, more reliable?" Include numbers or specific outcomes in the rewrite where possible. This applies to all roles: developers should quantify technical impact ("latency down 40%"), managers should quantify team/org impact ("retention at 95%", "grew 3 engineers to senior level").
2. **Keep their authentic voice** — Avoid generic corporate templates. If they struggled with something, show the real struggle and what they learned from it, not a canned humble-brag. Preserve their actual vocabulary and tone.
3. **Shift from blame to ownership** — Reframe any environment-blaming as "here's what I controlled and changed." Instead of "my boss didn't understand", write "I explained the idea poorly → I changed my approach → we found common ground." In conflict stories, focus on the candidate's actions and what they took responsibility for.
4. **Anchor to the role** — Make sure each achievement or skill maps to something the job description actually mentions or implies. If the user isn't sure what the company needs, suggest they read the job description and research the company before finalizing the answer.

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
- `references/QUESTION-FORMULAS.md` — 8 typical HR questions, each with
  "Зачем спрашивают" / "Что хотят услышать" / "Чего не стоит говорить"
  already worked out. Step 3 checks this file for a matching question
  before falling back to deriving the framing from RED-FLAGS.md directly.
