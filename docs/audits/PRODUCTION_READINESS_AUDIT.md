# Production Readiness Audit

> **Phase:** PharmaGen PRO v1.0 — Production Hardening
> **Date:** 2026-06-28 · **Type:** read-only engineering audit (no code changed)
> **Scope:** Reliability · Recovery · Logging · Monitoring · Determinism

## Verdict

The pipeline is **resilient for its happy path and for per-SKU failures**
(robust resume, internal retry, clean Ctrl+C), but has **three structural gaps**:
(1) no disk-space / resource guard, (2) post-mortem logging does not capture the
prompt or Gemini's response, and (3) the render stage is **non-deterministic by
design** — re-running does not reproduce the same images. None block current
operation; all matter for unattended/CRM operation.

Severity: 🔴 high · 🟡 medium · ⚪ low.

---

## 1. Reliability

| # | Scenario | Current behaviour (evidence) | Recovery | Gap | Sev |
|---|---|---|---|---|---|
| R1 | **Gemini fails / errors** | `send_message` / `wait_for_image_generation` raise or time out → SKU marked FAILED, error screenshot, `log_failure`, `need_reset`; driver re-initialised on `WebDriverException` during batch reset. `src/rpa_orchestrator.py` main loop + reset block | ✅ resume + end-of-run retry pass | Throttling only inferred from consecutive timeouts (backoff `30·n`, `180s`) | 🟡 |
| R2 | **Internet drops** | Surfaces as Selenium timeouts / WebDriver exceptions → same path as R1. No explicit connectivity probe. | ✅ resume on re-run | A long outage burns the batch as failures before the user notices | 🟡 |
| R3 | **Disk full** | **No free-space check anywhere** (verified: no `shutil.disk_usage`). A failed write raises → caught as a per-item exception (download/save), logged, loop continues; the error screenshot write may also fail. | ⚠️ partial (degrades to per-item failures) | Silent partial completion; no pre-flight capacity guard | 🔴 |
| R4 | **SSOT corrupted** | `main.py` pre-flight validates `SKU.csv` exists+non-empty and `master.json`/design-specs parse as JSON → aborts **exit 2** before any stage (`main.py preflight()`). Loaders also degrade to `{}` if missing. | ✅ clean abort | Malformed **rows** inside `SKU.csv` are not schema-validated (only existence/parse) | 🟡 |
| R5 | **One passport corrupted** | Stage 1 wraps each file in try/except → logs `EXCEPTION`/`BLOCKED`, continues. Combo-drug with incomplete API → `ValueError` blocked + logged. | ✅ isolated to that SKU | Passports with `schema_version` ≠ 2.0/2.1 are **silently skipped** (`continue`, no warning) | 🟡 |
| R6 | **PNG not produced** | Generation timeout → `image_ready=False` → `error_gen_<stem>.png` screenshot, FAILED, `consecutive_timeouts++`, `need_reset`, `log_failure`; retried in end-of-run pass. | ✅ resume + retry | — | ⚪ |
| R7 | **WEBP not created** | Stage 3 per-file try/except → prints `[ERROR]`, continues; the raw PNG is left intact so `--resume` retries it next run. | ✅ re-run with `--resume` | Failure is **stdout-only** (no `failed/` copy, not in a failure log) | 🟡 |
| R8 | **User interruption (Ctrl+C)** | Stage 2 catches `KeyboardInterrupt` (progress already saved per SKU, driver quit in `finally`, summary printed); `main.py` catches it → graceful, **exit 130**. | ✅ resume | — | ⚪ |

## 2. Recovery — "continue or start over?"

**Continue, in all cases.** No stage restarts from zero after a failure:

- **Stage 1** — deterministic; re-run overwrites in place; `--resume` skips entirely when all Markdown exists.
- **Stage 2** — native resume via `gemini_rpa_progress_v23.txt` + scan of `render_output/raw/`; already-rendered SKUs skipped; timed-out SKUs auto-retried in an end-of-run pass.
- **Stage 3** — `--resume` skips any SKU whose `.webp` already exists.
- **Cross-stage** — `main.py` stops the pipeline on a hard stage failure and skips downstream; re-run with `--resume`.

## 3. Logging — "why did SKU 217 fail?"

| Question | Answerable today? | Source / gap |
|---|---|---|
| *Which SKU failed and at what stage?* | ✅ Yes | `render_output/failed_logs/failures.log` (`file/stage/error/recovery/result`) + `logs/gemini_rpa_*.log` |
| *Visual state at failure?* | ✅ Yes | `error_gen_<stem>.png` / `error_dl_<stem>.png` screenshots in `render_output/failed/` |
| *What prompt was sent?* | ⚠️ Indirect | The prompt **is** `pipeline/passports.markdown/<stem>.md`, but the log records only its char count (`rpa_orchestrator.py:1340`), not the content or a hash |
| *What did Gemini reply?* | 🔴 No | Textual response is never captured; the image is a blob; only failure screenshots exist |

**Gap:** no per-SKU correlation record tying {prompt hash · timestamp · Gemini textual response · outcome}. Post-mortems rely on screenshots + re-deriving the prompt from the MD file.

## 4. Monitoring — "391 / done / remaining / errors / ETA"

| Metric | Available? | Where |
|---|---|---|
| Total (391) | ✅ | Stage 1/2 logs, `main.py` summary |
| Done | ✅ | count of `render_output/raw/*.png`; `main.py` artifact table |
| Remaining + **ETA** | ✅ | `python -m src.rpa_orchestrator --estimate` (dry-run) |
| Errors | ⚠️ | `failures.log` (not aggregated into a live counter) |
| Live progress % | ⚠️ | only `[i/N]` per-SKU log lines; no single live dashboard / machine-readable feed |

**Gap:** metrics exist but are **scattered** across logs/estimate/summary and are not exposed as a single structured (JSON) status suitable for an external monitor or CRM.

## 5. Determinism — "same results in six months?"

| Stage | Deterministic? | Evidence |
|---|---|---|
| Stage 1 (passports) | ✅ Yes | Re-run produces **byte-identical** Markdown (verified twice in prior phases via `git diff` = 0) |
| Stage 2 (render) | 🔴 **No** | Gemini is a generative model driven through the UI; no seed/temperature control is available; the same prompt yields a different image each run |
| Stage 3 (WEBP) | ✅ Yes* | Fixed LANCZOS + quality ladder for a given input PNG (*but its input varies with Stage 2) |

**Conclusion:** re-running 391 SKU in six months reproduces the **same Markdown
passports** but **different images**. The pipeline is **not reproducible at the
asset level by design.** Operational implication: `output/` is the *system of
record* for delivered images — assets must be **preserved**, not regenerated, to
keep results stable. **[design constraint — confirm acceptable with stakeholders]**

---

## Prioritized remediation backlog (documentation only — no code changes this phase)

1. 🔴 **Disk/resource pre-flight guard** before Stage 2/3 (R3) — *follow-up code task*.
2. 🔴 **Determinism policy**: formally treat `output/` as the system of record; document that images are not reproducible (§5).
3. 🔴 **Post-mortem record per SKU**: persist `{stem, prompt_hash, timestamp, outcome}` (and optionally Gemini's text reply) (§3).
4. 🟡 Aggregate a **single structured status/metrics file** (total/done/remaining/errors/ETA) for monitoring (§4).
5. 🟡 Emit an explicit **warning when a passport is skipped** for schema mismatch (R5); add a `failed/` trail for Stage 3 (R7).
6. 🟡 Validate `SKU.csv` **row schema**, not just file presence (R4).

> This audit only identifies gaps. Per the phase scope, nothing was fixed in code.
