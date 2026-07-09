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
  version: 1.3.1
  author: mniedre
  description_claudeai: >
    Turns the current chat into wiki-style Markdown pages saved to your project. Use when you
    want to document or summarise what was discussed: "запиши wiki", "create notes", "document
    this session".
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
Куда сохранить файлы — в текущую директорию (`./`) или указать другой путь?
```

Wait for the user's response. Accept either a confirmation (use `./`) or a custom path. Then proceed.

## Step 3 — Write the wiki files

For each confirmed topic, write a Markdown file to the **current working directory** (project
root). Use this structure — adapt section depth and length to what the chat actually covered,
but keep all seven sections:

For Python topics, use `references/python-template.md` as the base structure — read it before
writing. For other languages/domains, use the generic structure below.

```markdown
# <Topic Name>

> One-sentence definition. Not just what it is — why it exists and what problem it solves.

## Ментальная модель

How to picture this in your head. Use a diagram, analogy, or step-by-step flow where it helps.
Separate the **concept** (what it means) from the **syntax** (how you write it).

Example flow diagram:
```
данные
↓
фильтр
   ↓
преобразование
   ↓
результат
```

## Основные концепции

Explain the core ideas. Draw from explanations in the chat — paraphrase the reasoning.
Prefer "Почему" over just the fact: not "generator экономит память" but
"generator хранит только текущее состояние итерации, а не всю коллекцию целиком — поэтому
не тратит память на элементы, которые ещё не нужны".

## Ключевые сценарии

_(Overview table — followed by a full expanded section for each.)_

| Сценарий | Когда использовать |
|----------|-------------------|
| ...      | ...               |

---

# <Scenario 1 name>

Full expanded explanation. What happens, why it works this way, what to watch for.
Include code from the chat with inputs, outputs, and explanation of what the example shows.

```<lang>
# code here
```

---

# <Scenario 2 name>

_(Repeat per scenario using H1 headings so each reads as a standalone reference section.)_

---

## Эквивалент

_(Include only for complex syntax constructs — comprehensions, decorators, generators, etc.)_

Show the equivalent written with simpler/more explicit constructs (e.g. a plain `for` loop),
so the reader understands what the shorthand actually expands to.

```<lang>
# shorthand
[x * 2 for x in nums if x > 0]

# equivalent
result = []
for x in nums:
    if x > 0:
        result.append(x * 2)
```

## Где применяется

Real situations where this is useful. Be specific: "when building X", "when debugging Y".

## Когда НЕ использовать

Situations where this construct is the wrong choice — and what to use instead. If nothing
came up in the chat, omit this section.

## С чем часто путают

Common mix-ups: similar-looking constructs, subtle differences in behaviour, naming confusion.
One paragraph or comparison table per pair. Omit if not discussed.

## Сложность / Производительность

_(Include for collections, algorithms, data structures.)_

Time and space complexity. Explain *why* — not just O(n) but what operation drives it.
Omit for topics where performance wasn't discussed and isn't relevant.

## Подводные камни

Gotchas and mistakes that came up (or were strongly implied) in the conversation.
Omit if none.

## Типичные вопросы с собеседований

Questions commonly asked about this topic. Include the expected answer or key points
to hit. Omit if not discussed in the session.

## Summary — что важно помнить

5–10 bullet points. The things to recall first when encountering this topic.

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

## File conflicts

Before writing each file, check whether it already exists at the chosen path. If it does, ask:

```
Файл `python-decorators.md` уже существует. Что сделать?

1. Оставить прежний (пропустить этот файл)
2. Заменить (перезаписать)
3. Сохранить оба (`python-decorators-2.md`)
4. Указать другой путь
```

Wait for the answer before writing. Apply the chosen action. If the user picks option 3,
append `-2` to the filename (or `-3` if `-2` also exists, etc.). If multiple files conflict,
ask once per file — don't batch them into a single question.
