# ADR-006: Unified `main.py` + subprocess orchestration

**Status:** Accepted · **Date:** 2026-06-27

## Context
The pipeline was three separate scripts (`pass_tomd.py`,
`gemini_image_generator.py`, `webp_converter.py`) with drifting, partly broken
hard-coded paths and no single entry point. A production-ready system needed one
command, centralized configuration, resume, and logging — **without changing the
proven stage logic**.

## Decision
Introduce **`main.py`** as the single entry point. It runs each stage as an
**isolated subprocess** (`python -m src.<stage>`), with paths centralized in
**`config.yaml`** (via `src/utils.py`) and **root shims** preserving the legacy
commands/imports. Stage modules were moved into `src/` via `git mv` (byte-faithful).

## Consequences
- ✅ One resumable command; byte-faithful stage behaviour (Stage 1 verified identical).
- ✅ Subprocess isolation: a stage crash cannot corrupt the orchestrator; each stage keeps its own logging.
- ✅ Backward compatible (shims + re-exports).
- ⚠️ Stages signal failure only via **exit code**; logical failures that exit 0 are partly masked — see the Production Readiness audit (mitigated by a post-render zero-output guard in `main.py`).

## Alternatives considered
In-process imports (module-level side effects, e.g. the RPA's import-time logging
setup); a monolithic rewrite (high regression risk, rejected).
