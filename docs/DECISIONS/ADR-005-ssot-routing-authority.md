# ADR-005: `SSOT/SKU.csv` as the primary routing authority

**Status:** Accepted · **Date:** reconstructed 2026-06-28 (introduced ~P6.0)

## Context
Product attributes lived in several places — JSON passports, `master.json`, and
`SKU.csv` — which produced conflicting routing decisions (which template a SKU
gets) and inconsistent unit-count labels. Template routing needs **one**
authority to be deterministic.

## Decision
Treat **`SSOT/SKU.csv`** as the **primary routing authority**: `package_type`
drives template selection, and `unit_count_standard` overrides the JSON
passport's value. The JSON passport and `master.json` are secondary
(`src/passport_generator.py` `agent_1_router()`).

## Consequences
- ✅ Deterministic, single-source routing; conflicts resolved by precedence.
- ✅ Corrections are made in one place (the SSOT).
- ⚠️ Edits to routing behaviour must go through `SKU.csv`, not the JSON passports.

## Alternatives considered
JSON-passport-driven routing (the earlier approach; conflict-prone and
non-authoritative).
