# PharmaGen PRO — Полный архитектурный аудит и план реструктуризации

## Executive Summary

Аудит 390 SKU pipeline (389 passports v2.1 + 1 test v3.0). Выявлено **37 проблем** в 6 категориях. Ниже — детальный breakdown с приоритезацией и конкретными fix-планами.

---

## 1. AUDIT REPORT — Критические находки

### 1.1 Дублирование логики (CRITICAL)

| # | Проблема | Файлы | Severity |
|---|---------|-------|----------|
| A1 | **Два параллельных конвейера** — `convert_passports_to_md.py` (v3.0 schema) и `pass_tomd_v2.1.py` (v2.1 schema) делают одно и то же: JSON → Markdown. Они используют разные схемы, разные шаблоны, разную верификацию | [convert_passports_to_md.py](file:///c:/pharma_v2/convert_passports_to_md.py) vs [pass_tomd_v2.1.py](file:///c:/pharma_v2/pass_tomd_v2.1.py) | 🔴 CRITICAL |
| A2 | **Два калькулятора размеров** — `dimension_calculator.py` (legacy, flat/cubic grouping) и `pharma_pkg/dimension_resolver.py` (новый, primary→secondary clearance). Оба активны, но используются разными конвейерами | [dimension_calculator.py](file:///c:/pharma_v2/dimension_calculator.py) vs [dimension_resolver.py](file:///c:/pharma_v2/pharma_pkg/dimension_resolver.py) | 🔴 CRITICAL |
| A3 | **Двойная верификация** — `verification_agent.py` содержит и `agent_2_verifier()` (функция, используемая v2.1) и `VerificationAgent` (класс, используемый v3.0 converter). Класс обёртывает функцию, но добавляет собственную логику статусов с конфликтующими порогами | [verification_agent.py](file:///c:/pharma_v2/verification_agent.py) | 🟡 HIGH |
| A4 | **`pass_tomd_old.py`** — 36KB мёртвого кода, предшественник v2.1. Не используется | [pass_tomd_old.py](file:///c:/pharma_v2/pass_tomd_old.py) | 🟢 LOW |

---

### 1.2 Конфликты схем (CRITICAL)

| # | Проблема | Детали | Severity |
|---|---------|--------|----------|
| B1 | **Schema mismatch**: `protocol.md` описывает Passport v3.0 (cv/kb/llm/validation блоки), но **ВСЕ 389 рабочих паспортов** — schema_version 2.1 (flat structure: brand_name, label_content, branding, etc.). Единственный v3.0 паспорт — `test_passport.json`, который `pass_tomd_v2.1.py` пропускает (`schema not in ("2.0", "2.1")`) | [protocol.md](file:///c:/pharma_v2/.agents/protocol.md) vs фактические passports | 🔴 CRITICAL |
| B2 | **`analyze-pharma.md` workflow** ожидает Passport v3.0 output (cv.spatial, cv.color_palette, kb.name), но ни один рабочий паспорт не использует этот формат | [analyze-pharma.md](file:///c:/pharma_v2/.agents/workflows/analyze-pharma.md) | 🔴 CRITICAL |
| B3 | **`convert_passports_to_md.py`** ожидает v3.0 schema (`cv.geometry.package_type`, `llm.text_interpretation.brand`), но все данные — v2.1. Скрипт фактически нерабочий на текущих данных | [convert_passports_to_md.py](file:///c:/pharma_v2/convert_passports_to_md.py) | 🔴 CRITICAL |
| B4 | **`GEMINI_RENDER_SPEC_EU_BLISTER.md`** описывает промпт-шаблон с blister strip (вытащенный из коробки), но в реальных шаблонах T1/T2/T3 в `pass_tomd_v2.1.py` — `FORBIDDEN: loose pills, blister pack`. Прямое противоречие | [GEMINI_RENDER_SPEC_EU_BLISTER.md](file:///c:/pharma_v2/SSOT/GEMINI_RENDER_SPEC_EU_BLISTER.md) vs templates in pass_tomd_v2.1.py | 🟡 HIGH |

---

### 1.3 Перезапись контекста между агентами

| # | Проблема | Детали | Severity |
|---|---------|--------|----------|
| C1 | **Agent 1 (Router)** всегда возвращает `is_override=False` — bottle override dead code. Строки 154-157 (`is_bottle = True`) → line 170 (`return "T1", False`). Бутылки маршрутизируются как T1 без override | [pass_tomd_v2.1.py:170-177](file:///c:/pharma_v2/pass_tomd_v2.1.py#L170-L177) | 🟡 HIGH |
| C2 | **Agent 3 (Architect)** получает `is_override` (всегда False), но содержит полный `TEMPLATE_BOTTLE` (строки 486-522) — мёртвый template, никогда не используется | [pass_tomd_v2.1.py:486-522](file:///c:/pharma_v2/pass_tomd_v2.1.py#L486-L522) | 🟡 HIGH |
| C3 | **Art-director.md** workflow описывает **единый шаблон рендера** (single template для всех), противореча системе T1/T2/T3 в `pass_tomd_v2.1.py` | [art-director.md](file:///c:/pharma_v2/.agents/workflows/art-director.md) | 🟡 HIGH |
| C4 | **Verification пропускает всё** — `brand_color_verified` присутствует во ВСЕХ 389 паспортах со значением `false`, что штрафует на -0.25 каждый паспорт. Результат: 37 из 389 падают ниже 0.70, но генерация не блокируется | [verification_agent.py:48-52](file:///c:/pharma_v2/verification_agent.py#L48-L52) | 🟡 HIGH |

---

### 1.4 Prompt Conflicts & Inconsistencies

| # | Проблема | Детали | Severity |
|---|---------|--------|----------|
| D1 | **Ingredient line duplication** — если `brand_name` ≈ `ingredient_name`, строка удаляется (L551-552), но дедупликация неточная: `brand_name.lower() in ingredient_name.lower()` даёт false positive для "Kamagra" в "Super Kamagra" | [pass_tomd_v2.1.py:551-552](file:///c:/pharma_v2/pass_tomd_v2.1.py#L551-L552) | 🟡 HIGH |
| D2 | **"Pills" terminology enforcement** — regex `re.sub(r'\b(?:Capsules?|Tablets?)\b', 'Pills', md)` на строке 710 не учитывает контекст. Заменяет даже внутри SERIES VISUAL ANCHOR или HTML-комментариев | [pass_tomd_v2.1.py:709-711](file:///c:/pharma_v2/pass_tomd_v2.1.py#L709-L711) | 🟢 MEDIUM |
| D3 | **FRONT PANEL GRID** не включает `ingredient_name` — строки 626-633 содержат brand_name, product_name, dosage, unit_count, но `ingredient_name` (active ingredient) отображается только если != brand_name и используется sentinel pattern | [pass_tomd_v2.1.py:619-635](file:///c:/pharma_v2/pass_tomd_v2.1.py#L619-L635) | 🟡 HIGH |
| D4 | **TZ_PharmaGen_PRO_FINAL.md** описывает markdown schema v2.0 (Part 4.1) с `[SCENE ENVIRONMENT]`, `[TYPOGRAPHY CONSTRAINTS]`, `[BRANDING]` блоками, но фактические шаблоны T1/T2/T3 используют `[SCENE HARDWARE]`, `[COLOR]`, `[PURITY]` — несовпадение секционирования | [TZ_PharmaGen_PRO_FINAL.md:208-248](file:///c:/pharma_v2/SSOT/TZ_PharmaGen_PRO_FINAL.md#L208-L248) | 🟢 MEDIUM |

---

### 1.5 RPA/Image Generator Issues

| # | Проблема | Детали | Severity |
|---|---------|--------|----------|
| E1 | **Error screenshots** — 24 error_gen_*.png файлов в корне проекта. Проблемы: timeout на image generation (240s), случайное открытие "+" attachment menu вместо Send button | Root directory error_gen_*.png | 🟡 HIGH |
| E2 | **Batch reset** — в предыдущей сессии добавлен `need_reset` флаг и JavaScript send button. Последний прогон: 17/20 success (85%), 3 errors. Причины ошибок: timeout и DOM instability | [gemini_image_generator.py](file:///c:/pharma_v2/gemini_image_generator.py) | 🟡 HIGH |
| E3 | **Image format** — генерируемые изображения сохраняются как PNG (874-989 KB), хотя protocol.md требует WEBP ≤500KB 2048×2048. Постпроцессинг отсутствует | Images directory | 🟡 HIGH |
| E4 | **Progress tracking** — `gemini_rpa_progress_v23.txt` (35 SKU) vs `gemini_rpa_progress.txt` (legacy) — два файла прогресса, не синхронизированы | Progress files | 🟢 MEDIUM |

---

### 1.6 Verification Layer Gaps

| # | Проблема | Детали | Severity |
|---|---------|--------|----------|
| F1 | **Нет cross-check цветов** — `brand_color_verified` всегда `false` в паспортах. Нет логики сравнения `palette.primary` с SSOT master данными | Verification gaps | 🟡 HIGH |
| F2 | **Нет проверки geometry vs product** — router определяет T1/T2/T3, но verifier не проверяет, адекватен ли выбранный template для данного SKU (например, spray → T2, а не T1) | Missing validation | 🟡 HIGH |
| F3 | **Нет hallucination detection** — после генерации рендера нет никакой проверки: соответствует ли сгенерированное изображение промпту (brand name, colors, dosage) | Missing post-render validation | 🟡 HIGH |
| F4 | **`project_reviewer.md`** workflow проверяет поля `primary_geometry`, `dosage_type`, `pill_color`, `material` — которых нет в v2.1 schema. Полностью неприменим к текущим данным | [project_reviewer.md](file:///c:/pharma_v2/.agents/workflows/project_reviewer.md) | 🟡 HIGH |

---

## 2. UPDATED ARCHITECTURE SUMMARY

### 2.1 Целевая архитектура (предлагаемая)

```
pipeline/passports/*.json (v2.1 — ЕДИНСТВЕННЫЙ формат)
        ↓
[Agent 1: Router]           — template routing T1/T2/T3/Bottle by geometry+product
        ↓
[Agent 2: Verifier]         — heuristic checks, SSOT cross-validation, confidence scoring
        ↓
[Agent 3: Architect]        — deterministic Markdown prompt builder
        ↓
pipeline/passports.markdown/*.md
        ↓
[gemini_image_generator.py] — Selenium RPA batch processor
        ↓
images/*.png
        ↓
[Agent 4: Post-Processor]   — PNG→WEBP conversion, 2048×2048, ≤500KB
        ↓
ready_images/*.webp
```

### 2.2 Файлы для удаления (dead code)

| Файл | Причина |
|------|--------|
| `convert_passports_to_md.py` | Дубликат, работает с несуществующим v3.0 schema |
| `dimension_calculator.py` | Заменён `pharma_pkg/dimension_resolver.py` |
| `pass_tomd_old.py` | Предшественник v2.1, 36KB мёртвого кода |
| `pipeline/passports/test_passport.json` | Единственный v3.0 паспорт, ломает batch processing |

### 2.3 Файлы для обновления

| Файл | Изменение |
|------|-----------|
| `.agents/protocol.md` | Синхронизировать schema с v2.1 (текущие данные), или чётко пометить как target v3.0 roadmap |
| `.agents/workflows/analyze-pharma.md` | Адаптировать под v2.1 schema |
| `.agents/workflows/project_reviewer.md` | Адаптировать field names под v2.1 |
| `.agents/workflows/art-director.md` | Синхронизировать с T1/T2/T3 system, не single template |
| `SSOT/GEMINI_RENDER_SPEC_EU_BLISTER.md` | Пометить как deprecated или привести в соответствие с FORBIDDEN blister policy |
| `verification_agent.py` | Расширить проверки, убрать class wrapper |
| `pass_tomd_v2.1.py` | Fix bottle override, ingredient dedup, grid completeness |

---

## 3. PROPOSED CHANGES

### Phase 1 — Dead Code Cleanup & Schema Consistency

> [!IMPORTANT]
> Все удаления — мягкие (перенос в `_archive/`). Никаких необратимых операций.

#### [ARCHIVE] [convert_passports_to_md.py](file:///c:/pharma_v2/convert_passports_to_md.py)
- Перенести в `_archive/convert_passports_to_md_v3.py`
- Причина: ожидает v3.0 schema, которой нет ни у одного из 389 рабочих паспортов

#### [ARCHIVE] [dimension_calculator.py](file:///c:/pharma_v2/dimension_calculator.py)
- Перенести в `_archive/`
- Причина: заменён `pharma_pkg/dimension_resolver.py`

#### [ARCHIVE] [pass_tomd_old.py](file:///c:/pharma_v2/pass_tomd_old.py)
- Перенести в `_archive/`

#### [DELETE] pipeline/passports/test_passport.json
- Единственный v3.0 паспорт, вызывает silent skip в main pipeline

---

### Phase 2 — Fix Agent 1 Router (Bottle Override)

#### [MODIFY] [pass_tomd_v2.1.py](file:///c:/pharma_v2/pass_tomd_v2.1.py)

**Fix C1**: `agent_1_router()` — возвращать `is_override=True` для bottles.

```diff
     if is_bottle:
-        return "T1", False
+        return "T1", True
```

**Fix D1**: Ingredient deduplication — использовать exact match вместо substring.

```diff
-    if brand_name.lower() in ingredient_name.lower() or ingredient_name.lower() in brand_name.lower():
+    if brand_name.strip().lower() == ingredient_name.strip().lower():
```

**Fix D3**: Добавить ingredient_name в FRONT PANEL GRID когда он отличается от brand_name.

```diff
     grid_lines = [
         f'- Top:          "{brand_name}"',
+        f'- Below Top:    "{ingredient_display}"',
         f'- Center:       "{product_name}"',
-        f'- Below Center: "{dosage}"',
+        f'- Below Center: "{dosage}"',
```

---

### Phase 3 — Strengthen Verification Agent

#### [MODIFY] [verification_agent.py](file:///c:/pharma_v2/verification_agent.py)

Расширить `agent_2_verifier()` следующими проверками:

1. **CHECK 7: Geometry vs Router consistency** — проверять что T1/T2/T3 assignment соответствует packaging_geometry
2. **CHECK 8: SSOT cross-validation** — загружать SSOT/master.json и проверять primary/accent цвета
3. **CHECK 9: Product name != empty** — базовая валидация
4. **Remove `brand_color_verified` penalty** — раз поле всегда false, оно шумит. Либо реализовать реальный cross-check, либо убрать штраф
5. **Удалить `VerificationAgent` class** — legacy wrapper, не используется активным конвейером

---

### Phase 4 — Workflow/Protocol Synchronization

#### [MODIFY] [protocol.md](file:///c:/pharma_v2/.agents/protocol.md)
- Добавить секцию "CURRENT STATUS: All production passports use v2.1 schema"
- Чётко пометить v3.0 schema как target/roadmap, не как текущий формат
- Добавить mapping table: v2.1 field → v3.0 equivalent

#### [MODIFY] [analyze-pharma.md](file:///c:/pharma_v2/.agents/workflows/analyze-pharma.md)
- Адаптировать input/output schema references под v2.1

#### [MODIFY] [art-director.md](file:///c:/pharma_v2/.agents/workflows/art-director.md)
- Заменить single template → T1/T2/T3 dispatching logic
- Добавить bottle override variant

#### [MODIFY] [project_reviewer.md](file:///c:/pharma_v2/.agents/workflows/project_reviewer.md)
- Заменить field names на v2.1: `primary_geometry` → `packaging_geometry`, etc.

---

### Phase 5 — Image Post-Processing Pipeline

#### [NEW] [image_postprocessor.py](file:///c:/pharma_v2/image_postprocessor.py)

Новый скрипт для post-processing сгенерированных изображений:
- PNG → WEBP конвертация (Pillow)
- Resize до 2048×2048 с сохранением aspect ratio (pad to square)
- Compression до ≤500KB
- Запись в `ready_images/`

---

### Phase 6 — RPA Hardening

#### [MODIFY] [gemini_image_generator.py](file:///c:/pharma_v2/gemini_image_generator.py)

1. Интегрировать `image_postprocessor.py` в post-save pipeline
2. Увеличить timeout до 300s для сложных промптов
3. Добавить retry logic с exponential backoff (1 retry per SKU)
4. Консолидировать progress tracking в один файл

---

## 4. VERIFICATION LAYER SPECIFICATION

### Source Strategy
```
Level 1: Structural validation (JSON schema, required fields)
Level 2: SSOT cross-validation (master.json lookup, color matching)  
Level 3: Semantic validation (geometry↔template consistency, dosage format)
Level 4: Post-render OCR validation (future — compare rendered text vs prompt)
```

### Confidence Logic (Updated)
| Check | Weight | Description |
|-------|--------|-------------|
| active_ingredient == product_name | -0.15 | Likely unfilled |
| active_ingredient empty | -0.15 | Missing data |
| primary == background (#FFF) | -0.30 | Invisible text risk |
| dosage no numeric | -0.20 | Invalid dosage format |
| unit_count empty | -0.10 | Missing quantity |
| **geometry↔template mismatch** | **-0.20** | **NEW: Router inconsistency** |
| **product_name empty** | **-0.25** | **NEW: Core identity missing** |
| **SSOT color mismatch** | **-0.10** | **NEW: Brand palette deviation** |

### Hallucination Prevention
- Deterministic templates (no LLM free-form generation for prompts)
- Exact quoted values only in FRONT PANEL GRID
- `_PURITY_ANCHOR` constraint block in every template
- Post-render: future OCR comparison (Phase 7+)

---

## 5. COMPATIBILITY REPORT

| Аспект | Backward Compatible? | Примечание |
|--------|---------------------|-----------|
| JSON passports v2.1 | ✅ Да | Нет изменений в schema |
| Markdown output format | ✅ Да | Структура та же, добавляется ingredient line |
| `gemini_rpa_md.py` | ✅ Да | Не трогается |
| SSOT/master.json | ✅ Да | Read-only |
| Image output format | ⚠️ Добавляется WEBP | PNG всё ещё генерируется, WEBP — postprocess |
| `verification_failures.log` | ⚠️ Расширяется | Новые типы предупреждений |
| `_archive/` | ✅ Безопасно | Мёртвый код, не ломает ничего |

---

## 6. EXECUTION ORDER

| Фаза | Действие | Риск | Время |
|------|---------|------|-------|
| 1 | Dead code cleanup → `_archive/` | 🟢 Minimal | 5 min |
| 2 | Fix Router (bottle override) + ingredient dedup | 🟢 Low | 15 min |
| 3 | Strengthen Verifier | 🟡 Medium | 20 min |
| 4 | Sync workflows/protocol docs | 🟢 Low | 15 min |
| 5 | Image post-processor (PNG→WEBP) | 🟢 Low | 15 min |
| 6 | RPA hardening | 🟡 Medium | 20 min |

**Total estimated: ~90 min of execution**

---

## Open Questions

> [!IMPORTANT]
> **Q1: Bottle Override Policy** — В `TZ_PharmaGen_PRO_FINAL.md` (line 107) написано: "bottle НЕ маршрутизируется в T2. Только T1 + geometry override." Но текущий код возвращает `is_override=False` для бутылок. Нужно ли включить bottle override (рендер как цилиндр), или оставить все SKU как картонные коробки?

> [!IMPORTANT]
> **Q2: v3.0 Schema Roadmap** — protocol.md и analyze-pharma.md описывают Passport v3.0 с cv/kb/llm блоками. Это target архитектура для будущей миграции, или мертвый документ? Если target — оставить docs, пометить как roadmap. Если deprecated — архивировать.

> [!IMPORTANT]
> **Q3: Blister Strip Policy** — `GEMINI_RENDER_SPEC_EU_BLISTER.md` описывает рендер с вытащенным блистером, но шаблоны T1/T2/T3 запрещают blister. Какая политика верна? Только коробка, или коробка + блистер?

> [!WARNING]
> **Q4: `brand_color_verified` field** — Присутствует во всех 389 паспортах как `false`. Это флаг для будущего auto-verification, или устаревшее поле? Рекомендация: убрать штраф -0.25 из verifier пока не реализован реальный cross-check, иначе 100% паспортов получают необоснованный penalty.
