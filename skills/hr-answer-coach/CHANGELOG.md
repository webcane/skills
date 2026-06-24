# Changelog — hr-answer-coach

All notable changes to this skill. Released per skill as tag
`hr-answer-coach/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

## [Unreleased]

### Changed
- **Moved "Common Question Formulas" out of SKILL.md into `references/QUESTION-FORMULAS.md`** — this block was ~150 of SKILL.md's 339 lines, always loaded into context even though Step 3 only ever needs the single entry matching the question actually being diagnosed. SKILL.md now points Step 3 at the reference file by name instead of inlining all 8 entries; progressive disclosure loads it only when needed.
- **BREAKING: SKILL.md instructional text translated to English** — all workflow/step instructions are now written in English (the user-facing wizard remains bilingual RU/EN, unchanged). Russian text is kept only where it's literally the example phrase or HR-question wording being matched/quoted.
- **Step 3 (diagnosis) now requires explicit question framing before the phrase-by-phrase red-flag scan** — every diagnosis must state, up front: (1) "Зачем спрашивают?" — what HR is evaluating with this question, (2) "Что хотят услышать?" — which answer model is being used (Past→Present→Future, STAR, PAR, etc.) and its structure, (3) "Чего не стоит говорить?" — the specific red-flag phrases for that question. Previously this framing only existed inside the "Common Question Formulas" reference section and wasn't surfaced as a required part of every diagnosis response.
- Description shortened to 195 characters (was unbounded prose) for the Claude.ai upload limit.

### Added
- **Core Principles section expanded to four principles** — now explicitly frame both red-flag diagnosis and rewrite:
  1. **Emphasize business value** — watch for claims without metrics/results; applies equally to developers and managers
  2. **Be authentic** — avoid generic templates; preserve user's real voice
  3. **Own your outcomes** — watch for blame-shifting, victim framing; rewrite should show what candidate controlled and changed
  4. **Connect to the role** — achievements must map to job description; irrelevant examples waste credibility
- Step 3 updated to watch for all four principle violations: missing metrics, generic language, blame-shifting, and off-topic achievements
- Step 4 updated to apply all four principles during rewrite: add measurable results, keep authentic voice, shift from blame to ownership, anchor achievements to the role

## [1.6.0] - 2026-06-22

### Added
- **Explicit language selection (RU/EN)** — Step 1 now asks which language to use for the entire interaction (Russian or English). If both HR question and draft answer are provided on first trigger, language is auto-detected from the text — no choice needed.
- **Bilingual wizard** — all wizard steps and output are now available in both Russian and English, respecting the user's language choice

### Changed
- **Restructured Common Question Formulas** — each of 8 typical HR questions now includes: _Зачем спрашивают?_ (HR's intent), _Что хотят услышать_ (answer formula), _Чего не стоит говорить_ (specific red-flag phrases). Makes the "why" transparent so candidates understand HR's evaluation logic, not just follow a template.
- **"Расскажи о своих слабых сторонах?" formula** — refined to explicit **PAR** structure (Problem/Awareness → Action → Result), distinct from STAR and PPF, with concrete example (micromanagement → delegation growth), red flags clarified (fake-humble, abstract, blaming environment, job-critical weakness)
- **Step 1 workflow** — explicit language selection replaces implicit Russian default; language auto-detection when input text is provided

### Added (previous)
- **"Какие ваши сильные стороны?" formula** — strengths question (specific skill → concrete example with metrics → company relevance), with red flags (generic/clichéd qualities, examples without proof, irrelevant strengths, process-focused language)
- **"Кем вы видите себя через пять лет?" formula** — future-vision question (career path → specific direction → company alignment), with red flags (uncertainty, defensive framing about management, unrealistic ambitions)
- **"Tell me about your work experience" formula** — structure for opening career narrative (current role → key journey → relevance to role), with red flags (résumé dump, overstating expertise, no connection to their needs)
- **Common Question Formulas** section: 6 concrete answer patterns (job search, why-this-company, weaknesses, conflict, salary, work experience) with deep context on HR intent, formula structure, and avoidable mistakes
- Universal answer formula inline in Step 4 rewrite guidance

## [1.0.0] - 2026-06-22

## [1.0.0] - 2026-06-22

### Added
- Initial release
- Interactive wizard: collect HR question + draft answer, context round
  (company type, sensitive context), red-flag diagnosis, Past-Present-Future
  / STAR rewrite, iteration loop
- `references/RED-FLAGS.md` — catalog of 8 common red-flag patterns with
  RU job-market specifics
- `references/ANSWER-STRUCTURE.md` — Past-Present-Future and STAR rewrite
  frameworks with tone calibration by company type
