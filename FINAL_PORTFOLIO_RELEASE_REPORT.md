# Final portfolio release report — 2026-11-18

## A. Summary

The approved security cleanup and GitHub migration are completed. The three-stage runtime, 391 JSON passports and required SSOT/source files are preserved. No product feature or image-generation algorithm was changed during publication.

## B. Branch state

The approved cleaned runtime baseline is `48cfff2715f67c511092d9090fbb8c21df110adb`, replacing old master `cb61dd0be122b59b7fcf37f4c5d7fea04d67a2b8`. Master is the default and sole public branch. Dev and backup/full-history-pre-v1.0 were retired after fresh-clone checks and default-branch verification. This documentation update is a fast-forward follow-up to the approved runtime baseline. Unrelated histories were never merged. [Tag objects and migration details](REMOTE_REF_MIGRATION_REPORT.md).

## C. Security

Exposed historical credentials, browser/account captures, diagnostics and unreviewed bulk assets were removed from reachable public history. A fresh mirror of every advertised public ref passed known-credential, pattern, private-path, excluded-path and selected sensitive-blob checks with zero findings. S1/S2 revocation and S3 affected-session termination are owner attestations; no old key was tested against a provider. S4 stays private. Existing Git identity metadata is owner-authorised. [Security scope and limits](FINAL_SECURITY_AUDIT.md).

## D. Cleanup

The original dev tree had 5,533 files; the approved cleaned publication has 509. All 5,031 excluded local files remain privately retained, all 391 JSON passports remain, and 420 protected source/data/test files match the input candidate. Private source/history and recovery bundles were preserved and independently restored. No recovery archive or internal archive location is published.

## E. Tests

Compilation, CLI, dependency validation and 18/18 unit tests passed both before publication and in fresh public master clones. Prior isolated validation regenerated 391 passports with 391 matching SHA-256 values and checked synthetic Stage 3 processing and resume. [Commands, evidence and limitations](FINAL_TEST_RESULTS.md).

## F. Documentation

README, architecture, runbooks and the five final reports distinguish executed checks from historical results. Verified historical output remains 389 WebPs for 391 records, with exports 132 and 218 missing. The real, owner-authorised 400x400 generic historical preview loads on GitHub; branded source photographs remain excluded. No new catalogue images were generated.

## G. Remote publication

[indexdeny/pharma_v2](https://github.com/indexdeny/pharma_v2) is public. GitHub API and Git transport confirm default master, exactly one branch, two cleaned annotated tags and no legacy branch refs. Fresh public cloning and runtime checks passed. README rendering, its historical preview and documentation destinations were checked on GitHub. Secret Scanning and Push Protection remain enabled. Addressed atomic pushes used exact expected-old leases; no mirror push, public PR or protection bypass was used.

## H. Portfolio readiness

**READY WITH LIMITATIONS.** Suitable for presenting the implemented workflow and measured results. This is not Production Ready, clinical/regulatory approval or a new complete catalogue acceptance.

## I. Remaining risks

Authenticated Gemini rendering and catalogue-wide visual/medical acceptance were not rerun. Stage 0 is manual, rendering is attended and non-deterministic, dependencies are not locked, and storefront adoption is owner-reported. Rewritten refs do not erase prior clones or GitHub caches. Original branded photos and unreviewed weights remain excluded. [Operational limits](README.md#known-limitations).

## J. Next action

Use the factual [portfolio summary](PORTFOLIO_PUBLICATION_SUMMARY.md) with these limitations. A private GitHub Support request draft is available for cache review; it has not been sent. No further ref replacement is required for this migration.
