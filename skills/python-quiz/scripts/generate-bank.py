#!/usr/bin/env python3
"""
Generate a single comprehensive prompt for python-quiz question bank generation.

Reads standard topics from references/standard-topics.json and outputs
a formatted prompt. When processed by the LLM in a single response,
this produces the complete question bank without multi-round batching.

Usage:
    python3 generate-bank.py [--questions-per-topic N] [--language ru|en]
"""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
TOPICS_PATH = os.path.join(SKILL_DIR, "references", "standard-topics.json")


def load_standard_topics():
    with open(TOPICS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def build_prompt(topics, questions_per_topic, language):
    """Build a single comprehensive prompt for the LLM."""

    lang_instruction = {
        "ru": "Все вопросы должны быть на русском языке.",
        "en": "All questions must be in English.",
    }[language]

    prompt_title = {
        "ru": "Ты — генератор банка вопросов по Python для интерактивного теста.",
        "en": "You are a Python question bank generator for an interactive quiz.",
    }[language]

    task_line = {
        "ru": f"Сгенерируй ровно {questions_per_topic} вопроса на КАЖДУЮ тему из списка ниже (распределяя вопросы по подтемам внутри темы).",
        "en": f"Generate exactly {questions_per_topic} questions for EVERY topic in the list below (distributing across subtopics within the topic).",
    }[language]

    coding_note = {
        "ru": "Один coding task — добавь в конце, отдельно от тем.",
        "en": "One coding task — add at the end, separately from topics.",
    }[language]

    distro_header = {
        "ru": f"## Распределение типов на каждую тему ({questions_per_topic} вопроса)",
        "en": f"## Type distribution per topic ({questions_per_topic} questions)",
    }[language]

    single_label = {
        "ru": "- 2 single-choice (один правильный из 4)",
        "en": "- 2 single-choice (one correct out of 4)",
    }[language]

    multi_label = {
        "ru": "- 1 multi-choice (2-3 правильных из 4-5)",
        "en": "- 1 multi-choice (2-3 correct out of 4-5)",
    }[language]

    short_label = {
        "ru": "- 1 short-answer (текстовый ответ)",
        "en": "- 1 short-answer (text response)",
    }[language]

    plus_coding = {
        "ru": "Плюс 1 coding task в конце (всего).",
        "en": "Plus 1 coding task at the end (total).",
    }[language]

    rules = {
        "ru": [
            "1. Каждый вопрос САМОДОСТАТОЧЕН: понятен без внешнего контекста, не ссылается на «код выше».",
            "2. Текст вопроса — законченное предложение, не обрывается.",
            "3. Правильный ответ соответствует реальному поведению Python 3.10+.",
            "4. Для single/multi: answer — буква или строка букв (например 'A' или 'AB').",
            "5. Для short: answer — краткий эталонный ответ (1-3 предложения).",
            "6. Сложность: равномерно easy/medium/hard по теме (кроме coding task — он medium или easy).",
        ],
        "en": [
            "1. Each question is SELF-CONTAINED: understandable without external context.",
            "2. Question text is a complete sentence, never truncated.",
            "3. Correct answer matches actual Python 3.10+ behavior.",
            "4. For single/multi: answer is a letter or string of letters (e.g. 'A' or 'AB').",
            "5. For short: answer is a concise reference answer (1-3 sentences).",
            "6. Difficulty: evenly easy/medium/hard per topic (except coding task — it's medium or easy).",
        ],
    }[language]

    format_header = {
        "ru": "## Формат JSON-банка",
        "en": "## JSON bank format",
    }[language]

    format_instruction = {
        "ru": "Верни ТОЛЬКО JSON-массив вопросов (без markdown-блоков, без ```json```):",
        "en": "Return ONLY a JSON array of questions (no markdown blocks, no ```json```):",
    }[language]

    topics_header = {
        "ru": "## Список тем и подтем",
        "en": "## Topic and subtopic list",
    }[language]

    topics_note = {
        "ru": "(Темы — стандартная программа Python Middle/Senior из references/standard-topics.json)",
        "en": "(Topics — standard Python Middle/Senior syllabus from references/standard-topics.json)",
    }[language]

    instruction_header = {
        "ru": "## Инструкция",
        "en": "## Instruction",
    }[language]

    instruction_one_shot = {
        "ru": "Сгенерируй ВСЕ вопросы в ОДНОМ ответе. Не останавливайся посередине.",
        "en": "Generate ALL questions in ONE response. Do not stop midway.",
    }[language]

    instruction_json_only = {
        "ru": "Выведи только JSON (без markdown-блоков, без ```json```, без пояснений).",
        "en": "Output only JSON (no markdown blocks, no ```json```, no explanations).",
    }[language]

    instruction_total = {
        "ru": f"Всего вопросов: {questions_per_topic} на каждую тему (распределяя по подтемам) + 1 coding task.",
        "en": f"Total questions: {questions_per_topic} per topic (distributed across subtopics) + 1 coding task.",
    }[language]

    lines = []
    lines.append(prompt_title)
    lines.append("")
    lines.append("## Задача")
    lines.append(task_line)
    lines.append(coding_note)
    lines.append(lang_instruction)
    lines.append("")
    lines.append(distro_header)
    lines.append(single_label)
    lines.append(multi_label)
    lines.append(short_label)
    lines.append(plus_coding)
    lines.append("")
    lines.append("## Правила генерации")
    for r in rules:
        lines.append(r)
    lines.append("")
    lines.append(format_header)
    lines.append(format_instruction)
    lines.append("```")
    lines.append("""{"generated_at": "<ISO>", "source": "standard-topics.json", "topics_count": N, "questions_count": M, "questions": [
  {"id": 1, "type": "single", "topic": "...", "subtopic": "...", "difficulty": "medium",
   "text": "Вопрос?", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], "answer": "A"},
  {"id": 2, "type": "multi", "topic": "...", "subtopic": "...", "difficulty": "easy",
   "text": "Вопрос?", "options": ["A. ...", "B. ...", "C. ...", "D. ...", "E. ..."], "answer": "AB"},
  {"id": 3, "type": "short", "topic": "...", "subtopic": "...", "difficulty": "hard",
   "text": "Вопрос?", "answer": "Краткий эталонный ответ."},
  {"id": N, "type": "coding", "topic": "coding", "subtopic": "coding", "difficulty": "medium",
   "text": "Описание задачи + пример входа/выхода.", "answer": "Ожидаемое решение."}
]}""")
    lines.append("```")
    lines.append("")
    lines.append(topics_header)
    lines.append("")
    lines.append(topics_note)
    lines.append("")

    for entry in topics:
        lines.append(f"### {entry['topic']}")
        for st in entry["subtopics"]:
            lines.append(f"  - {st}")
        lines.append("")

    lines.append(instruction_header)
    lines.append(instruction_one_shot)
    lines.append(instruction_json_only)
    lines.append(instruction_total)

    return "\n".join(lines)


def main():
    args = sys.argv[1:]

    questions_per_topic = 4
    language = "ru"

    i = 0
    while i < len(args):
        if args[i] == "--questions-per-topic" and i + 1 < len(args):
            questions_per_topic = int(args[i + 1])
            i += 2
        elif args[i] == "--language" and i + 1 < len(args):
            language = args[i + 1].lower()
            i += 2
        else:
            i += 1

    if language not in ("ru", "en"):
        print(f"Error: unsupported language '{language}'. Use 'ru' or 'en'.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(TOPICS_PATH):
        print(f"Error: topics file not found at {TOPICS_PATH}", file=sys.stderr)
        sys.exit(1)

    data = load_standard_topics()
    topics = data[language]

    prompt = build_prompt(
        topics=topics,
        questions_per_topic=questions_per_topic,
        language=language,
    )

    print(prompt)


if __name__ == "__main__":
    main()
