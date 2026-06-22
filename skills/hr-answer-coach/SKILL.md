---
name: hr-answer-coach
description: Interactive wizard that analyzes a draft answer to an HR/interview question, flags red-flags an HR person would actually notice (victim framing, disloyalty signals, arrogance, clichés, oversharing), and helps rewrite the answer using a Past-Present-Future structure. Use whenever the user pastes an HR question plus their draft answer, asks "как лучше ответить HR на вопрос", wants feedback on an interview answer, or asks to check a response for red flags before a job interview.
metadata:
  author: webcane
  version: 1.5.1
---

# HR Answer Coach

Analyzes a candidate's draft answer to an HR/interview question from two
angles at once: **how an HR person would actually read it** (red flags,
hidden signals) and **how to fix it** (career-coach rewrite). The skill
exists because candidates usually can't hear their own red flags — phrases
that feel honest to them ("меня сократили", "хочу стабильности") land as
warning signs to the person evaluating them.

Default language for the whole interaction is Russian, since the primary
use case is the Russian job market (RF companies, emigration/sanctions
subtext, loyalty signaling). If the user writes in another language, match
theirs instead.

Do not skip straight to a rewrite. The value of this skill is the
**diagnosis** — showing the user *why* each phrase reads badly — before
proposing a fix. A rewrite with no diagnosis is just a better answer the
user can't reproduce next time.

## Workflow

### Step 1 — Collect the question + draft answer

