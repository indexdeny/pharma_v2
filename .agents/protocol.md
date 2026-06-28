# PHARMAGEN PRO: PACKAGING RECONSTRUCTION PROTOCOL v3.0

> **PRODUCTION STATUS (2026-06):**
> All 389 production passports use **schema v2.1** (flat structure: `brand_name`, `label_content`, `branding`, etc.).
> The v3.0 schema below is the **target architecture roadmap** for future migration.
> Active production pipeline: `pass_tomd.py` → `pipeline/passports.markdown/` → `gemini_image_generator.py`.
> **P6.0 Update (2026-06-04):** Template routing now driven by `SSOT/SKU.csv` `package_type` field.
> New template added: `T_BOTTLE_BOX` for vertical containers (bottles, vials, inhalers, pens).

## 1. CORE PHILOSOPHY
The objective is NOT drug recognition, but **Packaging Design Reconstruction**.
The system extracts the design DNA to enable high-fidelity 3D reconstruction and packshot generation.

### SOURCE PRIORITY (RECONSTRUCTION MODE):
1. **PRIMARY (Hard CV)**: Geometry, Proportions, Layout Zones, Palette, Composition.
2. **SECONDARY (Soft Logic)**: Semantic OCR, KB Hints, Branding, Material.

## 2. PASSPORT SCHEMA (v3.0 — ROADMAP)
All analysis outputs must strictly follow this JSON structure. No deviations allowed.

```json
{
  "passport_version": "3.0",

  "meta": {
    "source_file": "string",
    "image_size": [width, height],
    "reconstruction_type": "template_reconstruction"
  },

  "cv": {
    "geometry": {
      "package_type": "box_vertical_standard | box_vertical_slim | box_horizontal_flat | box_square | bottle_plastic_round | bottle_plastic_tall | bottle_glass_round | vial_glass_small | tube_standard | sachet_flat | blister_card | foil_strip | jar_wide",
      "orientation": "horizontal|vertical|square",
      "aspect_ratio": float,
      "silhouette_confidence": float,
      "estimated_dimensions": [w, h, d]
    },

    "spatial": {
      "object_detected": boolean,
      "bbox": {
        "format": "normalized",
        "value": [ymin, xmin, ymax, xmax]
      },
      "confidence": float
    },

    "color_palette": {
      "primary": { "hex": "string", "confidence": float },
      "secondary": [ { "hex": "string", "confidence": float } ],
      "design_colors": [ { "hex": "string", "role": "accent|background|text" } ]
    },

    "ocr": {
      "raw_text": "string",
      "semantic_hints": ["string"],
      "blocks": [ { "text": "string", "bbox": [ymin, xmin, ymax, xmax], "confidence": float } ]
    },

    "layout": {
      "zones": [
        { "type": "title|dosage|brand|logo|warnings|legal|graphics", "bbox": [ymin, xmin, ymax, xmax], "hierarchy": 1-5 }
      ],
      "composition": "string"
    }
  },

  "kb": {
    "verified_name": "string",
    "design_guideline": "string"
  },

  "llm": {
    "design_reconstruction": {
      "style": "string",
      "visual_hierarchy": "string",
      "material_properties": {
        "material": "string",
        "finish": "matte|glossy|satin",
        "opacity": float
      }
    },

    "product_mapping": {
      "category": "string",
      "template_id": "box_vertical_standard | box_vertical_slim | ... (see cv.geometry)",
      "uv_map_hints": "string"
    }
  },

  "validation": {
    "status": "pending|valid|invalid|review_needed",
    "errors": [],
    "reconstruction_confidence": float
  }
}
```

## 2. CORE RULES
1. **Coordinates**: MUST be normalized (0.0 to 1.0).
2. **Isolation**: 
    - `cv` block contains raw visual evidence. 
    - `llm` block contains interpretations. 
    - LLM MUST NOT modify `cv` data (bboxes, colors).
3. **Confidence**: Every element in `cv` and `llm` mapping must have a `confidence` score (0.0-1.0).
4. **Layout vs OCR**: OCR tracks text blocks. Layout tracks functional zones. They are separate layers.

## 3. EXECUTION PIPELINE
1. **detect_object**: Identify the main product packaging.
2. **crop_object**: Focus processing on the identified bbox.
3. **extract_evidence**: Run OCR and Color analysis on the crop.
4. **kb_lookup**: Retrieve source of truth from Master List.
5. **interpretation**: LLM reconciles CV evidence with KB data.
6. **validation**: Final check for conflicts (e.g. CV color vs KB brand colors).

## 4. SKILLS INTERFACE
- `detect_object(image_path) -> {"bbox": [y1, x1, y2, x2], "confidence": float}`
- `crop_object(image_path, bbox) -> cropped_image_path`
- `save_to_wiki(sku_id, data)`: Save the final Passport 3.0 JSON.

## 5. DATA SOURCE PRIORITY (STRICT)

Data sources must follow strict hierarchy:

1. CV layer (object detection, colors, OCR)
2. Knowledge Base (CSV / master list)
3. LLM interpretation

Rules:

* CV data is absolute and MUST NOT be modified
* KB data overrides LLM assumptions
* LLM may only interpret, never override

---

## 6. ZERO-INFERENCE RULE

If required data is missing:

* return null
* OR set validation.status = "review_needed"

Under no circumstances may the system guess or fabricate values.

---

## 7. VALIDATION LOGIC

Validation must enforce:

* CV vs LLM consistency
* KB vs LLM consistency
* required fields completeness
* confidence thresholds

If conflict detected:

* mark validation.status = "invalid"
* populate validation.errors[]

If confidence < 0.8:

* mark validation.status = "review_needed"

---

## 8. IMAGE OUTPUT CONSTRAINTS (PRODUCTION)

All generated images MUST:

* be exactly **1024×1024 pixels** (1:1 aspect ratio)
* be in **PNG** format
* maintain 1:1 square composition
* white background (#FFFFFF)

> [!NOTE]
> ~~Legacy note in older protocol drafts referenced 2048×2048 WEBP.~~
> **This is DEPRECATED.** Production render constraints in `pass_tomd.py` (`_RENDER_CONSTRAINTS`) are authoritative: 1024×1024 px, PNG, white background.

---

## 9. DETERMINISTIC EXECUTION

* Same input MUST produce identical output
* Randomness is forbidden
* Pipeline order MUST NOT change

---

## 10. STRICT JSON MODE

All outputs must:

* strictly follow Passport v2.1 schema for production
* v3.0 schema (§2 above) is roadmap — not enforced in current pipeline
* contain no extra fields
* contain no missing required fields
* contain no free-form text outside defined schema

Markdown or natural language is forbidden unless explicitly required.
