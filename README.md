# PharmaGen PRO

> Automated render factory that turns a pharmaceutical product catalogue (SSOT)
> into clean, production-ready packshot images through a single, resumable
> command-line pipeline.

*(English first — Русская версия ниже / Russian version below.)*

---

## Features

- **One command, whole catalogue.** `python main.py --full` runs every stage end to end.
- **Three well-separated stages** — Passport generation, AI render (RPA), final image optimization.
- **Single source of truth (SSOT).** Routing and product data come only from `SSOT/SKU.csv` + `SSOT/master.json`.
- **Centralized configuration** in one `config.yaml`; sensible built-in defaults if it is missing.
- **Resume-safe.** Interrupt at any point and re-run with `--resume` — no duplicated work.
- **Structured logging** (rich console + per-run file logs) and a final summary report.
- **Backward compatible.** Legacy entry points still work via thin shims.

## Architecture

```
SSOT  (SKU.csv + master.json)
  │
  ▼
Passport Generator   ── Stage 1 ──  src/passport_generator.py
  │
  ▼
Markdown Passports   (pipeline/passports.markdown/)
  │
  ▼
AI Renderer (RPA)    ── Stage 2 ──  src/rpa_orchestrator.py   (Selenium → Gemini)
  │
  ▼
PNG Output           (render_output/raw/)
  │
  ▼
WEBP Optimizer       ── Stage 3 ──  src/image_processor.py
  │
  ▼
Final Assets         (output/  ·  WEBP 1600×1600, ≤500 KB)
```

`main.py` orchestrates the three Stages, each as an isolated subprocess, adding
pre-flight checks, resume, retries, logging and a summary — without changing any
stage's internal logic. Editable diagram sources live in [`docs/diagrams/`](docs/diagrams/).

## Repository Structure

| Path | Purpose |
|---|---|
| `main.py` | Single entry point / orchestrator. |
| `config.yaml` | Central configuration (paths, RPA, image processor, logging). |
| `requirements.txt` | Runtime dependencies. |
| `src/` | Pipeline runtime: `passport_generator`, `rpa_orchestrator`, `image_processor`, `utils`. |
| `pharma_pkg/` | Routing / geometry / classifier library (used by Stage 1). |
| `schemas/` · `verification_agent.py` | Validation schema helpers and the rule-based verifier. |
| `SSOT/` | Single source of truth — `SKU.csv`, `master.json`, design specs. |
| `pipeline/` | Stage data: `passports/` (JSON input), `passports.markdown/` (MD output), `cv/`. |
| `render_output/` | Stage 2 output: `raw/` (PNG), `failed/`, `failed_logs/`. |
| `output/` | Stage 3 output — final WEBP assets (the shipped deliverables). |
| `input/` | Source product photos. |
| `scripts/` | Auxiliary / maintenance tools (QA, snapshots, sync utilities). |
| `tests/` | Unit tests. |
| `docs/` | Documentation and editable diagram sources. |
| `logs/` | Per-run logs (git-ignored). |
| `trash/` | Archival store of legacy/superseded artifacts (never auto-restored). |
| `pass_tomd.py`, `gemini_image_generator.py`, `webp_converter.py` | Back-compat shims → `src/`. |

## Installation

Requires **Python 3.10+** (Windows; the render Stage drives Chrome).

```bash
python -m pip install -r requirements.txt
```

The render Stage additionally needs a local **Chrome** with a Chrome profile that
has an authenticated **Gemini** session (see Known Limitations).

## Configuration

All tuning lives in [`config.yaml`](config.yaml). Defaults mirror the original
scripts, so the Pipeline runs even without the file. Sections:

- `paths.*` — SSOT, Stage I/O and bookkeeping locations.
- `rpa.*` — Chrome profile, Gemini URL, timeouts, batch size, `headless`.
- `image_processor.*` — final WEBP size (`1600×1600`) and weight cap (`500 KB`).
- `pipeline.render_retries` — stage-level retries for the render Stage.
- `logging.level` — `INFO` / `DEBUG` / `WARNING` / `ERROR`.

