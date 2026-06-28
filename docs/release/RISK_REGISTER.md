# Risk Register

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> Likelihood × Severity, with mitigation and recovery. Recovery references use
> two ID schemes: **DR-n** → [docs/ops/DISASTER_RECOVERY.md](../ops/DISASTER_RECOVERY.md);
> **R-n** → the resilience matrix (R1–R8) in
> [docs/audits/PRODUCTION_READINESS_AUDIT.md](../audits/PRODUCTION_READINESS_AUDIT.md).

| ID | Risk | Likelihood | Severity | Mitigation | Recovery |
|---|---|---|---|---|---|
| RK-1 | **Gemini DOM/UI change** breaks the render selectors | Medium | 🔴 Critical | Monitor for same-stage mass failures; isolate selector layer; API renderer (v2.0) removes it | Re-align selectors in `src/rpa_orchestrator.py` (dev task); `output/` backup preserves delivered assets — DR-3 |
| RK-2 | **Browser session invalidated** (logout/expired) | Medium | High | Keep the Chrome profile logged in; pre-run checklist | Re-login in the profile; `--render-only --resume` — DR-2/DR-6 |
| RK-3 | **Chrome update** breaks driver match | Medium | Medium | `webdriver-manager` auto-matches; record working version | Clear driver cache; re-run — DR-2 |
| RK-4 | **Windows update / reboot** mid-run | Low | Medium | Pause updates during long runs | `--resume` — DR-7 |
| RK-5 | **Disk full** during render/convert | Medium | High | (No guard today — TD-C1) free space before runs | Free space; `--resume` — R3 (disk-full) / DR-1 (disk loss) |
| RK-6 | **Interrupted rendering** (Ctrl+C / crash) | High | Low | Per-SKU progress saved; clean Ctrl+C handling | `--resume` continues — R8 |
| RK-7 | **Corrupted SSOT** | Low | High | SSOT backed up; `main.py` pre-flight aborts on bad SSOT | Restore `SSOT/`; re-run Stage 1 — DR-5 |
| RK-8 | **Human operational mistake** (deletes data, runs with browser open, wrong config) | Medium | Medium | OPERATIONS runbook + Acceptance Test + backups | Restore from backup; resume — BACKUP_STRATEGY |
| RK-9 | **Non-deterministic re-render** loses a delivered image | Medium | High | Treat `output/` as system of record; back it up | Restore from backup (cannot reproduce) — §Determinism |
| RK-10 | **Unpushed history divergence** (`master` 5 vs `origin/master` 46) | Medium | Medium | Backup branch + `origin/master` preserve the original | `git reset --hard backup/full-history-pre-v1.0`; decide on force-push — GIT_RELEASE_AUDIT GR-1 |

## Top risks for management attention

1. **RK-1 (Gemini DOM change)** — the single highest-impact technical risk; the root reason for the v2.0 API-renderer item on the roadmap.
2. **RK-5 (disk full)** — the one unmitigated production risk in code today (TD-C1).
3. **RK-9 (non-deterministic assets)** — drives the backup-first operating policy.
