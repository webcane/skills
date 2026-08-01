# Changelog — idea-to-concept

All notable changes to this skill. Released per skill as tag
`idea-to-concept/v<version>`. The version in `SKILL.md` frontmatter
(`metadata.version`) is the source of truth.

## [1.3.0] - 2026-08-01

### Added
- 13 new methods across three roles (v1.3.0):
  - **Analysis:** `feynman`, `deduction`, `five-whys`, `three-questions`.
  - **Generation:** `dialectic`, `six-hats`, `reframing`, `inversion`, `analogy`,
    `mind-map`.
  - **Validation:** `hadi`, `ice`, `rat` — offered after a hypothesis is formed.
- Execution Protocol Step 5: after a hypothesis is formed, offer hypothesis validation
  (hadi / ice / rat); output format gains a "Hypothesis validation" section (v1.3.0).
- `--help` mode (Mode 0): prints the full method catalog — all 20 methods grouped by
  role, when to use each, and the routing decision rule — then stops without running an
  analysis. Invoke as `/idea-to-concept --help` (user) or `mode: help` in an
  `analyze:` block (sub-agent) (v1.3.0).

## [1.1.0] - 2026-07-31

### Changed
- Renamed skill from **hypothes-to-concept** to **idea-to-concept** (v1.1.0): broader
  input naming (idea/problem/proposal/decision) and explicit mention of the structured
  reasoning methods (socratic, TRIZ, Einstein, working-backwards, scientific-method)
  in the description.

## [1.0.0] - 2026-07-31

### Added
- Initial release of the **hypothes-to-concept** skill (v1.0.0) — structured reasoning:
  analyze, clarify, reformulate, or solve a problem via a rigorous method (auto
  recommendation or explicit selection), surfacing assumptions and resolving
  contradictions. Domain-agnostic; usable as a sub-agent by other skills.
