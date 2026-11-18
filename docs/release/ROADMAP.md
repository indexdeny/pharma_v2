# Roadmap

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tag names are retained; their objects were replaced with cleaned historical versions on 2026-11-18. See the [ref migration report](../../REMOTE_REF_MIGRATION_REPORT.md).

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> Grounded in the existing architecture and the audit findings — no speculative
> features. Effort: S (hours) / M (days) / L (week+) / XL (multi-week).

## v1.1 — Reliability (minor improvements)

| Item | Business value | Effort | Dependencies |
|---|---|---|---|
| Free-disk-space pre-flight guard (TD-C1) | Prevents silent partial runs | S | none |
| Per-SKU post-mortem record — `{stem, prompt_hash, timestamp, outcome}` (TD-C2) | Diagnosable failures | S–M | none |
| Warn on schema-skip; Stage-3 `failed/` trail (TD-M4) | No silent data gaps | S | none |
| Remove/annotate orphaned `.env` keys (TD-L1) | Clear credential model | S | none |

## v1.2 — Operations (operational improvements)

| Item | Business value | Effort | Dependencies |
|---|---|---|---|
| Single structured (JSON) status/metrics feed — total/done/remaining/errors/ETA | External monitoring | M | none |
| One-shot `regenerate(sku)` helper | Faster operator workflow | S–M | none |
| Archive legacy `pipeline/cv/`; trim `opencv`/`numpy` from prod env (TD-L2) | Leaner runtime | S | none |

## v1.5 — CRM Adapter maturity

| Item | Business value | Effort | Dependencies |
|---|---|---|---|
| Thin service adapter: `render` / `status` / `regenerate` API | CRM can trigger & query | M | v1.2 status feed |
| Async job **queue** with one render worker | Orderly CRM-driven runs | M | adapter |
| Status store + event hooks (RenderStarted/PassportGenerated/ImageReady/ImageFailed/Completed) | Event-driven integration | M–L | adapter, status feed |

> Implements **Option 2** from [BUSINESS_VALUE_INTEGRATION.md](../BUSINESS_VALUE_INTEGRATION.md), over the unchanged renderer.

## v2.0 — API renderer (architectural)

| Item | Business value | Effort | Dependencies |
|---|---|---|---|
| Replace browser RPA with an **API-based image renderer** (e.g. Imagen/Vertex) | Concurrency, determinism, removes Gemini-DOM risk (RK-1) | XL | Paid-API budget decision; CRM-volume/SLA justification |
| Multi-worker concurrent rendering | Scale to 100s of SKU in parallel | L | API renderer |

> v2.0 directly retires the highest technical risk (RK-1) and the throughput
> ceiling, but is justified only when CRM volume/SLA demand it (see CRM Readiness
> audit). The surrounding Pipeline (passports, optimization, SSOT, resume) is
> already sound and would be reused.

## Sequencing rationale

v1.1 buys reliability cheaply; v1.2 makes the system observable/automatable;
v1.5 delivers CRM value without re-architecting; v2.0 is the only item that
changes the core, and only when the business case is clear.
