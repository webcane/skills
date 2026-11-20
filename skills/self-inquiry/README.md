# self-inquiry

Evidence-based self-inquiry: интерактивное самоисследование с тремя фазами,
семью выбираемыми модулями, проверкой гипотез и пересмотром выводов.
Не клинически валидированный тест, не диагностика и не психотерапия.

## Установка из checkout

Выполнить из корня этого репозитория:

```bash
# Собрать все пакеты и установить в Codex, OpenCode и Claude Code
bash scripts/install-local.sh self-inquiry

# Или установить только в выбранный harness
bash scripts/install-local.sh self-inquiry --target codex
bash scripts/install-local.sh self-inquiry --target opencode
bash scripts/install-local.sh self-inquiry --target claude-code
```

`INSTALL_DIR` ограничивает установку одним каталогом; прежние команды сохраняются:

```bash
INSTALL_DIR="$HOME/.agents/skills" bash scripts/install-local.sh self-inquiry
INSTALL_DIR="$HOME/.config/opencode/skills" bash scripts/install-local.sh self-inquiry
INSTALL_DIR="$HOME/.claude/skills" bash scripts/install-local.sh self-inquiry

# Для произвольного каталога формат можно задать явно
INSTALL_DIR=/path/to/skills bash scripts/install-local.sh self-inquiry --target codex
```

Без `INSTALL_DIR` пути по умолчанию: `~/.agents/skills` для Codex,
`${XDG_CONFIG_HOME:-~/.config}/opencode/skills` для OpenCode,
`~/.claude/skills` для Claude Code. `--target all` выбирает все три;
сочетание `INSTALL_DIR` и `--target all` отклоняется как неоднозначное.

Установщик собирает пакет и заменяет существующую папку `self-inquiry` в выбранном
каталоге. Не храните личные итоги в папке skill: повторная установка их удалит.
Для установки в проект укажите абсолютный путь к его `.agents/skills` (Codex),
`.opencode/skills` (OpenCode) или `.claude/skills` (Claude Code).
Откройте новую сессию и проверьте обнаружение skill клиентом.

Пути соответствуют официальным справочникам:
[Codex](https://learn.chatgpt.com/docs/build-skills),
[OpenCode](https://opencode.ai/docs/skills/),
[Claude Code](https://code.claude.com/docs/en/skills).

## Использование

В Codex: `$self-inquiry`. В Claude Code: `/self-inquiry`.
В OpenCode попросите загрузить skill `self-inquiry`.
Можно сразу добавить запрос:

- «Помоги понять, почему я откладываю сложные разговоры».
- «Хочу обзор моих ценностей и сильных сторон».
- «Пересмотри прежнюю гипотезу по этим новым ситуациям».

Интервью задаёт один вопрос за раз. Можно пропускать вопросы и завершать сессию.
По умолчанию результаты остаются в чате; сохранение в файл — по запросу.

## Сборка пакетов

```bash
# Собирает универсальный пакет и все три платформенных ZIP
bash scripts/package-skill.sh self-inquiry
```

Универсальный `dist/self-inquiry.skill` — tar.gz с `SKILL.md`, references и templates;
подходит также для ручной распаковки в каталог OpenCode.
Для Claude.ai предусмотрен отдельный `dist/self-inquiry-claudeai.zip`.
Для отдельной пересборки доступны `package-skill-codex.sh`,
`package-skill-claude-code.sh` и `package-skill-claudeai.sh`.
Требуются Python 3 с PyYAML, tar, zip и unzip.
Пакеты собираются локально; команды не публикуют GitHub Release и не устанавливают
skill в другие клиенты автоматически.
