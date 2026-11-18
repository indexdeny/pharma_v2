# Backup Strategy

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tags are unchanged.

> What to keep, what is regenerable, and what is gone forever if lost. Driven by
> one fact from the Production Readiness audit: **rendered images are
> non-deterministic** — they cannot be reproduced, only restored.

## Tier 1 — Must back up (irreplaceable)

| Item | Why |
|---|---|
| `SSOT/` (`SKU.csv`, `master.json`, design specs) | System of record for inputs; Stage 0 (photo → JSON) is a **manual** step, not regenerable in-repo. |
| `pipeline/passports/` (JSON passports) | Stage 1 inputs; produced by the manual Stage 0. |
| `output/` (final WEBP) | **Delivered assets; non-reproducible.** |
| `render_output/raw/` (PNG) | **Non-reproducible** render results; also the basis of resume. |
| `gemini_rpa_progress_v23.txt` | Resume tracker (rebuildable from `raw/`, but cheap to keep). |
| `config.yaml` | Deployment configuration. |
| Chrome profile / Gemini session | The real credential (handle as a **secret** — see below). |

## Tier 2 — Recoverable (regenerable, optional to back up)

| Item | How to regenerate |
|---|---|
| `pipeline/passports.markdown/` | `python main.py --passports-only` (deterministic, byte-identical). |
| `logs/`, `verification_failures.log`, `render_output/failed*/` | Re-created on the next run. |
| `__pycache__/`, `venv/` | Rebuilt by Python / `pip install -r requirements.txt`. |

## Tier 3 — Cannot be recovered if Tier 1 is lost

- The exact **rendered images** (`output/` + `render_output/raw/`). Re-rendering
  produces *different* images (Gemini is generative, no seed). If these are lost
  and not backed up, the visual catalogue must be re-rendered from scratch and
  will not match the previous deliverables.

## Cadence & method

- **3-2-1:** ≥3 copies, on ≥2 media, ≥1 off the working machine.
- Back up Tier 1 **on every change to SSOT/passports** and **after each render batch**.
- A simple full-folder snapshot of the Tier 1 paths is sufficient (no special tooling).

## Secrets handling

- **Do not** back up `.env` to shared/plaintext locations. Note: `.env` keys are
  **orphaned** (not used by the pipeline — see Bus Factor audit); the real secret
  is the Chrome profile/session.
- If backing up the Chrome profile, store it encrypted/access-controlled — it
  grants access to the logged-in Google/Gemini account.

## Restore procedure

1. Deploy code & environment ([DEPLOYMENT.md](../../DEPLOYMENT.md)).
2. Restore Tier 1 paths into place.
3. Run the [Acceptance Test](ACCEPTANCE_TEST.md).
4. Continue with `python main.py --full --resume` (only missing work runs).
