# Repository Scorecard

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tag names are retained; their objects were replaced with cleaned historical versions on 2026-11-18. See the [ref migration report](../../REMOTE_REF_MIGRATION_REPORT.md).

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> Honest 1–10 scoring with justification. Not inflated; critical where warranted.

| Area | Score | Justification |
|---|---:|---|
| **Architecture** | 8/10 | Clean boundaries, subprocess isolation, no import cycles, file-based seams. −2: two oversized core modules and the browser-RPA constraint. |
| **Documentation** | 9/10 | Extensive and current: bilingual README, ADRs, three audits, ops/deployment/DR/backup, design rationale, business brief, this release set. −1: one stale `ARCHITECTURE.md` header. |
| **Maintainability** | 7/10 | Config-driven, tested libs, back-compat shims. −3: ~1,500/~1,600-LOC modules, undocumented magic numbers, hardcoded brand heuristics. |
| **Readability** | 7/10 | Clear naming and structure. −3: the two large files; bilingual (RU/EN) comments in the render module. |
| **Operational Readiness** | 7/10 | Resume, internal retry, runbook, DR playbooks, monitoring via estimate/summary. −3: no disk guard; metrics scattered, not a single feed. |
| **Deployment** | 8/10 | `DEPLOYMENT.md`, `requirements.txt`, acceptance test, auto driver provisioning. −2: Windows-only defaults; manual one-time browser login. |
| **Testing** | 5/10 | 18 unit tests cover `pharma_pkg`, the verifier and QA helpers. −5: Stage 2/3 and the `main.py` orchestration are untested; the render path is inherently hard to test. The honest weak spot. |
| **Recovery** | 8/10 | Strong resume, documented backup tiers, per-scenario DR. −2: non-deterministic images and no disk guard. |
| **CRM Readiness** | 4/10 | Clean file-based seams, but no API, events, status model, or concurrency. Analysis done (Option 2 path), nothing built. Honestly low. |
| **Business Readiness** | 8/10 | Catalogue shipped (391 rendered, 389 final WEBP); value articulated; bilingual decision brief with options. −2: throughput/scale limits. |
| **Repository Hygiene** | 9/10 | Minimal root, `scripts/`, archival `trash/`, sound `.gitignore`, no committed secrets. −1: undocumented `dev` branch; unpushed history divergence. |
| **Knowledge Transfer** | 8/10 | ADRs, design rationale, project history, bus-factor audit raise the bus factor to ≥2. −2: specialist renderer knowledge (selectors) and magic numbers remain. |

## Overall

**Weighted impression: ≈ 7.3 / 10 — a solid, well-documented internal product
with clearly-stated constraints.** The standout strengths are documentation and
hygiene; the genuine weak spots are **testing coverage of the render/orchestration
path** and **CRM readiness** (by design — not yet built). Neither is hidden; both
are tracked in [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md) and [ROADMAP.md](ROADMAP.md).
