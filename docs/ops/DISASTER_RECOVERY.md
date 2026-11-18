# Disaster Recovery

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tag names are retained; their objects were replaced with cleaned historical versions on 2026-11-18. See the [ref migration report](../../REMOTE_REF_MIGRATION_REPORT.md).

> Per-failure playbooks. Each entry: **symptom → impact → recovery → prevention.**
> Backups referenced here are defined in [BACKUP_STRATEGY.md](BACKUP_STRATEGY.md).
> The golden rule: rendered images are **not reproducible** — recover them from
> backup, never assume re-rendering returns the same images.

## DR-1 — SSD / disk failure
- **Symptom:** machine won't boot, or `output/` / `render_output/` / `SSOT/` unreadable.
- **Impact:** total loss of code + data if not backed up.
- **Recovery:** new machine → follow [DEPLOYMENT.md](../../DEPLOYMENT.md) → restore from backup: `SSOT/`, `pipeline/passports/`, `output/`, `render_output/raw/`, `gemini_rpa_progress_v23.txt`, `config.yaml` → run [Acceptance Test](ACCEPTANCE_TEST.md) → `main.py --full --resume`.
- **Prevention:** scheduled backups (3-2-1); keep `output/` off the single working SSD.

## DR-2 — Chrome failure or auto-update
- **Symptom:** Stage 2 cannot launch the driver, or every SKU fails at driver init.
- **Impact:** rendering stops (Stages 1 and 3 unaffected).
- **Recovery:** ensure Chrome is installed and reachable; `webdriver-manager` provisions a matching chromedriver automatically — re-run `--render-only --resume`. If a Chrome update broke the matching, clear the webdriver-manager cache so it re-downloads.
- **Prevention:** pin/record the working Chrome version in [DEPENDENCY_INVENTORY.md](DEPENDENCY_INVENTORY.md); test after Chrome updates.

## DR-3 — Gemini changed its DOM / UI
- **Symptom:** repeated failures at the **same stage across many SKUs** (e.g. `send_message`, `wait_for_image_generation`, blob download), not random per-SKU timeouts.
- **Impact:** rendering is fully blocked — this is the highest-risk architectural dependency (browser RPA, no API).
- **Recovery:** stop the run. The selectors live in `src/rpa_orchestrator.py` (`send_message`, `wait_for_image_generation`, `download_blob_image`, response counters). They must be re-aligned to the new Gemini UI — a **development task**, not an operator action. Until then, rendering cannot proceed.
- **Prevention:** treat the selector layer as a known fragility (see Bus Factor audit); keep `output/` backed up so a UI outage never costs delivered assets.

## DR-4 — Lost / corrupted progress tracker
- **Symptom:** `gemini_rpa_progress_v23.txt` missing or garbled; resume re-processes everything.
- **Impact:** low — Stage 2 also rebuilds "done" state by **scanning `render_output/raw/`**, so already-rendered SKUs are still skipped even without the tracker.
- **Recovery:** restore the tracker from backup if available; otherwise just re-run `--render-only --resume` — the raw-dir scan reconstructs progress; only genuinely missing PNGs are re-rendered.
- **Prevention:** include the tracker in backups; never delete `render_output/raw/`.

## DR-5 — Corrupted SSOT
- **Symptom:** `main.py` pre-flight aborts (exit 2) on `SKU.csv`/`master.json`; or odd routing if a CSV row is malformed.
- **Impact:** Stage 1 cannot run / produces wrong routing.
- **Recovery:** restore `SSOT/` from backup; re-run `--passports-only`; confirm `pipeline/passports.markdown/` regenerates identically.
- **Prevention:** `SSOT/` is the system of record for inputs — back it up on every change; edit via the documented sync scripts in `scripts/`.

## DR-6 — No network
- **Symptom:** Stage 2 SKUs fail as Selenium timeouts / WebDriver errors.
- **Impact:** rendering only (Stages 1 and 3 are offline-capable).
- **Recovery:** restore connectivity → `--render-only --resume`. Progress is preserved; only un-rendered SKUs run.
- **Prevention:** run rendering on a stable connection; the built-in backoff already absorbs short blips.

## DR-7 — Windows update / reboot mid-run
- **Symptom:** the run is killed; partial output on disk.
- **Impact:** low — equivalent to an interruption.
- **Recovery:** `main.py --full --resume` (or the relevant stage). Per-SKU progress was saved; no duplication.
- **Prevention:** pause Windows updates during long render runs; rely on resume otherwise.

---

## Recovery quick-reference

| Lost | Recoverable? | How |
|---|---|---|
| Code | ✅ | git |
| `pipeline/passports.markdown/` | ✅ | regenerate Stage 1 (deterministic) |
| `gemini_rpa_progress_v23.txt` | ✅ | rebuilt from `render_output/raw/` scan |
| `SSOT/`, `pipeline/passports/` (inputs) | ⚠️ backup only | not regenerable in-repo (Stage 0 is manual) |
| `render_output/raw/`, `output/` (images) | 🔴 backup only | **non-deterministic** — re-render yields *different* images |
