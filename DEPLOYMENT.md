# PharmaGen PRO — Deployment Guide

> How to stand up PharmaGen PRO from scratch on a new machine, keep it updated,
> and roll back. For day-to-day running see [OPERATIONS.md](OPERATIONS.md); for
> failure handling see [docs/ops/DISASTER_RECOVERY.md](docs/ops/DISASTER_RECOVERY.md).

## 1. Prerequisites

| Requirement | Detail |
|---|---|
| OS | Windows 10/11 (paths in `config.yaml` are Windows-shaped). |
| Python | 3.10+ (tested on 3.10.11). |
| Google Chrome | Required for Stage 2 (tested with the current stable channel; see [Dependency Inventory](docs/ops/DEPENDENCY_INVENTORY.md)). |
| Google account | With access to **Gemini** image generation (gemini.google.com). |
| Network | Outbound HTTPS to `gemini.google.com` for Stage 2. |
| Tesseract OCR | **Optional** — only for `scripts/render_qa.py`. |

> **Credential model (important):** the renderer authenticates via a **logged-in
> Chrome profile**, *not* an API key. `.env` keys are orphaned and not read by the
> pipeline (see the Bus Factor audit). Treat the Chrome profile as the secret.

## 2. Get the code & data

```bash
git clone <repo-url> pharma_v2      # or copy the project folder
cd pharma_v2
```

The repository already contains the SSOT and pipeline inputs. If deploying with
existing production data, also restore (see [Backup Strategy](docs/ops/BACKUP_STRATEGY.md)):
`SSOT/`, `pipeline/passports/`, and — to avoid re-rendering — `render_output/raw/`,
`output/`, and `gemini_rpa_progress_v23.txt`.

## 3. Python environment

```bash
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
```

Verify:

```bash
venv\Scripts\python.exe main.py --help
venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

## 4. Directories

These are created automatically when missing, so no manual setup is normally
needed: `render_output/{raw,failed,failed_logs}`, `output/`, `logs/`. The inputs
that **must exist**: `SSOT/` (SKU.csv + master.json + design specs) and
`pipeline/passports/` (JSON passports). Layout reference: [docs/REPO_AUDIT.md](docs/REPO_AUDIT.md).

## 5. Browser profile & Gemini session (Stage 2 only)

1. In `config.yaml`, set `rpa.browser_profile_dir` and `rpa.browser_profile_name`
   to a Chrome profile you control, and `rpa.downloads_dir` to that browser's
   download folder.
2. Open Chrome with that profile and **log in to Gemini once** (the session is
   reused by automation).
3. Close any other browser using the same profile before a run (Chrome forbids
   two processes sharing one profile — including the embedded Antigravity browser).
4. Keep `rpa.headless: false` — Gemini blocks image generation in headless mode.

## 6. Configuration review

Open [`config.yaml`](config.yaml) and confirm: `paths.*` point at the real data
dirs; `rpa.*` profile/downloads are correct; timeouts/batch are defaults. Missing
keys fall back to built-in defaults in `src/utils.py`.

## 7. Smoke test (before first production run)

Run the [Acceptance Test](docs/ops/ACCEPTANCE_TEST.md). When every item passes,
the deployment is **Production Ready**.

## 8. Updating an existing deployment

```bash
git pull                                   # fetch new code
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Stage 1 output is deterministic, so re-running `--passports-only` after an update
must leave `pipeline/passports.markdown/` byte-identical (a quick regression check).

## 9. Rollback

1. Back up current state first (see [Backup Strategy](docs/ops/BACKUP_STRATEGY.md)).
2. Return code to a known-good revision: `git checkout <tag-or-commit>`.
3. Restore data from backup if it changed.
4. Re-validate with the Acceptance Test, then continue with `python main.py --full --resume`.

Because rendered images are **non-deterministic** (see Production Readiness audit),
roll back **data from backup** — do not expect re-rendering to reproduce prior images.

## 10. Backup before/after deploy

Always snapshot `SSOT/`, `pipeline/`, `output/`, `render_output/raw/`,
`gemini_rpa_progress_v23.txt`, and `config.yaml` before a deploy or update — full
policy in [Backup Strategy](docs/ops/BACKUP_STRATEGY.md). Never commit `.env` or
share the Chrome profile in plaintext backups.
