# PHARMAGEN PRO — ARCHITECTURE v2.3
> **Last Updated:** 2026-06-04 | **Pipeline Version:** P8.0 | **Schema:** v2.1

> **Note:** This document describes the internal Stage logic (agents, templates,
> routing) which is unchanged. For the **current repository layout and how to run
> the Pipeline**, the authoritative sources are the project [README](../README.md)
> and [REPO_AUDIT.md](REPO_AUDIT.md). Some folder/command references in the older
> sections below predate the unified `main.py` + `src/` structure.

---

## 1. Production Pipeline Overview

```
INPUT (389 source JPG images)
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 0: ANALYSIS (Manual / Workflow)              │
│  Workflow: /analyze-pharma                          │
│  Input:    input/{sku_id}.jpg + SSOT/master.json    │
│  Output:   pipeline/passports/{sku_id}.json (v2.1)  │
│  Agent:    Gemini via IDE + analyze-pharma.md       │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 1: VERIFICATION (Optional Pre-Check)         │
│  Workflow: /project_reviewer                        │
│  Script:   verification_agent.py (v2.3)             │
│  Checks:   12 deterministic checks                  │
│  Threshold: confidence ≥ 0.75 → PASS               │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 2: PASSPORT GENERATION (Production Core)     │
│  Script:   pass_tomd.py                             │
│  Input:    pipeline/passports/*.json (389 files)    │
│            SSOT/SKU.csv (routing authority)         │
│            SSOT/master.json (brand specs)           │
│            SSOT/master_pharma_design_specs.json     │
│  Output:   pipeline/passports.markdown/*.md         │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 3: IMAGE GENERATION (RPA Automation)         │
│  Script:   gemini_image_generator.py                │
│  Input:    pipeline/passports.markdown/*.md         │
│  Transport: Selenium → Gemini Chat                  │
│  Output:   render_output/raw/{sku_id}.png           │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 4: POST-PROCESSING (Active Production)       │
│  Script:   image_postprocessor.py                   │
│  Input:    render_output/raw/{sku_id}.png           │
│  Output:   render_output/processed/{sku_id}.png     │
│  Process:  EXIF normalize → RGB → resize 1024×1024  │
└─────────────────────────────────────────────────────┘
       │
       ▼
OUTPUT (389 PNG renders, 1024×1024px, white background)
```

---

## 2. Internal Architecture of pass_tomd.py

### Agent Stack (3 internal agents):

```
agent_1_router(data)
  → Determines template: T1 | T2 | T3 | T_BOTTLE_BOX
  → Determines is_bottle_override: bool
  → Uses: SKU_REGISTRY (from SSOT/SKU.csv) as PRIMARY authority
  → Falls through to: geometry_mapping.py + GEOMETRY_MAPPING

agent_2_verifier(data)      ← verification_agent.py (separate file)
  → 12 deterministic checks
  → Returns: confidence (0.0–1.0), warnings[], verified (≥0.75)
  → Called from: project_reviewer workflow (pre-run QA)

agent_3_passport_architect(data, template_id, is_override, verifier_result)
  → Builds final Markdown prompt using TEMPLATE_MAP[template_id]
  → Applies resolve_unit_label() for correct quantity labels
  → Applies purge_forms() for dosage cleaning
  → Writes: pipeline/passports.markdown/{sku_id}.md
```

### Template System (TEMPLATE_MAP):

| Template | Description | Triggers | Proportions |
|---|---|---|---|
| `T1` | Standard horizontal box | pills/packs/boxes/strips/units | 2:1:1 (landscape) |
| `T2` | Vertical slender (slim box) | spray/nasal drops | 1:3:0.5 (tall slim) |
| `T3` | Horizontal long | sachets/tubes/cream | 3:1:0.5 (wide flat) |
| `T_BOTTLE_BOX` | Vertical portrait carton | bottles/vials/inhalers/pens | 1:2.2:1 (portrait) |

### Routing Priority (agent_1_router):
```
1. SKU_REGISTRY (SSOT/SKU.csv) package_type → most authoritative
   ├─ package_type in VERTICAL_PACKAGE_TYPES → T_BOTTLE_BOX
   ├─ package_type in {"sachets","tubes","tube"} → T3
   └─ else → fall through to GEOMETRY_MAPPING
2. is_vertical_container(pkg_type, primary_geometry_csv, geom_json) → T_BOTTLE_BOX
3. GEOMETRY_MAPPING (pharma_pkg/geometry_mapping.py) → T1/T2/T3
4. Default → T1
```

