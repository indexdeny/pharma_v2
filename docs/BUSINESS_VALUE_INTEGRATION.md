# PharmaGen PRO — Business Value & Integration

> A decision-oriented brief for management and the senior engineer. It frames the
> question "how should PharmaGen PRO live in the company?" — not the code.
> Cost is expressed in **effort/complexity**, not money.
> *(English first; Русская версия ниже.)*

## Executive Summary

PharmaGen PRO turns a pharmaceutical product catalogue into standardized,
web-ready packshot images through one automated pipeline. It has rendered the full
catalogue of **391 SKU** end to end and is production-ready as a **standalone
tool**. The strategic question is integration with the CRM. The system's value is
high (standardization + automation of manual design work); its main constraint is
that rendering is driven through the **Gemini browser UI** (free, but serial and
fragile). This brief lays out three integration paths and recommends a **phased,
low-risk middle option**.

## Current State

- **Done:** unified one-command pipeline (`main.py`), centralized config, resume,
  logging, tests, and full documentation (architecture, ADRs, operations, DR,
  backup, audits). 391 SKU delivered as WEBP in `output/`.
- **Limitations (from the audits):** rendering uses a logged-in **browser session,
  not an API** (architectural); it is **single-threaded** (one browser); images
  are **non-deterministic** (not reproducible); there is **no programmatic API,
  event channel, or status model** yet for a CRM to consume.

## Business Value

- **Standardization** — every SKU rendered to one consistent visual standard (colour zoning, optics, regulated text), removing per-image manual design.
- **Speed & scale of catalogue work** — a whole catalogue is produced by one command instead of manual art production.
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
betting on re-architecting the fragile, free renderer**. Keep `output/` as the
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
Полный каталог из **391 SKU** отрендерен от начала до конца; как **отдельный
инструмент** система готова к продакшену. Стратегический вопрос — интеграция с
CRM. Ценность высокая (стандартизация + автоматизация ручного дизайна); главное
ограничение — рендеринг идёт через **браузерный UI Gemini** (бесплатно, но
последовательно и хрупко). Ниже — три пути интеграции и рекомендация в пользу
**поэтапного, низкорискового среднего варианта**.

## Текущее состояние (Current State)

- **Сделано:** единый конвейер одной командой (`main.py`), централизованный
  конфиг, resume, логирование, тесты и полная документация (архитектура, ADR,
  эксплуатация, DR, бэкап, аудиты). 391 SKU поставлены в `output/` как WEBP.
- **Ограничения (по аудитам):** рендер использует **сессию браузера, а не API**
  (архитектурное); **однопоточность** (один браузер); изображения
  **недетерминированы** (не воспроизводятся); пока **нет программного API, канала
  событий и модели статусов** для потребления со стороны CRM.

## Бизнес-ценность (Business Value)

- **Стандартизация** — каждый SKU в едином визуальном стандарте (цветовое
  зонирование, оптика, регуляторный текст), без ручного дизайна на каждое изображение.
- **Скорость и масштаб** — весь каталог производится одной командой вместо ручного арт-продакшена.
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
