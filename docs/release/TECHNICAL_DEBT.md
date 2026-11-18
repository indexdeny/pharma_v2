# Technical Debt Register

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tag names are retained; their objects were replaced with cleaned historical versions on 2026-11-18. See the [ref migration report](../../REMOTE_REF_MIGRATION_REPORT.md).

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> Synthesized from the Production Readiness, Bus Factor, CRM Readiness and
> Architecture Health reviews. Effort: S (hours) / M (days) / L (week+).

## Critical — real production risks

| ID | Description | Impact | Probability | Recommended solution | Effort |
|---|---|---|---|---|---|
| TD-C1 | **No free-disk-space guard** before Stage 2/3 writes | A full disk degrades to silent per-item failures mid-run | Medium | Pre-flight `shutil.disk_usage` check; fail fast with a clear message | S |
| TD-C2 | **Post-mortem logging cannot reproduce a render** — prompt text and Gemini's reply are not captured | Hard to diagnose why a specific SKU failed | Medium | Persist `{stem, prompt_hash, timestamp, outcome}` per SKU | S–M |

## High — architectural limitations

| ID | Description | Impact | Probability | Recommended solution | Effort |
|---|---|---|---|---|---|
| TD-H1 | **Browser-RPA render**: serial, non-headless, **non-deterministic** | Caps throughput; images not reproducible | Certain (by design) | API renderer (ROADMAP v2.0) | L |
| TD-H2 | **Gemini UI/DOM fragility** (selector contract) | A UI change halts rendering | Medium | Isolate/annotate selectors; monitor; API renderer removes it | M |
| TD-H3 | **No CRM-facing API / events / status model / queue** | CRM can only consume files | Certain | Thin adapter (ROADMAP v1.5) | M–L |

## Medium — maintainability

| ID | Description | Impact | Probability | Recommended solution | Effort |
|---|---|---|---|---|---|
| TD-M1 | Two large modules (`passport_generator` ~1,500 LOC, `rpa_orchestrator` ~1,600 LOC) | Onboarding/maintenance cost | Medium | Split by responsibility when next touched | M |
| TD-M2 | **Magic numbers / heuristics undocumented in code** (optics 25°/35°/85mm, verifier weights, RGB ladder) | Risky to change safely | Medium | Constants glossary / inline rationale | S |
| TD-M3 | **Brand names hardcoded** in `is_liquid_or_device` (`lumigan/xalatan/latisse`) | New products may need code edits | Medium | Move to a data-driven list | S |
| TD-M4 | Schema-mismatch passports **silently skipped**; Stage 3 failures are **stdout-only** | Quiet data gaps | Low | Emit warnings; add a Stage-3 `failed/` trail | S |

## Low — cosmetic / hygiene

| ID | Description | Impact | Probability | Recommended solution | Effort |
|---|---|---|---|---|---|
| TD-L1 | **Orphaned `.env` keys** (`GEMINI_API_KEY`, `HF_TOKEN`) not used by the Pipeline | Misleading to a maintainer | n/a | Remove/annotate `.env`; document the browser-session credential | S |
| TD-L2 | `opencv-python` + `numpy` + legacy `pipeline/cv/` unused by the Pipeline | Dead weight | n/a | Archive `pipeline/cv/` to `trash/`; trim env | S |
| TD-L3 | `docs/ARCHITECTURE.md` header shows stale internal `v2.3/P8.0` | Reader confusion | n/a | Align to v1.0.0 naming | S |
| TD-L4 | Bilingual (RU/EN) code comments in render module | Onboarding friction | n/a | Normalize over time | S |

> All items are documentation findings; none were fixed in this phase (release engineering, not development).
