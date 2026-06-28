# PHARMAGEN PRO — ARCHITECTURE SNAPSHOT
> **Generated:** 2026-06-07 03:10:31 | **Introspection Agent:** P10.0 Snapshot Engine

---

## 1. Pipeline Flow

```
INPUT (389 source JPG images)
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 0: ANALYSIS (Manual / Workflow)              │
│  Workflow: /analyze-pharma                          │
│  Input:    input/{sku_id}.jpg + SSOT/master.json    │
│  Output:   pipeline/passports/{sku_id}.json (v2.1)  │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 1: VERIFICATION (Deterministic QA)           │
│  Script:   verification_agent.py (v2.3)             │
│  Checks:   12 checks | Threshold: confidence ≥ 0.75  │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 2: PASSPORT GENERATION (Production Core)     │
│  Script:   pass_tomd.py                             │
│  Input:    pipeline/passports/*.json (389 files)    │
│  Output:   pipeline/passports.markdown/*.md         │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 3: IMAGE GENERATION (RPA Automation)         │
│  Script:   gemini_image_generator.py                │
│  Output:   render_output/raw/{sku_id}.png           │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 4: POST-PROCESSING (Active Production)       │
│  Script:   image_postprocessor.py                   │
│  Output:   render_output/processed/{sku_id}.png     │
└─────────────────────────────────────────────────────┘
       │
       ▼
OUTPUT (389 PNG renders, 1024×1024px, normalized)
```

---

## 2. Active Code Modules

