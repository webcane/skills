# howtotalk

A communication and persuasion coach for hard conversations. Describe the
situation; the skill diagnoses it, picks one to three frameworks, and writes
the actual words: the opening, the key phrases, the responses to pushback, and
what to do afterwards.

It is not a collection of theory. The frameworks are reference material; the
output is a plan and a script.

## Modes

| Mode | What you get |
|---|---|
| `analyze` (default) | Diagnosis, framework choice, phased plan, exact scripts, risks, follow-up |
| `select` | Three ranked frameworks with confidence and rationale |
| `practice` | Role-play with a realistic counterpart, coaching, and a debrief |

Modes work through an explicit token or natural language. There are no
`/skill:subcommand` commands — that syntax does not exist in Codex or OpenCode.

```text
Codex:     $howtotalk mode: select — my manager presented my project as his own
OpenCode:  @howtotalk mode: practice — refusing a colleague's weekend shift swap
Claude:    /howtotalk mode: analyze — asking for a raise next week
```

Natural-language equivalents work too: "which framework should I use?",
"потренируй меня", "давай разыграем разговор", "use NVC for this".

## Examples

```text
$howtotalk My boss took credit for my project in a meeting. I want to address it
without damaging the relationship.

$howtotalk mode: select I need to tell a client we can't add two features for free.

$howtotalk mode: practice I need to tell my partner that I feel invisible when
they spend the whole evening on their phone.
```

## The thirteen frameworks

NVC, Radical Candor, Crucial Conversations, Difficult Conversations, Never
Split the Difference, Getting to Yes, Influence, Storytelling, Motivational
Interviewing, Socratic Method, SCARF, Active Listening, DESC.

Full index with "best for" and "watch out" is in `SKILL.md`; the one-page
version is `references/quick-reference.md`.

## How routing works

1. Restate the situation, including power and emotional temperature.
2. Classify the job and score it against the detection matrix.
3. Pick one primary framework and at most two secondary ones.
4. Read the selected framework file. Do not invent techniques.
5. Design phases: prepare, open, navigate, close.
6. Write the words in the user's language, with responses to pushback.
7. Name the risks and the follow-up.

Emotion overrides the analytical route: above medium, listening and safety come
first. Safety overrides everything: abuse, threats, and crisis are not
communication problems.

## Structure

```text
skills/howtotalk/
├── SKILL.md
├── references/
│   ├── frameworks/            # 13 core framework guides
│   │   └── details/           # 13 deep dives, loaded on demand
│   ├── routing.md             # emotion, culture, power, decision flow
│   ├── pipelines.md           # 7 multi-framework sequences
│   ├── situations.md          # cognitive biases and defense mechanisms
│   ├── digital-adaptation.md  # text, voice, video, email
│   ├── quick-reference.md     # all 13 frameworks on one page
│   └── phrasebook-ru.md       # Russian scripts and phrase patterns
├── CHANGELOG.md
├── README.md
└── LICENSE
```

## Install

From the repository root:

```bash
bash scripts/install-local.sh howtotalk --target opencode
bash scripts/install-local.sh howtotalk --target codex
bash scripts/install-local.sh howtotalk --target claude-code
```

Or build the packages:

```bash
bash scripts/package-skill.sh howtotalk
```

## Language

The skill replies in the language of the request. Russian scripts are grounded
in `references/phrasebook-ru.md`, with attention to «вы»/«ты», forms of address,
and the difference between a direct request and a public challenge. The
framework reference files are in English; the output is not.

## Safety

This is not therapy and not a substitute for professional help. For immediate
danger in Russia, call 112. Psychological help: 8-495-989-50-50 (Moscow, 24/7);
children and parents: 8-800-2000-122. International: befrienders.org.

For abuse, coercion, threats, or stalking, the skill does not coach persuasion
or confrontation. It prioritizes safety planning and specialist support.

## Attribution

Adapted from [ironyjk/howtotalk](https://github.com/ironyjk/howtotalk), MIT,
Copyright © 2026 ironyjk. The framework content is condensed and restructured
for progressive disclosure, localized for Russian-language use, and stripped of
platform-specific installation and command syntax. See `LICENSE`.
