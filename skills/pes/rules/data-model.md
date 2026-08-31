# Reminders data model

Apple Reminders is the **only** source of truth (invariant 15 in
[invariants.md](invariants.md)). Everything below is a convention layered on top of
the real fields the MCP exposes — see [mcp-tools.md](mcp-tools.md) for the exact
schema. The goal: a human can open Reminders.app with no Claude involved and
understand the whole system. Keep to this convention exactly; don't improvise new
lists or tag shapes mid-session.

## Lists (top-level, flat — see the nesting gap in mcp-tools.md)

| List | Holds | Entity types inside |
|---|---|---|
| `Inbox` | Unprocessed capture | raw items (no type tag needed) |
| `Strategic` | L1 state | Value, Area, Goal, Priority, Strategy — distinguished by `type-*` tag |
| `Initiatives` | L2 connective tissue | Initiative |
| `Plans` | L2 tactical commitments | Plan |
| `Tasks` | L3 operational actions | Task |
| `Results` | Actual outcomes | Result |

Six lists, flat, no nesting — deliberately not one list per Area. Area is a tag
(`area-*`), not a list, per spec §2 ("Areas — это контекст, а не обязательная
линейная ступень иерархии").

None of these lists are assumed to pre-exist. [workflows/init.md](../workflows/init.md)
bootstraps the skeleton (and the WIP Limit entry below) on first use, or on
request — run it before relying on this model against a fresh Reminders setup.

## Tags (native Reminders tags — regex `^#?[\p{L}\p{N}_-]+$`, no colons, no spaces)

| Tag family | Example | Meaning |
|---|---|---|
| `type-*` | `type-value`, `type-area`, `type-goal`, `type-priority`, `type-strategy` | disambiguates entries inside the mixed `Strategic` list |
| `p0` `p1` `p2` `p3` | `p0` | Strategic Priority — on Priority entries, Initiatives, and (optionally, inherited) Plans. Never on Tasks — Strategic Priority is not a Task property (invariant 10). |
| `area-*` | `area-career`, `area-finance` | context tag on Initiative/Plan/Task; slug from the Area's title in `Strategic` |
| `value-*` | `value-autonomy` | optional, only if the user wants a Task/Initiative to cite a Value explicitly — never required (spec §2: Values are not mandatory Task fields) |
| `status-*` | `status-active`, `status-completed`, `status-cancelled`, `status-deferred` | lifecycle state for Plans (and Initiatives). Machine-checkable via `filterTags` — don't rely on parsing `note` text for status. |
| `init-<slug>` | `init-ai-engineering-career` | on a Plan: which Initiative it implements |
| `plan-<slug>` | `plan-python-interview-prep` | on a Task or Result: which Plan it belongs to |
| `goal-<slug>` | `goal-increase-stable-income` | on an Initiative: which Goal it serves |
| `adhoc` | `adhoc` | on an **ad-hoc task** — no PML linkage, deliberately not tied to any Plan. Not "Activity": `Task = activity` already distinguishes Task from Outcome/Result in [outcomes.md](outcomes.md); `adhoc` distinguishes pes-linked Tasks from bare ones instead. |

**Every Task carries exactly one of `plan-<slug>` (a **pes task**) or `adhoc`
(an **ad-hoc task**) — never neither, never both.** `pes` is specifically a PML
agent; a Task with no classification tag is a modeling gap, not a valid "just
didn't say" state. See
[workflows/tasks.md](../workflows/tasks.md) for how creation resolves which one
applies.

Slugs: lowercase, hyphens, derived from the entity's `title`, stable once created
(don't reslug on rename — add a new tag and keep the old one on existing links, or
bulk-update if the user explicitly confirms a rename propagation).

## Notes field (structured `Key: value` lines — human-readable, freeform beyond that)

**Value / Area / Goal / Strategy** (`Strategic` list): free text description. No
required keys.

**Priority entry** (`Strategic` list, `type-priority` + `p0..p3` tag):
```
Priority: P0
Label: Financial Stability
```

**Initiative** (`Initiatives` list):
```
Type: project | hypothesis | initiative
Goal: <goal title>
```
(Strategic Priority lives in the `p0..p3` tag, not repeated in notes.)

**Plan** (`Plans` list) — every Plan must have all of these (invariants 1, 2; see
[outcomes.md](outcomes.md) for what happens when one is missing):
```
Initiative: <initiative title>
Expected Outcome: <what state will be true when this Plan succeeds>
Time Horizon: <deadline or period, e.g. 2026-09-30 or "Q3 2026">
Status: active
```
`dueDate` field mirrors the Time Horizon deadline when it's a single date.

**Task** (`Tasks` list):
```
Done when: <observable completion criterion>
```
`priority` = Operational Priority (High/Medium/Low — Reminders' native field).
`dueDate` = urgency, independent of Strategic Priority (invariant 11). `tags`
carries exactly one of `plan-<slug>` (pes task, belongs to a Plan) or `adhoc`
(ad-hoc task, deliberately not part of PML), plus `area-*` if relevant.

**Result** (`Results` list) — created already `completed: true` (it's a log entry,
not an action to perform):
```
Plan: <plan title>
Task(s): <optional — which tasks contributed>
Recorded: <date>
```
Title = the actual result statement (not the activity — see
[outcomes.md](outcomes.md) for the Task/Outcome/Result distinction).

## Operational Priority ↔ Reminders `priority` field

| Reminders value | Label | Meaning |
|---|---|---|
| `0` | none | not set |
| `1` | High | |
| `5` | Medium | |
| `9` | Low | |

This is the *only* priority dimension that lives on a Task. Strategic Priority
(P0–P3) never appears on a Task — see [priorities.md](priorities.md).

## WIP limit storage

Stored as a single reminder in `Strategic`, title `WIP Limit`, note holding the
integer (default `3` if this reminder doesn't exist yet — offer to create it on
first use rather than guessing a hidden default). The user can edit the number
directly in Reminders.app; the skill always re-reads it, never caches it across
turns (invariant 15).

## Worked example — how it actually looks in Reminders.app

```
List: Plans
  ☐ AI Engineering Career — Python Interview Prep      [tags: init-ai-engineering-career, p0]
     Notes:
       Initiative: AI Engineering Career
       Expected Outcome: быть готовым к Python technical interview
       Time Horizon: 2026-09-15
       Status: active
     Due: 2026-09-15

List: Tasks
  ☐ Решить 10 задач Python (LeetCode Easy)               [tags: plan-ai-engineering-career-python-interview-prep, area-career]
     Notes: Done when: 10/10 solved and self-reviewed
     Priority: High   Due: 2026-09-05

  ☐ Забрать посылку с почты                              [tags: adhoc]
     Notes: Done when: посылка в руках
     Priority: Low   Due: 2026-09-01

List: Results
  ☑ Успешно пройти mock interview с оценкой 8/10         [tags: (none required)]
     Notes:
       Plan: AI Engineering Career — Python Interview Prep
       Recorded: 2026-09-14
```
