# Dependency Lifecycle Review

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> For each dependency: why it exists, whether it is active, legacy, replaceable,
> removable, and any vendor lock-in. Complements the operational
> [DEPENDENCY_INVENTORY.md](../ops/DEPENDENCY_INVENTORY.md) (which lists versions).

## Production-core (required, active)

| Dependency | Why | Active | Replaceable | Lock-in |
|---|---|---|---|---|
| **selenium** | Stage 2 browser automation (drives Gemini UI) | ✅ | Only by switching to an image **API** (v2.0 roadmap) | Coupled to the browser-RPA approach |
| **Chrome** (system) | The browser Selenium drives | ✅ | With another Selenium-supported browser, but Gemini UI is the real target | Indirect (via Gemini) |
| **webdriver-manager** | Provisions a matching chromedriver | ✅ | Yes (manual driver management) | Low |
| **Pillow** | Stage 3 image processing → WEBP | ✅ | Yes (other imaging libs) | Low |
| **PyYAML** | `config.yaml` loading | ✅ | Yes; absence degrades to built-in defaults | None |
| **rich** | Console logging + run summary | ✅ | Yes; absence degrades to plain logging | None |
| **pydantic** | Stage 1 schema models (`schemas/common.py`, used by `pharma_pkg` routing) | ✅ | Yes (plain dataclasses) | None |

## External service

| Dependency | Why | Lock-in |
|---|---|---|
| **Gemini UI** (`gemini.google.com`) | The image generator (Stage 2) | 🔴 **High** — the central architectural lock-in; no API contract, UI can change (see RISK_REGISTER). v2.0 roadmap targets replacing it with an API renderer. |

## Optional

| Dependency | Why | Status |
|---|---|---|
| **pytesseract** + Tesseract | OCR QA diagnostic (`scripts/render_qa.py`) | Not installed; optional. |

## Present but NOT used by the production Pipeline (removal candidates)

| Dependency | Why present | Recommendation |
|---|---|---|
| **opencv-python** | Legacy `pipeline/cv/` (Stage 0 detection) | Not imported by the 3 Stages → **removable from the production environment**; keep only if `pipeline/cv/` is retained. |
| **numpy** | Legacy `pipeline/cv/` | Same as OpenCV. |
| **Legacy CV pipeline** (`pipeline/cv/` + `yolov8n.pt`) | Earlier OCR/CV approach | `ultralytics` (YOLO) is **not installed** → the CV detection is not runnable. **Candidate for archival** to `trash/` (a future cleanup, not this phase). |

## Summary

- The production-core set is **lean and justified**; PyYAML/rich are soft (graceful fallback).
- The only **serious lock-in is the Gemini UI** (browser RPA); everything else is replaceable.
- **OpenCV, numpy and the legacy `pipeline/cv/`** are dead weight in the production runtime and are safe future-removal candidates (env/code change — deferred; see TECHNICAL_DEBT and ROADMAP v1.2).
