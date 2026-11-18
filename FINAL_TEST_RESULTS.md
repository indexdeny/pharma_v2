# Final local test results — 2026-11-18

Executed in a new isolated Python 3.10.11 environment, installed from unchanged requirements.txt. pip check passed.

```powershell
python -m compileall -q main.py src pharma_pkg schemas
python main.py --help
python -m unittest discover -s tests -p "test_*.py"
python -m pip check
```

All commands exited 0. Unit tests: **18 run, 18 passed, 0 failed, 0 skipped**. Tests were not changed for this migration. The earlier warning-selection correction belongs to the input candidate.

Isolated Stage 1: **391/391** JSON passports compiled; all **391 SHA-256 values** match the pre-cleanup reference. Stage 1 resume skipped completed work. Stage 3 processed a synthetic 128×96 fixture into a valid 1600×1600 WebP of 4,634 bytes; resume preserved the output timestamp. A separate file-only Stage 2 resume check verified that missing-image tracker entries are retried and existing raw files are counted; no browser was created.

420 required source/data/test files match the input candidate. CSV and master contain 391 unique product records; 391 JSON passports have supported schema_version and nonempty sku_id. There is no full formal SSOT JSON schema in this repository: structural/readability checks and compiler routing/fit checks are reported, not invented full-schema certification.

[Machine-readable results](docs/evidence/20261118-final-local-verification.json), [validated dependency versions](docs/evidence/20261118-validated-dependencies.txt), [historical output evidence](docs/portfolio-evidence.md).

Authenticated Gemini rendering, catalogue-wide visual/medical acceptance, and optional legacy CV/OCR dependencies are **NOT VERIFIED**. No historical commercial images were regenerated.
