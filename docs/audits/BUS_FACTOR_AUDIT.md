# Bus Factor / Knowledge Transfer Audit

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tag names are retained; their objects were replaced with cleaned historical versions on 2026-11-18. See the [ref migration report](../../REMOTE_REF_MIGRATION_REPORT.md).

> **Phase:** PharmaGen PRO v1.0 — Production Hardening
> **Date:** 2026-06-28 · **Type:** read-only audit (no code changed)
> **Question answered:** *Could another developer maintain PharmaGen PRO in six
> months without the author?*

## Verdict

**Current bus factor ≈ 1.** The pipeline runs and is now documented at the
surface (README, ARCHITECTURE, REPO_AUDIT), but several load-bearing pieces rely
on knowledge that exists only in the author's head or in opaque constants. None
are blockers, but together they would cost a new maintainer significant
reverse-engineering time. The findings below, if documented, raise the bus
factor to ≥2.

Severity legend: 🔴 high (blocks understanding) · 🟡 medium (slows maintenance) · ⚪ low (nice to have).

---

## A. Author-dependent / operational knowledge

| # | Item | Where | Severity |
|---|---|---|---|
| A1 | **The renderer authenticates via a logged-in browser session, NOT an API key.** A maintainer must know to log into Gemini once in the configured Chrome profile and keep that profile valid. | `config.yaml` `rpa.browser_profile_dir`; `src/rpa_orchestrator.py` `create_driver()` | 🔴 |
| A2 | **Gemini UI is reverse-engineered via CSS/DOM selectors** (`model-response`, input box, blob download via JS). Only the author knows why each selector/wait exists; a Gemini UI change breaks rendering silently. | `src/rpa_orchestrator.py` `send_message()`, `wait_for_image_generation()`, `download_blob_image()` | 🔴 |
| A3 | **Stage 0 (source image → JSON passport) is a manual Gemini-in-IDE workflow**, not in the automated pipeline. A maintainer cannot regenerate JSON passports from photos without this tribal knowledge. | `.agents/workflows/analyze-pharma.md` | 🟡 |
| A4 | **Operational ritual**: the embedded Antigravity browser must be closed before a run (Chrome single-profile lock); runs are long and interactive. | `src/rpa_orchestrator.py` header comments | 🟡 |

## B. Decisions made but never explained

| # | Decision | Where | Severity |
|---|---|---|---|
| B1 | **Optical calibration**: `3/4 isometric, 25° pitch, box rotated 35°, 85mm lens, f/8` (and `20° pitch / 25–30° rotation` variants for vertical templates). No recorded rationale for these exact values. | `src/passport_generator.py:570, 608, 646, 684, 721, 758, 796, 834, 872, 910` | 🟡 |
| B2 | **"Accent stripe on Row 6, front face only; carton otherwise pure white #FFFFFF."** A strict art-direction rule with no documented "why". | `src/passport_generator.py:562, 581, 593` | 🟡 |
| B3 | **Production confidence threshold 0.75** (raised from 0.70) and the per-check penalty weights. Why 0.75 and why each weight is unexplained. | `verification_agent.py:161, 170-177` | 🟡 |
| B4 | **"P-numbering"** (P6.0, P8.0, P20, P21, P22) referenced across code comments with no glossary. | passim in `src/`, docs | ⚪ |

> Partially mitigated by the new [ADRs](../DECISIONS/) and
> [PROJECT_HISTORY.md](../../PROJECT_HISTORY.md), but the *specific numeric values*
> in B1/B3 remain unexplained. **[rationale to confirm with author]**

## C. Magic numbers

| # | Value(s) | Meaning | Where | Severity |
|---|---|---|---|---|
| C1 | RGB ladder `<40`, `>215`, `>200 & <50`, … → colour names | hex → human colour-name classifier | `src/passport_generator.py:143-150` | 🟡 |
| C2 | `r>200 and g>200 and b<50 → "Premium Gold Accent"` | one rule of the ladder | `src/passport_generator.py:145` | 🟡 |
| C3 | Fallback primary dims `85×55×8`, `15×120×15`, `35×95×35` mm | estimated container sizes when data missing | `src/passport_generator.py:286-290` | 🟡 |
| C4 | accent fallback `#ADD8E6` | default accent when palette missing | `src/passport_generator.py:1014` | ⚪ |
| C5 | Verifier penalties `-0.15 / -0.30 / -0.20 / -0.25 / -0.10 …`, threshold `0.75` | scoring weights | `verification_agent.py:161, 170-177` | 🟡 |
| C6 | RPA waits `2.5s`, `0.5`, `0.3`, `0.1`, `0.02`; timeouts `180/60/30`; `batch_size 1`; cleanup every `10`; `keep_last 2`; backoff `30·n` (max `120`), `180` on throttle | UI timing/throttle heuristics | `src/rpa_orchestrator.py:286,301,304,306,366,449,484; config.yaml rpa.*` | 🟡 |
| C7 | WEBP `quality=95`, `step=4`, `method=6`, `1600×1600`, `≤500 KB` | final image encode parameters | `src/image_processor.py:28-29,33; config.yaml image_processor.*` | ⚪ |

