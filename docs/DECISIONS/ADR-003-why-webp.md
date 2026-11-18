# ADR-003: WEBP (1600×1600, ≤500 KB) as the final asset format

**Status:** Accepted · **Date:** reconstructed 2026-06-28 · **[confirm with author]**

## Context
Final packshots are delivered for web/catalogue use. They must be small enough
for fast delivery yet keep pharmaceutical label text legible. Raw Gemini PNGs are
large and unbounded in size.

## Decision
Convert raw PNGs to **WEBP at 1600×1600** with **auto-tuned quality** targeting
**≤500 KiB** (`src/image_processor.py`: start quality 95, step 4, `method=6`,
LANCZOS upscale to preserve text legibility).

## Consequences
- Target **≤500 KiB**, with broad WebP browser support. The bounded quality loop can fail; inspect output bytes.
- LANCZOS resampling does not restore missing detail or prove label legibility; visual acceptance is required.
- ⚠️ Lossy; quality is reduced automatically if 500 KB is exceeded.
- Repeatability depends on input, settings and codec/library versions; this is not deterministic AI image generation.

## Alternatives considered
PNG (too large, no weight cap), JPEG (artifacts on text/edges), AVIF
(tooling/support maturity at the time).

## Operational boundary

A per-file compression failure returns false, while the batch can still exit successfully. Stage success is not a guarantee that every file meets the byte target. The measured historical set did meet its size target; that does not prove all future inputs will.
