---
name: session-notes
description: >
  Reads the current chat session and produces wiki-style Markdown pages (one per topic) saved
  to the project root. Use this skill whenever the user wants to capture, document, or summarise
  what was discussed — phrases like "запиши это как wiki", "сделай документацию по теме",
  "сохрани наши заметки", "create wiki notes", "document this session", "turn this chat into
  docs", or any request to extract knowledge/examples from the conversation into files. Trigger
  even when the user doesn't say "wiki" explicitly but clearly wants structured notes or
  reference docs from the chat.
color: blue
metadata:
  version: 1.0.0
  author: mniedre
---

# session-wiki

Turn the current conversation into one or more wiki-style Markdown reference pages, saved to
the project root. Each file covers exactly one topic and is written to be useful standalone —
someone who wasn't in the chat should be able to read it and understand the concept with
working examples.

## Step 1 — Identify topics

Scan the entire conversation (everything visible in context). Extract the distinct topics or
concepts discussed. A topic is a coherent technical or conceptual subject the participants
explored together — not every message, but meaningful clusters of learning.

Good signals: repeated questions about the same thing, code snippets around a shared concept,
a "how does X work" thread, a decision made with reasoning.

Draft a short list: one line per topic with a proposed filename (`kebab-case.md`).

## Step 2 — Confirm with the user

Show the proposed topic list before writing any files:

```
Я нашёл следующие темы в нашем чате. Создать wiki-страницы для них?

1. **Python decorators** → `python-decorators.md`
2. **Async/await patterns** → `async-await.md`

Можно добавить, убрать или переименовать темы.
```

Wait for confirmation. Adjust the list if the user edits it. Then proceed.

## Step 3 — Write the wiki files

For each confirmed topic, write a Markdown file to the **current working directory** (project
root). Use this structure — adapt section depth and length to what the chat actually covered,
but keep all seven sections:

```markdown
# <Topic Name>

> One-sentence definition. What is this and why does it matter?

## Основные концепции

Explain the core ideas and mental model. Draw directly from explanations given in the chat —
paraphrase the reasoning, don't just bullet-list facts.

## Ключевые сценарии

Describe 2–4 situations where this topic applies. Ground them in the actual use cases from
the conversation.

| Сценарий | Когда использовать |
|----------|-------------------|
| ...      | ...               |

## Практические примеры

### Пример 1 — <short label>

Reproduce or reconstruct code/commands from the chat. Include the surrounding context: what
problem was being solved, what the input was, what the output looked like.

```<lang>
# code here
```

Explain what the example demonstrates in 1–3 sentences.

_(Add more examples as needed — one per distinct concept variation shown in the chat.)_

## Где применяется

List real situations in the project or domain where this knowledge is directly useful. Be
specific: "when building X", "when debugging Y", not generic "in Python projects".

## Подводные камни

Gotchas, edge cases, or mistakes that came up (or were implied) in the conversation. If none
were discussed, omit this section.

## Summary — что важно помнить

3–5 bullet points. The things someone should recall first when they encounter this topic.
Keep them tight and memorable.

---
_Составлено из сессии: <today's date>_
```

## Writing quality rules

**Draw from the chat, don't invent.** Every example, gotcha, and scenario should trace back to
something that was actually discussed. If you need to fill a gap for completeness, mark it with
`_(добавлено для контекста)_`.

**Code examples first.** If the chat had working code, reproduce it exactly (correcting obvious
typos). Invented examples come last and only to fill gaps.

**Match the session language.** If the chat was in Russian, write in Russian. If it mixed
languages, match what was used for explanations (usually the user's language) but keep code
and technical terms as-is.

**One file per topic.** Don't merge unrelated topics. Don't split a single topic across files.

**Filename convention:** name the file after the topic in kebab-case — e.g. `python-decorators.md`,
`async-await.md`, `git-rebase.md`. All lowercase, no spaces, no generic names like `topic.md`.

## Edge cases

- **No code in the chat** → skip the code examples section; focus on concepts and scenarios.
- **Ambiguous topic boundaries** → prefer fewer, broader pages over many narrow ones. Merge
  if two topics are closely related and appeared together in the chat.
