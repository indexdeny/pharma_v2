# PharmaGen PRO — Business Value & Integration

> **Historical integration proposal; corrected 2026-11-18.** CRM options and effort ratings below are proposals, not implemented integrations or measured business impact. The verified historical result is 389 final WebPs for 391 catalogue records; SKU 132/218 exports are missing. Current browser/visual acceptance is not established and no Production Ready certification is claimed.

> A decision-oriented brief for management and the senior engineer. It frames the
> question "how should PharmaGen PRO live in the company?" — not the code.
> Cost is expressed in **effort/complexity**, not money.
> *(English first; Русская версия ниже.)*

## Executive Summary

PharmaGen PRO turns a pharmaceutical product catalogue into standardized,
web-oriented packshot concepts through an operator-assisted pipeline. The historical set has **389 final WebPs for 391 catalogue records**, with final exports 132/218 absent. Local tests do not certify current attended rendering or production readiness. The strategic question is integration with the CRM. The system's value is
high (standardization + automation of manual design work); its main constraint is
that rendering is driven through the **Gemini browser UI** (serial and
fragile; current pricing/eligibility were not assessed). This brief lays out three integration paths and recommends a **phased,
low-risk middle option**.

## Current State

- **Done:** unified one-command pipeline (`main.py`), centralized config, resume,
  logging, tests, and full documentation (architecture, ADRs, operations, DR,
  backup, audits). 389 historical final WebPs were measured in the archived output set; final exports 132/218 were absent.
- **Limitations (from the audits):** rendering uses a logged-in **browser session,
  not an API** (architectural); it is **single-threaded** (one browser); images
  are **non-deterministic** (not reproducible); there is **no programmatic API,
  event channel, or status model** yet for a CRM to consume.

## Business Value

- **Standardization goal** — templates specify colour zoning, composition and label fields; catalogue-wide visual consistency and regulatory text correctness still require human acceptance.
- **Workflow automation** — Stages 1–3 share one CLI; Stage 0 remains manual and attended rendering remains necessary. No throughput improvement was measured here.
- **Reduced manual labour** — passport compilation, routing, sanitization and image optimization are automated and auditable.
- **Reproducible inputs** — the deterministic stages (passports) and the SSOT make the *input* side fully traceable and re-runnable.

## Integration Options

| # | Option | What it means | Effort | Complexity |
|---|---|---|---|---|
| 1 | **Standalone tool** | Keep as-is. CRM consumes finished assets from `output/` via a shared folder/manual export. | **S** | **S** |
| 2 | **Partial CRM integration** *(recommended)* | A thin service/adapter over the existing stages: per-SKU API (`render`/`status`/`regenerate`), a job **queue with one render worker**, a status store, and file-drop/event hooks. Render logic unchanged. | **M** | **M** |
| 3 | **Full CRM integration** | Real-time, event-driven, scalable: multiple concurrent render workers, SLAs, full lifecycle in the CRM. Requires solving the architectural limits (browser→API renderer, single-thread→concurrency). | **L–XL** | **L–XL** |

## Cost (effort & complexity, not money)

| Option | Build effort | Operational complexity | Risk added |
|---|---|---|---|
| 1 Standalone | minimal | low (manual hand-off) | none |
| 2 Partial | moderate (adapter + queue + status) | moderate | low — render engine untouched |
| 3 Full | high (re-architect rendering for concurrency, likely a **paid image API**) | high | high — depends on replacing browser RPA |

## Risks

- 🔴 **Gemini browser-automation dependency** — a Gemini UI change can halt rendering (DOM selectors). Highest single risk.
- 🔴 **Non-determinism** — images cannot be reproduced; `output/` must be treated as the system of record and backed up.
- 🟡 **Throughput ceiling** — serial single-browser rendering caps volume; true concurrency needs an API renderer (cost) or multiple sessions (unsupported today).
- 🟡 **Bus factor / operational knowledge** — mitigated by this documentation set, but the renderer remains specialist territory.

## Recommendation

Adopt **Option 2 (Partial CRM integration)** as the next step. It delivers
automation value (CRM can trigger renders, read status, fetch assets) **without
betting on re-architecting the UI-dependent renderer**. Keep `output/` as the
system of record. Defer **Option 3** until catalogue volume or SLA pressure
justifies the cost of an API-based, concurrent renderer — at which point the
browser-RPA constraint (and its determinism/throughput limits) is the thing to
buy out, not the surrounding pipeline, which is already sound.

---
---

# PharmaGen PRO — Бизнес-ценность и интеграция (Русская версия)

> Документ для принятия решения — для руководства и senior-разработчика. Отвечает
> на вопрос «как PharmaGen PRO должен жить в компании?», а не про код. Стоимость —
> в **трудозатратах и сложности**, не в деньгах.

