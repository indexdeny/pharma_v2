# Acceptance Test

> A single hand-over gate. Run top to bottom from the project root; tick each box.
> **When every box passes, the deployment may be declared `Production Ready`.**
> Note: Stage 2 (render) is an **attended** check — it needs a logged-in browser
> and cannot be a fully automated CI gate.

| # | Check | Command | Expected | ☑ |
|---|---|---|---|---|
| 1 | Environment & deps | `venv\Scripts\python.exe -m pip install -r requirements.txt` | installs cleanly | ☐ |
| 2 | Entry point | `venv\Scripts\python.exe main.py --help` | usage prints, exit 0 | ☐ |
| 3 | Config exists & parses | `venv\Scripts\python.exe -c "from src.utils import load_config; load_config()"` | no error | ☐ |
| 4 | SSOT found | confirm `SSOT/SKU.csv` and `SSOT/master.json` exist & non-empty | both present | ☐ |
| 5 | Unit tests (QA) | `venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"` | `OK` (18 tests) | ☐ |
| 6 | **Stage 1** — passports | `venv\Scripts\python.exe main.py --passports-only` | `converted 391/391`, `git diff` on `pipeline/passports.markdown/` empty (deterministic) | ☐ |
| 7 | **Stage 2** — render *(attended)* | `venv\Scripts\python.exe -m src.rpa_orchestrator --estimate` | paths resolve, remaining/ETA shown. *Full render requires a logged-in Gemini session in the Chrome profile.* | ☐ |
| 8 | **Stage 3** — WEBP | `venv\Scripts\python.exe main.py --process-images-only --resume` | runs, exit 0 (skips existing on resume) | ☐ |
| 9 | Resume (no duplication) | re-run #6 / #8 with `--resume` | finished work skipped, no duplicates | ☐ |
| 10 | WEBP output present & valid | inspect `output/*.webp` | files exist; `1600×1600`; each ≤ 500 KB | ☐ |
| 11 | QA (optional) | `venv\Scripts\python.exe scripts/render_qa.py` | runs if Tesseract installed; otherwise skip | ☐ |

## Sign-off

- All non-optional boxes ticked → **Production Ready**.
- Stage 2 full render verified manually at least once on the target machine.
- Backups of Tier-1 data confirmed (see [BACKUP_STRATEGY.md](BACKUP_STRATEGY.md)).

> Determinism note: checks #10/#11 verify **presence and format**, not pixel
> equality — rendered images are non-reproducible by design.