Use an alternate file with `--config path/to/config.yaml`.

## Usage

```bash
python main.py --full                      # all three Stages
python main.py --full --resume             # continue after an interruption
python main.py --passports-only            # Stage 1 only
python main.py --render-only --limit 5     # Stage 2, first 5 unprocessed
python main.py --render-only --from 50-min # Stage 2, start at stem 50-min
python main.py --process-images-only --resume   # Stage 3 only
python main.py --full --debug              # verbose logging
```

Flags: `--resume`, `--headless` (debug only — Gemini blocks headless render),
`--debug`, `--limit N`, `--from STEM`, `--config PATH`.

## Pipeline Stages

| Stage | Module | Input | Output |
|---|---|---|---|
| **1 — Passports** | `src/passport_generator.py` | `pipeline/passports/*.json` + SSOT | `pipeline/passports.markdown/*.md` |
| **2 — Renderer (RPA)** | `src/rpa_orchestrator.py` | `pipeline/passports.markdown/*.md` | `render_output/raw/*.png` |
| **3 — WEBP Optimizer** | `src/image_processor.py` | `render_output/raw/*.png` | `output/*.webp` |

- **Stage 1** is deterministic: JSON Passports + SSOT → Markdown Passports.
- **Stage 2** drives Chrome via Selenium against Gemini and saves raw PNGs.
- **Stage 3** upscales to WEBP `1600×1600` with auto-tuned quality (≤500 KB).

## Resume System

Re-running with `--resume` never duplicates work:

- **Stage 1** — skipped when every JSON Passport already has a Markdown file; otherwise re-generated in place.
- **Stage 2** — resumes natively via `gemini_rpa_progress_v23.txt` plus a scan of `render_output/raw/`; already-rendered SKUs are skipped and timed-out SKUs are retried automatically.
- **Stage 3** — skips any SKU whose `.webp` already exists.

**Ctrl+C** is safe at any point: progress is saved, the subprocess is terminated
cleanly, and `--resume` continues from where it stopped.

## Project Status

- **391 SKU rendered** (389 final WEBP)
- **Production Ready**
- **Unified Pipeline** (single entry point)
- **Resume Supported**

## Known Limitations

- The render Stage requires a **logged-in Gemini session** in the configured Chrome profile and must run **non-headless** (Gemini blocks headless image generation).
- Rendering is **browser-driven (RPA)**, not API-based; throughput depends on Gemini's UI.
- **Stage 0** (source image → JSON Passport) is a separate manual analysis step and is not part of this automated Pipeline.
- Profile/Downloads paths in `config.yaml` default to a **Windows** layout.

## Development Notes

Architecture principles:

- **SSOT only** — no business data is invented; routing comes from `SSOT/`.
- **Config-driven paths** — every location is resolvable from `config.yaml`, anchored to the project root.
- **Subprocess isolation** — each Stage runs exactly as its standalone script; the orchestrator never alters stage logic.
- **Faithful refactor** — Stage logic, templates, sanitization, color zoning and the WEBP math are unchanged.
- **Backward compatibility** — root shims preserve legacy commands and imports.

Run the tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## License / Internal Use

**Internal project of Pharma Progressive.** All rights reserved. For internal use
only — not for public distribution.

---
---

# PharmaGen PRO (Русская версия)

> Автоматизированная фабрика рендеринга, превращающая каталог фармацевтической
> продукции (SSOT) в чистые, готовые к продакшену изображения упаковок через
> единый возобновляемый конвейер командной строки.

## Возможности (Features)