## Краткое резюме (Executive Summary)

PharmaGen PRO превращает каталог фармацевтической продукции в стандартизированные,
готовые для веба изображения упаковок через единый автоматизированный конвейер.
Исторически проверены **389 итоговых WebP для 391 записи каталога**; экспорты 132/218 отсутствуют. Новый браузерный прогон и полная визуальная приёмка не выполнялись; готовность к production не заявляется. Стратегический вопрос — интеграция с
CRM. Ценность высокая (стандартизация + автоматизация ручного дизайна); главное
ограничение — рендеринг идёт через **браузерный UI Gemini** (последовательно и хрупко; цена и доступность аккаунта не проверялись). Ниже — три пути интеграции и рекомендация в пользу
**поэтапного, низкорискового среднего варианта**.

## Текущее состояние (Current State)

- **Сделано:** единый конвейер одной командой (`main.py`), централизованный
  конфиг, resume, логирование, тесты и полная документация (архитектура, ADR,
  эксплуатация, DR, бэкап, аудиты). Измерены 389 исторических итоговых WebP; экспорты 132/218 отсутствуют.
- **Ограничения (по аудитам):** рендер использует **сессию браузера, а не API**
  (архитектурное); **однопоточность** (один браузер); изображения
  **недетерминированы** (не воспроизводятся); пока **нет программного API, канала
  событий и модели статусов** для потребления со стороны CRM.

## Бизнес-ценность (Business Value)

- **Цель стандартизации** — шаблоны задают композицию, цвет и поля этикетки; единообразие каталога и корректность текста требуют визуальной приёмки.
- **Автоматизация этапов** — единый CLI охватывает Stage 1–3; Stage 0 ручной, рендер требует оператора. Измеренного выигрыша производительности здесь нет.
- **Снижение ручного труда** — компиляция паспортов, маршрутизация, санитаризация
  и оптимизация изображений автоматизированы и проверяемы.
- **Воспроизводимые входы** — детерминированные этапы (паспорта) и SSOT делают
  входную сторону полностью отслеживаемой и перезапускаемой.

## Варианты интеграции (Integration Options)

| № | Вариант | Суть | Трудозатраты | Сложность |
|---|---|---|---|---|
| 1 | **Отдельный инструмент** | Оставить как есть. CRM забирает готовые ассеты из `output/` через общую папку/ручной экспорт. | **S** | **S** |
| 2 | **Частичная интеграция с CRM** *(рекомендуется)* | Тонкий сервис-адаптер над существующими этапами: API на SKU (`render`/`status`/`regenerate`), **очередь с одним рендер-воркером**, хранилище статусов, хуки событий/файлов. Логика рендера не меняется. | **M** | **M** |
| 3 | **Полная интеграция в CRM** | Реальное время, событийность, масштабируемость: несколько параллельных воркеров, SLA, полный жизненный цикл в CRM. Требует снять архитектурные ограничения (браузер→API, однопоточность→параллелизм). | **L–XL** | **L–XL** |

## Стоимость (трудозатраты и сложность, не деньги)

| Вариант | Трудозатраты | Операционная сложность | Добавляемый риск |
|---|---|---|---|
| 1 Отдельный | минимальные | низкая (ручная передача) | нет |
| 2 Частичный | умеренные (адаптер + очередь + статусы) | умеренная | низкий — движок рендера не трогаем |
| 3 Полный | высокие (переархитектура рендера, вероятно **платный image API**) | высокая | высокий — зависит от замены браузерного RPA |

## Риски (Risks)

- 🔴 **Зависимость от браузерной автоматизации Gemini** — изменение UI Gemini может остановить рендер (DOM-селекторы). Наибольший единичный риск.
- 🔴 **Недетерминизм** — изображения невоспроизводимы; `output/` нужно считать системой записи и бэкапить.
- 🟡 **Потолок пропускной способности** — последовательный рендер одним браузером ограничивает объём; реальный параллелизм требует API-рендера (стоимость) или нескольких сессий (сейчас не поддерживается).
- 🟡 **Bus factor / операционные знания** — смягчены этим набором документации, но рендер остаётся зоной специалиста.

## Рекомендация (Recommendation)

Выбрать **Вариант 2 (частичная интеграция с CRM)** как следующий шаг. Он даёт
ценность автоматизации (CRM запускает рендер, читает статус, забирает ассеты)
**без ставки на переархитектуру хрупкого бесплатного рендера**. `output/` остаётся
системой записи. **Вариант 3** отложить до момента, когда объём каталога или
давление SLA оправдают стоимость API-рендера с параллелизмом — тогда «выкупать»
нужно именно ограничение браузерного RPA (и связанные с ним пределы детерминизма и
пропускной способности), а не окружающий конвейер, который уже устойчив.
