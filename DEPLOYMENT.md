# Deployment guide

Current local-candidate guidance, 2026-11-18. Publication remains on hold pending credential remediation; see the [audit](docs/portfolio-audit.md).

## Prerequisites

Use an authorised working copy, Windows, Python 3.10+ and sufficient disk. Rendering additionally needs Chrome, driver provisioning/network access and an authorised Gemini account. OCR diagnostics separately need pytesseract/Tesseract.

## Environment and offline checks

From the repository root:

```powershell
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m compileall -q main.py src pharma_pkg schemas
venv\Scripts\python.exe main.py --help
venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Installation is an operator procedure, not a fresh-install result. Dependencies are not locked. The audit uses Python 3.10.11 and the existing project venv.

## Data and artifacts

Retained inputs are `SSOT/` and `pipeline/passports/`; Stage 0 prepares those manually. Fresh clones omit generated prompts, images, logs and progress. Generate prompts in a disposable copy with `main.py --passports-only`, or restore outputs/state from an authorised backup. Restore raw renders, finals and tracker together. See [backup strategy](docs/ops/BACKUP_STRATEGY.md) and [migration recovery](ROLLBACK_PLAN.md).

## Local configuration

Copy `config.example.yaml` to ignored `config.local.yaml`; fill in absolute browser profile/download paths and verify all I/O paths. Supply `--config config.local.yaml` consistently. Relative `paths.*` resolve from the project root; browser paths are passed to the browser layer. Existing default paths retain legacy machine details, a publication finding.

Committed config uses `output/test1`; defaults use `output`. A root `images/` directory overrides the configured Stage 3 input. Do not infer the active destination from an old runbook.

## Attended rendering

Use a dedicated authorised Chrome profile, log in manually and close other processes sharing it. Keep `headless: false`. **Review chat-history deletion before running the renderer.** Do not test against personal conversations.

```powershell
venv\Scripts\python.exe main.py --config config.local.yaml --render-only --limit 1
```

Inspect the image and failures before expanding the batch. Chrome/authenticated rendering was not exercised here. [Operations](OPERATIONS.md); [acceptance](docs/ops/ACCEPTANCE_TEST.md).
