# Changelog — session-notes

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
