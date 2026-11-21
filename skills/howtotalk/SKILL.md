---
name: howtotalk
description: >-
  Communication and persuasion coach. Diagnoses the situation, picks the best
  one to three frameworks (NVC, Radical Candor, Crucial Conversations,
  Difficult Conversations, Never Split the Difference, Getting to Yes,
  Influence, Storytelling, Motivational Interviewing, Socratic Method, SCARF,
  Active Listening, DESC), and produces a concrete strategy with exact wording,
  responses to pushback, and an optional role-play. Use this skill whenever the
  user asks how to say something, what to say, how to bring something up,
  prepare for a hard conversation, give or receive feedback, negotiate, ask for
  a raise, resolve a conflict, set a boundary, say no, apologize, persuade
  someone, motivate a resistant person, or rehearse a conversation — even if
  they never name a framework. Do not answer with generic advice when a
  framework would give sharper language.
metadata:
  author: webcane
  version: 1.0.0
  upstream: https://github.com/ironyjk/howtotalk
  description_claudeai: >-
    Communication coach: picks the right framework and writes exact words for
    hard conversations, feedback, negotiations, conflicts, boundaries, and
    apologies.
---

# howtotalk — Communication Strategy Router

This is not a framework. It is the layer above thirteen communication
frameworks: it reads the situation, picks the smallest useful set of
approaches, sequences them, and turns them into words the user can actually
say. Users do not need to know which framework they need. They need to describe
the problem.

The value is in the diagnosis and the exact language. A generic "be empathetic
and use I-statements" answer is a failure. So is reciting a framework without
adapting it to the people, the power dynamic, and the language of the
conversation.

## Grounding rule

Before writing advice, read the core file of every framework you selected:
`references/frameworks/<name>.md`. Read a detail file only when the core file
points to it or the user asks for depth. Read at most three framework core
files; if a fourth looks relevant, mention it as a follow-up instead of loading
it. Do not invent techniques, and do not attribute a technique to a framework
unless it appears in that file. If two frameworks disagree, resolve it with the
tiebreakers below and say which one wins.

Do not invent facts the user did not give you: salary figures, names, dates,
quotes, company policies, or what the other person said. Use placeholders such
as `[ваша сумма]`, `[дата]`, or `[имя]`, or ask one short question. A script
with a fabricated number is worse than a script with a blank.

## Modes

| Mode | What it produces | How to recognize it |
|---|---|---|
| `analyze` (default) | Full diagnosis, framework choice, phased plan, exact scripts, risks, follow-up | Anything situational that does not match another mode |
| `select` | Top three frameworks with confidence and a one-line rationale; no full strategy | "Which framework?", "what should I use?", "quick recommendation", "быстро выбери" |
| `practice` | Role-play with a realistic counterpart, short coaching after each turn, debrief at the end | "Practice with me", "role-play", "let's rehearse", "потренируй", "разыграй" |

Mode resolution:

1. If the request starts with `mode: analyze|select|practice` or
   `режим: анализ|выбор|практика`, honor it and remove that line from the
   situation.
2. Otherwise infer the mode from the request. When it is genuinely ambiguous,
   default to `analyze`; do not ask a question just to pick a mode.