| Module / File | Size (Bytes) | Description | Functions | Classes |
|---|---|---|---|---|
| [`gemini_image_generator.py`](file:///c:/pharma_v2/gemini_image_generator.py) | 75,884 | ╔══════════════════════════════════════════════════════════════════════════════╗ | 23 | 0 |
| [`image_postprocessor.py`](file:///c:/pharma_v2/image_postprocessor.py) | 4,269 | PHARMAGEN PRO: Image Post-Processor | 2 | 0 |
| [`pass_tomd.py`](file:///c:/pharma_v2/pass_tomd.py) | 69,129 |  | 19 | 0 |
| [`render_qa.py`](file:///c:/pharma_v2/render_qa.py) | 16,993 | PHARMAGEN PRO — Render QA (OCR Post-Render Quality Assurance) | 8 | 0 |
| [`verification_agent.py`](file:///c:/pharma_v2/verification_agent.py) | 15,355 | AGENT 2: VERIFICATION AGENT | 6 | 1 |
| [`pharma_pkg/__init__.py`](file:///c:/pharma_v2/pharma_pkg/__init__.py) | 25 |  | 0 | 0 |
| [`pharma_pkg/dimension_resolver.py`](file:///c:/pharma_v2/pharma_pkg/dimension_resolver.py) | 5,279 |  | 4 | 0 |
| [`pharma_pkg/geometry_mapping.py`](file:///c:/pharma_v2/pharma_pkg/geometry_mapping.py) | 5,771 | PHARMAGEN PRO: Geometry Mapping & Taxonomy Bridge | 1 | 1 |
| [`pharma_pkg/primary_classifier.py`](file:///c:/pharma_v2/pharma_pkg/primary_classifier.py) | 998 |  | 0 | 2 |
| [`pharma_pkg/secondary_templates.py`](file:///c:/pharma_v2/pharma_pkg/secondary_templates.py) | 315 |  | 0 | 1 |
| [`schemas/analysis_passport.py`](file:///c:/pharma_v2/schemas/analysis_passport.py) | 477 |  | 0 | 2 |
| [`schemas/common.py`](file:///c:/pharma_v2/schemas/common.py) | 3,404 |  | 0 | 7 |

---

## 3. Function & Class Declarations
### File: `gemini_image_generator.py`
> ╔══════════════════════════════════════════════════════════════════════════════╗

#### Functions:
- ` def log_failure(filename: str, stage: str, error: str, recovery_attempted: str, result: str) `
  * Append-only deterministic failure log.
- ` def create_driver() -> webdriver.Chrome `
  * Создаёт и возвращает Chrome WebDriver в headless-режиме
- ` def find_chat_input(driver: webdriver.Chrome) -> object `
  * Ищет поле ввода текста в чате Gemini.
- ` def send_message(driver: webdriver.Chrome, text: str) -> None `
  * Отправляет текстовое сообщение в чат Gemini.
- ` def wait_for_ready_response(driver: webdriver.Chrome) -> bool `
  * Ждёт ответ 'READY' от Gemini после отправки системного промпта.
- ` def clean_old_chats(driver: webdriver.Chrome, keep_last: int=2, force: bool=False) `
  * Cleans up old chats in the Gemini sidebar to avoid UI lag.
- ` def get_timeout_stems_from_log() -> list[str] `
  * Parses failures.log and extracts stems of passports that failed with wait_for_image_generation (timeout).
- ` def print_estimate() `
  * Dry-run output estimating remaining SKUs and execution ETA.
- ` def prime_gemini(driver: webdriver.Chrome) -> None `
  * Role Priming: загружает страницу и отправляет системный промпт.
- ` def get_current_files_in_downloads() -> set `
  * Возвращает множество полных путей к файлам в папке Downloads,
- ` def wait_for_new_download(files_before: set, timeout: int=DOWNLOAD_TIMEOUT) -> str | None `
  * Мониторит папку Downloads и ждёт появления нового полностью
- ` def find_download_button(driver: webdriver.Chrome) -> object | None `
  * Ищет кнопку скачивания изображения в интерфейсе Gemini.
- ` def get_all_blob_images(driver: webdriver.Chrome) -> list `
  * Returns all generated image elements with a blob URL.
- ` def wait_for_chat_idle(driver: webdriver.Chrome, timeout: int=90) -> bool `
  * Waits for the Gemini chat to become idle (no longer generating, input ready).
- ` def wait_for_image_generation(driver: webdriver.Chrome, responses_before: int, timeout: int=IMAGE_GENERATION_TIMEOUT) -> bool `
  * Ждёт генерации нового изображения в чате Gemini.
- ` def save_raw_image(image_bytes: bytes, target_path: str) -> str | None `
  * Сохраняет исходные байты изображения без изменений.
- ` def download_blob_image(driver: webdriver.Chrome, passport_stem: str) -> str | None `
  * Сохраняет сгенерированное изображение через canvas.toDataURL() в исходном формате PNG.
- ` def get_passport_files() -> list[Path] `
  * Возвращает отсортированный список .md файлов из MD_DIR.
- ` def read_passport(filepath: Path) -> str `
  * Читает содержимое .md файла и возвращает строку.
- ` def rename_and_move_image(downloaded_file: str, passport_stem: str) -> str `
  * Переименовывает скачанный файл согласно имени паспорта и
- ` def load_progress() -> set `
  * Загружает список уже обработанных паспортов из файла прогресса,
- ` def save_progress(passport_stem: str) -> None `
  * Записывает имя обработанного паспорта в файл прогресса.
- ` def main() `

### File: `image_postprocessor.py`
> PHARMAGEN PRO: Image Post-Processor

#### Functions:
- ` def process_image(input_path: Path, output_dir: Path, failed_dir: Path=DEFAULT_FAILED_DIR) -> tuple[bool, str] `
  * Process a single image:
- ` def main() `

### File: `pass_tomd.py`
#### Functions:
- ` def _load_sku_csv() -> dict `
  * Load SSOT/SKU.csv into a dict keyed by picture filename.
- ` def _load_ssot_master() -> dict `
  * Load SSOT/master.json. Returns empty dict if not found.
- ` def _load_design_specs() -> dict `
  * Load master_pharma_design_specs.json. Returns empty dict if not found.
- ` def hex_to_rgb(hex_color: str) -> tuple[int, int, int] | None `
- ` def relative_luminance(rgb: tuple[int, int, int]) -> float `
- ` def contrast_ratio(hex1: str, hex2: str) -> float `
  * WCAG contrast ratio between two hex colors. Range: 1.0–21.0.
- ` def hex_to_name_hint(hex_color: str) -> str `
- ` def is_liquid_or_device(product_name: str, geom: str) -> bool `
- ` def agent_1_router(data: dict) -> tuple[str, bool] `
  * Determines template (T1, T2, T3, T_BOTTLE_BOX) and whether bottle override is active.
- ` def get_primary_package(data: dict) -> PrimaryPackage `
  * Gets or estimates the PrimaryPackage from passport JSON.
- ` def purge_forms(text: str) -> str `
  * Remove dosage-form suffixes, leaving only the numeric portion.
- ` def resolve_unit_label(sku_id: str, unit_count_raw: str) -> str `
  * Returns the correctly formatted quantity label for the front panel.
- ` def is_vertical_container(package_type: str, primary_geometry: str, geom_json: str) -> bool `
  * Returns True if the primary container is vertical (tall and narrow),
- ` def detect_sub_brand(product_name: str) -> str | None `
- ` def detect_material_override(product_name: str, geom: str, pkg_type: str='') -> str | None `
  * Return a material safety spec string if the product requires light-protective packaging.
- ` def is_rx_product(product_name: str, internal_type: str) -> bool `
- ` def sanitize_text(text) `
- ` def agent_3_passport_architect(data: dict, template_id: str, is_override: bool, secondary: SecondaryPackageTemplate, verify_result: dict) -> str `
- ` def main() `

### File: `render_qa.py`
> PHARMAGEN PRO — Render QA (OCR Post-Render Quality Assurance)

#### Functions:
- ` def extract_text(image_path: Path) -> tuple[bool, str] `
  * Run OCR on a single image.
- ` def load_passport(sku_stem: str, passports_dir: Path) -> dict | None `
  * Load the JSON passport for a given SKU stem.
- ` def extract_numeric(s: str) -> str `
  * Extract the first numeric value (including decimals) from a string.
- ` def check_image(image_path: Path, passport: dict) -> dict `
  * Run OCR and perform QA checks against passport data.
- ` def bool_icon(value) -> str `
  * Convert bool/None to a readable icon for Markdown.
- ` def dup_icon(value) -> str `
  * Convert brand_duplicated bool/None to a readable icon for Markdown. True means FAIL (DUPLICATE).
- ` def write_report(results: list[dict], report_path: Path) `
  * Write a Markdown QA report.
- ` def main() `

### File: `verification_agent.py`
> AGENT 2: VERIFICATION AGENT

#### class `VerificationResult`
- *Fields:* `data: dict, confidence: float, warnings: list[str], verified: bool, sku_registry_match: bool, template_validated: bool, checks_passed: int, checks_total: int`

#### Functions:
- ` def _load_ssot() -> dict `
- ` def _load_sku_csv() -> dict `
  * Load SSOT/SKU.csv keyed by picture filename.
- ` def _hex_to_rgb(hex_color: str) -> tuple[int, int, int] | None `
  * Convert #RRGGBB or RRGGBB to (R, G, B) tuple. Returns None on failure.
- ` def _relative_luminance(rgb: tuple[int, int, int]) -> float `
  * WCAG relative luminance formula.
- ` def contrast_ratio(hex1: str, hex2: str) -> float `
  * WCAG contrast ratio between two hex colors.
- ` def agent_2_verifier(data: dict) -> VerificationResult `
  * Deterministic heuristic verifier for passport v2.1 data.

### File: `pharma_pkg/__init__.py`
*No class or function declarations found.*

### File: `pharma_pkg/dimension_resolver.py`
#### Functions:
- ` def load_mapping() -> dict `
- ` def resolve_secondary(primary: PrimaryPackage) -> SecondaryPackageTemplate `
- ` def validate_fit(primary: PrimaryPackage, secondary: SecondaryPackageTemplate) -> None `
- ` def estimate_primary_from_secondary(package_type: PrimaryPackageType, sec_w: float, sec_h: float, sec_d: float) -> PrimaryPackage `
  * Estimates primary package dimensions by reversing the secondary packaging dimensions logic.

### File: `pharma_pkg/geometry_mapping.py`
> PHARMAGEN PRO: Geometry Mapping & Taxonomy Bridge

#### class `RouteStatus`
- *Fields:* `PRODUCTION, PLACEHOLDER_ROUTE`

#### Functions:
- ` def map_geometry_to_family(geom_str: str, product_name: str, package_type: str='') -> PackagingFamily `
  * Deterministic translation from raw packaging geometry strings, product names, and package types

### File: `pharma_pkg/primary_classifier.py`
#### class `PrimaryPackageType`
- *Fields:* `BLISTER, SYRINGE, BOTTLE`

#### class `PrimaryPackage`
- *Fields:* `type: PrimaryPackageType, geometry: str, width_mm: float, height_mm: float, depth_mm: float`
  * ` def __post_init__(self) ` — *No docstring*

### File: `pharma_pkg/secondary_templates.py`
#### class `SecondaryPackageTemplate`
- *Fields:* `name: str, box_width_mm: float, box_height_mm: float, box_depth_mm: float, render_shape: str`

### File: `schemas/analysis_passport.py`
#### class `ObservedZone`
- *Fields:* `raw_text: Optional[str], bbox: UVBox, ocr_confidence: float, visual_score: float`

#### class `AnalysisPassport`
- *Fields:* `image_path: str, detected_family: PackagingFamily, zones: Dict[str, ObservedZone], palette: ObservedPalette`

### File: `schemas/common.py`
#### class `UVBox`
- *Docstring:* Нормализованные координаты UV [0, 1]. Для CV-слоя.
- *Fields:* `y1: float, x1: float, y2: float, x2: float`
  * ` def validate_geometry(self) -> 'UVBox' ` — *No docstring*

#### class `PackagingFamily`
- *Fields:* `BOX_VERTICAL_STANDARD, BOX_VERTICAL_SLIM, BOX_HORIZONTAL_FLAT, BOX_SQUARE, BOTTLE_PLASTIC_ROUND, BOTTLE_PLASTIC_TALL, BOTTLE_GLASS_ROUND, VIAL_GLASS_SMALL, TUBE_STANDARD, SACHET_FLAT, BLISTER_CARD, FOIL_STRIP, JAR_WIDE, BOX_MULTIPACK`

#### class `TypographySpec`
- *Fields:* `font_family: AllowedFonts, font_weight: int, case: Literal['uppercase', 'lowercase', 'titlecase', 'original'], tracking: float, max_font_scale: float, min_font_scale: float, line_clamp: int, allow_multiline: bool`

#### class `ObservedPalette`
- *Fields:* `dominant_colors: List[str], detected_background: Optional[str], color_confidence: float`

#### class `RenderPalette`
- *Fields:* `primary_bg: str, text_primary: str, accent_color: Optional[str]`

#### class `SurfaceFinishSpec`
- *Fields:* `lamination: Literal['matte', 'glossy'], spot_uv: bool, foil: bool, embossing: bool`

#### class `NormalizedBox`
- *Fields:* `x: float, y: float, width: float, height: float, anchor: Literal['top_left', 'center']`

---

## 4. Routing System (pass_tomd.py)

**Available Templates (TEMPLATE_MAP):**
- `T1`
- `T1_SMALL`
- `T1_LARGE`
- `T2`
- `T3`
- `T_BOTTLE_BOX`
- `T_MULTIPACK`
- `T_VERT_VIAL`
- `T_VERT_DROPPER`
- `T_VERT_INHALER`

**Router Docstring (agent_1_router):**
> Determines template (T1, T2, T3, T_BOTTLE_BOX) and whether bottle override is active.
    Uses geometry_mapping.py to determine routing and placeholder policy.
    Also checks SKU_REGISTRY for vertical container types (bottles, vials, inhalers, pens).

**Actual Template Distribution (389 Passports):**

| Template | Assigned SKU Count | Percentage |
|---|---|---|
| `T1` | 282 | 72.5% |
| `T1_LARGE` | 6 | 1.5% |
| `T1_SMALL` | 35 | 9.0% |
| `T3` | 21 | 5.4% |
| `T_BOTTLE_BOX` | 22 | 5.7% |
| `T_MULTIPACK` | 5 | 1.3% |
| `T_VERT_DROPPER` | 4 | 1.0% |
| `T_VERT_INHALER` | 4 | 1.0% |
| `T_VERT_VIAL` | 10 | 2.6% |

---

## 5. Verification Rules (verification_agent.py)

* **Production Confidence Threshold:** ` 0.75 `

| Check ID | Heuristic Rule | Weight / Penalty |
|---|---|---|
| CHECK 1 | active_ingredient == product_name | **-0.15** |
| CHECK 2 | active_ingredient empty | **-0.15** |
| CHECK 3 | primary_color == background_white | **-0.3** |
| CHECK 4 | dosage no numeric value | **-0.2** |
| CHECK 5 | unit_count empty | **-0.1** |
| CHECK 6 | geometry ↔ template consistency | **-0.2** |
| CHECK 7 | product_name empty | **-0.25** |
| CHECK 8 | SSOT master.json color cross-validation | **-0.1** |
| CHECK 9 | SKU.csv package_type↔unit_count label | **-0.15** |
| CHECK 10 | vertical container template validation | **-0.15** |
| CHECK 11 | accent_hex contrast ratio vs white | **-0.1** |
| CHECK 12 | SKU.csv ↔ JSON record existence | **-0.1** |

---

## 6. SSOT Databases & Design Specs

### SSOT/SKU.csv Statistics
* **Total Rows:** 389
* **Unique Primary Geometries:**
  - `Aluminum`
  - `Autoinjector Pen (COP)`
  - `Blister (Alu-Alu)`
  - `Blister (PVC/Aluminium)`
  - `Bottle (HDPE)`
  - `Glass Type I`
  - `Inhaler (HFA/Generic)`
  - `Sachet (Foil)`
  - `Tube (Aluminum)`

**Distribution of package_type:**

| package_type | Count |
|---|---|
| `bottle` | 4 |
| `box` | 8 |
| `inhaler` | 4 |
| `multipack` | 5 |
| `pen` | 5 |
| `pills` | 332 |
| `sachets` | 6 |
| `tube` | 15 |
| `vials` | 10 |

### Sub-Brand Visual Rules (master_pharma_design_specs.json)

| Sub-Brand | Finish Override | Triggers | Surface Treatment |
|---|---|---|---|
| `black_edition` | `matte_luxury_soft_touch` | black | Soft-touch matte coating with Spot UV gloss on logo and brand name zone |
| `gold_edition` | `metallic_premium_gloss` | gold | High-gloss metallic gold base with embossed brand name in relief |
| `professional_grade` | `clinical_precision_matte` | professional | Matte base with structured data grid layout, minimal decorative elements |
| `super_active` | `high_energy_gloss` | super active, super-active | High-gloss finish with dynamic diagonal graphic element suggesting speed/absorption |
| `oral_jelly` | `` | oral jelly, oral-jelly | Flexible foil/laminate sachet, multi-color flavor stripe coding |
| `strips` | `` | strips, strip | Slim card format, minimalist layout, premium matte or soft-touch laminate |
| `soft_tabs` | `pastel_soft_matte` | soft tabs, soft-tabs | Soft pastel color palette, rounded pill motif as graphic element on packaging |
| `forte` | `` | forte |  |
| `plus_combination` | `` | plus, dxt plus, fxt plus |  |
| `super_kamagra` | `` | super kamagra |  |
| `super_p_force` | `` | super p force, super p-force |  |
| `original_edition` | `` | original |  |

### Photosensitive Compounds & Container Overrides

| Compound Key | Required Container | Material | Triggers |
|---|---|---|---|
| `nitroglycerin_class` | `VIAL` | `amber_glass_type_I` | nitroglycerin, nitro, glyceryl trinitrate |
| `sodium_nitroprusside_class` | `VIAL` | `amber_glass_type_I_opaque_overwrap` | nitroprusside, sodium nitroprusside, nipride |
| `epinephrine_class` | `VIAL` | `amber_glass_type_I` | epinephrine, adrenaline, adrenalin, epipen |
| `injectable_hormones` | `VIAL` | `amber_glass_type_I` | testosterone, estradiol, progesterone, hcg, hgh... |
| `ophthalmic_drops` | `DROPPER` | `opaque_ldpe_white_or_amber_hdpe` | eye drop, ophthalmic, ocular, bimatoprost, latanoprost... |
| `albuterol_inhalers` | `INHALER` | `opaque_plastic_inhaler_housing` | albuterol, salbutamol, ventolin, inhaler, turbuhaler... |
| `ergotamine_class` | `BLISTER` | `alu_alu_cold_form` | ergotamine, ergot, cafergot |
| `light_sensitive_antibiotics` | `BOTTLE` | `amber_hdpe_or_glass_type_II` | doxycycline, ciprofloxacin solution, levofloxacin solution, amphotericin |
| `high_sensitivity_standard` | `VIAL` | `amber_glass_type_I_carton` | furosemide injection, sodium nitroprusside, dacarbazine, chlorpromazine |
| `general_light_sensitive` | `BOTTLE` | `dynamic_amber_glass_or_hdpe` | injection, injectable, hormone, hormonal, insulin... |

---

## 7. Current Render Output State

| Output Directory | Image Count | Status |
|---|---|---|
| `render_output/raw/` | 0 | Raw generator output |
| `render_output/processed/` | 0 | Post-processed 1024x1024 RGB normalizations |
| `render_output/failed/` | 0 | Screenshot logs on Selenium exception (current files in failed/ dir) |

* **Progress Count (done SKUs):** `158` / 389
* **Coverage:** `0` / 389 unique SKU (0.0%)
  - **Missing SKU Stems:** `1-min`, `10-min`, `100-min`, `101-min`, `102-min`, `103-min`, `104-min`, `105-min`, `106-min`, `107-min`, `108-min`, `109-min`, `11-min`, `110-min`, `111-min`, `112-min`, `113-min`, `114-min`, `115-min`, `116-min`, `117-min`, `118-min`, `119-min`, `12-min`, `120-min`, `121-min`, `122-min`, `124-min`, `125-min`, `126-min`, `127-min`, `128-min`, `129-min`, `13-min`, `130-min`, `131-min`, `132-min`, `133-min`, `134-min`, `135-min`, `136-min`, `138-min`, `139-min`, `14-min`, `141-min`, `143-min`, `144-min`, `145-min`, `146-min`, `147-min`, `148-min`, `149-min`, `15-min`, `150-min`, `151-min`, `152-min`, `155-min`, `156-min`, `157-min`, `158-min`, `159-min`, `16-min`, `160-min`, `161-min`, `162-min`, `164-min`, `165-min`, `166-min`, `17-min`, `170-min`, `171-min`, `172-min`, `173-min`, `175-min`, `176-min`, `177-min`, `178-min`, `179-min`, `18-min`, `180-min`, `181-min`, `183-min`, `184-min`, `185-min`, `186-min`, `187-min`, `188-min`, `189-min`, `19-min`, `190-min`, `191-min`, `192-min`, `194-min`, `195-min`, `196-min`, `197-min`, `198-min`, `199-min`, `2-min`, `20-min`, `200-min`, `201-min`, `202-min`, `203-min`, `204-min`, `205-min`, `206-min`, `207-min`, `208-min`, `209-min`, `21-min`, `210-min`, `211-min`, `212-min`, `213-min`, `214-min`, `215-min`, `216-min`, `217-min`, `218-min`, `219-min`, `22-min`, `220-min`, `221-min`, `222-min`, `223-min`, `224-min`, `225-min`, `226-min`, `227-min`, `228-min`, `229-min`, `23-min`, `230-min`, `231-min`, `232-min`, `233-min`, `234-min`, `235-min`, `237-min`, `238-min`, `239-min`, `24-min`, `240-min`, `241-min`, `242-min`, `243-min`, `244-min`, `245-min`, `246-min`, `247-min`, `248-min`, `249-min`, `25-min`, `250-min`, `251-min`, `252-min`, `253-min`, `254-min`, `255-min`, `256-min`, `257-min`, `258-min`, `259-min`, `26-min`, `260-min`, `261-min`, `262-min`, `263-min`, `265-min`, `266-min`, `267-min`, `268-min`, `269-min`, `27-min`, `270-min`, `271-min`, `272-min`, `275-min`, `277-min`, `278-min`, `279-min`, `28-min`, `281-min`, `282-min`, `283-min`, `284-min`, `285-min`, `286-min`, `287-min`, `288-min`, `29-min`, `290-min`, `291-min`, `293-min`, `295-min`, `296-min`, `297-min`, `298-min`, `299-min`, `3-min`, `30-min`, `300-min`, `301-min`, `302-min`, `303-min`, `304-min`, `305-min`, `307-min`, `308-min`, `309-min`, `31-min`, `310-min`, `311-min`, `312-min`, `313-min`, `314-min`, `315-min`, `316-min`, `317-min`, `318-min`, `319-min`, `320-min`, `321-min`, `322-min`, `323-min`, `324-min`, `325-min`, `326-min`, `327-min`, `328-min`, `329-min`, `330-min`, `331-min`, `332-min`, `333-min`, `334-min`, `335-min`, `336-min`, `337-min`, `34-min`, `340-min`, `341-min`, `344-min`, `345-min`, `346-min`, `347-min`, `348-min`, `349-min`, `35-min`, `350-min`, `351-min`, `352-min`, `353-min`, `354-min`, `355-min`, `356-min`, `357-min`, `359-min`, `36-min`, `360-min`, `362-min`, `363-min`, `364-min`, `365-min`, `366-min`, `367-min`, `369-min`, `37-min`, `370-min`, `371-min`, `372-min`, `373-min`, `374-min`, `375-min`, `376-min`, `377-min`, `378-min`, `379-min`, `38-min`, `380-min`, `381-min`, `382-min`, `383-min`, `384-min`, `385-min`, `386-min`, `387-min`, `388-min`, `390-min`, `391-min`, `392-min`, `393-min`, `395-min`, `396-min`, `398-min`, `399-min`, `4-min`, `40-min`, `400-min`, `401-min`, `402-min`, `403-min`, `404-min`, `405-min`, `406-min`, `407-min`, `408-min`, `409-min`, `41-min`, `410-min`, `411-min`, `412-min`, `413-min`, `414-min`, `415-min`, `416-min`, `417-min`, `418-min`, `419-min`, `42-min`, `420-min`, `421-min`, `422-min`, `423-min`, `424-min`, `425-min`, `426-min`, `427-min`, `428-min`, `429-min`, `43-min`, `430-min`, `431-min`, `432-min`, `433-min`, `434-min`, `44-min`, `45-min`, `46-min`, `47-min`, `48-min`, `49-min`, `5-min`, `50-min`, `51-min`, `52-min`, `58-min`, `59-min`, `6-min`, `60-min`, `61-min`, `62-min`, `63-min`, `64-min`, `65-min`, `66-min`, `67-min`, `70-min`, `71-min`, `72-min`, `73-min`, `74-min`, `75-min`, `76-min`, `77-min`, `78-min`, `79-min`, `8-min`, `80-min`, `81-min`, `82-min`, `83-min`, `85-min`, `86-min`, `87-min`, `88-min`, `89-min`, `9-min`, `90-min`, `91-min`, `92-min`, `93-min`, `94-min`, `95-min`, `96-min`, `97-min`, `98-min`, `99-min`

### Failure Breakdown (from failures.log)
> *Note: failure_breakdown is a historical/cumulative log of all generation attempts (including recovered/retried ones).* 

| Stage of Failure | Count |
|---|---|
| *No failures logged* | 0 |

### Diagnostic Alerts & Quality Issues

* **Empty Active Ingredients Count:** `0`
* **Low Confidence Passports (< 0.75):** `0`

---

## 8. Runtime Constants (gemini_image_generator.py)

| Constant | Value | Description |
|---|---|---|
| `BATCH_SIZE` | `1` | Static AST value |
| `BROWSER_PROFILE_DIR` | `'LOCAL_HOME\\.gemini\\antigravity-browser-profile\\Profile 1'` | Static AST value |
| `BROWSER_PROFILE_NAME` | `'Profile 1'` | Static AST value |
| `CHUNK` | `100` | Static AST value |
| `DOWNLOADS_DIR` | `'LOCAL_HOME\\Downloads'` | Static AST value |
| `DOWNLOAD_TIMEOUT` | `60` | Static AST value |
| `FAILED_DIR` | `'c:\\pharma_v2\\render_output\\failed'` | Static AST value |
| `GEMINI_URL` | `'https://gemini.google.com/app'` | Static AST value |
| `IMAGE_GENERATION_TIMEOUT` | `180` | Static AST value |
| `LOG_FILE` | `os.path.join(os.path.dirname(os.path.abspath(__file__)), f"gemini_rpa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")` | Static AST value |
| `MD_DIR` | `'c:\\pharma_v2\\pipeline\\passports.markdown'` | Static AST value |
| `POST_CLICK_DELAY` | `2` | Static AST value |
| `PROGRESS_FILE` | `os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gemini_rpa_progress_v23.txt')` | Static AST value |
| `RAW_DIR` | `'c:\\pharma_v2\\render_output\\raw'` | Static AST value |
| `READY_TIMEOUT` | `30` | Static AST value |
| `SYSTEM_PROMPT` | `'You are a silent image generation engine. Rules: Accept incoming text prompts and generate images immediately. No commentary, no questions, no explanations before or after generation. Do not modify, interpret, or summarize the prompt. Do not add elements not specified in the prompt. If the prompt is accepted, generate the image silently. Treat every incoming message as a direct image generation instruction. Confirm readiness with one word: READY'` | Static AST value |

---

## 9. Known Technical Debt & Backlog

| Technical Debt Issue | Severity | Target Remediation |
|---|---|---|
| `schemas/analysis_passport.py` is a stub (477 bytes), not integrated | Low | Backlog |
| `pharma_pkg/package_mapping.yaml` (351 bytes) superseded by Python code | Low | Backlog |
| `protocol.md` v3.0 schema is roadmap, not implemented | Low | Roadmap |
| `_freeze_legacy/` contains 4 legacy subdirs never referenced | Info | Archive |

---
*Architecture Snapshot generated automatically by generate_architecture_snapshot.py*