### Unit Count Label Resolution (resolve_unit_label):
```
pills/packs/boxes/strips/units → "{N} Pills"
vials                          → "{N} Vials" (or "1 Vial")
tubes/tube                     → "{N} Tube"
sachets                        → "{N} Sachets" (or "1 Sachet")
pens                           → "{N} Pen"
inhalers                       → "{N} Inhaler"
bottles/bottle                 → "{N} Bottle"
unknown                        → "{N} Pills" (safe fallback)
```

Data priority: `unit_count_standard` from SKU.csv > `unit_count_display` from JSON passport.

---

## 3. Data Sources (SSOT)

| File | Purpose | Format | Authority |
|---|---|---|---|
| `SSOT/SKU.csv` | Package type routing, unit counts | CSV | **PRIMARY** (P6.0+) |
| `SSOT/master.json` | Brand specs, colors, product info | JSON | Secondary |
| `SSOT/master_pharma_design_specs.json` | Design specifications | JSON | Secondary |
| `SSOT/geometry_types.json` | Packaging geometry enum | JSON | Reference |
| `gemini_rpa_progress_v23.txt` | RPA generator progress tracking | TXT (stems) | Production State |

### SKU.csv columns (key fields):
| Column | Description |
|---|---|
| `picture` | Filename key (e.g. `379-min.jpg`) |
| `package_type` | Routing authority: `pills/bottles/vials/sachets/tubes/inhalers/pens/...` |
| `primary_geometry` | Physical container description |
| `unit_count_standard` | Canonical unit count (overrides JSON field) |
| `dosage_type` | Unit type (mg/ml/etc) |

---

## 4. Folder Structure

```
pharma_v2/
├── .agents/                        # AI workflow definitions
│   ├── protocol.md                 # Master pipeline protocol v3.0 (roadmap)
│   └── workflows/
│       ├── analyze-pharma.md       # /analyze-pharma — Stage 0 workflow
│       ├── project_reviewer.md     # /project_reviewer — QA workflow (v2.3)
│       └── research-tools.md       # /research-tools — tooling R&D
├── SSOT/                           # Single Source of Truth
│   ├── SKU.csv                     # PRIMARY routing source (390 records)
│   ├── master.json                 # Brand registry (~615KB)
│   ├── master_pharma_design_specs.json
│   └── geometry_types.json
├── pipeline/                       # Active pipeline data
│   ├── passports/                  # JSON passports (389 files, schema v2.1)
│   ├── passports.markdown/         # Generated MD passports (389 files)
│   └── cv/                         # CV artifacts
├── render_output/                  # Rendering output
│   ├── processed/                  # Final PNGs (after generation)
│   ├── raw/                        # Chrome Downloads raw files
│   ├── failed/                     # Failed renders
│   └── failed_logs/                # Failure log files
├── input/                          # Source product photos (389 JPGs)
├── ready_images/                   # Delivered production renders
├── pharma_pkg/                     # Internal Python package
│   ├── geometry_mapping.py         # Fallback routing logic
│   ├── dimension_resolver.py       # Box dimension calculation
│   ├── primary_classifier.py       # Primary package detection
│   └── secondary_templates.py      # Secondary packaging templates
├── schemas/                        # Validation schemas
│   ├── analysis_passport.py        # Passport schema validator
│   └── common.py                   # Shared utilities
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md             # THIS FILE
│   ├── TZ_P6_0_SKU_ROUTING.md     # P6.0 technical specification
│   └── (audit reports)
├── _archive/                       # Deprecated code
├── _freeze_legacy/                 # Frozen legacy versions
├── pass_tomd.py                    # PRODUCTION — Markdown generator
├── gemini_image_generator.py       # PRODUCTION — RPA Selenium script
├── image_postprocessor.py          # PRODUCTION — Post-processor (1024x1024 normalizer)
├── verification_agent.py           # PRODUCTION — Verifier (v2.3)
├── render_qa.py                    # PRODUCTION — OCR QA diagnostic (P8.0)
├── .env                            # Environment variables
└── .gitignore
```

