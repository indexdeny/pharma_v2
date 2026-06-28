# ADR-001: Google Gemini as the image generator

**Status:** Accepted · **Date:** reconstructed 2026-06-28 · **[confirm with author]**

## Context
The project must produce photorealistic pharmaceutical packshots for the whole
catalogue (391 SKU) at low cost. The git history and `trash/_archive/` show a
series of renderer experiments that were tried and abandoned: DALL·E, Flux,
Hugging Face, Pollinations, and an Imagen wrapper. The Imagen/Vertex API route
was marked **ROADMAP_ONLY** because it "requires a paid Cloud project". A free,
high-quality generator was needed.

## Decision
Use **Google Gemini** as the image generator, accessed through its **chat UI
session** (not the paid API). See [ADR-004](ADR-004-why-rpa.md) for the transport.

## Consequences
- ✅ High-quality generation at **zero API cost** (uses an interactive session).
- ⚠️ Hard dependency on a logged-in browser session and on `gemini.google.com`.
- ⚠️ **Non-deterministic** output (no seed/temperature control via the UI) — see the Production Readiness audit.
- ⚠️ Brittle to Gemini UI changes (selector contract) — see the Bus Factor audit.

## Alternatives considered
DALL·E / Flux / Hugging Face / Pollinations (quality and/or cost trade-offs,
abandoned — see `trash/_archive/`); Imagen/Vertex **API** (paid Cloud billing,
deferred to roadmap).