## D. Unclear / undocumented heuristics

| # | Heuristic | Where | Severity |
|---|---|---|---|
| D1 | **Brand names hardcoded into logic**: `is_liquid_or_device()` keyword list includes specific brands (`lumigan`, `xalatan`, `latisse`). Adding products may require editing this list — non-obvious. | `src/passport_generator.py:152+` | 🔴 |
| D2 | Template routing chain: SKU.csv `package_type` → vertical/tube checks → `geometry_mapping` fallback → default T1. The precedence rules are spread across functions. | `src/passport_generator.py` `agent_1_router()`, `is_vertical_container()`; `pharma_pkg/geometry_mapping.py` | 🟡 |
| D3 | Text sanitization / dedup / unit-label resolution (`sanitize_text`, `purge_forms`, `resolve_unit_label`, MNN-vs-brand dedup, `%` purge for EMA). Rules are regulatory-driven but the rationale lives only in commit messages. | `src/passport_generator.py` | 🟡 |
| D4 | Data-driven overrides: photosensitive-compound and sub-brand trigger lists drive material/colour overrides. | `src/passport_generator.py` `_SPECS_PHOTOSENS`, `_SPECS_SUB_BRANDS` | 🟡 |

## E. Places impossible to understand without project history

- The `T_*` template zoo (`T1_SMALL`, `T1_LARGE`, `T_MULTIPACK`, `T_VERT_VIAL/DROPPER/INHALER`) and labels like *"Assorted Pack"* — introduced in P21/P22 (see [PROJECT_HISTORY.md](../../PROJECT_HISTORY.md)).
- The graveyard of renderer experiments (DALL·E, Flux, HF, Pollinations, Imagen) now in `trash/_archive/` — explains *why Gemini RPA* (see [ADR-001](../DECISIONS/ADR-001-why-gemini.md), [ADR-004](../DECISIONS/ADR-004-why-rpa.md)).

## F. Undocumented / misleading dependencies

| # | Dependency | Status | Severity |
|---|---|---|---|
| F1 | **`.env` keys are orphaned.** `GEMINI_API_KEY`, `GEMINI_API_KEY_OLD`, `HF_TOKEN` are **not read by the pipeline** (only `os.environ.copy()` at `main.py:302`). A maintainer would wrongly assume an API key is required; the real credential is the **browser session** (A1). | verified: no `getenv`/`dotenv` in `src/` | 🔴 |
| F2 | **System dependency: Google Chrome** (matching `chromedriver` via `webdriver-manager`) — not in `requirements.txt`, only implied. | `src/rpa_orchestrator.py` | 🟡 |
| F3 | **System dependency: Tesseract OCR** for `scripts/render_qa.py` (`pytesseract`), optional and undocumented as a system install. | `scripts/render_qa.py` | ⚪ |
| F4 | Network dependency on `gemini.google.com` availability/behaviour. | `config.yaml rpa.gemini_url` | 🟡 |

---

## Prioritized remediation backlog (documentation only — no code changes)

1. 🔴 Document the **browser-session credential model** and remove/annotate the orphaned `.env` keys (F1, A1).
2. 🔴 Document the **Gemini selector contract** and what breaks if the UI changes (A2).
3. 🔴 Extract the **brand-name heuristic** (D1) into a documented, data-driven list — *follow-up task, not this phase*.
4. 🟡 Add a **constants glossary** for the magic numbers in §C with their intent (B1, B3, C1–C7).
5. 🟡 Document Stage 0 (analyze-pharma) as the prerequisite for JSON passports (A3).

> This audit only identifies gaps. Per the phase scope, nothing was fixed in code.
