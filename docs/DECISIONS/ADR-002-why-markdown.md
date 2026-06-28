# ADR-002: Markdown as the passport / prompt format

**Status:** Accepted · **Date:** reconstructed 2026-06-28 · **[confirm with author]**

## Context
Each SKU needs a precise, structured prompt for the renderer, compiled
deterministically from the SSOT and the JSON passport. The format had to be
human-readable (so art-direction rules — colour zoning, optical calibration,
text-sanitization output — can be reviewed), diffable in git, and editable
without touching code.

## Decision
Compile each passport into a **Markdown prompt** at
`pipeline/passports.markdown/<stem>.md` (Stage 1, `src/passport_generator.py`).
The Markdown file **is** the prompt sent to the renderer.

## Consequences
- ✅ Human-auditable and version-controlled; reviewers can read the exact prompt.
- ✅ Deterministic generation from SSOT + JSON (verified byte-identical on re-run).
- ✅ Decouples prompt authoring from the renderer transport.
- ⚠️ The Markdown structure is an implicit contract with the renderer's expectations.

## Alternatives considered
Raw JSON prompt (less human-readable for art direction); ad-hoc string templates
inside the renderer (couples prompt to transport, not diffable).
