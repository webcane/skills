"""Run the four cane-learning stages and publish a reviewed article."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parent
STAGES = ("analyst", "designer", "writer", "reviewer")
TASK_COUNTS = {"focused": (3, 3), "standard": (3, 4), "deep": (4, 5)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_shape(value, schema, path="$"):
    """Validate the subset used by the bundled JSON Schemas."""
    kind = schema["type"]
    if kind == "object":
        require(isinstance(value, dict), f"{path}: ожидался объект")
        require(set(value) == set(schema["required"]), f"{path}: неверный набор полей")
        for key, child in schema["properties"].items():
            validate_shape(value[key], child, f"{path}.{key}")
    elif kind == "array":
        require(isinstance(value, list), f"{path}: ожидался массив")
        for number, item in enumerate(value):
            validate_shape(item, schema["items"], f"{path}[{number}]")
    elif kind == "string":
        require(isinstance(value, str) and value.strip(), f"{path}: ожидалась непустая строка")
        require("enum" not in schema or value in schema["enum"], f"{path}: неизвестное значение {value}")
    else:
        raise ValueError(f"{path}: неподдерживаемый тип схемы {kind}")


def index(items, key="id"):
    result = {item[key]: item for item in items}
    require(len(result) == len(items), f"Повторяющиеся значения {key}")
    return result


def refs(ids, valid, label, *, required=True):
    require((ids or not required) and len(set(ids)) == len(ids) and set(ids) <= set(valid),
            f"{label}: пустая, повторная или неизвестная ссылка {ids}")


def validate_links(role, data, state, depth):
    if role == "analyst":
        facets, knowledge, sources, mechanisms = (
            index(data[key]) for key in ("facets", "knowledge", "sources", "mechanisms")
        )
        core = {key for key, facet in facets.items() if facet["priority"] == "P0"}
        require(core and core <= {item["facet_id"] for item in knowledge.values()}, "P0 без знаний")
        for item in knowledge.values():
            refs([item["facet_id"]], facets, item["id"])
            refs(item["source_ids"], sources, item["id"])
        for mechanism in mechanisms.values():
            refs(mechanism["knowledge_ids"], knowledge, mechanism["id"])
        require(2 <= len(data["cases"]) <= 4, "Нужно 2–4 случая проверки модели")
        for case in data["cases"]:
            refs([case["mechanism_id"]], mechanisms, "Случай")
        return

    concept = state["analyst"]
    knowledge = index(concept["knowledge"])
    if role == "designer":
        facets, cells, tasks = index(concept["facets"]), index(data["cells"]), index(data["tasks"])
        pairs = {(cell["facet_id"], cell["competency"]) for cell in cells.values()}
        require(len(pairs) == len(cells), "Матрица содержит повторную пару грань × компетенция")
        mandatory = {key for key, cell in cells.items() if cell["importance"] == "required"}
        require({key for key, facet in facets.items() if facet["priority"] == "P0"} <=
                {cells[key]["facet_id"] for key in mandatory}, "P0 без обязательной клетки")
        for key, cell in cells.items():
            refs([cell["facet_id"]], facets, key)
            same_facet = {k for k, item in knowledge.items() if item["facet_id"] == cell["facet_id"]}
            refs(cell["knowledge_ids"], same_facet, key)
        tested = set()
        for key, task in tasks.items():
            check_ids = [check["cell_id"] for check in task["checks"]]
            refs(check_ids, cells, key)
            tested.update(check_ids)
        require(mandatory <= tested, "Обязательные клетки без задания")
        published = data["published_task_ids"]
        refs(published, tasks, "Опубликованные задания")
        minimum, maximum = TASK_COUNTS[depth]
        require(minimum <= len(published) <= maximum, f"Для {depth} нужно {minimum}–{maximum} заданий")
        return

    learning = state["designer"]
    cells = index(learning["cells"])
    if role == "writer":
        sections = index(data["sections"])
        require(sections, "Черновик без разделов")
        for key, section in sections.items():
            refs(section["knowledge_ids"], knowledge, key)
            refs(section["cell_ids"], cells, key, required=False)
            for cell_id in section["cell_ids"]:
                require(set(section["knowledge_ids"]) & set(cells[cell_id]["knowledge_ids"]),
                        f"{key}: отсутствует основание для {cell_id}")
        return

    sections, tasks = index(state["writer"]["sections"]), index(learning["tasks"])
    coverage = index(data["coverage"], "cell_id")
    mandatory = {key for key, cell in cells.items() if cell["importance"] == "required"}
    refs(list(coverage), mandatory, "Аудит покрытия", required=False)
    for key, row in coverage.items():
        refs([row["section_id"]], sections, key)
        refs([row["task_id"]], tasks, key)
        section = sections[row["section_id"]]
        task = tasks[row["task_id"]]
        require(key in section["cell_ids"] and row["quote"] in section["markdown"],
                f"{key}: цитата или связь с разделом отсутствует")
        require(key in {check["cell_id"] for check in task["checks"]},
                f"{key}: задача не проверяет клетку")
    blocking = any(item["severity"] == "blocking" for item in data["findings"])
    require((data["verdict"] == "revise") == blocking, "Вердикт расходится с замечаниями")
    if data["verdict"] == "pass":
        require(set(coverage) == mandatory, "Pass без доказательств по всем обязательным клеткам")
        explained = {key for section in sections.values() for key in section["knowledge_ids"]}
        core = {facet["id"] for facet in concept["facets"] if facet["priority"] == "P0"}
        require({key for key, item in knowledge.items() if item["facet_id"] in core} <= explained,
                "Pass при неполном покрытии P0")


def make_prompt(role, schema, brief, artifacts, feedback, previous):
    context = {"brief": brief, "artifacts": artifacts, "previous_review": feedback, "previous_stage_output": previous}
    return "\n\n".join([
        (ROOT / "methodology.md").read_text(encoding="utf-8"),
        (ROOT / "stages" / f"{role}.md").read_text(encoding="utf-8"),
        "Выполни только эту стадию. Верни один JSON-объект по схеме. "
        "Прочитай отзыв целиком, если он есть. Исправляй проблемы в пределах своей роли.",
        json.dumps(schema, ensure_ascii=False),
        json.dumps(context, ensure_ascii=False, indent=2),
    ])


def render_article(draft, learning):
    tasks = index(learning["tasks"])
    parts = [f"# {draft['title']}"]
    parts.extend(f"## {section['heading']}\n\n{section['markdown']}" for section in draft["sections"])
    parts.extend(["## Итоговая карточка", draft["review_card"], "## Самопроверка"])
    for number, key in enumerate(learning["published_task_ids"], 1):
        parts.append(f"### {number}. Задание\n\n{tasks[key]['prompt']}")
    if draft["deeper"]:
        parts.extend(["## Глубже", "\n".join(f"- {item}" for item in draft["deeper"])])
    return "\n\n".join(parts) + "\n"


def run(args, config, brief):
    args.out.mkdir(parents=True, exist_ok=False)
    depth = brief["depth"]
    brief["depth_policy"] = config["depth"][depth]
    write_json(args.out / "brief.json", brief)
    state, feedback, start = {}, None, 0
    for attempt in range(config["run"]["max_revisions"] + 1):
        name = f"round-{attempt + 1:02d}"
        folder = args.out / name
        folder.mkdir()
        for role in STAGES[:start]:
            write_json(folder / (config["contracts"][role] + ".json"), state[role])
        for position in range(start, len(STAGES)):
            role = STAGES[position]
            contract = config["contracts"][role]
            schema_path = ROOT / "schemas" / (contract + ".json")
            schema = read_json(schema_path)
            print(f"{name} · {role} → {contract}", flush=True)
            try:
                if args.replay:
                    raw = (args.replay / name / f"{contract}.json").read_text(encoding="utf-8")
                else:
                    prompt = make_prompt(role, schema, brief, {
                        key: state[key] for key in STAGES[:position]
                    }, feedback, state.get(role) if role != "reviewer" else None)
                    raw_file = folder / f"{contract}.raw.json"
                    with (folder / f"{role}.log").open("w", encoding="utf-8") as log:
                        subprocess.run(
                            [*config["run"]["command"], "--output-schema", str(schema_path),
                             "--output-last-message", str(raw_file), "-"],
                            input=prompt, encoding="utf-8", stdout=log, stderr=subprocess.STDOUT,
                            timeout=config["run"]["timeout_seconds"], check=True,
                        )
                    raw = raw_file.read_text(encoding="utf-8")
                artifact = json.loads(raw)
                validate_shape(artifact, schema)
                validate_links(role, artifact, state, depth)
            except (ValueError, OSError, subprocess.SubprocessError) as error:
                raise ValueError(f"{name}/{contract}: {error}") from error
            state[role] = artifact
            write_json(folder / f"{contract}.json", artifact)
        feedback = state["reviewer"]
        if feedback["verdict"] == "pass":
            (args.out / "article.md").write_text(
                render_article(state["writer"], state["designer"]), encoding="utf-8"
            )
            write_json(args.out / "result.json", {"status": "published", "round": name})
            return 0
        start = min(STAGES.index(item["owner"]) for item in feedback["findings"]
                    if item["severity"] == "blocking")
    write_json(args.out / "result.json", {"status": "revision_limit", "round": name})
    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path, help="TOML с учебным запросом")
    parser.add_argument("--out", type=Path, required=True, help="новый каталог результатов")
    parser.add_argument("--replay", type=Path, help="каталог подготовленных ответов для теста")
    args = parser.parse_args()
    try:
        config = tomllib.loads((ROOT / "pipeline.toml").read_text(encoding="utf-8"))
        brief = {
            "audience": "Опытный разработчик",
            "goal": "Практическое применение",
            "output_language": "ru",
            "depth": "standard",
            **tomllib.loads(args.request.read_text(encoding="utf-8")),
        }
        for key in ("topic", "technology", "version"):
            require(isinstance(brief.get(key), str) and brief[key].strip(), f"Нужно поле {key}")
        require(brief["depth"] in TASK_COUNTS, "Неизвестный режим глубины")
        require(type(config["run"]["max_revisions"]) is int and config["run"]["max_revisions"] >= 0,
                "max_revisions должен быть целым неотрицательным числом")
        return run(args, config, brief)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
