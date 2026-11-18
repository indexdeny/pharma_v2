# Operations

Current guidance, 2026-11-18. Run from the root with the same explicit config throughout a run. See [deployment](DEPLOYMENT.md) and [architecture](docs/ARCHITECTURE.md).

## Before a run

Confirm authorisation for data, images and account; free disk; SSOT/JSON integrity; a recent private backup; and output paths. Stage 2 needs a logged-in, exclusively owned Chrome profile. **The renderer deletes Gemini chat history during cleanup.** Use a dedicated authorised profile. The audit did not exercise account actions.

## Commands

```powershell
venv\Scripts\python.exe main.py --config config.local.yaml --passports-only
venv\Scripts\python.exe main.py --config config.local.yaml --render-only --limit 5
venv\Scripts\python.exe main.py --config config.local.yaml --process-images-only --resume
venv\Scripts\python.exe main.py --config config.local.yaml --full --resume
```

`--from STEM` sets a render start position, not single-SKU regeneration. `--headless` is a debug override, not evidence of supported unattended rendering. `python -m src.rpa_orchestrator --estimate` reads local state and writes logs without launching Chrome; set `PHARMAGEN_CONFIG` when directly invoking a module with alternate config.

## Inspecting state

| Signal | Location |
|---|---|
| Stage status, duration, file counts | CLI summary and run log |
| Browser/per-SKU failures | RPA logs and configured failure screenshots/logs |
| Resume state | Configured tracker plus raw-image filenames |
| Verifier warnings | Configured failure log and generated override report |
| Final images | `image_processor.output_dir`, currently `output/test1` |

Generated files are ignored by Git. A successful stage exit does not certify every SKU. Compare expected IDs, readable files, dimensions and byte limits; inspect text and packaging visually.

## Recovery and reruns

For auth/UI failures, stop and inspect logs; restore login manually or repair selectors in a separate reviewed change. Preserve failures privately. Use the same config and restored raw/progress state before resuming.

Stage 1 resume compares counts. For content freshness, generate into an empty isolated directory. Stage 3 skips any existing filename, including invalid files. Before regeneration, copy affected raw/final files and tracker records into private recovery storage, then review which entries need removal. This guide does not perform destructive regeneration.

Ctrl+C termination is handled; power loss is not transactional. Inspect interrupted writes before resuming. Authenticated rendering and catalogue-wide visual acceptance remain **NOT VERIFIED**. [Historical recovery scenarios](docs/ops/DISASTER_RECOVERY.md) are retained; current paths and limitations here take precedence.
