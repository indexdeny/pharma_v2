# CRM Readiness Audit

> **Phase:** PharmaGen PRO v1.0 — Production Hardening
> **Date:** 2026-06-28 · **Type:** read-only integration analysis (no code changed)
> **Goal:** look at the pipeline through a CRM's eyes — integration points, APIs,
> events, statuses, queues, per-SKU regeneration. **Analysis only; nothing built.**

## Verdict

PharmaGen PRO is today a **batch CLI tool**, not a service. Its stage boundaries
are clean (file-based handoffs keyed by SKU stem), which makes integration
*tractable*, but four things are missing for CRM: **a programmatic API**, an
**event/callback channel**, an **explicit status model**, and **concurrency**
(the render stage is serial by design). This document maps what exists to what a
CRM integration would need.

---

## 1. Integration points (what exists)

SKU identity = the filename **stem** (e.g. `217-min`), keyed off the `picture`
column in `SSOT/SKU.csv`. The pipeline is a chain of file-based handoffs:

```
SSOT/ (SKU.csv + master.json)  +  pipeline/passports/<stem>.json
        │  Stage 1
        ▼
pipeline/passports.markdown/<stem>.md
        │  Stage 2 (Gemini RPA)
        ▼
render_output/raw/<stem>.png
        │  Stage 3
        ▼
output/<stem>.webp        ← final deliverable, addressable by SKU stem
```

These boundaries are the natural integration seams: a CRM can drop inputs and
read `output/<stem>.webp` per SKU. **Coupling risk:** integration via the
filesystem + stem convention is implicit; there is no contract/manifest.

## 2. Programmatic API — needed vs. existing

| Need | Exists today? | Closest current mechanism |
|---|---|---|
| `render(sku_id)` | 🔴 No | `python main.py --render-only --from <stem> --limit 1` (operates on the *unprocessed* list, skips done) |
| `regenerate(sku_id, force=True)` | 🔴 No | Manual: delete `render_output/raw/<stem>.png` (+ `output/<stem>.webp`) then re-run (see §6) |
| `status(sku_id)` | 🔴 No | Derive from filesystem (see §5) |
| `batch(sku_ids)` / `list_status()` | 🔴 No | Whole-catalogue CLI only |

The logic exists internally (`src/passport_generator.py`, the per-passport loop
in `src/rpa_orchestrator.py`, `process_batch` in `src/image_processor.py`) but is
**not exposed as a stable, per-SKU callable**. Current entry point is the CLI /
subprocess orchestrator, not `render(sku)`.

## 3. Events — needed vs. existing

**None are emitted today.** The pipeline communicates only via log lines and
files. Where each requested event *would* hook into existing code:

| Event | Natural emit point (current code) |
|---|---|
| `RenderStarted` | start of the per-passport loop iteration (`rpa_orchestrator` main loop) |
| `PassportGenerated` | after the Stage 1 Markdown write (`passport_generator.main`) |
| `ImageReady` | after `save_progress(stem)` on success |
| `ImageFailed` | inside `log_failure(...)` |
| `Completed` | end-of-run summary (`main.py` / RPA `finally`) |

**Gap:** no event bus, callback, or webhook channel — a CRM cannot subscribe; it
must poll the filesystem.

## 4. Statuses — needed vs. existing

There is **no explicit status field**; state is *implicit* in the filesystem:

| CRM status | How it maps today | Persisted? |
|---|---|---|
| `Pending` | MD exists, no `raw/<stem>.png` | implicit |
| `Running` | in-flight; only visible in the live log | 🔴 not persisted |
| `Retry` | timed-out stem re-attempted in the end-of-run pass | 🔴 transient |
| `Completed` | `raw/<stem>.png` (and/or `output/<stem>.webp`) present | implicit (file) |
| `Failed` | entry in `failed_logs/failures.log` + screenshot | yes (log) |
| `Cancelled` | Ctrl+C | 🔴 not recorded per SKU |

**Gap:** no per-SKU state machine or status store; statuses must be inferred.

## 5. Queues & concurrency — "20 / 100 / 500 SKU at once?"

| Stage | Parallelizable? | Reality |
|---|---|---|
| Stage 1 (passports) | ✅ trivially | pure transform, ~all 391 in seconds |
| **Stage 2 (render)** | 🔴 **No (serial by design)** | one Chrome browser, one Gemini chat, `batch_size=1` (context reset per image); throughput = N × per-image latency (up to the 180 s timeout). Backoff/throttle handling implies Gemini rate-limits. |
| Stage 3 (WEBP) | ✅ easily | CPU/IO; currently a serial loop but fast |

**Answer:** generating 20 / 100 / 500 SKU *simultaneously* is **not possible
today** — rendering is a sequential queue of one. True concurrency would require
multiple authenticated browser sessions/profiles (unsupported) and would risk
Gemini throttling. **For CRM, model rendering as an async job queue with a single
render worker** (or N workers = N sessions, a future capability).

## 6. Per-SKU regeneration — "re-render SKU 217 alone?"

Possible but **indirect**:

1. Delete `render_output/raw/217-min.png` (makes it "unprocessed" again).
2. `python main.py --render-only --from 217-min --limit 1`.
3. Delete `output/217-min.webp` and run `python main.py --process-images-only` (without `--resume`, or it skips the existing file).

**Gap:** no one-shot `regenerate(217)`; regeneration means manual artifact
deletion + targeted re-run.

## 7. SKU lifecycle (conceptual, for CRM modelling)

```
Pending ──▶ Running ──▶ Completed
              │  ▲          
              ▼  └── Retry  
            Failed            (Cancelled on user/host interruption)
```

---

## CRM-readiness matrix

| Capability | Status | Note |
|---|---|---|
| Integration points (file-based, per-stem) | 🟢 present | clean seams; needs a documented contract |
| Programmatic API (`render(sku)`) | 🔴 missing | CLI/subprocess only |
| Events / callbacks | 🔴 missing | poll-only |
| Explicit status model | 🟡 implicit | inferable from filesystem |
| Concurrency / queue | 🔴 serial | render is one-at-a-time |
| Per-SKU regeneration | 🟡 indirect | manual delete + re-run |
| Cancellation | 🟡 partial | Ctrl+C, not per-SKU |

## Recommended integration shape (analysis, not a build instruction)

A thin **service/adapter layer** over the existing stages would close the gaps
without touching stage logic: a per-SKU API (`render`/`status`/`regenerate`), an
async **job queue** with one render worker, a **status store** (the state machine
in §7), and **event hooks** at the five points in §3. The file-based seams in §1
remain the data contract. **All of this is future work — out of scope for this
audit phase.**

> This audit only analyses integration readiness. Per the phase scope, no code
> or interfaces were built.