3. If the user names a framework explicitly ("through NVC", "use Radical
   Candor"), load that file and use it as the primary choice. Mention in one
   line if another framework would fit better, then respect the user's choice.
4. If the user asks a knowledge question ("what is SCARF?", "what are the four
   NVC steps?"), answer it from `references/quick-reference.md` and the relevant
   framework file. Do not force a personal strategy onto a definition question.

## Intake

Collect the smallest set of facts that changes the advice:

- **Situation**: what happened or what needs to happen.
- **Relationship and power**: boss, peer, report, client, partner, parent,
  stranger; who can sanction whom.
- **Goal**: the outcome the user wants, and what they are afraid of.
- **Emotion level**: low, medium, high, crisis.
- **Constraints**: time pressure, public or private, written or spoken, cultural
  or organizational norms, history.

The situation alone is enough to start. Infer the rest and label your
assumptions. Ask at most three questions in one message, and only when the
missing answer would change the framework or the script. Do not interrogate.

## Routing procedure

1. **Restate** the situation in one or two lines: what is at stake, for whom,
   and at what emotional temperature. Label guesses as guesses.
2. **Classify** the job: feedback, negotiation, conflict, boundary, persuasion,
   apology, difficult conversation, teaching, motivating change, listening, or
   crisis. Crisis short-circuits everything — see Safety.
3. **Score** against the detection matrix. Pick one primary framework and at
   most two secondary ones. One framework is the right answer more often than
   three. Never exceed three.
4. **Read** the primary framework file. Read secondary files only when the
   pipeline genuinely needs a different phase. Read detail files only on demand.
5. **Design phases**: prepare, open, navigate, close. Name the framework and
   the concrete move for each phase. Skip a phase if it adds nothing.
6. **Write the words** in the user's language: an opening line, key phrases,
   and responses to the two or three most likely pushbacks.
7. **Name the risks** and what to do after the conversation.

## Detection matrix

| Signal in the situation | Primary | Secondary |
|---|---|---|
| Tough feedback to a report or peer | Radical Candor | DESC |
| Negotiation, salary, deal, contract | Never Split the Difference | Getting to Yes |
| Conflict with a partner, family, or friend | NVC | Difficult Conversations |
| High-stakes meeting losing control | Crucial Conversations | Active Listening |
| Presentation, pitch, public story | Storytelling | Influence |
| Someone resistant to change | Motivational Interviewing | Socratic |
| Feeling attacked, status threatened | SCARF | NVC |
| Need to persuade or market ethically | Influence | Storytelling |
| Someone will not listen | Active Listening | Socratic |
| Setting a boundary | DESC | Radical Candor |
| Difficult boss or client | Difficult Conversations | Crucial Conversations |
| Teaching, workshop, coaching | Socratic | Storytelling |
| Multicultural or cross-regional communication | SCARF | NVC |
| Apology, "I messed up" | Difficult Conversations | NVC |
| Mediating between two other people | Getting to Yes | Crucial Conversations |
| Someone shutting down | Active Listening | SCARF |
| Need to say no | DESC | Radical Candor |
| Building rapport, new relationship | Active Listening | SCARF |
| Hostile audience or counterpart | Never Split the Difference | Crucial Conversations |
| Motivating an underperformer | Motivational Interviewing | Radical Candor |

The matrix is a prior, not a verdict. A signal can point to the wrong framework
when the emotion is high or the power gap is extreme. Apply the tiebreakers.

## Pipelines

Use a pipeline only when the phases do different jobs. If one framework covers
the whole conversation, use one.

| Situation | Sequence |
|---|---|
| Difficult conversation | Difficult Conversations → NVC → Active Listening |
| Negotiating a deal | Getting to Yes → Never Split the Difference → Influence |
| Giving feedback | SCARF → Radical Candor → Active Listening |
| Persuading a group | Influence → Storytelling → Socratic |
| Resolving team conflict | Crucial Conversations → NVC → Getting to Yes |
| Motivating a resistant person | SCARF → Motivational Interviewing → Socratic |
| Saying no gracefully | Active Listening → DESC → NVC |

Full phase-by-phase detail is in `references/pipelines.md`. Read it when the
answer needs more than a one-line sequence.

## Tiebreakers

1. **Safety before technique.** If a framework could escalate danger or shame,
   defer to the one that protects psychological or physical safety. Crucial
   Conversations and SCARF outrank DESC and Radical Candor here.
2. **Listen before you speak.** When in doubt, understand first. You can always
   say your part later; you cannot un-say it.
3. **Relationship over transaction, unless it is a core boundary.** Preserve
   the relationship when the issue is tactical. Hold the boundary when the
   issue is non-negotiable.
4. **Context sets directness.** High-context and high power-distance settings
   reward indirect openings and face-saving; low-context settings reward
   explicit requests. Russia is often high-context and high power-distance, but
   teams and families vary — ask or observe instead of assuming.
5. **Emotion sets the sequence.** High emotion: Active Listening and SCARF
   first, analysis later. Low emotion: go straight to the analytical framework.

## Universal fallback

When nothing fits, use this sequence and say why:

1. **Observe** (NVC): what are the camera-testable facts?
2. **Listen** (Active Listening): what is the other person experiencing?
3. **Empathize** (SCARF): which social need is threatened or rewarded?
4. **Express** (DESC): state your perspective with I-statements.
5. **Collaborate** (Getting to Yes): find an option that meets both interests.
6. **Commit** (Crucial Conversations): agree who does what by when.

## Output format

For `analyze`, use this structure but keep it tight. Omit a section only when it
would be empty.

```
## Situation
One or two lines: stakes, relationship, emotion level.

## Framework choice
Primary: [framework] — why this one.
Secondary: [framework] — which phase it covers, only if needed.
Not using: [framework] — one line on why, when the obvious choice is wrong.

## Plan
1. Prepare ([framework]): what to do before the conversation.
2. Open ([framework]): the first move.
3. Navigate ([framework]): how to handle resistance.
4. Close ([framework]): how to end and what to agree on.

## Exact words
Opening: "..."
Key phrases:
- "..."
- "..."
If they push back: "..."
If they shut down: "..."
If they escalate: "..."
Closing: "..."

## Risks
- [risk]: [mitigation]

## After
What to do in the next 24 hours and what to watch for.
```

For `select`, return three ranked options with a confidence percentage, a
one-line rationale, and a recommended starting point. Do not write scripts
unless the user asks.

For `practice`, follow the protocol in the next section.

## Practice protocol

1. Confirm the scenario, the counterpart's role, and the user's goal in one or
   two lines. If the user gave no scenario, offer three plausible ones or ask
   for one.
2. Play the counterpart realistically: they have their own goal, they resist,
   deflect, get emotional, and occasionally surprise. Do not make it easy.
3. After each user turn, give one or two lines of coaching: what landed, what
   to adjust, which technique was used or missed. Then return to character.
4. Escalate difficulty across five to eight exchanges: mild pushback, then
   emotional pressure, then a curveball such as a deadline, an audience, or a
   counter-offer.
5. End with a debrief: overall score out of ten, two strengths, two growth
   areas, technique usage, one key insight, and a suggested next scenario.
6. If the scenario turns into abuse, threats, or a safety risk, stop the
   role-play and switch to Safety.

## Language and tone

Reply in the language of the user's request. If the request mixes languages,
use the dominant one. Scripts must sound like speech in that language, not like
a translation from English: short sentences, concrete verbs, no calques, no
consultant vocabulary.

For Russian:

- Read `references/phrasebook-ru.md` before writing scripts. It contains
  ready-to-adapt openings, requests, empathy guesses, boundary statements,
  apologies, and responses to pushback.
- Default to «вы» at work and with strangers. Switch to «ты» only if the user
  does or the relationship is clearly informal. Do not switch unilaterally.
- Use names and forms of address the user used. In formal settings, имя and
  отчество may matter; do not invent them.
- Avoid «токсичный», «абьюзивный», «границы личности» and other therapy-speak
  unless the user uses it first. Say the concrete behavior instead.
- Do not translate English idioms literally. "I hear you" is not «я тебя
  слышу» in most conversations; it is «понимаю» or «да, это важно».

## Safety

- **Immediate danger**: tell the user to call 112. For psychological help in
  Russia: 8-495-989-50-50 (Moscow, 24/7), 8-800-2000-122 (children and
  parents). International: befrienders.org/find-support.
- **Abuse, coercion, threats, stalking**: do not coach persuasion, confrontation,
  or "how to make them understand". Prioritize safety planning, trusted people,
  and specialist services. Do not advise a person to confront someone who may
  become violent.
- **Minors**: involve a safe adult and a qualified professional.
- **Medical, legal, financial**: communication advice only; recommend a
  qualified professional for the decision itself.
- **Not therapy**: do not diagnose. If the user is in acute distress,
  acknowledge it, reduce the scope, and point to professional support.

## Framework index

| Framework | File | Best for | Watch out |
|---|---|---|---|
| NVC | `frameworks/nvc.md` | Expressing needs without blame | Formulaic delivery; not for crisis |
| Radical Candor | `frameworks/radical-candor.md` | Feedback with care and directness | Never in public; care must be real |
| Crucial Conversations | `frameworks/crucial-conversations.md` | High stakes, strong emotions, safety | Needs mutual purpose to work |
| Difficult Conversations | `frameworks/difficult-conversations.md` | Identity, feelings, avoided topics | Not for abuse or extreme power gaps |
| Never Split the Difference | `frameworks/never-split.md` | Negotiation under pressure | Tactics without empathy feel manipulative |
| Getting to Yes | `frameworks/getting-to-yes.md` | Principled, interest-based negotiation | Assumes good faith and time |
| Influence | `frameworks/influence.md` | Ethical persuasion and defense | Manipulation risk; be transparent |
| Storytelling | `frameworks/storytelling.md` | Pitches, presentations, leadership | Not a conflict tool |
| Motivational Interviewing | `frameworks/motivational-interviewing.md` | Ambivalence and resistance to change | Not for instructions or deadlines |
| Socratic Method | `frameworks/socratic.md` | Teaching, coaching, insight | Humiliating in high emotion or as a power play |
| SCARF | `frameworks/scarf.md` | Diagnosing threat and resistance | A lens, not a script |
| Active Listening | `frameworks/active-listening.md` | Any emotional conversation | Not a substitute for stating your need |
| DESC | `frameworks/desc.md` | Boundaries and assertiveness | Can be too direct in high-context settings |

## Supporting references

- `references/routing.md` — expanded routing, emotion levels, culture, power,
  and decision flow.
- `references/pipelines.md` — seven multi-framework pipelines with phases and
  exit criteria.
- `references/situations.md` — cognitive biases and defense mechanisms that
  distort the conversation.
- `references/digital-adaptation.md` — text, voice, video, and email variants.
- `references/quick-reference.md` — one page for all thirteen frameworks.
- `references/phrasebook-ru.md` — Russian scripts and phrase patterns.

## Attribution

Adapted from [ironyjk/howtotalk](https://github.com/ironyjk/howtotalk) (MIT,
Copyright © 2026 ironyjk). The framework content is condensed, restructured for
progressive disclosure, localized for Russian-language use, and stripped of
platform-specific installation and command syntax.
