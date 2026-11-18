# Architecture

Observed on 2026-11-18 at dev `df31165`. Cleanup preserves runtime algorithms. This replaces the obsolete five-stage diagram; older revisions remain in Git and the external backup.

## Components

| Component | Responsibility |
|---|---|
| `main.py` | CLI, preflight, ordered subprocess execution, stage retry and summary |
| `src/utils.py` | Root paths, YAML/default merging, environment overrides and logging |
| `src/passport_generator.py` | Passport loading, routing, fit checks, verification and Markdown/report writes |
| `pharma_pkg/` | Geometry/classification and secondary dimensions |
| `verification_agent.py` | Heuristic checks, confidence and warnings |
| `schemas/` | Pydantic/CV helper models, not complete enforcement of production JSON |
| `src/rpa_orchestrator.py` | Chrome/Gemini UI, chat cleanup, downloads, progress and retry |
| `src/image_processor.py` | Resize and iterative WebP quality reduction |
| Root shims | Compatibility entry points/imports for the three modules |
| `scripts/` | Auxiliary operator tools, outside the canonical stages |

## Data Flow

Manual source analysis → JSON passport; JSON + SSOT → Markdown; Markdown + authenticated Gemini → raw PNG; PNG → WebP. See [diagram source](diagrams/pipeline.mmd). `main.py` orchestrates only Stages 1–3.

## SSOT

`SSOT/SKU.csv` supplies routing/product fields; `SSOT/master.json` supplies metadata and design rules; `SSOT/master_pharma_design_specs.json` supplies visual rules. Stage 1 uses configured paths. The verifier loads relative `SSOT/` paths at import time, so run from the repository root. The current snapshot has 391 CSV picture IDs and master registry entries, not a fixed future catalogue size.

## Inputs / Outputs

Retained `pipeline/passports/*.json` are manual Stage 0 outputs. `input/` and `pipeline/cv/` remain analysis evidence. Stage 1 writes ignored Markdown, the verifier log and `docs/DATA_DRIVEN_OVERRIDE_AUDIT.md`. Stage 2 writes raw PNG, failure logs/screenshots and the progress tracker. Stage 3 writes `output/test1` in committed config, `output` in defaults. An existing root `images/` directory overrides the configured Stage 3 source.

## Stage Boundaries

Each stage runs through the same Python interpreter in a separate subprocess with the repository root as working directory. `PHARMAGEN_CONFIG` propagates alternate configuration; headless/debug flags have environment overrides. Manual analysis, optional CV/OCR, maintenance and repository migration remain separate. The `.agents/protocol.md` v3 proposal is roadmap material; compiler inputs remain v2.0/v2.1 records.

## Failure Handling

Preflight checks input presence and JSON readability, not complete business validity. A failed stage stops downstream execution. Stage-level render retry uses `pipeline.render_retries`; Stage 2 also handles per-SKU failures. Strict chat cleanup stops a run if history cleanliness is unconfirmed. Cleanup can delete prior Gemini conversations: use a dedicated authorised account/profile.

Stage 1 returns failure on incomplete conversion, but low-confidence verifier warnings can coexist with generated Markdown. Orchestrator guards use aggregate output counts. Stage 2/3 per-file failures do not always propagate to the overall exit status; old files can satisfy aggregate guards. A successful exit is insufficient evidence of complete catalogue acceptance.

## Resume Logic

- Stage 1 compares JSON/Markdown counts, without matching IDs, hashes or freshness.
- Stage 2 counts tracker stems only when the corresponding raw PNG exists, and also scans existing raw filenames. Missing-image tracker entries are retried. Restore images and tracker together.
- Stage 3 skips existing output filenames without reopening them for validation.
- Ctrl+C is handled by the orchestrator; interrupted writes and power loss are not transactional.

## External Dependencies

Python packages are in `requirements.txt`. Stage 2 needs Chrome, driver provisioning, network and an authenticated Gemini account. OCR diagnostics separately require pytesseract/Tesseract. Local Stage 1/3 verification needs no browser. A new isolated environment installed the core requirements and passed pip check, CLI and unit checks. Optional legacy CV/OCR dependencies were not exercised.

## QA Boundaries

Unit tests cover packaging, verifier and mocked OCR helper behaviour. Isolated checks compile 391 passports and process a synthetic image, including resume. Asset inventory checks decoding, dimensions and bytes. These do not prove label fidelity, clinical correctness, branding permission, visual consistency or successful authenticated rendering. Human catalogue-wide acceptance remains unverified.

## Known Architectural Trade-offs

File-based state is inspectable but lacks transactional per-item status. Counts and filenames can conceal stale data. UI automation needs selector maintenance and generates non-deterministic images. Large compiler/RPA modules concentrate logic. Lower-bounded dependencies and browser configuration limit reproducibility. Cleanup introduces no runtime dependency or algorithm refactor.
