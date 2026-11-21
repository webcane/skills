# Changelog — howtotalk

All notable changes to this skill. Released per skill as tag
`howtotalk/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

## [1.0.0] - 2026-11-21

### Added

- Single umbrella skill that routes a situation to one to three of thirteen
  communication frameworks: NVC, Radical Candor, Crucial Conversations,
  Difficult Conversations, Never Split the Difference, Getting to Yes,
  Influence, Storytelling, Motivational Interviewing, Socratic Method, SCARF,
  Active Listening, and DESC.
- Three modes: `analyze`, `select`, and `practice`, resolved from an explicit
  `mode:` token or natural language. No harness-specific slash subcommands.
- Progressive disclosure: 13 core framework files plus 13 deep-dive files under
  `references/frameworks/`, loaded only when selected.
- `references/routing.md` with emotion levels, power dynamics, cultural
  adaptation, and framework compatibility.
- `references/pipelines.md` with seven multi-framework sequences and exit
  criteria for each phase.
- `references/situations.md` combining cognitive-bias and defense-mechanism
  maps.
- `references/digital-adaptation.md` for text, voice, video, and email.
- `references/quick-reference.md` with all thirteen frameworks on one page.
- `references/phrasebook-ru.md` with Russian scripts for NVC, DESC, Radical
  Candor, Difficult Conversations, negotiation, active listening, apologies,
  refusals, pushback, and follow-up.
- Safety boundaries for crisis, abuse, minors, and professional-scope
  questions, with Russian and international helplines.
- A grounding rule that forbids inventing the user's numbers, names, dates,
  quotes, or company policies; scripts use placeholders such as `[ваша сумма]`
  instead of fabricated specifics.

### Changed

- Restructured the upstream fourteen-skill layout into one package with
  reference files, so installation, versioning, and triggering work the same in
  Codex, OpenCode, and Claude Code.
- Rewrote the router from 538 lines to a focused procedure with a hard limit of
  three frameworks and an explicit grounding rule: read the framework file
  before writing advice.
- Localized the cultural layer for Russian-language use while keeping the
  high-context and power-distance concepts.
- Replaced fictional `/skill:subcommand` syntax with modes and natural-language
  triggers.
- Normalized framework names to lowercase hyphenated IDs.

### Removed

- Upstream installer, `.claude-plugin/` metadata, Korean README, and the
  SessionStart auto-update hook.
- Korean-language glosses and table columns, Korean-specific narrative
  frameworks, and Korea-only crisis contacts.
- `user-invocable: false` and Skill-tool dependency, which do not apply to this
  hub's packaging model.

### Notes

- Adapted from [ironyjk/howtotalk](https://github.com/ironyjk/howtotalk) (MIT,
  Copyright © 2026 ironyjk). See `LICENSE`.
