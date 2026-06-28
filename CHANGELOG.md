# Changelog

All notable changes to **PharmaGen PRO** are documented here.
Format inspired by [Keep a Changelog](https://keepachangelog.com/).

## [v1.0.0] — Initial Production Release — June 2026

**PharmaGen PRO — Version 1.0 — Production Release.**

### Highlights
- **391 SKU** rendered end to end and delivered as final WEBP assets.
- **Unified Pipeline** — one entry point (`main.py`) over three stages (passports → render → final images).
- **Resume** — interruption-safe; re-running continues without duplicating work.
- **QA** — rule-based verifier plus a unit-test suite.
- **WEBP** — final assets at 1600×1600, ≤500 KB.
- **CLI** — `--full` / `--passports-only` / `--render-only` / `--process-images-only` with `--resume`, `--limit`, `--from`, `--headless`, `--debug`, `--config`.
- **Documentation** — architecture, ADRs, audits, deployment, operations, disaster recovery, backup, dependency inventory, acceptance test, design rationale, and a business/CRM brief.
- **Production Ready.**

### Release composition
This release groups four hardening phases (see the corresponding commits):
1. **Architecture Unification** — `main.py` + `config.yaml` + `src/` package + back-compat shims; stale absolute paths fixed.
2. **Repository Cleanup** — `scripts/`, archival `trash/`, bilingual README, Mermaid diagrams, repo audit.
3. **Production Hardening** — Bus Factor / Production Readiness / CRM Readiness audits, ADR-001..006, project history.
4. **Operations Documentation** — deployment, operations, disaster recovery, backup, dependency inventory, acceptance test, design rationale, business value & integration.

### Known limitations
- Rendering is browser-driven (Gemini RPA): requires a logged-in session, runs non-headless, and is single-threaded.
- Rendered images are **non-deterministic**; `output/` is the system of record (not reproducible by re-running).

## [0.x] — Pre-release development — May–June 2026

Foundational development (squashed into a single baseline commit): OCR/CV
groundwork, the passport compiler, the template system, renderer experiments,
the Gemini RPA renderer, and catalogue work (P20–P22) that rendered all 391 SKU.
See [PROJECT_HISTORY.md](PROJECT_HISTORY.md) for the full narrative.
