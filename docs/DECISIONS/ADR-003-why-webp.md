# ADR-003: WEBP (1600×1600, ≤500 KB) as the final asset format

**Status:** Accepted · **Date:** reconstructed 2026-06-28 · **[confirm with author]**

## Context
Final packshots are delivered for web/catalogue use. They must be small enough
for fast delivery yet keep pharmaceutical label text legible. Raw Gemini PNGs are
large and unbounded in size.

## Decision
Convert raw PNGs to **WEBP at 1600×1600** with **auto-tuned quality** to stay
**≤500 KB** (`src/image_processor.py`: start quality 95, step 4, `method=6`,
LANCZOS upscale to preserve text legibility).

## Consequences
- ✅ Hard **≤500 KB** weight cap per asset; broad browser support.
- ✅ LANCZOS upscale preserves legibility of small pharma fonts.
- ⚠️ Lossy; quality is reduced automatically if 500 KB is exceeded.
- ✅ Deterministic for a given input PNG.

## Alternatives considered
PNG (too large, no weight cap), JPEG (artifacts on text/edges), AVIF
(tooling/support maturity at the time).
