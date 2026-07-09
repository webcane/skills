# Changelog — session-notes

## [Unreleased]

## [2.1.0] - 2026-07-09

### Changed
- `language-reference.md`: added "Основные сценарии" with H1 expanded sections (was missing vs python-template)
- `python-template.md`: now only Python-specific additions (closures, functools.wraps, GIL, gotchas, Эквивалент patterns); extends language-reference.md via include instruction
- Routing: Python = language-reference.md + python-template.md

## [2.0.0] - 2026-07-09

### Added
- 10 note types with dedicated templates in `references/`: language-reference, cs-system-design, tool-cookbook, reading-notes, article-notes, cheat-sheet, terms, recipes, interview-notes, personal-knowledge
- Type detection step: each topic is classified before writing
- Routing table in SKILL.md: type → template file

### Changed
- SKILL.md slimmed down — structure lives in `references/` templates, not inline
- Step 2 now shows type alongside topic name and filename

## [1.2.0] - 2026-07-09

## [1.3.1] - 2026-07-09

### Fixed
- python-template.md: added missing `## Что это` and `## Примеры` sections, fixed order (Как работает before Синтаксис), renamed "Типичные" → "Частые вопросы с собеседований"

## [1.3.0] - 2026-07-09

### Added
- Sections: "Когда НЕ использовать", "С чем часто путают", "Эквивалент" (for complex syntax), "Сложность / Производительность", "Типичные вопросы с собеседований"
- Mental model block: separate concept from syntax, use flow diagrams
- "Почему" writing rule: explain mechanisms, not just consequences
- `references/python-template.md`: unified template for all Python topics

## [1.2.1] - 2026-07-09

### Added
- File conflict handling: if a file already exists, ask user to keep, replace, save both, or choose another path

## [1.2.0] - 2026-07-09

### Changed
- Each scenario now gets its own expanded H1 section (with code, reasoning, output) in addition to the overview table

## [1.1.1] - 2026-07-09

## [1.1.0] - 2026-07-09

### Added
- Ask user where to save files (current directory or custom path) before writing

## [1.0.0] - 2026-07-09

### Added
- Initial skill: reads current chat session, identifies topics, confirms with user, writes wiki-style MD files to project root
