# PharmaGen PRO — Project History

> A narrative of how the product evolved — **not** a changelog. It exists so a new
> maintainer understands *why the system looks the way it does*. Milestones are
> grounded in the git history (46 commits, 2026-05-02 → 2026-06-11) and the later
> hardening work; where a feature-to-version mapping is inferred from commit
> messages it is noted as such.

```
v0.1  OCR / CV foundation
  │
  ▼
v0.3  Passports (JSON → Markdown)
  │
  ▼
v0.5  Templates (geometry routing, size system)
  │
  ▼
v0.7  Renderer (experiments → Gemini RPA)
  │
  ▼
v1.0  Production (391 SKU) → Unification → Hardening
```

---

## Phase 1 — OCR / CV foundation (~v0.1–0.3, 2026-05-02)

The project began as a computer-vision effort: read pharmaceutical product photos
and extract structured data. The residue of this era is `pipeline/cv/`
(detection, OCR, zone/geometry classifiers, `yolov8n.pt`). This established the
input side: source photos in `input/` and the idea of a per-SKU "passport".

## Phase 2 — Passports (~v0.3–0.46, 2026-05-02 → 05-10)

Focus shifted to turning extracted data into a precise, reviewable prompt. The
**passport** concept solidified: a JSON record per SKU, compiled into a
human-readable **Markdown** prompt ([ADR-002](docs/DECISIONS/ADR-002-why-markdown.md)).
This is the lineage of today's `src/passport_generator.py` and the
`pharma_pkg/` routing/geometry/classifier library, plus the rule-based
`verification_agent.py`.

## Phase 3 — Renderer experiments (~v0.47–0.48, 2026-05-17 → 05-18)

Many image generators were tried and discarded — DALL·E, Flux, Hugging Face,
Pollinations, and an Imagen wrapper (all now in `trash/_archive/`). Commit
*"Add auto-fallback logic to Plan B"* captures the instability of this period.
The lesson — API renderers were costly or low-quality — drove the eventual choice
of Gemini ([ADR-001](docs/DECISIONS/ADR-001-why-gemini.md)) over a paid API
([ADR-004](docs/DECISIONS/ADR-004-why-rpa.md)).

## Phase 4 — Templates & data discipline (~v0.49–0.66, 2026-05-25 → 06-05)

The art-direction system matured: geometry-based template routing (T1/T2/T3 and
the bottle/vertical family), colour zoning, and the optical calibration rules.
Data discipline tightened in parallel — palette and price-matching work that led
to **SSOT/SKU.csv becoming the routing authority**
([ADR-005](docs/DECISIONS/ADR-005-ssot-routing-authority.md), introduced ~P6.0).

## Phase 5 — Catalogue hardening: P20–P22 (2026-06-06)

A burst of catalogue-level work in a single day:
- **P20** — full price match, SKU corrections, passport rebuild, project cleanup.
- **P21** — the multipack template `T_MULTIPACK` for the 5 "Test Pack" SKUs, with quantity rendered as *"Assorted Pack"*.
- **P22** — the template **size system**: `T1_SMALL`/`T1_LARGE` for pills and `T_VERT_VIAL`/`T_VERT_DROPPER`/`T_VERT_INHALER` for vertical containers.

This is why the template "zoo" exists today — each entry answers a specific
packaging case discovered during the catalogue pass.

## Phase 6 — Gemini RPA renderer & production runs (~v0.69–0.73.1, 2026-06-06 → 06-11)

The Selenium RPA renderer (`gemini_image_generator.py`, now
`src/rpa_orchestrator.py`) was stabilized: batch context resets, timeout/throttle
backoff, failure screenshots, an end-of-run retry pass, and the
`gemini_rpa_progress_v23.txt` resume tracker. The full catalogue of **391 SKU**
was rendered to PNG and optimized to WEBP ([ADR-003](docs/DECISIONS/ADR-003-why-webp.md)).
At this point the project was production-complete but existed as three loose scripts.

## Phase 7 — Unification (2026-06-27)

The three scripts were unified behind a single entry point **`main.py`** with a
central **`config.yaml`**, a `src/` package, subprocess orchestration, resume,
and rich logging — preserving stage logic byte-for-byte
([ADR-006](docs/DECISIONS/ADR-006-unified-entrypoint.md)). Stale `c:\pharma_v2`
paths were fixed; root shims kept backward compatibility.

## Phase 8 — Repository polish (2026-06-28)

Root minimized; utilities moved to `scripts/`; legacy/experimental artifacts
archived to `trash/` (via `git mv`, history preserved); a bilingual README and
editable Mermaid diagrams added. See [REPO_AUDIT.md](docs/REPO_AUDIT.md).

## Phase 9 — Production Hardening (2026-06-28, current)

The dev phase was declared complete and a hardening phase opened: the
[Bus Factor](docs/audits/BUS_FACTOR_AUDIT.md),
[Production Readiness](docs/audits/PRODUCTION_READINESS_AUDIT.md) and
[CRM Readiness](docs/audits/CRM_READINESS_AUDIT.md) audits, the
[ADRs](docs/DECISIONS/), and this history — preparing the project to be owned by
a team rather than its author.

---

## Milestone reference (from git)

| Date | Milestone | Commit |
|---|---|---|
| 2026-05-02 | Initial commit | `6911bdf` |
| 2026-05-18 | HF renderer + auto-fallback "Plan B" | `8bf918f`, `6584346` |
| 2026-06-06 | P20 — full price match, passport rebuild | `c613978` |
| 2026-06-06 | P21 — multipack template (`T_MULTIPACK`) | `c72da7e`, `90ec6ea` |
| 2026-06-06 | P22 — template size system | `6890c54` |
| 2026-06-11 | Last tagged dev build (v0.73.1) | `5a275d8` |
| 2026-06-27 | Unification (`main.py` + `src/` + `config.yaml`) | *(post-v0.73.1)* |
| 2026-06-28 | Repository polish + Production Hardening | *(post-v0.73.1)* |

> The "Version 0.1 → 1.0" arc above maps the author's mental model onto the commit
> record; exact per-version feature boundaries are approximate and reconstructed
> from commit messages.
