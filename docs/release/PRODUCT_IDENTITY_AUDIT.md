# Product Identity Audit

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tags are unchanged.

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> Goal: does the repository present itself consistently as a **product**, not a
> pile of scripts? Findings only — terminology is **not** blindly replaced.

## Canonical vocabulary (already used consistently)

**PharmaGen PRO** (the product) · **Pipeline** (the whole) · **Stage 1/2/3** ·
**Renderer** (Stage 2) · **Passport** · **SSOT** · **WEBP** · **RPA**.

These appear consistently across `README.md`, `docs/ARCHITECTURE.md`, the audits,
ADRs, and the operations set. The product identity is **strong**.

## Residual "script / utility / tool / generator" usages

A repository-wide scan found ~29 occurrences across the top-level docs. Each was
assessed for whether a change would improve clarity:

| Usage | Where | Verdict |
|---|---|---|
| `scripts/` folder, "maintenance tools/utilities" | `scripts/README.md`, README | **Keep** — accurate: these *are* auxiliary tools, deliberately separated from the Pipeline. |
| "standalone tool" | `docs/BUSINESS_VALUE_INTEGRATION.md` | **Keep** — a deliberate framing of integration Option 1. |
| "Passport **Generator**", "image **generator**" | diagrams, Stage names | **Keep** — "Passport Generator" is the canonical Stage-1 name. |
| "compatibility **shim** / script" | root shims' docstrings | **Keep** — the shims literally are small scripts. |
| Legacy "script" wording | `docs/ARCHITECTURE.md` older sections | **Acceptable** — historical; the file already defers to README for current structure. |

## Verdict

Product identity is **consistent and clear**; no blind renaming is warranted.
The remaining `script/tool/utility` uses are either accurate (the `scripts/`
folder, maintenance tools) or deliberate (business framing). 

**Optional, low-value polish** (not required for v1.0.0): management-facing
material may lead with "PharmaGen PRO / Pipeline / Stage" phrasing; align the
`docs/ARCHITECTURE.md` header to the v1.0.0 naming (see GIT_RELEASE_AUDIT GR-4).
No action is required for the release.
