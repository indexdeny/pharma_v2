# Architecture Health Check

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tags are unchanged.

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> Evaluation only — **not** a refactoring request.

## Module map

```
main.py (orchestrator)
   └─ subprocess ─▶ src/passport_generator.py   ─┐
                    src/rpa_orchestrator.py       ├─ src/utils.py (config, paths, logging)
                    src/image_processor.py       ─┘
src/passport_generator.py ─▶ pharma_pkg/ (routing/geometry/classifier), verification_agent.py
root shims (pass_tomd / gemini_image_generator / webp_converter) ─▶ src/*
```

## Assessment

| Question | Verdict | Notes |
|---|---|---|
| Module boundaries logical? | ✅ Good | Orchestrator / stages / config-lib / routing-lib are cleanly separated. |
| Coupling acceptable? | ✅ Good | Stages communicate via **files** (JSON→MD→PNG→WEBP), not shared state. `src → pharma_pkg / verification_agent` are normal library deps. |
| Responsibilities separated? | ✅ Mostly | Each Stage has one job; `utils` owns config/logging; `main.py` owns control flow only. |
| God objects? | 🟡 **Watch** | `src/passport_generator.py` (~1,500 lines) concentrates templates + routing + colour logic + sanitization + verifier call + stats; `src/rpa_orchestrator.py` (~1,600 lines) concentrates all Selenium flow + retry/backoff + progress + cleanup. Both are **large** and trend toward god-modules. |
| Dependency direction clean? | ✅ Good | `main → src → libs`; shims → src; no import cycles. |
| Layering respected? | ✅ Good | entry → stages (subprocess) → libraries → data/SSOT. |

## Strengths

- **Subprocess isolation** is the standout decision: it quarantines the fragile, non-deterministic render Stage behind a process boundary, so failures and import-time side effects can't corrupt the orchestrator or other Stages.
- File-based seams make state inspectable and **resume** trivial.
- Config-driven paths + backward-compat shims keep the surface stable.

## Concerns (structural debt, not for this phase)

1. The **two large modules** (`passport_generator`, `rpa_orchestrator`) are the main maintainability risk; if they keep growing, split by responsibility (e.g. templates vs routing vs sanitization; driver vs flow vs progress). Tracked in [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md).
2. **Bilingual code comments** (Russian + English) in the render module raise the onboarding bar slightly.

## Verdict

Architecture is **healthy for a v1.0 internal product**. Boundaries, coupling and
dependency direction are sound; the only real structural debt is the size of the
two core modules. No redesign is warranted now.
