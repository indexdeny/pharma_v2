# PharmaGen PRO v1.0.1 — Patch Release (June 2026)

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tags are unchanged.

> Draft body for the GitHub Release of tag `v1.0.1` (the latest, fully
> reproducible release). Patch over [v1.0.0](RELEASE_NOTES_v1.0.0.md).

## Fixed
- **Missing `pydantic` runtime dependency declared** in `requirements.txt`.
  `pydantic` is required by Stage 1 (`schemas/common.py`, via `pharma_pkg`
  routing) but was absent from the dependency list — a from-scratch install per
  the README failed Stage 1 with `ModuleNotFoundError`. Found by a clean-machine
  reproducibility test (fresh checkout + isolated venv + install from
  `requirements.txt` only).

## Why a patch (SemVer)
No change to the pipeline, architecture, logic or algorithms — only
`requirements.txt` (and its docs). A pure packaging bug fix → **1.0.1**.

## Reproducibility
The `v1.0.1` snapshot was re-verified from a clean machine: `git archive v1.0.1`
→ isolated venv → install from `requirements.txt` only → `main.py --help`,
18/18 tests, Stage 1 (391/391) and Stage 3 all pass. (Stage 2 render is attended —
it needs a logged-in Gemini browser session.)

## Internal use
Internal project of **Pharma Progressive**. Not for public distribution.
