# ADR-004: Selenium RPA (browser) instead of an image API

**Status:** Accepted · **Date:** reconstructed 2026-06-28 · **[confirm with author]**

## Context
Having chosen Gemini ([ADR-001](ADR-001-why-gemini.md)), a transport was needed.
The API route (Imagen/Vertex) was **ROADMAP_ONLY** because it requires a **paid
Cloud project**. Gemini's image generation is available for free through the
interactive chat UI, which has no official automation API.

## Decision
Drive Gemini through **Selenium browser automation (RPA)** using a
**pre-authenticated Chrome profile** (`src/rpa_orchestrator.py`). Selenium RPA is
the **sole canonical render client**; the image is extracted from the page's
`blob:` URL via JavaScript.

## Consequences
- ✅ Zero API cost; uses the free interactive session.
- ⚠️ Requires a logged-in browser profile and must run **non-headless** (Gemini blocks headless image generation).
- ⚠️ **Serial** (one browser, one chat, `batch_size=1`) — the concurrency bottleneck in the CRM Readiness audit.
- ⚠️ Brittle to Gemini UI/DOM changes; mitigated by retries, backoff, batch resets, screenshots, and the resume tracker.

## Alternatives considered
Imagen/Vertex **API** (paid, deferred to roadmap); other API-based renderers
(abandoned — see `trash/_archive/`).
