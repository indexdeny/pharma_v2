# PRODUCTION BOUNDARY SPECIFICATION

This document defines the strict boundaries of the PharmaGen PRO render factory architecture. Files are strictly categorized, and no roadmap, archive, or experimental code may contaminate the active production runtime.

---

# PRODUCTION SYSTEM

These files and directories are the **only** components allowed in the active runtime. They must remain lean, deterministic, and free of unnecessary abstractions.

- **Core Code / Executables**:
  - [pass_tomd.py](file:///c:/pharma_v2/pass_tomd.py): Markdown prompt compiler and verifier executor.
  - [gemini_image_generator.py](file:///c:/pharma_v2/gemini_image_generator.py): Selenium RPA browser render loop.
  - [image_postprocessor.py](file:///c:/pharma_v2/image_postprocessor.py): Output image processor and validator.
  - [verification_agent.py](file:///c:/pharma_v2/verification_agent.py): Rule-based verifier.
- **Packages**:
  - `pharma_pkg/`: Core geometry mappings and classifier modules.
  - `schemas/`: Common data structures. Only `PackagingFamily` is runtime-active.
  - `tests/`: Automated unit tests.
- **SSOT Configurations**:
  - `SSOT/master.json`
  - `SSOT/master_pharma_design_specs.json`

---

# ROADMAP SYSTEM

These components are target schemas, ideas, or architectural blueprints intended for future quarters. They are **forbidden** from being imported, instantiated, or referenced in the active runtime.

- **Roadmap Schemas (schemas/common.py)**:
  - `SceneArchetype`
  - `TypographySpec`
  - `RenderPalette`
  - `SurfaceFinishSpec`
  - `NormalizedBox`
- **Future Templates**:
  - T5+ multi-shot dual-render templates (primary container + secondary box in one frame). Not yet implemented.
- **Future / Roadmap-Only Rendering Clients**:
  - [imagen_renderer.py](file:///c:/pharma_v2/imagen_renderer.py): **ROADMAP_ONLY**. Batch renderer wrapper using Google GenAI SDK (requires paid Cloud project, not active in the Selenium-based production pipeline).
  - Direct API-based Gemini/Vertex render wrappers. Selenium RPA remains the sole canonical render client.

---

# ARCHIVE SYSTEM

These files are legacy, superseded, or redundant. They are separated into frozen/archive folders and **must never be restored automatically** or referenced by runtime systems.

- **Folders**:
  - `_archive/`: Contains superseded scripts, pipelines, and HTML files.
  - `_freeze_legacy/`: Old mapping logic, dead schemas, and configurations.
- **Unused root files**:
  - Archived files like `PATCH_REPORT_v2_3.md` and `pharmagen_tz_claude.html` moved to `_archive/`.

---

# EXPERIMENTAL SYSTEM

These files, configs, and notebooks are for prototyping only. They are **strictly forbidden** from the `main` or production release branches and must remain isolated.

- **Notebooks / Draft scripts**:
  - Any `.ipynb` exploratory notebooks.
  - Scratch scripts in the brain workspace or `scratch/` folders.
- **Experimental models**:
  - Custom local LLM fine-tunes or custom diffusion weights.