- **Одна команда — весь каталог.** `python main.py --full` выполняет все этапы от начала до конца.
- **Три чётко разделённых этапа** — генерация Passport, AI-рендер (RPA), финальная оптимизация изображений.
- **Единый источник правды (SSOT).** Маршрутизация и данные о продукте берутся только из `SSOT/SKU.csv` + `SSOT/master.json`.
- **Централизованная конфигурация** в одном `config.yaml`; разумные значения по умолчанию, если файла нет.
- **Безопасное возобновление.** Прервите в любой момент и перезапустите с `--resume` — без дублирования работы.
- **Структурированное логирование** (rich-консоль + файловые логи на каждый запуск) и итоговый отчёт.
- **Обратная совместимость.** Старые точки входа работают через тонкие шимы.

## Архитектура (Architecture)

```
SSOT  (SKU.csv + master.json)
  │
  ▼
Passport Generator   ── Stage 1 ──  src/passport_generator.py
  │
  ▼
Markdown Passports   (pipeline/passports.markdown/)
  │
  ▼
AI Renderer (RPA)    ── Stage 2 ──  src/rpa_orchestrator.py   (Selenium → Gemini)
  │
  ▼
PNG Output           (render_output/raw/)
  │
  ▼
WEBP Optimizer       ── Stage 3 ──  src/image_processor.py
  │
  ▼
Final Assets         (output/  ·  WEBP 1600×1600, ≤500 КБ)
```

`main.py` оркестрирует три Stage, каждый — как изолированный подпроцесс, добавляя
pre-flight проверки, resume, retry, логирование и итоговый отчёт — не меняя
внутреннюю логику этапов. Редактируемые исходники диаграмм — в [`docs/diagrams/`](docs/diagrams/).

## Структура репозитория (Repository Structure)

| Путь | Назначение |
|---|---|
| `main.py` | Единая точка входа / оркестратор. |
| `config.yaml` | Центральная конфигурация (пути, RPA, обработчик изображений, логирование). |
| `requirements.txt` | Зависимости рантайма. |
| `src/` | Рантайм конвейера: `passport_generator`, `rpa_orchestrator`, `image_processor`, `utils`. |
| `pharma_pkg/` | Библиотека маршрутизации / геометрии / классификации (этап Stage 1). |
| `schemas/` · `verification_agent.py` | Помощники схем валидации и rule-based верификатор. |
| `SSOT/` | Единый источник правды — `SKU.csv`, `master.json`, спецификации дизайна. |
| `pipeline/` | Данные этапов: `passports/` (вход JSON), `passports.markdown/` (выход MD), `cv/`. |
| `render_output/` | Выход Stage 2: `raw/` (PNG), `failed/`, `failed_logs/`. |
| `output/` | Выход Stage 3 — финальные WEBP-ассеты (поставляемый результат). |
| `input/` | Исходные фотографии продуктов. |
| `scripts/` | Вспомогательные / обслуживающие инструменты (QA, снапшоты, sync-утилиты). |
| `tests/` | Юнит-тесты. |
| `docs/` | Документация и редактируемые исходники диаграмм. |
| `logs/` | Логи на каждый запуск (в .gitignore). |
| `trash/` | Архив легаси/устаревших артефактов (никогда не восстанавливается автоматически). |
| `pass_tomd.py`, `gemini_image_generator.py`, `webp_converter.py` | Шимы обратной совместимости → `src/`. |

## Установка (Installation)

Требуется **Python 3.10+** (Windows; этап рендера управляет Chrome).

```bash
python -m pip install -r requirements.txt
```

Этапу рендера дополнительно нужен локальный **Chrome** с профилем, в котором есть
авторизованная сессия **Gemini** (см. «Известные ограничения»).

## Конфигурация (Configuration)

Все настройки — в [`config.yaml`](config.yaml). Значения по умолчанию повторяют
оригинальные скрипты, поэтому конвейер работает и без файла. Разделы:

- `paths.*` — SSOT, ввод/вывод этапов и служебные пути.
- `rpa.*` — профиль Chrome, URL Gemini, таймауты, размер батча, `headless`.
- `image_processor.*` — размер финального WEBP (`1600×1600`) и лимит веса (`500 КБ`).
- `pipeline.render_retries` — повторы на уровне этапа для рендера.
- `logging.level` — `INFO` / `DEBUG` / `WARNING` / `ERROR`.

