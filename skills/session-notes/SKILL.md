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
  version: 2.0.0
  author: mniedre
  description_claudeai: >
    Turns the current chat into wiki-style Markdown pages saved to your project. Use when you
    want to document or summarise what was discussed: "запиши wiki", "create notes", "document
    this session".
---

# session-notes

Turn the current conversation into one or more Markdown reference pages. Each file covers
one topic, uses a structure matched to its type, and is written to be useful standalone.

## Step 1 — Identify topics and classify types

Scan the entire conversation. For each topic, determine:

1. **Topic name** → proposed `kebab-case.md` filename
2. **Note type** from the list below

| # | Type | When |
|---|------|------|
| 1 | Language Reference | concept/syntax in a programming language |
| 2 | CS / System Design | algorithm, data structure, protocol, pattern, distributed systems |
| 3 | Tool Cookbook | CLI tool, framework, library, API — "how to use X" |
| 4 | Reading Notes | book |
| 5 | Article Notes | blog post, paper, talk, docs page |
| 6 | Cheat Sheet | dense lookup reference, commands, flags |
| 7 | Terms | glossary entry / definition |
| 8 | Recipes | step-by-step procedure, runbook |
| 9 | Interview Notes | interview prep or debrief |
| 10 | Personal Knowledge | observation, lesson learned, decision |

If the type is unclear, use the closest match or note "Unknown" — you'll propose a new type
to the user in Step 2.

## Step 2 — Confirm with user

Show topics, types, and filenames before writing anything. Ask where to save:

```
Я нашёл следующие темы:

1. **Python decorators** (Language Reference → Python) → `python-decorators.md`
2. **CAP theorem** (CS / System Design) → `cap-theorem.md`

Куда сохранить — текущая директория (`./`) или другой путь?
```

Wait for confirmation. Adjust if the user edits topics, types, or path. Then proceed.

## Step 3 — Write files using the right template

For each topic, read the matching template from `references/` and use it as the structure.
Adapt sections to what the chat actually covered — omit _(optional)_ sections if the topic
or conversation doesn't warrant them.

| Type | Template |
|------|----------|
| Language Reference — Python | `references/python-template.md` |
| Language Reference — other | `references/language-reference.md` |
| CS / System Design | `references/cs-system-design.md` |
| Tool Cookbook | `references/tool-cookbook.md` |
| Reading Notes | `references/reading-notes.md` |
| Article Notes | `references/article-notes.md` |
| Cheat Sheet | `references/cheat-sheet.md` |
| Terms | `references/terms.md` |
| Recipes | `references/recipes.md` |
| Interview Notes | `references/interview-notes.md` |
| Personal Knowledge | `references/personal-knowledge.md` |
| Unknown | form a basic structure from the content; propose the type to the user |

## Writing quality rules

**Draw from the chat, don't invent.** Every example and scenario should trace back to the
conversation. If you add something for completeness, mark it `_(добавлено для контекста)_`.

**Explain the "почему".** Not "generator saves memory" but "generator stores only the current
iteration state, not the whole collection — so it never allocates memory for elements not yet
needed".

**Match the session language.** Write in the user's language; keep code and technical terms as-is.

**One file per topic.** Don't merge unrelated topics. Don't split one topic across files.

**Filename:** kebab-case named after the topic — `python-decorators.md`, `cap-theorem.md`.

## File conflicts

Before writing each file, check if it already exists at the chosen path. If it does, ask:

```
Файл `python-decorators.md` уже существует. Что сделать?

1. Оставить прежний (пропустить)
2. Заменить (перезаписать)
3. Сохранить оба (`python-decorators-2.md`)
4. Указать другой путь
```

Ask once per conflicting file. If the user picks option 3, append `-2` (or `-3` etc.).
