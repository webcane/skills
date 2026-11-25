# OpenSpec support

Use OpenSpec as the behavioral contract, then apply the skill's ordinary
invariant/scenario/test audit. No CLI installation or separate workflow is
required. Read the local repository instructions and actual schema/layout;
custom workflows may use different artifact paths.

## Select the scope and sources

- For a named change, read its directory under `openspec/changes/<change>/`.
  Typical inputs are `proposal.md`, `design.md`, `tasks.md`, and delta specs
  under `specs/<capability>/spec.md`. Read the corresponding current specs under
  `openspec/specs/<capability>/spec.md` as the baseline.
- With no change specified, use an unambiguous target from the request or diff.
  If several changes could apply, ask for the target; do not pick an arbitrary
  directory or combine all active changes.
- For a current-system audit, use the selected current specs. Archived changes
  under `openspec/changes/archive/` are history, not extra current requirements.
  Only use one as the target when explicitly requested, recording its historical
  baseline or uncertainty about that baseline.
- Read `openspec/config.yaml` and the change's `.openspec.yaml` when present to
  identify custom schema/context. Follow declared local paths; absent optional
  artifacts or CLI are not by themselves a validation failure.

Specs define behavior; proposal and design explain intent and constraints;
tasks help locate implementation and candidate tests. Checked task boxes and
artifact readiness do not prove that behavior passed a test. If documents
disagree on an important expectation, surface the conflict rather than silently
choosing whichever makes the implementation pass.

## Resolve the effective contract

For an active change, compare its deltas with the relevant baseline **in memory**.
Do not merge specs on disk. If already synced, reconcile matching content instead
of counting both versions as separate requirements. Keep unrelated current
behavior as a relevant regression boundary, without expanding to the whole repo.

| Delta operation | Audit treatment |
| --- | --- |
| `ADDED` | Include the new requirement and its scenarios |
| `MODIFIED` | Validate the intended changed contract, not the superseded baseline wording; inspect retained scenarios and flag unexplained losses |
| `REMOVED` | Stop requiring the former behavior; verify explicit removal/migration expectations where stated, without inventing a new return code or policy |
| `RENAMED` | Preserve the requirement's identity and trace old → new; apply associated modifications if present |

Missing targets, ambiguous renames, or conflicting deltas are contract gaps.
Do not resolve them by editing specifications during test filling. For no-spec
changes explicitly allowed by local metadata/schema, use the stated scope and
relevant unchanged specs; do not invent a delta just to run validation.

Preserve explicit requirement IDs. Otherwise use a report-local key formed from
capability path + requirement heading, and scenario heading for each scenario.
Include source path/heading and operation, with old/new identity when renamed.
Do not add synthetic IDs to source specs.

Translate each `Scenario` (including GIVEN/WHEN/THEN conditions) into an
observable assertion and executable selector. A requirement with three required
scenarios is not fully verified because one scenario passes. Add risk-based
scenarios beyond the written examples when useful, clearly labeled as derived.

## Execute and report

Use existing behavioral tests and the normal project runner. If an installed
`openspec` CLI helps discover artifacts, inspect its local help/version first;
do not assume remote documentation matches the installed version. Read-only
listing/status and spec validation are optional. A successful `openspec validate`
checks specification artifacts; it does not establish implementation behavior.
Record it separately from requirement coverage.

In `audit`, return the report without editing. When saving is requested, prefer
the project's established report location; otherwise use
`openspec/changes/<change>/VALIDATION.md` for an active change, or a scoped report
under `validation/` for current/historical audits. These are this skill's report
conventions, not required OpenSpec artifacts. Do not write into an archive as a
side effect of auditing it.

Add source links, change/capability/requirement/scenario identity, effective
contract decisions, test selectors, actual results, and unresolved gaps. Use
`coverage_complete`, not task completion, as the report's evidence flag. An
unimplemented change can be planned or reported as missing coverage; do not
require a completed phase or manufacture successful executions.

Only tests, test-only fixtures, and the requested validation report may change.
Leave proposal/design/specs/tasks/config untouched. Do not check off tasks,
sync specs, archive changes, or invoke implementation commands during validation.
