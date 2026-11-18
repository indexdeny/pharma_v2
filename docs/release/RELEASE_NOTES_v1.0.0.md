# PharmaGen PRO v1.0.0 — Production Release (June 2026)

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tag names are retained; their objects were replaced with cleaned historical versions on 2026-11-18. See the [ref migration report](../../REMOTE_REF_MIGRATION_REPORT.md).

> Draft body for the GitHub Release of tag `v1.0.0`. Paste into the GitHub
> Release description when publishing (see the project's release procedure).
> **Not yet published** — publishing requires the rewritten history on the
> remote; defer until after the management presentation.

## What it is
PharmaGen PRO is an internal render factory that turns a pharmaceutical product
catalogue (SSOT) into standardized, web-ready packshot images through one
resumable command-line **Pipeline** (passports → render → final images).

## Status
**✅ Production Ready with Known Limitations** — see
[RELEASE_CERTIFICATION.md](RELEASE_CERTIFICATION.md).

## Highlights
- **391 SKU rendered to PNG; 389 delivered as final WEBP** (`output/`).
- **Unified Pipeline** — one entry point (`main.py`) over three stages.
- **Resume** — interruption-safe; re-running never duplicates work.
- **QA** — rule-based verifier + 18 unit tests.
- **WEBP** — final assets at 1600×1600, ≤500 KB.
- **CLI** — `--full` / `--passports-only` / `--render-only` / `--process-images-only` (+ `--resume`, `--limit`, `--from`, `--headless`, `--debug`, `--config`).
- **Documentation** — architecture, ADRs, audits, deployment, operations, disaster recovery, backup, design rationale, business/CRM brief, and the release-engineering set.

Full detail: [CHANGELOG.md](../../CHANGELOG.md).

## Known Limitations
- Rendering is **browser-driven (Gemini RPA)**: serial, non-headless, **non-deterministic** (`output/` is the system of record).
- **Gemini UI fragility** is the top technical risk (RK-1).
- **No free-disk-space guard** (TD-C1) — the one unmitigated production risk in code.
- **No CRM API/events/status/queue** (TD-H3); render path is **untested** (Testing 5/10).

## Roadmap (summary)
- **v1.1 — Reliability:** disk-space guard, per-SKU post-mortem logging.
- **v1.2 — Operations:** structured status/metrics feed, single-SKU regenerate, trim legacy CV.
- **v1.5 — CRM adapter:** `render`/`status`/`regenerate` API + job queue + events.
- **v2.0 — API renderer:** replace browser RPA (concurrency + determinism).

Full detail: [ROADMAP.md](ROADMAP.md).

## Release contents
Tag `v1.0.0` → commit "Operations Documentation". History: one squashed
pre-1.0 baseline + four phase commits (Architecture Unification → Repository
Cleanup → Production Hardening → Operations Documentation).

## Internal use
Internal project of **Pharma Progressive**. Not for public distribution.
