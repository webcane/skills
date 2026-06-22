# Changelog — hr-answer-coach

All notable changes to this skill. Released per skill as tag
`hr-answer-coach/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

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
