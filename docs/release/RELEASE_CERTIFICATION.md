# Release Certification

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tags are unchanged.

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> Final engineering certification, synthesized from the release-engineering audit set.

| Field | Value |
|---|---|
| **Project Name** | PharmaGen PRO |
| **Version** | 1.0.0 (annotated tag `v1.0.0`) |
| **Repository Status** | Clean, minimal root, tagged; history rewritten locally (not pushed — see [GIT_RELEASE_AUDIT](GIT_RELEASE_AUDIT.md) GR-1) |
| **Production Status** | Operating — full catalogue rendered to PNG (391 in `render_output/raw/`); **389** delivered as final WEBP in `output/` (2-SKU gap — see [GIT_RELEASE_AUDIT](GIT_RELEASE_AUDIT.md) GR-5) |
| **Deployment Readiness** | Ready (Windows; documented in [DEPLOYMENT.md](../../DEPLOYMENT.md); gated by [ACCEPTANCE_TEST](../ops/ACCEPTANCE_TEST.md)) |
| **Operational Readiness** | Ready (runbook, disaster recovery, backup strategy in place) |
| **CRM Readiness** | Not yet — file-based integration only; programmatic adapter is analysed, not built ([CRM Readiness audit](../audits/CRM_READINESS_AUDIT.md), ROADMAP v1.5) |

## Known Limitations

- Rendering is **browser-driven (Gemini RPA)**: serial, non-headless, **non-deterministic**; `output/` is the system of record.
- **Gemini UI fragility** (RK-1) is the top technical risk.
- **No free-disk-space guard** (TD-C1) — the one unmitigated production risk in code.
- **No CRM API/events/status/queue** (TD-H3); render path is **untested** (Testing 5/10).

## Recommended Usage

Use as a **standalone internal Pipeline** run by an operator per the
[Operations Manual](../../OPERATIONS.md). Integrate with the CRM via **file
hand-off** from `output/` now; pursue a programmatic adapter (ROADMAP v1.5) when
CRM automation is required. Always keep Tier-1 backups (images are not reproducible).

## Recommended Next Development Phase

**v1.1 — Reliability** (disk-space guard + per-SKU post-mortem logging), then
**v1.5 — CRM adapter** when integration is greenlit. See [ROADMAP.md](ROADMAP.md).

## Final Engineering Verdict

> ## ✅ Production Ready with Known Limitations

**Justification (objective, from the audits):** the system performs its job end
to end and has shipped the catalogue (391 SKU rendered, 389 final WEBP), with strong documentation,
resume, recovery and hygiene — well beyond *Beta* or *Release Candidate*. It is
**not** certified as unqualified *Production Ready* because of real, documented
production risks and constraints: no disk-space guard (TD-C1), non-deterministic
browser-RPA rendering with Gemini-UI fragility (RK-1, TD-H1/H2), and limited
automated test coverage of the render/orchestration path (Testing 5/10). These
are known, tracked, and have owners in the roadmap — appropriate for an internal
v1.0.0 release used by a trained operator.

---

### Release-engineering document set

[GIT_RELEASE_AUDIT](GIT_RELEASE_AUDIT.md) · [PRODUCT_IDENTITY_AUDIT](PRODUCT_IDENTITY_AUDIT.md) ·
[TECHNICAL_DEBT](TECHNICAL_DEBT.md) · [RISK_REGISTER](RISK_REGISTER.md) · [ROADMAP](ROADMAP.md) ·
[ARCHITECTURE_HEALTH](ARCHITECTURE_HEALTH.md) · [DEPENDENCY_LIFECYCLE](DEPENDENCY_LIFECYCLE.md) ·
[REPOSITORY_SCORECARD](REPOSITORY_SCORECARD.md)