Ask the user to paste, in one message:
- the HR question being asked (any question — this skill is not limited to
  a fixed list: "почему ищете работу", "расскажите о себе", "слабые
  стороны", "почему именно к нам", "ожидания по зарплате", "как разрешали
  конфликт" — all fair game)
- their current draft answer (even a rough/unfinished one)

If the user already pasted both in their first message (as in this skill's
own trigger example), skip straight to Step 2 instead of asking again.

### Step 2 — Context (one AskUserQuestion round, max 4 options each)

Ask two short questions before analyzing:

**A. Тип компании** — affects what reads as a red flag and what tone to
recommend:
- Российская корпорация / госкомпания
- Стартап
- Международная компания / международная команда
- Не уверен(а) / не указано

**B. Чувствительный контекст** (multiSelect) — only ask if not obvious from
the draft itself:
- Уход из/в международную компанию, релокация, ограничения по работе из РФ
- Сокращение или увольнение с предыдущего места
- Конфликт с руководством/командой на предыдущем месте
- Ничего из этого

Use the answers to calibrate Step 3 — e.g. "ограничения на работу из РФ" is
a sharper red flag when the target is a Russian-only company than when the
target itself is international.

### Step 3 — Red-flag diagnosis

Read `references/RED-FLAGS.md` for the pattern catalog. Go phrase by phrase
through the user's draft (not the whole answer at once) and for each
flagged phrase produce:

1. The quoted phrase
2. **Почему плохо** — what the HR person concludes about the candidate (not
   just "звучит плохо" — name the inference: victim framing, disloyalty,
   arrogance, passive cliché, oversharing, mercenary motivation, etc.)
3. Severity — call out critical (signals disloyalty, conflict-proneness,
   or victim framing) vs. minor (clichés that just dilute impact) so the
   user knows what to fix first

Don't invent red flags that aren't there — if a draft is clean, say so
plainly rather than padding the response with weak nitpicks.

### Step 4 — Rewrite

Read `references/ANSWER-STRUCTURE.md` for the rewrite frameworks. Default
to the **Past (factual, neutral) → Present (skill/motivation) → Future
(value to them)** structure for "why are you looking" / "why us" type
questions; use the STAR variant instead for behavioral/conflict questions
("расскажите о ситуации, когда...").

**Universal answer formula** (works for most HR questions):
- **Прошлое (Past):** Factual, neutral reason for change — no victim framing, no complaints
- **Настоящее (Present):** What you're skilled at and what motivates you — new challenges, growth areas, types of work
- **Будущее (Future):** Concrete value you'll bring to *them* — how your interests align with what they need

Produce one rewritten answer, calibrated to the company type from Step 2.
Keep it in the user's own voice/vocabulary where possible — don't make it
sound like a template.

### Step 5 — Iterate

Ask if the user wants it shorter, more confident, less formal, or wants a
second version for a different company type. Loop on this until they're
satisfied — don't re-run the full diagnosis on every iteration, just adjust
the rewrite.

## Common Question Formulas

Reference these patterns when rewriting answers to typical HR questions. Each follows the same structure:
- **Зачем спрашивают?** — what the HR person is evaluating
- **Что хотят услышать** — the answer formula (structure and tone)
- **Чего не стоит говорить** — specific phrases and patterns that trigger red flags

---

### "С чем связан твой поиск?" / "Почему ты ищешь новую работу?"

**Зачем спрашивают?**
Выяснить, нормально ли ты уходишь (карьерный рост, новые задачи) или сбегаешь (конфликт, неудача). Хотят услышать логику, а не драму.

**Что хотят услышать:**
(Факт без негатива) → (Что тебя мотивирует) → (Почему именно здесь)
- Прошлое: Нейтральная причина ухода — смена направления, новые вызовы, развитие навыка (НЕ "сократили", "не понимал начальник", "надоело")
- Настоящее: Что тебе интересно делать, какие задачи тебя зажигают (технологии, масштаб, характер работы)
- Будущее: Конкретное совпадение между твоей мотивацией и этой ролью

**Чего не стоит говорить:**
"Сократили, начальник не понимал, надоело, нужны деньги, хочу стабильности" — все это звучит как жалоба, а не карьерный выбор.

---

### "Почему именно наша компания?" / "Почему ты хочешь работать у нас?"

**Зачем спрашивают?**
Проверяют, ты ли нас ищешь или мы просто один из сотни резюме. Хотят услышать, что ты сделал домашнее задание.

**Что хотят услышать:**
(Твой фон) → (Конкретные факты о них) → (Чем ты им полезен)
- Прошлое: Краткое упоминание того, чем ты занимаешься (контекст только)
- Настоящее: Конкретные детали о компании — продукт, техстек, рынок, как они решают задачи (НЕ "инновационная", "амбициозная команда")
- Будущее: Какие конкретные проблемы ты можешь решить для них, основываясь на том, что ты о них узнал

**Чего не стоит говорить:**
"Вы инновационная компания, амбициозная команда, интересный продукт" — это выглядит как гугл (скопировалось из их сайта). Также не переусложняй, как сильно ты хочешь работать — это звучит отчаянно.

---

### "Расскажи о своих слабых сторонах"

**Зачем спрашивают?**
Насколько ты самокритичен и готов расти. Хотят услышать не жалобу на себя, а доказательство того, что ты способен распознавать проблемы и действовать.

**Что хотят услышать:**
Структура **PAR** (Problem/Awareness → Action → Result) — отличается от STAR и PPF:
- **Проблема/Осознание:** Одна конкретная слабость, которую ты заметил (не generic-humble вроде "слишком перфекционист", не абстрактная "есть точки роста")
- **Действие:** Конкретные шаги, которые ты предпринял (наставник, эксперимент, изменение подхода) — ты брал инициативу
- **Результат:** Что конкретно изменилось в твоем поведении (не "команда стала работать лучше", а "я теперь делегирую")

**Пример:**
"Моя зона роста — делегирование. Раньше я занимался микроконтролем: постоянно проверял результаты, перепроверял код. Я начал сознательно давать коллегам задачи без постоянного надзора и просить feedback вместо того, чтобы сам все проверять. Теперь я доверяю процессу и могу сосредоточиться на стратегических вещах."

**Чего не стоит говорить:**
- Fake-humble: "Я слишком много работаю, слишком требователен к себе, не умею говорить нет"
- Абстрактное: "Мне интересно развиваться, есть точки для роста" (что это за точки?)
- Винить окружение: "Мне легче сделать самому, чем ждать, пока коллеги..." (ты винишь их медлительность, а не называешь свою проблему)
- Центральная слабость для роли: если ищут Java-разработчика, не говори "не знаю Java"

---

### "Расскажи о ситуации, когда ты конфликтовал с коллегой/начальником"

**Зачем спрашивают?**
Как ты решаешь конфликты: берёшь ответственность или ищешь виноватых. Хотят услышать про действия, а не про чувства.

**Что хотят услышать:**
(Факт) → (Твоя ответственность) → (Твои действия) → (Результат)
- Ситуация: Нейтральное описание (кто, что, почему возник конфликт — БЕЗ обвинений)
- Задача: Что надо было сделать и почему это была твоя ответственность
- Действие: Конкретные шаги ТЫ (не "мы обсудили" — "я предложил", "я документировал", "я инициировал")
- Результат: Конкретный исход (проблема решена, отношения улучшились, команда выросла)

**Чего не стоит говорить:**
"Он был неправ, я был прав, я ничего не виноват" — это жалоба. Также не оканчивай на "я ничего не выучил" — покажи, что конфликт чему-то научил.

---

### "Какие у тебя ожидания по зарплате?"

**Зачем спрашивают?**
Понять, укладываешься ли ты в бюджет и готов ли к переговорам или будешь требовать.

**Что хотят услышать:**
(Исследование) → (Обоснованное число) → (Гибкость)
- Прошлое: Данные о рынке (какие зарплаты видел в этой области и на твоём уровне)
- Настоящее: Твои ожидания, основанные на опыте и скоупе этой конкретной роли (не на прошлой зарплате)
- Будущее: Готовность обсуждать (компенсация за счёт бонуса, акций, гибкости, роста) — показываешь, что готов к диалогу

**Чего не стоит говорить:**
"Не знаю, сколько мне платили раньше" (неуверенность), "Вот столько я требую, не меньше" (агрессия), якорение только на прошлую зарплату — это ограничивает переговоры.

---

### "Расскажите о вашем опыте работы" / "Расскажи о себе профессионально"

**Зачем спрашивают?**
Структурировать твой путь, понять твою логику мышления и умение выделять главное. Это не резюме — это рассказ.

**Что хотят услышать:**
(Кто ты сейчас) → (Ключевой пример/прогресс) → (Почему это важно для этой роли)
- Кто ты: Текущая роль, основная экспертиза, годы в поле (одно предложение)
- Ключевой пример: 1–2 достижения или области, где ты вырос, и чему это тебя научило (НЕ список всех мест)
- Почему сейчас: Как этот опыт напрямую решает их задачи или подходит для этой роли (не просто "интересно")

**Чего не стоит говорить:**
"Начинал как..., потом был..., затем..." (резюме по датам), "Я умею всё: требования, архитектуру, DevOps, фронтенд" (звучит как защита), огромное количество компаний и технологий без контекста, ответ дольше 2 минут — скучно и показываешь, что не можешь выделить главное.

---

### "Кем вы видите себя через пять лет?" / "Где вы хотите быть через 5 лет?"

**Зачем спрашивают?**
Оценить твою мотивацию, амбиции и укладываешься ли ты в долгосрочную стратегию компании. Хотят услышать реалистичный вектор, а не бегство или слишком узкую фокусировку.

**Что хотят услышать:**
(Твой путь) → (Конкретное направление) → (Связь с компанией)
- Путь: Краткое резюме того, куда ты уже пришёл в карьере (1–2 предложения, не самовосхваление)
- Вектор: Специфический, реалистичный рост (глубина экспертизы, новые навыки, архитектура, лидерство в узкой области) — не "открою свой бизнес" и не "займу вашу должность"
- Связь с компанией: Как эта компания помогает тебе расти в этом направлении (развивают именно эту экспертизу? Есть менторы? Задачи, где ты вырастешь?)

**Чего не стоит говорить:**
"Направление может измениться, не знаю точно, хочу открыть свой стартап, хочу в менеджмент, хочу на твою должность" — всё это звучит как отсутствие плана. Также не фокусируйся на том, чего ты НЕ хочешь ("не в менеджмент") — фокусируйся на том, что ты ХОЧЕШЬ.

---

### "Какие ваши сильные стороны?" / "Расскажите о своих преимуществах"

**Зачем спрашивают?**
Найти одну силу, которая тебя выделяет, и понять, сможешь ли ты её применить в их контексте. Хотят услышать не шаблонные качества, а осознание своих реальных преимуществ.

**Что хотят услышать:**
(Одна конкретная сила) → (Пример с результатом/метриками) → (Релевантность для них)
- Сила: Одна, но специфическая (не "многоролевой", а "проектирую масштабируемые системы" или "быстро разбираюсь в незнакомом коде")
- Пример: Реальная ситуация, где эта сила проявилась. Не процесс ("помогал команде"), а конкретный результат — artifact, метрики, impact (70% latency drop, запустили за 3 месяца, удвоили пропускную способность)
- Релевантность: Как эта сила решает именно их задачи — смотри их job description, стек, масштаб задач

**Чего не стоит говорить:**
"Несколько ролей одновременно, помогаю команде работать эффективнее, коммуникабельный, стрессоустойчивый" — все это звучит как generic cliché или мягкие скилы без доказательства. Также не говори о силе, которая не связана с вакансией (если ищут backend-архитектора, не лучшее время рассказывать о лидерских качествах). Не пропускай пример — заявление без доказательства не credible.

---

## References

- `references/RED-FLAGS.md` — catalog of common red-flag patterns (RU job
  market specifics included) with the HR inference each one triggers
- `references/ANSWER-STRUCTURE.md` — Past-Present-Future and STAR rewrite
  frameworks, plus tone calibration by company type
