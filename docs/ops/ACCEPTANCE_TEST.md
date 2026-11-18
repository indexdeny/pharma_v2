# Acceptance checks

Current checklist, 2026-11-18. Historical release documents do not certify this candidate. Completed local checks and exact results are in [portfolio evidence](../portfolio-evidence.md).

| Check | Procedure | Acceptance boundary |
|---|---|---|
| Syntax/import surfaces | `python -m compileall -q main.py src pharma_pkg schemas` | Exit 0; execution dependencies still require separate checks |
| CLI | `python main.py --help` | Exit 0 without starting a browser |
| Unit suite | `python -m unittest discover -s tests -p "test_*.py"` | All discovered tests pass; record count/date |
| Source readability | Parse SSOT JSON/CSV and all input JSON passports | Record unique IDs, supported schema_version and missing records; no claim of full clinical validation |
| Stage 1 | Run in isolated copy with empty generated directory | Output count matches JSON set; inspect failures; compare content hashes for unchanged inputs |
| Resume | Run Stage 1 and Stage 3 twice in the same disposable copy | Stage 1 skips completed stage; existing Stage 3 file remains unchanged; note count/filename limitations |
| Stage 3 | Process a synthetic fixture in an isolated directory | Valid WebP, configured dimensions and byte target; not catalogue acceptance |
| Real image delivery | Compare expected IDs with readable final files | Explain missing/failed outputs; human visual acceptance required |
| Browser/Gemini | Attended authorised session, small batch | Verify login, cleanup, selectors, download, progress and output; NOT VERIFIED here |
| Publication | Revoked exposed credentials, privacy/rights review, clean scan | Blocked pending owner confirmation and approved remediation |

Run from the repository root using the explicit project venv interpreter. Do not regenerate historical production outputs as a test. Do not equate successful local checks with Production Ready or LinkedIn readiness. Public master promotion and branch retirement require the remaining migration gates in the [audit](../portfolio-audit.md).