---

## 5. Agent Responsibilities (Strict Boundaries)

| Agent | File | Responsibility | Forbidden |
|---|---|---|---|
| Analyzer | `analyze-pharma.md` workflow | Image → JSON passport v2.1 | Modifying CV data |
| Router | `agent_1_router()` in pass_tomd.py | JSON → Template selection | Business logic |
| Verifier | `verification_agent.py` | JSON → Confidence score + warnings | Modifying data |
| Architect | `agent_3_passport_architect()` | JSON + Template → Markdown | Routing decisions |
| Renderer | `gemini_image_generator.py` | Markdown → PNG via Gemini | Data transformation |
| Reviewer | `project_reviewer.md` workflow | Full pipeline QA report | Auto-fixing issues |

---

## 6. Schema Versions

| Version | Status | Location |
|---|---|---|
| v2.1 | **PRODUCTION** (current) | `pipeline/passports/*.json`, `analyze-pharma.md` |
| v3.0 | **ROADMAP** (not deployed) | `protocol.md` (Section 2) |

v3.0 introduces: `cv`, `kb`, `llm`, `validation` nested blocks, normalized bbox coordinates, per-element confidence scores.

---

## 7. Key Metrics (post-P6.0)

| Metric | Value |
|---|---|
| Total SKUs | 389 |
| Template T1 (pills/standard) | 334 |
| Template T3 (sachets/tubes) | 22 |
| Template T_BOTTLE_BOX (vertical) | 33 |
| Conversion errors | 0 |
| Production confidence threshold | ≥ 0.75 |

---

## 8. Running the Pipeline

The Pipeline now runs through the unified entry point `main.py` (see the
project [README](../README.md) for full usage). The internal Stage logic
documented above is unchanged.

```bash
# Whole catalogue, all three Stages (resume-safe)
python main.py --full --resume

# Individual Stages
python main.py --passports-only            # Stage 1: JSON -> Markdown
python main.py --render-only               # Stage 2: Markdown -> raw PNG (Chrome + Gemini)
python main.py --process-images-only       # Stage 3: raw PNG -> final WEBP (output/)
```

> The legacy single-script commands still work via back-compat shims
> (`python pass_tomd.py`, `python gemini_image_generator.py`,
> `python webp_converter.py`), but `main.py` is the canonical entry point.
> Note: the canonical final Stage writes WEBP to `output/` (via
> `src/image_processor.py`); `scripts/image_postprocessor.py` is a non-canonical
> alternative.

---

## 9. Known Issues & Technical Debt

| Issue | Severity | Status |
|---|---|---|
| `schemas/analysis_passport.py` is a stub (477 bytes), not integrated | Low | Backlog |
| `pharma_pkg/package_mapping.yaml` (351 bytes) superseded by Python code | Low | Backlog |
| `protocol.md` v3.0 schema is roadmap, not implemented | Low | Roadmap |
| `_freeze_legacy/` contains 4 legacy subdirs never referenced | Info | Archive |

---

## 10. Changelog

| Date | Version | Change |
|---|---|---|
| 2026-06-06 | P8.1 | Cleaned up root directory: archived 10 obsolete utility scripts and 1 test file; archived historical renders and reset render_output. |
| 2026-06-04 | v2.3 | verification_agent CHECK 10 vertical containers routing mismatch fix |
| 2026-06-04 | P8.0 | Restored image_postprocessor.py (CRIT-1); archived stale pre-P6 docs (CRIT-2); fixed CHECK 10 false-negative (WARN-1); added render_qa.py OCR QA (WARN-2); fixed detect_material_override() pkg_type gate (INFO-1) |
| 2026-06-04 | P7.0 | Full architectural audit, verification_agent v2.3, docs/ARCHITECTURE.md canonical doc created |
| 2026-06-04 | P6.0 | SKU.csv-driven routing, T_BOTTLE_BOX template, resolve_unit_label(), conditional purge |
| 2026-06-04 | v2.2 | verification_agent extended (checks 9-12), threshold 0.75, VerificationResult extended |
| 2026-06-04 | — | Project cleanup: 48 logs archived, dead scripts removed, art-director.md archived |
| 2026-05-30 | P5.x | Initial RPA pipeline, Selenium + Gemini integration |