Альтернативный файл — `--config path/to/config.yaml`.

## Использование (Usage)

```bash
python main.py --full                      # все три этапа
python main.py --full --resume             # продолжить после прерывания
python main.py --passports-only            # только Stage 1
python main.py --render-only --limit 5     # Stage 2, первые 5 необработанных
python main.py --render-only --from 50-min # Stage 2, начать со stem 50-min
python main.py --process-images-only --resume   # только Stage 3
python main.py --full --debug              # подробное логирование
```

Флаги: `--resume`, `--headless` (только для отладки — Gemini блокирует headless-рендер),
`--debug`, `--limit N`, `--from STEM`, `--config PATH`.

## Этапы конвейера (Pipeline Stages)

| Этап | Модуль | Вход | Выход |
|---|---|---|---|
| **1 — Passports** | `src/passport_generator.py` | `pipeline/passports/*.json` + SSOT | `pipeline/passports.markdown/*.md` |
| **2 — Renderer (RPA)** | `src/rpa_orchestrator.py` | `pipeline/passports.markdown/*.md` | `render_output/raw/*.png` |
| **3 — WEBP Optimizer** | `src/image_processor.py` | `render_output/raw/*.png` | `output/*.webp` |

- **Stage 1** детерминирован: JSON Passport + SSOT → Markdown Passport.
- **Stage 2** управляет Chrome через Selenium и сохраняет сырые PNG из Gemini.
- **Stage 3** масштабирует в WEBP `1600×1600` с авто-подбором качества (≤500 КБ).

## Система возобновления (Resume System)

Перезапуск с `--resume` никогда не дублирует работу:

- **Stage 1** — пропускается, если у каждого JSON Passport уже есть Markdown; иначе перегенерируется на месте.
- **Stage 2** — нативный resume через `gemini_rpa_progress_v23.txt` и скан `render_output/raw/`; обработанные SKU пропускаются, SKU с таймаутом повторяются автоматически.
- **Stage 3** — пропускает SKU, у которых `.webp` уже существует.

**Ctrl+C** безопасен в любой момент: прогресс сохраняется, подпроцесс корректно
завершается, а `--resume` продолжает с места остановки.

## Статус проекта (Project Status)

- **391 SKU отрендерено** (389 финальных WEBP)
- **Production Ready**
- **Единый конвейер (Unified Pipeline)**
- **Поддержка возобновления (Resume Supported)**

## Известные ограничения (Known Limitations)

- Этап рендера требует **авторизованной сессии Gemini** в настроенном профиле Chrome и должен работать **не в headless** (Gemini блокирует headless-генерацию изображений).
- Рендеринг — **через браузер (RPA)**, не через API; пропускная способность зависит от UI Gemini.
- **Stage 0** (исходное изображение → JSON Passport) — отдельный ручной шаг анализа, не входит в этот автоматизированный конвейер.
- Пути профиля/Downloads в `config.yaml` по умолчанию рассчитаны на **Windows**.

## Заметки для разработчиков (Development Notes)

Архитектурные принципы:

- **Только SSOT** — бизнес-данные не выдумываются; маршрутизация берётся из `SSOT/`.
- **Пути из конфига** — любое расположение резолвится из `config.yaml`, с привязкой к корню проекта.
- **Изоляция подпроцессов** — каждый Stage работает точно как отдельный скрипт; оркестратор не меняет логику этапов.
- **Точный рефакторинг** — логика этапов, шаблоны, санитаризация, цветовое зонирование и математика WEBP не изменены.
- **Обратная совместимость** — корневые шимы сохраняют старые команды и импорты.

Запуск тестов:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Лицензия / Внутреннее использование (License / Internal Use)

**Внутренний проект Pharma Progressive.** Все права защищены. Только для
внутреннего использования — не для публичного распространения.
