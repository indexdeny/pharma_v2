# PharmaGen PRO — Operations Manual

> The operator runbook: how to run the pipeline, read its state, and recover from
> the errors you will actually hit. Setup is in [DEPLOYMENT.md](DEPLOYMENT.md);
> deep failure playbooks are in [docs/ops/DISASTER_RECOVERY.md](docs/ops/DISASTER_RECOVERY.md).

## Pre-run checklist

- [ ] Chrome profile is **logged in to Gemini** (Stage 2).
- [ ] No other browser (incl. embedded Antigravity) is using that profile.
- [ ] Enough free disk for new PNG/WEBP output (there is **no automatic disk check**).
- [ ] `venv` active; `python main.py --help` works.

## Running

```bash
# whole catalogue, safe to repeat (skips finished work)
venv\Scripts\python.exe main.py --full --resume

# individual stages
venv\Scripts\python.exe main.py --passports-only
venv\Scripts\python.exe main.py --render-only            # needs logged-in browser
venv\Scripts\python.exe main.py --process-images-only --resume
```

## What to watch

| Signal | Where |
|---|---|
| Per-stage status / duration / artifact counts | `main.py` end-of-run summary table |
| Live per-SKU progress `[i/N]` | console + `logs/pharmagen_*.log`, `logs/gemini_rpa_*.log` |
| Remaining SKUs + ETA | `python -m src.rpa_orchestrator --estimate` (no browser) |
| Failures (per SKU) | `render_output/failed_logs/failures.log` + screenshots in `render_output/failed/` |

## Error-handling flow

```
Start generation
      │
      ▼
Error appears ──▶ What to check ──▶ Recover ──▶ Continue (--resume)
      │                                              │
      └──────────── if unrecoverable ───────────────┘
                         ▼
                 Full restart (rare)
```

## Common situations

| Symptom | Check | Action |
|---|---|---|
| Stage 2 times out on a SKU | `failures.log` (`stage: wait_for_image_generation`); screenshot in `failed/` | Auto-retried in the end-of-run pass; otherwise re-run `--render-only --resume`. |
| "Chrome already in use" / profile lock | Another browser on the same profile | Close it (incl. Antigravity), re-run. |
| All SKUs failing fast | Network / Gemini session expired | Re-login in the profile; check connectivity; re-run `--resume`. |
| No PNG produced | `failed/error_gen_<stem>.png` | Re-run `--render-only --resume` (resume re-attempts it). |
| Disk fills mid-run | Free space | Free space, then `--resume` (no data duplication). |
| Gemini UI changed (selectors fail) | Repeated failures at the same stage across SKUs | See [Disaster Recovery → Gemini DOM change](docs/ops/DISASTER_RECOVERY.md). |

## Re-render a single SKU

There is no one-shot `regenerate(sku)`. To redo e.g. `217-min`:

```bash
del render_output\raw\217-min.png        # makes it "unprocessed" again
del output\217-min.webp                  # so Stage 3 will rebuild it
venv\Scripts\python.exe main.py --render-only --from 217-min --limit 1
venv\Scripts\python.exe main.py --process-images-only
```

## Resume vs. full restart

- **Resume (default choice):** `--resume`. Safe after any interruption — finished
  SKUs are skipped, no duplication. This is correct in almost all cases.
- **Full restart (rare):** only when inputs themselves changed (new SSOT, rebuilt
  passports) and you intend to regenerate. Remember images are **not reproducible**;
  preserve `output/` first.

## Interrupting

Press **Ctrl+C** — progress is saved per SKU and the browser is closed cleanly.
Continue later with `--resume`.
