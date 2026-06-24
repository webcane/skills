---
name: thesis-to-text
description: Turn scattered notes into polished text (posts, articles, speeches, memos) through guided interviews, analysis, and approval gates. Use when writing from raw ideas and scattered thoughts.
metadata:
  author: webcane
  version: 1.0.2
---

# Thesis-to-Text Wizard

Turns a pile of raw theses, bullet points, or half-formed thoughts into a
finished, audience-ready text. Instead of asking the user to fill in a giant
prompt template by hand, this skill conducts the interview itself — one
block at a time, multiple-choice where possible — then reasons about gaps
and contradictions in the answers *before* writing anything, and only
drafts after the user has approved a plan.

Conduct the whole wizard in the user's language (match the language they
write in; default to the language of their raw notes if it's not already
clear).

## Workflow Overview

1. **Interview** — 8 blocks, one AskUserQuestion round per block.
2. **Analysis** — internal reasoning over what was collected.
3. **Validation** — surface contradictions/gaps, propose fixes.
4. **Plan Summary & Approval** — one-screen recap, explicit go-ahead required.
5. **Outline → Write → Review** — draft only after approval, then iterate.

Do not skip straight to writing after the interview. Stages 2–4 are what
make the final text good — they catch mismatches (e.g. "warm, inspiring
tone" selected for an audience marked "skeptical, exhausted") before they
end up baked into a draft nobody wants to fix line-by-line.

## Stage 1: Interview

Ask one block per AskUserQuestion call. Every question needs 2-4 concrete
preset options (per AskUserQuestion's limit) — the user can always pick
"Other" to give a custom answer, so presets should be genuinely useful
defaults, not filler.

**A. Role & style** — domain (e.g. B2B marketing / expert article / social
post / speech) and voice (concise & business-like / warm & inspiring /
ironic & provocative / academic but accessible).

**B. Context & background** — where it's published (Telegram, LinkedIn,
internal blog, spoken delivery), what preceded it (previous post, industry
news, seasonality), and the main problem/trend the audience cares about
right now.

**C. Audience portrait** — who they are (role, level), their knowledge
level (novice / pro / mixed), their top 2-3 pains or objections, and their
current emotional state (tired, skeptical, hopeful, confused).

**D. Raw theses** — don't force this into multiple choice. Ask the user to
paste their raw notes, drafts, keywords, quotes, facts, or even just
scattered emotions directly. Capture everything verbatim — disorganized is
fine, that's the input this skill exists to organize.

**E. Goal** — desired reader action (subscribe, buy, reply, change their
mind, nothing — just inform), desired feeling (calm, confidence, curiosity,
urgency), and the single takeaway the reader should keep even if they
forget everything else.

**F. Format** — target length (characters or words), structure needs
(subheadings, bullet lists, bold emphasis, intro/outro shape), and the
mood of the opening vs. closing paragraph.

**G. Hard constraints** — banned words/clichés, tone strictness (no fluff,
straight to the point / conversational slang allowed / strictly formal),
and how to handle competitor brand mentions.

**H. Extra requests (optional)** — e.g. 3 headline/opening-line variants,
restrict metaphors to one domain (sport / cooking / IT / nature), or a
final pass to replace bureaucratic phrasing with live verbs. Offer to skip
this block if the user has nothing to add.

## Stage 2: Analysis

Before drafting anything, reason through the collected material and present
the reasoning to the user as a short note (plain text, no new questions
yet):

1. **Core problem/contradiction** — what's the central tension or claim in
   the raw theses (Block D)?
2. **Likely gaps** — what details would strengthen the piece that the
   interview didn't surface (a missing example, an unaddressed objection
   from Block C, a number that needs a source)?
3. **Success criteria** — concrete, checkable criteria the finished draft
   should meet (e.g. "names the old approach by name," "includes at least
   one of the three case numbers," "ends on the single takeaway from
   Block E").
4. **Decomposition** — break the piece into the sections/components it'll
   actually be written in, so Stage 5's outline has real beats to fill.

## Stage 3: Validation

Cross-check all 8 blocks against the Stage 2 analysis for contradictions —
tone vs. audience emotional state, requested length vs. structural
complexity, banned words vs. the metaphor domain requested, format vs.
publication platform. List anything inconsistent with a proposed
fix/hypothesis for each. If nothing is inconsistent, say so explicitly
rather than inventing a problem — don't pad this stage.

## Stage 4: Plan Summary & Approval

Compile a one-screen recap: role/voice, audience snapshot, the single core
takeaway, the success criteria from Stage 2, and the section skeleton from
Stage 2's decomposition. Ask for explicit approval (proceed / adjust
something) before moving on. Do not start Stage 5 without it — if the user
flags something, loop back to the relevant interview block, not straight
to a rewritten plan.

## Stage 5: Outline → Write → Review

**Outline** — produce 3 headline/opening-line variants, the section beats
with a one-line description of each, word-count targets per section, and
the intended mood of the opening and closing paragraphs. Get confirmation
or a revision request before writing the full draft.

**Write** — draft the full text section by section, following the approved
outline and every constraint from Block G (banned words, tone, metaphor
domain, length).

**Review** — collaborative loop: the user requests specific rewording or
structural changes, iterate until they're satisfied. If Block H asked for
a canzelyarizm/dead-phrasing pass, do that as the final step before
delivering the text — flag what was replaced, don't silently rewrite past
what was asked.

## Guardrails

- Never skip Stage 2-4 to save time, even if the user seems impatient —
  offer a fast path ("no issues found, proceed?") rather than dropping the
  stage outright.
- AskUserQuestion: max 4 options per question, always allow custom input,
  one block per round — don't bundle multiple interview blocks into a
  single question.
- The final deliverable is the text itself in a code block — this skill
  produces no files, scripts, or other artifacts.
