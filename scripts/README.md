# scripts/ — Auxiliary & Maintenance Tools

Operator tools that are **not** part of the three-stage production pipeline
(`main.py`). Run them from the **repository root** so relative paths resolve.

| Script | Purpose |
|---|---|
| `render_qa.py` | OCR-based QA diagnostic over rendered images (requires Tesseract + `pytesseract`). |
| `image_postprocessor.py` | Alternative post-processor (2048px WEBP). Non-canonical — the canonical final stage is `src/image_processor.py` → `output/`. |
| `generate_architecture_snapshot.py` | Generates an architecture snapshot from the live code. |
| `download_last_image.py` | Manual debug helper to pull the last generated image from the Gemini UI. |
| `sync_p23_palette.py` | Maintenance: palette sync against the SSOT. |
| `sync_passports_refined.py` | Maintenance: passport refinement sync. |
| `update_dosages.py` | Maintenance: dosage field updates. |

Example:

```bash
python scripts/render_qa.py
python scripts/generate_architecture_snapshot.py
```
