# Git & Release-Metadata Audit

> **Historical snapshot — current maintenance notice (2026-11-18):** The assessment below records an earlier state, not current acceptance or publication readiness. Current paths, measured results and security/publication limits are in the [portfolio audit](../portfolio-audit.md). The owner has superseded the old internal-publication restriction; third-party rights are not implied. Historical tags are unchanged.

> **Phase:** v1.0.0 Final Release Engineering · **Date:** 2026-06-28
> Read-only audit — **this phase performed no rewrite**. (The v1.0.0 baseline
> squash that rewrote the pre-1.0 history was a *prior* release-cleanup event,
> documented below as GR-1.)

## History

```
ba1530f  Operations Documentation        ← tag v1.0.0
8dfa369  Production Hardening
49aae46  Repository Cleanup
0b680bd  Architecture Unification
6bbcb3f  PharmaGen PRO 0.x — pre-1.0 development baseline
```

- **Understandable?** Yes. A clean linear history: one squashed baseline (the 46 pre-1.0 `Test v0.x` dev commits) followed by four phase-named commits that map 1:1 to the project's hardening phases.
- **Would another engineer follow the evolution?** Yes — commit subjects are phase names, bodies explain scope, and [PROJECT_HISTORY.md](../../PROJECT_HISTORY.md) narrates the squashed era.
- **Commit-message consistency:** consistent — `Subject` = phase, descriptive body, `Co-Authored-By` trailer on each.

## Branch strategy

| Branch | Role | Note |
|---|---|---|
| `master` | release line (5 commits) | current; carries tag `v1.0.0`. |
| `backup/full-history-pre-v1.0` | safety backup (46 + 4 commits) | full pre-rewrite history; keep until the rewrite is confirmed/published. |
| `dev` | pre-existing | **purpose undocumented — finding GR-2.** |
| `origin/master` | remote (46 commits) | original history; **diverged** from local (finding GR-1). |

## Release tag

- `v1.0.0` is **annotated** (tagger + message), pointing at `ba1530f`. Sufficient for this release.
- Recommendation: tag future releases the same way (annotated, `vMAJOR.MINOR.PATCH`).

## Release metadata (version consistency)

| Location | Version | Status |
|---|---|---|
| `git tag` | `v1.0.0` | ✅ |
| `CHANGELOG.md` | `v1.0.0` | ✅ |
| `src/__init__.py` `__version__` | `1.0.0` | ✅ |
| `config.yaml` | (none) | ⚪ acceptable (no version field) |
| `README.md` | no explicit version string | 🟡 finding GR-3 |
| `docs/ARCHITECTURE.md` header | `v2.3 / Pipeline P8.0 / Schema v2.1` | 🟡 finding GR-4 — internal schema/pipeline versioning predates the v1.0.0 release naming |

> Note: `docs/ARCHITECTURE.md` versions describe an **internal schema/pipeline axis** (P-numbers, schema v2.1), not the product release; they are not strictly "wrong", but a reader may confuse them with the product version.

## Findings & remaining risks

| # | Finding | Severity |
|---|---|---|
| GR-1 | `master` diverged from `origin/master` (5 vs 46 commits, rewritten hashes). Publishing requires `git push --force-with-lease`; **not done** (deliberate, pending decision). `origin/master` + backup branch preserve the original. | 🟡 process |
| GR-2 | `dev` branch exists with no documented purpose. | ⚪ |
| GR-3 | `README.md` carries no explicit version string. | ⚪ |
| GR-4 | `docs/ARCHITECTURE.md` header still shows internal `v2.3 / P8.0`, not aligned to v1.0.0 naming. | ⚪ |
| GR-5 | **Catalogue count is inconsistent across the repo**: `output/` = **389** final WEBP, `render_output/raw/` = **391** PNG, `SKU.csv` = **390** rows, `master.json` = **393** product entries, `docs/ARCHITECTURE.md` = **389**. The committed docs (README, CHANGELOG, ADRs) use the loose "391". The verified per-stage truth: **391 rendered to PNG, 389 delivered as final WEBP.** | 🟡 |

No genuine defect requiring a history change was found. GR-3/GR-4 are doc-only and may be aligned later; GR-1 is a publication decision for the owner. GR-5: the release-engineering docs (this set) use the precise per-stage figures (391 rendered / 389 final); the committed README/CHANGELOG keep the loose "391" and should be aligned in a future commit — **not amended here** to avoid a v1.0.0 history rewrite.
