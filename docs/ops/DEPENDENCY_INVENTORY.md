# Dependency Inventory

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tags are unchanged.

> The complete dependency surface, with the versions this deployment was **tested
> with**. For external software whose support window we don't control (Chrome,
> Gemini), the policy is "tested with", not "supported range".

## Runtime — core pipeline (required)

| Dependency | Role | Tested version | Required |
|---|---|---|---|
| Python | Interpreter | 3.10.11 | ✅ (3.10+) |
| selenium | Stage 2 — browser automation | 4.44.0 | ✅ |
| webdriver-manager | Stage 2 — provisions matching chromedriver | 4.1.1 | ✅ |
| Pillow | Stage 3 — image processing → WEBP | 12.2.0 | ✅ |
| PyYAML | `config.yaml` loading | 6.0.3 | ✅ (falls back to defaults if absent) |
| rich | Console logging + run summary | 15.0.0 | ✅ (degrades to plain logging if absent) |
| pydantic | Stage 1 schema models (`schemas/common.py`, via `pharma_pkg` routing) | 2.13.x | ✅ (required for routing) |

Pinned loosely in [`requirements.txt`](../../requirements.txt).

## System / external (required for Stage 2)

| Dependency | Role | Tested with | Notes |
|---|---|---|---|
| Google Chrome | Stage 2 browser | current stable channel | Must match a chromedriver (auto via webdriver-manager). |
| Gemini UI (`gemini.google.com`) | Image generation backend | as-is (no version) | **Architectural dependency** — UI changes can break Stage 2 (see Disaster Recovery DR-3). |
| Windows | OS | 10/11 | Profile/Downloads paths in `config.yaml` are Windows-shaped. |
| Authenticated Google/Gemini session | Real credential | n/a | Lives in the Chrome profile, **not** an API key. |

## Optional

| Dependency | Role | Status |
|---|---|---|
| pytesseract + Tesseract OCR | `scripts/render_qa.py` (OCR QA diagnostic) | **Not installed**; install only if running QA. |

## Present but NOT used by the production pipeline

| Dependency | Where used | Status |
|---|---|---|
| opencv-python | `pipeline/cv/` (legacy Stage 0 detection) | Installed (4.13.0.92) but the 3 production Stages do not import it. |
| numpy | `pipeline/cv/` | Installed (2.2.6); same as above. |
| ultralytics (YOLO) | `pipeline/cv/detect.py` + `yolov8n.pt` | **Not installed** → the legacy CV detection is not currently runnable. |

> Stage 0 (source photo → JSON passport) is a **manual Gemini-in-IDE workflow**
> (`.agents/workflows/analyze-pharma.md`); the `pipeline/cv/` code is legacy from
> an earlier OCR/CV approach and is not part of the automated pipeline.

## Version policy

- **Core pip deps:** upgrade together; re-run the [Acceptance Test](ACCEPTANCE_TEST.md) after any change.
- **Chrome:** record the working version here after each verified upgrade; test Stage 2 after Chrome updates.
- **Gemini UI:** unversioned and outside our control — treated as a monitored fragility.
