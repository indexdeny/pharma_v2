import os
import json
import re
import hashlib
from pathlib import Path

import sys
sys.stdout.reconfigure(encoding="utf-8")

# Imports from packaging modules
from pharma_pkg.primary_classifier import PrimaryPackage, PrimaryPackageType
from pharma_pkg.secondary_templates import SecondaryPackageTemplate
from pharma_pkg.dimension_resolver import resolve_secondary, validate_fit, estimate_primary_from_secondary
from pharma_pkg.geometry_mapping import map_geometry_to_family, GEOMETRY_MAPPING, RouteStatus, PackagingFamily
from verification_agent import agent_2_verifier

# ================= SETTINGS =================
INPUT_DIR    = Path("pipeline/passports")
OUTPUT_DIR   = Path("pipeline/passports.markdown")
FAILURES_LOG = Path("verification_failures.log")
SSOT_MASTER  = Path("SSOT/master.json")
DESIGN_SPECS_PATH = Path("SSOT/master_pharma_design_specs.json")
SKU_CSV_PATH = Path("SSOT/SKU.csv")
# ============================================

def _load_sku_csv() -> dict:
    """
    Load SSOT/SKU.csv into a dict keyed by picture filename.
    Returns: { "1-min.jpg": {"name": "Atomoxetine (Generic)", "active_ingredient": "Atomoxetine",
                              "package_type": "pills", "primary_geometry": "Blister (PVC/Aluminium)",
                              "unit_count_standard": "30", "dosage_type": "mg"}, ... }
    """
    result = {}
    if not SKU_CSV_PATH.exists():
        return result
    import csv
    with open(SKU_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pic = row.get("picture", "").strip()
            if pic:
                result[pic] = {
                    "name":               row.get("name", "").strip(),
                    "active_ingredient":  row.get("active_ingredient", "").strip(),
                    "package_type":       row.get("package_type", "").strip().lower(),
                    "primary_geometry":   row.get("primary_geometry", "").strip(),
                    "unit_count_standard": row.get("unit_count_standard", "").strip(),
                    "minimal_dosage":     row.get("minimal_dosage", "").strip(),
                    "dosage_type":        row.get("dosage_type", "").strip(),
                }
    return result

SKU_REGISTRY = _load_sku_csv()

def _load_ssot_master() -> dict:
    """Load SSOT/master.json. Returns empty dict if not found."""
    if SSOT_MASTER.exists():
        with open(SSOT_MASTER, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _load_design_specs() -> dict:
    """Load master_pharma_design_specs.json. Returns empty dict if not found."""
    if DESIGN_SPECS_PATH.exists():
        with open(DESIGN_SPECS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

SSOT = _load_ssot_master()
SSOT_SKU_REGISTRY = SSOT.get("sku_registry", {})
DESIGN_SPECS = _load_design_specs()
_SPECS_SUB_BRANDS = DESIGN_SPECS.get("sub_brand_visual_rules", {})
_SPECS_PHOTOSENS  = DESIGN_SPECS.get("photosensitive_compounds", {})

# =============================================
# COLOR UTILITIES
# =============================================

def hex_to_rgb(hex_color: str) -> tuple[int, int, int] | None:
    h = hex_color.upper().lstrip("#")
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    if len(h) != 6:
        return None
    try:
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return None

def relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c):
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def contrast_ratio(hex1: str, hex2: str) -> float:
    """WCAG contrast ratio between two hex colors. Range: 1.0–21.0."""
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    if not rgb1 or not rgb2:
        return 21.0
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker  = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

COLOR_NAMES = {
    "#005A9C": "Medical Blue",
    "#003366": "Navy",
    "#00788C": "Teal",
    "#006A4E": "Pharma Green",
    "#5C6BC0": "Soft Indigo",
    "#00695C": "Deep Teal",
    "#8D6E63": "Warm Taupe",
    "#B71C1C": "Clinical Red",
    "#C9A227": "Muted Gold",
    "#607D8B": "Slate Blue",
    "#455A64": "Charcoal",
    "#DDA7A5": "Rose",
    "#6B2D5C": "Bordeaux",
    "#E2583E": "Poppy",
    "#4B4632": "Tapenade",
    "#0D5FB8": "North Star Cobalt",
    "#FFFFFF": "White",
    "#000000": "Black",
}

def hex_to_name_hint(hex_color: str) -> str:
    h = "#" + hex_color.upper().lstrip("#")
    if h in COLOR_NAMES:
        return COLOR_NAMES[h]
    rgb = hex_to_rgb(hex_color)
    if not rgb:
        return "Not Specified"
    r, g, b = rgb
    if r < 40  and g < 40  and b < 40:  return "Deep Matte Black"
    if r > 215 and g > 215 and b > 215: return "Clean Pharmaceutical White"
    if r > 200 and g > 200 and b < 50:  return "Premium Gold Accent"
    if r < 50  and g > 180 and b > 180: return "Teal / Cyan"
    if r > 180 and g < 50  and b < 50:  return "Clinical Red"
    if r < 60  and g < 60  and b > 150: return "Royal Blue"
    if r < 80  and g > 150 and b < 80:  return "Safety Green"
    return f"HEX: {h}"

def is_liquid_or_device(product_name: str, geom: str) -> bool:
    name_lower = product_name.lower()
    geom_upper = geom.upper()
    
    liquid_keywords = [
        "solution", "drops", "syrup", "suspension", "eye", "ophthalmic", 
        "injectable", "injection", "spray", "inhaler", "nasal", "gel", 
        "cream", "ointment", "shampoo", "lotion", "oil", "infusion", "liquid",
        "lumigan", "xalatan", "latisse"
    ]
    
    geom_keywords = [
        "SPRAY", "DROPPER", "INHALER", "VIAL", "AMPOULE", "TUBE", "PEN", "SYRINGE"
    ]
    
    if any(kw in name_lower for kw in liquid_keywords):
        return True
    if any(g in geom_upper for g in geom_keywords):
        return True
        
    return False

# =============================================
# AGENT 1: ROUTER
# =============================================

def agent_1_router(data: dict) -> tuple[str, bool]:
    """
    Determines template (T1, T2, T3, T_BOTTLE_BOX) and whether bottle override is active.
    Uses geometry_mapping.py to determine routing and placeholder policy.
    Also checks SKU_REGISTRY for vertical container types (bottles, vials, inhalers, pens).
    """
    sku_id = str(data.get("sku_id", ""))
    geom = str(data.get("packaging_geometry", "BOX")).upper().strip()
    product_name = str(data.get("product_name", ""))

    # Pull SKU.csv data for this SKU
    sku_entry = SKU_REGISTRY.get(sku_id, {})
    pkg_type = sku_entry.get("package_type", "").lower()
    primary_geom_csv = sku_entry.get("primary_geometry", "")

    # Check if this is a vertical container → vertical portrait carton
    if is_vertical_container(pkg_type, primary_geom_csv, geom):
        # Vertical containers: tall portrait carton, no bottle override
        # (we render the CARTON, not the bottle itself)
        if pkg_type in ("vials", "vial"):
            return "T_VERT_VIAL", False
        elif pkg_type in ("bottle", "bottles"):
            return "T_VERT_DROPPER", False
        elif pkg_type in ("inhaler", "inhalers"):
            return "T_VERT_INHALER", False
        return "T_BOTTLE_BOX", False

    # sachets and tubes → T3 (long horizontal carton)
    _HORIZONTAL_TYPES = {"sachets", "sachet", "tubes", "tube", "pen", "pens"}
    if pkg_type in _HORIZONTAL_TYPES:
        return "T3", False

    # Existing routing logic below (unchanged)
    family = map_geometry_to_family(geom, product_name, pkg_type)
    route = GEOMETRY_MAPPING.get(family, GEOMETRY_MAPPING[PackagingFamily.BOX_VERTICAL_STANDARD])
    template_id = route.get("template_id", "T1")
    is_override = route.get("is_bottle_override", False)

    # Route pills to T1 sub-templates based on quantity
    if template_id == "T1" and pkg_type in ("pills", "pill"):
        min_pkg = data.get("minimal_package")
        try:
            q = int(min_pkg)
        except (TypeError, ValueError):
            q = 30
        if q <= 10:
            template_id = "T1_SMALL"
        elif q > 60:
            template_id = "T1_LARGE"
        else:
            template_id = "T1"

    return template_id, is_override


# =============================================
# PRIMARY PACKAGE CLASSIFIER / EXTRACTOR
# =============================================

def get_primary_package(data: dict) -> PrimaryPackage:
    """Gets or estimates the PrimaryPackage from passport JSON."""
    pp = data.get("primary_package")
    
    # 1. Classify type
    geom_str = str(data.get("packaging_geometry", "BOX")).upper()
    product_name_lower = data.get("product_name", "").lower()
    
    is_liquid = is_liquid_or_device(data.get("product_name", ""), geom_str)
    
    if is_liquid:
        if geom_str in ("BOTTLE", "VIAL", "JAR", "AMPOULE", "SPRAY", "DROPPER", "INHALER"):
            p_type = PrimaryPackageType.BOTTLE
            p_geom = "cylindrical"
        elif geom_str in ("SYRINGE", "PEN", "TUBE", "SACHET"):
            p_type = PrimaryPackageType.SYRINGE
            p_geom = "elongated"
        else:
            p_type = PrimaryPackageType.BOTTLE
            p_geom = "cylindrical"
    else:
        # Solid oral form: MUST be Blister + Carton
        p_type = PrimaryPackageType.BLISTER
        p_geom = "flat_rectangular"

    # 2. Check if primary package dimensions are defined in JSON
    if pp and pp.get("type") and pp.get("width_mm") is not None and float(pp["width_mm"]) > 0:
        return PrimaryPackage(
            type=PrimaryPackageType(pp["type"].upper()),
            geometry=pp.get("geometry", p_geom),
            width_mm=float(pp["width_mm"]),
            height_mm=float(pp["height_mm"]),
            depth_mm=float(pp["depth_mm"])
        )

    # 3. Fallback: parse secondary packaging dimensions and reverse clearancing
    sec_packaging = data.get("secondary_packaging", {})
    dim_str = sec_packaging.get("dimensions", "") if sec_packaging else ""
    nums = [float(x) for x in re.findall(r'\d+(?:\.\d+)?', str(dim_str))]

    if len(nums) == 3:
        sec_w, sec_h, sec_d = nums
        try:
            return estimate_primary_from_secondary(p_type, sec_w, sec_h, sec_d)
        except ValueError:
            pass

    # 4. Ultimate fallback to base defaults
    if p_type == PrimaryPackageType.BLISTER:
        return PrimaryPackage(type=p_type, geometry=p_geom, width_mm=85, height_mm=55, depth_mm=8)
    elif p_type == PrimaryPackageType.SYRINGE:
        return PrimaryPackage(type=p_type, geometry=p_geom, width_mm=15, height_mm=120, depth_mm=15)
    else:
        return PrimaryPackage(type=p_type, geometry=p_geom, width_mm=35, height_mm=95, depth_mm=35)

# =============================================
# SUB-BRAND AND MATERIAL SAFETY DETECTORS
# =============================================

def purge_forms(text: str) -> str:
    """Remove dosage-form suffixes, leaving only the numeric portion."""
    if not text:
        return ""
    # Extended suffix list: EN, RU, abbreviated forms
    for token in [
        'tablets', 'tablet', 'capsules', 'capsule', 'pills', 'pill',
        'tab', 'tabs', 'caps', 'cap',
        'doses', 'dose',
        'pcs', 'шт', 'штук',
        'ml', 'мл',
        'g', 'г',
    ]:
        text = re.sub(rf'(?i)\b{re.escape(token)}\.?\b', '', text)
    return re.sub(r'\s+', ' ', text).strip()


# Mapping package_type → display label on front panel
_PACKAGE_TYPE_LABEL = {
    # Solid oral forms → normalize to "Pills"
    "pills":    "Pills",
    "pill":     "Pills",
    "packs":    "Pills",
    "pack":     "Pills",
    "boxes":    "Pills",
    "box":      "Pills",
    "strips":   "Pills",
    "strip":    "Pills",
    "units":    "Pills",
    "unit":     "Pills",
    # Non-tablet forms → own label
    "vials":    "Vials",
    "vial":     "Vial",
    "tubes":    "Tubes",
    "tube":     "Tube",
    "sachets":  "Sachets",
    "sachet":   "Sachet",
    "pens":     "Pens",
    "pen":      "Pen",
    "inhalers": "Inhalers",
    "inhaler":  "Inhaler",
    "bottles":  "Bottles",
    "bottle":   "Bottle",
    "blisters": "Blisters",
    "blister":  "Blister",
    "multipacks": "Multipacks",
    "multipack": "Multipacks",
}

def resolve_unit_label(sku_id: str, unit_count_raw: str) -> str:
    """
    Returns the correctly formatted quantity label for the front panel.

    Logic:
      1. Look up package_type in SKU_REGISTRY by sku_id
      2. Map package_type to display label
      3. Get unit_count_standard from SKU_REGISTRY (preferred) or purge_forms(unit_count_raw)
      4. Return "{count} {label}" string

    Examples:
      pills, 30   → "30 Pills"
      vials, 10   → "10 Vials"
      tubes, 1    → "1 Tube"
      sachets, 7  → "7 Sachets"
      pens, 1     → "1 Pen"
      inhalers, 1 → "1 Inhaler"
      bottles, 1  → "1 Bottle"
    """
    sku_entry = SKU_REGISTRY.get(sku_id, {})
    pkg_type = sku_entry.get("package_type", "").lower().strip()

    if pkg_type in ("multipack", "multipacks"):
        return "Assorted Pack"

    # Get count: prefer SKU.csv standard over JSON field
    count_from_csv = sku_entry.get("unit_count_standard", "").strip()
    count_from_json = purge_forms(unit_count_raw).strip()

    # Use CSV count if it's a clean digit, otherwise fall back to JSON
    if count_from_csv.isdigit():
        count = count_from_csv
    elif count_from_json.isdigit():
        count = count_from_json
    else:
        # Last resort: extract leading digit from JSON
        m = re.match(r'^(\d+)', count_from_json)
        count = m.group(1) if m else "1"

    # Resolve label from package_type
    label = _PACKAGE_TYPE_LABEL.get(pkg_type)

    if label is None:
        # Unknown package_type: fallback to Pills for safety
        label = "Pills"

    # Singular/plural handling override
    if count == "1":
        if label == "Vials": label = "Vial"
        elif label == "Sachets": label = "Sachet"
        elif label == "Bottles": label = "Bottle"
        elif label == "Tubes": label = "Tube"
        elif label == "Pens": label = "Pen"
        elif label == "Inhalers": label = "Inhaler"
        elif label == "Blisters": label = "Blister"
        elif label == "Boxes": label = "Box"
        elif label == "Strips": label = "Strip"
        elif label == "Packs": label = "Pack"
        elif label == "Units": label = "Unit"
        elif label == "Multipacks": label = "Multipack"
    else:
        if label == "Vial": label = "Vials"
        elif label == "Sachet": label = "Sachets"
        elif label == "Bottle": label = "Bottles"
        elif label == "Tube": label = "Tubes"
        elif label == "Pen": label = "Pens"
        elif label == "Inhaler": label = "Inhalers"
        elif label == "Blister": label = "Blisters"
        elif label == "Box": label = "Boxes"
        elif label == "Strip": label = "Strips"
        elif label == "Pack": label = "Packs"
        elif label == "Unit": label = "Units"
        elif label == "Multipack": label = "Multipacks"

    return f"{count} {label}"


def is_vertical_container(package_type: str, primary_geometry: str, geom_json: str) -> bool:
    """
    Returns True if the primary container is vertical (tall and narrow),
    requiring a portrait-orientation secondary carton box.

    Vertical containers: bottles, dropper bottles, eye drops, nasal sprays,
                         vials (multi-unit), inhalers
    """
    pkg = package_type.lower().strip()
    geom_csv = primary_geometry.lower().strip()
    geom_js = geom_json.upper().strip()

    VERTICAL_PACKAGE_TYPES = {"bottles", "bottle", "vials", "vial", "inhalers", "inhaler"}
    VERTICAL_CSV_GEOMETRIES = {
        "bottle (hdpe)", "bottle (amber glass)", "glass type i",
        "inhaler (hfa/generic)", "vial (glass type i)"
    }
    VERTICAL_JSON_GEOMS = {"BOTTLE", "VIAL", "AMPOULE", "DROPPER", "INHALER", "SPRAY"}

    if pkg in VERTICAL_PACKAGE_TYPES:
        return True
    if geom_csv in VERTICAL_CSV_GEOMETRIES:
        return True
    if geom_js in VERTICAL_JSON_GEOMS:
        return True
    return False

def detect_sub_brand(product_name: str) -> str | None:
    name_lower = product_name.lower()
    for rule_name, rule_data in _SPECS_SUB_BRANDS.items():
        if not isinstance(rule_data, dict):
            continue
        triggers = rule_data.get("triggers", [])
        imagen_anchor = rule_data.get("imagen_anchor")
        if triggers and imagen_anchor:
            for t in triggers:
                if re.search(rf'\b{re.escape(t)}\b', name_lower):
                    return imagen_anchor
    return None

def detect_material_override(product_name: str, geom: str, pkg_type: str = "") -> str | None:
    """
    Return a material safety spec string if the product requires light-protective packaging.

    Gate (either condition triggers the check):
    - JSON packaging_geometry is a vertical liquid container form factor, OR
    - SKU.csv pkg_type indicates a liquid container (vials / inhalers / bottle / bottles)
      This covers products rendered as secondary carton boxes (geom=BOX) that are
      actually injectables or ophthalmics — P8.0 fix for INFO-1 (15 missed SKUs).
    """
    geom_upper = geom.upper().strip()
    light_protective_geom = {"BOTTLE", "VIAL", "AMPOULE", "DROPPER", "SPRAY"}
    pkg_type_liquid = {"vials", "vial", "inhalers", "inhaler", "bottle", "bottles"}

    # Expand gate: allow check if pkg_type indicates liquid container (covers BOX secondary renders)
    if geom_upper not in light_protective_geom and pkg_type.lower() not in pkg_type_liquid:
        return None
        
    name_lower = product_name.lower()
    for comp_name, comp_data in _SPECS_PHOTOSENS.items():
        if not isinstance(comp_data, dict):
            continue
        triggers = comp_data.get("triggers", [])
        render_spec = comp_data.get("material_render_spec")
        if triggers and render_spec:
            for t in triggers:
                if re.search(rf'\b{re.escape(t)}\b', name_lower):
                    if comp_name == "general_light_sensitive":
                        if geom_upper == "AMPOULE":
                            return "amber borosilicate glass Type I ampoule, light-protective, heat-sealed"
                        elif geom_upper in ("VIAL", "DROPPER"):
                            return "amber glass vial Type I, UV-protective coating, rubber stopper"
                        else:
                            return "amber HDPE or opaque light-protective plastic bottle, child-resistant cap"
                    return render_spec
    return None

OTC_SIGNALS = [
    "vitamin", "supplement", "zinc", "magnesium", "calcium",
    "omega", "probiotic", "antacid", "laxative", "antiseptic cream",
    "multivitamin", "herbal",
    "loratadine", "cetirizine", "fexofenadine", "desloratadine",
    "ibuprofen", "paracetamol", "acetaminophen", "aspirin",
    "omeprazole", "esomeprazole",
]

def is_rx_product(product_name: str, internal_type: str) -> bool:
    name_lower = product_name.lower()
    for signal in OTC_SIGNALS:
        if signal in name_lower:
            return False
    return True

# =============================================
# VISUAL TEMPLATES (FROM test_v62)
# =============================================

_PURITY_ANCHOR = (
    "All visible surface elements are clean, intentional, and commercially realistic. "
    "Every printed value is drawn exclusively from the FRONT PANEL GRID. "
    "Typography is purposeful — no decorative filler, no metadata labels, no field names. "
    "Intentionally minimal clean pharmaceutical packaging. "
    "All visible elements are complete and final as specified above. "
    "The front face contains the brand badge as specified in the FRONT PANEL GRID. "
    "No medical crosses, molecule structures, DNA graphics, swooshes, or decorative pharmaceutical iconography allowed unless explicitly specified in the FRONT PANEL GRID. "
    "No logo, emblems, brand marks, or text is drawn on the top panel (upper part) of the packaging."
)

_RENDER_CONSTRAINTS = (
    "[ISOLATION ANCHOR]: One sealed box only. "
    "True seamless pure solid white studio background with no gradients, no horizon line, no floor textures, and no environmental ambient lighting. "
    "No loose elements, no props, no cropping of packaging edges. "
    "Soft contact shadow beneath box only. "
    "Square composition optimized for e-commerce catalog rendering. "
    "Object occupies approximately half of the frame with generous surrounding negative space. "
    "Neutral commercial product photography perspective with no wide-angle distortion. 1024×1024 px, 1:1 ratio, PNG format."
)

_ATTENTION_ANCHOR = (
    "PRIMARY RENDERING SURFACE: The front face is the sole canvas for all brand, dosage, and identity elements. "
    "All other surfaces are strictly secondary and contain only logistical data. "
    "The brand name '{brand_name}' is strictly forbidden on the side panel, barcode area, expiration blocks, or secondary positions. Front face only."
)

_TERMINOLOGY_MAP = (
    "TERMINOLOGY MAP (strictly enforced):\n"
    "- The quantity label '{unit_count}' appears exactly once on the entire package "
    "within the tight label in the bottom-right corner. "
    "It is strictly forbidden to repeat, clone, or output this quantity label anywhere else."
)

_SHARED_FORBIDDEN = """\
[RENDER CONSTRAINTS]:
- Object: secondary carton ONLY
- FORBIDDEN: loose pills, blister pack, pill bottle, HDPE jar, any primary container
- FORBIDDEN: any logo graphics, emblems, or brand marks on the top face of the packaging (top face must be completely blank clean white)
- FORBIDDEN: any badge, icon, or emblem beyond the single Brand Badge already specified in the FRONT PANEL GRID top-right corner
- FORBIDDEN: medical cross icons, DNA graphics, molecule stick-models, swooshes, stethoscopes, or figurative medical imagery anywhere on packaging
- FORBIDDEN: printing the text "Brand Logo", "Rx", "Active Ingredient", "Dosage", "Quantity", or any other field label name on the rendered surface
- FORBIDDEN: human hands, pill inserts floating outside packaging
- FORBIDDEN: accent colour stripe or band on any side panel or back panel — accent stripe is on front face only (Row 6 of FRONT PANEL GRID)
- FORBIDDEN: glossy app-icon aesthetics, neumorphism, mobile UI button styling, startup-style logo rendering on the Brand Badge
- FORBIDDEN: badge rendered as a dominant visual element — the badge must remain smaller and less prominent than all typography
- FORBIDDEN: rendering the brand name, active ingredient, dosage or quantity text in any colour other than black — no blue, purple, green, red or tinted lettering on text. Coloured ink appears ONLY in the badge and accent stripe.
- Text rule: print ONLY the quoted string values from the FRONT PANEL GRID — never invent additional text\
"""

TEMPLATE_T1 = """\
[SCENE HARDWARE]: 3/4 isometric, 25° pitch, box rotated 35°, 85mm lens, f/8.
Softbox top-left (key) + soft fill right. No specular on text zones. 
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]: 
Primary object — EU standard pharmaceutical medicine carton box. \
STRICT PROPORTIONS: width:height:depth = 3.6:2.2:1 ratio. The box is WIDER than it is tall. Landscape orientation. NOT square. NOT portrait. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T1_SMALL = """\
[SCENE HARDWARE]: 3/4 isometric, 25° pitch, box rotated 35°, 85mm lens, f/8.
Softbox top-left (key) + soft fill right. No specular on text zones. 
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]: 
Primary object — EU standard thin landscape pharmaceutical medicine carton box (small). \
STRICT PROPORTIONS: width:height:depth = 4.2:2.4:0.6 ratio. The box is a very thin, flat landscape carton, optimized for small blister counts. NOT square. NOT portrait. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: THIN_LANDSCAPE_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T1_LARGE = """\
[SCENE HARDWARE]: 3/4 isometric, 25° pitch, box rotated 35°, 85mm lens, f/8.
Softbox top-left (key) + soft fill right. No specular on text zones. 
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]: 
Primary object — EU standard deep landscape pharmaceutical medicine carton box (large). \
STRICT PROPORTIONS: width:height:depth = 3.2:2.4:1.6 ratio. The box is a deep, thick landscape carton with substantial depth, designed for high blister counts. NOT square. NOT portrait. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: DEEP_LANDSCAPE_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T2 = """\
[SCENE HARDWARE]: 3/4 isometric, 25° pitch, box rotated 35°, 85mm lens, f/8.
Softbox top-left (key) + soft fill right. No specular on text zones. 
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]: 
Primary object — EU standard vertical slender pharmaceutical medicine carton box. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID (VERTICAL HIERARCHY)]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: SLENDER_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T3 = """\
[SCENE HARDWARE]: 3/4 isometric, 25° pitch, box rotated 35°, 85mm lens, f/8.
Softbox top-left (key) + soft fill right. No specular on text zones. 
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]: 
Primary object — EU standard long horizontal pharmaceutical medicine carton box. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID (HORIZONTAL LAYOUT)]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: LONG_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T_BOTTLE_BOX = """\
[SCENE HARDWARE]: 3/4 isometric, 20° pitch, box rotated 25°, 85mm lens, f/8.
Softbox top-left (key) + vertical strip fill right. No specular on text zones.
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]:
Primary object — EU standard VERTICAL pharmaceutical medicine carton box designed to contain a bottle or dropper. \
STRICT PROPORTIONS: width:height:depth = 1:2.2:1 ratio. The box is TALLER than it is wide. Portrait orientation. NOT landscape. NOT square. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID (PORTRAIT / VERTICAL HIERARCHY)]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: VERTICAL_BOTTLE_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T_MULTIPACK = """\
[SCENE HARDWARE]: 3/4 isometric, 20° pitch, box rotated 30°, 85mm lens, f/8.
Softbox top-left (key) + soft fill right. No specular on text zones. 
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]: 
Primary object — EU standard elongated multi-blister pharmaceutical medicine carton box (multipack). \
STRICT PROPORTIONS: width:height:depth = 4.5:2.0:1 ratio. The box is significantly wider than it is tall, designed to fit multiple blister packs side-by-side. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID (MULTIPACK HORIZONTAL LAYOUT)]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: MULTIPACK_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T_VERT_VIAL = """\
[SCENE HARDWARE]: 3/4 isometric, 20° pitch, box rotated 25°, 85mm lens, f/8.
Softbox top-left (key) + vertical strip fill right. No specular on text zones.
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]:
Primary object — EU standard portrait pharmaceutical medicine carton box designed to contain a small squat glass vial. \
STRICT PROPORTIONS: width:height:depth = 1.0:1.4:1.0 ratio. The box is a compact, small, relatively squat portrait carton. NOT landscape. NOT square. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID (PORTRAIT / VERTICAL HIERARCHY)]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: SQUAT_PORTRAIT_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T_VERT_DROPPER = """\
[SCENE HARDWARE]: 3/4 isometric, 20° pitch, box rotated 25°, 85mm lens, f/8.
Softbox top-left (key) + vertical strip fill right. No specular on text zones.
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]:
Primary object — EU standard vertical pharmaceutical medicine carton box designed to contain a dropper bottle. \
STRICT PROPORTIONS: width:height:depth = 1.0:2.2:1.0 ratio. The box is tall and narrow. Portrait orientation. NOT landscape. NOT square. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID (PORTRAIT / VERTICAL HIERARCHY)]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: SLENDER_PORTRAIT_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_T_VERT_INHALER = """\
[SCENE HARDWARE]: 3/4 isometric, 20° pitch, box rotated 25°, 85mm lens, f/8.
Softbox top-left (key) + vertical strip fill right. No specular on text zones.
#FFFFFF background. Contact shadow soft 60% opacity.

{render_constraints}

[RENDER TARGET]:
Primary object — EU standard vertical pharmaceutical medicine carton box designed to contain a larger inhaler canister. \
STRICT PROPORTIONS: width:height:depth = 1.2:1.8:1.2 ratio. The box is a substantial, wide portrait carton. Portrait orientation. NOT landscape. NOT square. \
Surface: BRIGHT WHITE (#FFFFFF) matte laminate cardboard. The box base colour is PURE WHITE — no grey tones, no off-white, no neutral grey wash. Fold lines visible. {surface_finish}.

[SURFACE COLOUR MANDATE]: The carton is WHITE. The ONLY non-white colour on the front face is the brand accent stripe (Row 6) in {accent_hex} and the brand badge block. All other surfaces remain pure white #FFFFFF.

{geometry_override}
[FRONT PANEL GRID (PORTRAIT / VERTICAL HIERARCHY)]:
{front_panel_grid_lines}

[SIDE PANEL]:
- Left face: GS1 barcode vertical + "LOT / EXP" field labels + Braille dots pattern. Compact "LOT / EXP" stamp. Dense regulatory pharmaceutical microprint texture. No accent stripe on side panel.

[COLOR]:
- Brand Badge/Graphic Colour: {primary_hex} ({primary_desc}) — used ONLY for corner badge icon, NOT for any text
- All Text Ink: #000000 (solid black) — name, ingredient, dosage, quantity all printed in black
- Accent Stripe: {accent_hex} ({accent_desc}) — Row 6 only
- Box Surface: #FFFFFF pure white — NEVER grey, NEVER off-white, NEVER monochrome

[PURITY]:
{purity_anchor}
{regulatory_rules}

{_SHARED_FORBIDDEN}

Batch Stability Anchor: [ID-hash-{sku_hash}]. Render with maximum typographic fidelity. No creative interpretation of text placement or label hierarchy. All typography must remain fully legible, correctly spelled, and typographically coherent.

<!-- EU_FORMAT: WIDE_PORTRAIT_CARTON | Rx_BADGE: REMOVED -->
"""

TEMPLATE_MAP = {
    "T1": TEMPLATE_T1,
    "T1_SMALL": TEMPLATE_T1_SMALL,
    "T1_LARGE": TEMPLATE_T1_LARGE,
    "T2": TEMPLATE_T2,
    "T3": TEMPLATE_T3,
    "T_BOTTLE_BOX": TEMPLATE_T_BOTTLE_BOX,
    "T_MULTIPACK": TEMPLATE_T_MULTIPACK,
    "T_VERT_VIAL": TEMPLATE_T_VERT_VIAL,
    "T_VERT_DROPPER": TEMPLATE_T_VERT_DROPPER,
    "T_VERT_INHALER": TEMPLATE_T_VERT_INHALER
}

# =============================================
# AGENT 3: PASSPORT ARCHITECT
# =============================================

def sanitize_text(text):
    if not text: return ""
    return text.replace("[", "").replace("]", "").strip()

def agent_3_passport_architect(data: dict, template_id: str,
                               is_override: bool, secondary: SecondaryPackageTemplate, verify_result: dict) -> str:
    sku_id   = str(data.get("sku_id", ""))
    sku_hash = hashlib.md5(sku_id.encode()).hexdigest()[:8]

    label    = data.get("label_content", {})
    branding = data.get("branding", {})
    palette  = branding.get("palette", {})
    design   = branding.get("design_elements", {})

    brand_name = SKU_REGISTRY.get(sku_id, {}).get("name") or data.get("brand_name") or data.get("product_name", "Medicine")
    brand_name = sanitize_text(brand_name)
    product_name = sanitize_text(data.get("product_name", "Medicine"))
    
    ingredient_name = SKU_REGISTRY.get(sku_id, {}).get("active_ingredient") or data.get("active_ingredient") or product_name
    ingredient_name = sanitize_text(ingredient_name)
    ingredient_name = purge_forms(ingredient_name)
    ingredient_name = ingredient_name.replace(" (Generic)", "").strip()
    # Clean active ingredient from percent symbols
    ingredient_name = re.sub(r'\s*\d*(?:\.\d+)?%', '', ingredient_name).strip()

    # Construct Row 4 Dosage strictly from minimal_dosage and dosage_type
    sku_entry = SKU_REGISTRY.get(sku_id, {})
    min_dose = sku_entry.get("minimal_dosage") or data.get("minimal_dosage")
    dose_type = sku_entry.get("dosage_type") or data.get("dosage_type") or data.get("dosage_ref")
    
    if not min_dose or not str(min_dose).strip() or not dose_type or not str(dose_type).strip():
        dosage = "недостаточно данных"
    else:
        try:
            val = float(str(min_dose).strip())
            if val.is_integer():
                formatted_dose = str(int(val))
            else:
                formatted_dose = str(val)
        except ValueError:
            formatted_dose = str(min_dose).strip()
        
        formatted_type = str(dose_type).strip()
        dosage = f"{formatted_dose}{formatted_type}"

    unit_count_raw = sanitize_text(label.get("unit_count_display", ""))
    
    unit_count = resolve_unit_label(sku_id, unit_count_raw)

    primary_hex = palette.get("primary", "#000000")
    accent_hex  = palette.get("accent", "#ADD8E6")  # Light Blue fallback — replaces grey #AAAAAA
    accent_desc = hex_to_name_hint(accent_hex)

    # Surface finish
    is_varnished   = design.get("is_varnished", False)
    has_embossing  = design.get("has_logo_embossing", False)
    spot_uv        = design.get("spot_uv_areas") or []
    finish_parts = ["Matte cardboard"]
    if is_varnished and spot_uv:
        finish_parts.append(f"Spot UV varnish on: {', '.join(spot_uv)}")
    elif is_varnished:
        finish_parts.append("Spot UV varnish")
    if has_embossing:
        finish_parts.append("Typographic brand embossing")
    surface_finish = "; ".join(finish_parts)

    # Brand badge: deterministic abstract mark selection keyed to brand name hash.
    # Badge is a small restrained square in brand colour, top-right of front face.
    # Mark is a subtle flat white abstract geometry — no medical symbols, no UI icons.
    h_val = int(hashlib.md5(brand_name.encode("utf-8")).hexdigest(), 16)
    _BADGE_MARKS = [
        "thin circular ring",
        "abstract geometric line motif",
        "minimal hexagon outline",
        "abstract geometric line motif",  # weighted: line motif most neutral
    ]
    badge_mark = _BADGE_MARKS[h_val % len(_BADGE_MARKS)]

    badge_bg_hex = primary_hex
    badge_bg_desc = hex_to_name_hint(badge_bg_hex)

    # Determine badge mark text/ink color by contrast vs white/dark
    white_text_badge_colors = {
        "#003366", "#005A9C", "#006A4E", "#6B2D5C", "#0D5FB8", "#4B4632"
    }
    badge_text_color = "flat white"
    norm_badge_bg = "#" + badge_bg_hex.lstrip("#").upper()
    if norm_badge_bg not in white_text_badge_colors:
        badge_text_color = "flat black"

    # Geometry Override construction (positive-only anchors — no negations)
    geometry_override = ""
    if template_id == "T_BOTTLE_BOX":
        geometry_override = (
            "[FORM FACTOR — VERTICAL BOTTLE CARTON]: "
            "This is a TALL PORTRAIT-ORIENTED folded paperboard carton "
            "designed to contain a pharmaceutical bottle or dropper. "
            "The carton height is approximately 2x its width. "
            "Six flat faces, sharp 90° edges, visible fold lines. "
            "Portrait orientation — tall and narrow. "
            "Standard European pharmaceutical secondary packaging for liquid containers."
        )
    elif template_id == "T_VERT_VIAL":
        geometry_override = (
            "[FORM FACTOR — VERTICAL VIAL CARTON]: "
            "Folded paperboard carton, small and relatively squat portrait box. "
            "Designed for a single glass vial. Six flat faces, sharp 90° edges, visible fold lines. "
            "Matte laminate surface. Standard European packaging for vials."
        )
    elif template_id == "T_VERT_DROPPER":
        geometry_override = (
            "[FORM FACTOR — VERTICAL DROPPER CARTON]: "
            "Folded paperboard carton, tall and narrow portrait box. "
            "Designed for a dropper bottle or eye drops bottle. "
            "Six flat faces, sharp 90° edges, visible fold lines. "
            "Matte laminate surface. Standard European packaging for dropper bottles."
        )
    elif template_id == "T_VERT_INHALER":
        geometry_override = (
            "[FORM FACTOR — VERTICAL INHALER CARTON]: "
            "Folded paperboard carton, wide and substantial portrait box. "
            "Designed for an inhaler unit or nasal spray canister. "
            "Six flat faces, sharp 90° edges, visible fold lines. "
            "Matte laminate surface. Standard European packaging for inhalers."
        )
    elif template_id == "T_MULTIPACK":
        geometry_override = (
            "[FORM FACTOR — MULTIPACK CARTON]: "
            "This is an ELONGATED folded paperboard carton (multipack) "
            "designed to contain multiple blister packs or multiple individual packages. "
            "The carton width is significantly larger than its height (approximately 2.25x the height). "
            "Six flat faces, sharp 90° edges, visible fold lines. "
            "Landscape orientation — elongated and flat. "
            "Standard European pharmaceutical secondary packaging for multi-unit packs."
        )
    elif is_override:
        geometry_override = (
            "[GEOMETRY OVERRIDE]: Render as pharmaceutical bottle (round/tall cylindrical container). "
            "Apply cylindrical label wrap physics. Label wraps 270° of cylinder surface. Cap visible at top.\n"
        )
    elif template_id == "T1":
        geometry_override = (
            "[FORM FACTOR]: Folded paperboard carton. Rectangular parallelepiped. "
            "Six flat faces, sharp 90° edges, visible fold lines. Matte laminate surface. "
            "Standard European pharmaceutical secondary packaging."
        )
    elif template_id == "T1_SMALL":
        geometry_override = (
            "[FORM FACTOR — SMALL FLAT CARTON]: "
            "Folded paperboard carton. Very thin and flat profile. "
            "Six flat faces, sharp 90° edges, visible fold lines. Matte laminate surface. "
            "Standard thin flat European pharmaceutical secondary packaging."
        )
    elif template_id == "T1_LARGE":
        geometry_override = (
            "[FORM FACTOR — LARGE DEEP CARTON]: "
            "Folded paperboard carton. Deeper and thicker profile. "
            "Six flat faces, sharp 90° edges, visible fold lines. Matte laminate surface. "
            "Standard large capacity European pharmaceutical secondary packaging."
        )
    else:
        geometry_override = (
            f"[GEOMETRY OVERRIDE]: Secondary box dimensions: {int(secondary.box_width_mm)}x"
            f"{int(secondary.box_depth_mm)}x{int(secondary.box_height_mm)}mm. "
            f"Template: {secondary.name}. Render as medicine_box.\n\n"
        )

    rx_required = is_rx_product(product_name, data.get("internal_unit", {}).get("type", ""))

    _ingredient_line_sentinel = "__NO_INGREDIENT__"
    ingredient_display = ingredient_name if ingredient_name else _ingredient_line_sentinel

    attention_anchor_str = _ATTENTION_ANCHOR.replace('{brand_name}', brand_name)
    terminology_map_str = _TERMINOLOGY_MAP.replace('{unit_count}', unit_count)

    # Generate layout grid lines
    # Structure (front panel, top → bottom):
    #   Badge  — compact square in brand colour, top-right corner (floating element, not in text flow)
    #   Row 1  — Commercial name: brand_name, BOLD, largest
    #   Row 2  — Active ingredient: ingredient_name, regular 50% size (omitted if same as brand)
    #   Row 3  — Braille: embossed dots of ingredient_name, immediately below Row 2
    #   Row 4  — Dosage
    #   Row 5  — Unit count, bottom-right
    #   Row 6  — Accent stripe, very bottom edge
    grid_lines = [
        '- TEXT COLOUR MANDATE: All printed information text on the front face (Commercial Name, Active Ingredient, Dosage, Quantity) is solid BLACK #000000 ink. Brand colour is used ONLY for the corner badge and the Row 6 accent stripe — NEVER for the text characters themselves.',
        f'- Top-Right Corner / Brand Badge: a small restrained square, '
        f'approximately 6–8% of panel width, filled with solid brand colour {badge_bg_hex} ({badge_bg_desc}). '
        f'Inside the block: one subtle abstract geometric mark — {badge_mark} — rendered in {badge_text_color}, '
        f'occupying roughly half the block area. '
        f'No text inside the badge. No outline or border on the block itself. '
        f'Badge aligned near the top-right corner with minimal margin. '
        f'The badge is visually subordinate to the brand typography and must never become the primary focal element. '
        f'No glossy app-icon aesthetics, no neumorphism, no mobile UI button styling, no startup-style logo rendering.',
        f'- Row 1 / Commercial Name: "{brand_name}" — BOLD, largest text element on panel, maximum contrast against background, printed in solid BLACK #000000. Printed once only.',
    ]
    if ingredient_display != _ingredient_line_sentinel and ingredient_display.strip():
        grid_lines.append(
            f'- Row 2 / Active Ingredient: "{ingredient_display}" — regular weight, 50 percent font size of brand name, printed in solid BLACK #000000 text. '
            f'Printed in plain latin text directly below Row 1.'
        )
        grid_lines.append(
            f'- Row 3 / Braille Duplicate: embossed Braille dot pattern immediately below Row 2, '
            f'same width as Row 2 text block, encoding "{ingredient_display}". '
            f'Dots are raised tactile bumps, same colour as background, no printed ink. '
            f'Subtle, physically realistic pharmaceutical Braille relief — not decorative noise.'
        )
    else:
        grid_lines.append(
            f'- Row 3 / Braille Duplicate: embossed Braille dot pattern immediately below Row 1, '
            f'encoding "{brand_name}". '
            f'Dots are raised tactile bumps, same colour as background, no printed ink. '
            f'Subtle, physically realistic pharmaceutical Braille relief — not decorative noise.'
        )
    grid_lines.extend([
        f'- Row 4 / Dosage: "{dosage}" — bottom row, LEFT corner, printed in solid BLACK #000000. Render only the minimal dosage and dosage form joined with no separator in the bottom-left counter (e.g., "{dosage}" → "{dosage}"), with zero percentage symbols and no active-ingredient text in this zone.',
        f'- Row 5 / Quantity: "{unit_count}" — SAME bottom row, RIGHT corner, directly opposite the dosage, maximally separated horizontally (opposite corners), printed in solid BLACK #000000. Both dosage and quantity are on the single lowest information line. Printed once only.',
        f'- Row 6 / Accent Stripe: thin full-width horizontal colour band at the very bottom edge of the FRONT FACE, '
        f'height ~4mm, colour {accent_hex} ({accent_desc}). This stripe is on the front face only — not on side panels.',
    ])

    front_panel_grid_lines = "\n".join(grid_lines)

    if rx_required:
        regulatory_rules = "[REGULATORY]: Rx prescription product layout controls."
    else:
        regulatory_rules = "[REGULATORY]: OTC product — no Rx or prescription markings anywhere on packaging."

    template_str = TEMPLATE_MAP[template_id]
        
    md = template_str.format(
        brand_name        = brand_name,
        product_name      = product_name,
        ingredient_name   = ingredient_display,
        dosage            = dosage,
        unit_count        = unit_count,
        primary_hex       = primary_hex,
        primary_desc      = hex_to_name_hint(primary_hex),
        accent_hex        = accent_hex,
        accent_desc       = hex_to_name_hint(accent_hex),
        surface_finish    = surface_finish,
        geometry_override = geometry_override,
        attention_anchor  = attention_anchor_str,
        terminology_map   = terminology_map_str,
        purity_anchor     = _PURITY_ANCHOR,
        render_constraints= _RENDER_CONSTRAINTS,
        front_panel_grid_lines = front_panel_grid_lines,
        sku_hash          = sku_hash,
        regulatory_rules  = regulatory_rules,
        _SHARED_FORBIDDEN = _SHARED_FORBIDDEN,
    )

    # Strip sentinel lines
    md = "\n".join(
        line for line in md.splitlines()
        if _ingredient_line_sentinel not in line
    )

    geom = str(data.get("packaging_geometry", "BOX"))
    family = map_geometry_to_family(geom, product_name, data.get("package_type", ""))
    route = GEOMETRY_MAPPING.get(family, GEOMETRY_MAPPING[PackagingFamily.BOX_VERTICAL_STANDARD])
    route_status = route["status"]

    confidence = verify_result.get("confidence", 1.0)
    warnings = "; ".join(verify_result.get("warnings", [])) if verify_result.get("warnings") else "none"

    # Series Visual Anchor
    sub_brand_anchor = detect_sub_brand(product_name)
    if sub_brand_anchor:
        md += (
            f"\n[SERIES VISUAL ANCHOR]: {sub_brand_anchor}\n"
            f"   Apply this series identity as the dominant visual tone of the packaging design.\n"
            f"   The brand base color palette is retained; the SERIES ANCHOR defines the "
            f"surface treatment, texture, and compositional emphasis that differentiates this \n"
            f"   line from the standard edition.\n"
        )

    # Material Safety Override (P8.0: also check via SKU.csv pkg_type for secondary carton renders)
    _sku_pkg_type = SKU_REGISTRY.get(sku_id, {}).get("package_type", "")
    material_override = detect_material_override(product_name, geom, _sku_pkg_type)
    if material_override:
        md += (
            f"\n[MATERIAL SAFETY OVERRIDE]: {material_override}\n"
            f"   Apply this material and packaging safety specification to ensure light protection.\n"
        )

    # Under Task 2 placeholder routing safety, add explicit HTML comment warning block
    if route_status == RouteStatus.PLACEHOLDER_ROUTE:
        md += (
            f"\n<!--\n"
            f"ROUTING_STATUS: PLACEHOLDER_ROUTE\n"
            f"REAL_FAMILY: {family.value}\n"
            f"TEMPORARY_TEMPLATE: {template_id}\n"
            f"PRODUCTION_SUPPORT: FALSE\n"
            f"-->\n"
        )

    series_tag = f" | SERIES: {sub_brand_anchor[:40]}" if sub_brand_anchor else ""
    routing_tag = " | ROUTING: PLACEHOLDER" if route_status == RouteStatus.PLACEHOLDER_ROUTE else ""
    
    if confidence < 0.50:
        status_flag = "REJECTED/MANUAL REVIEW"
    elif confidence < 0.70:
        status_flag = "REVIEW NEEDED"
    else:
        status_flag = "OK"

    md += (
        f"\n<!-- PASSPORT_VERSION: 2.1 | SKU: {sku_id} | TEMPLATE: {template_id}{routing_tag}"
        f" | CONFIDENCE: {confidence} | STATUS: {status_flag}{series_tag} | WARNINGS: {warnings} -->\n"
    )

    # Conditional purge of "Capsules", "Capsule", "Tablets", "Tablet" from rendered text values
    # Only applies to solid oral forms (pills, packs, boxes, strips, units)
    # Skip lines containing HTML comments to avoid corrupting metadata (even multi-line comments)
    _SOLID_ORAL_TYPES = {"pills", "pill", "packs", "pack", "boxes", "box", "strips", "strip", "units", "unit"}
    sku_pkg_type = SKU_REGISTRY.get(sku_id, {}).get("package_type", "pills").lower()
    purged_lines = []
    in_comment = False
    for line in md.splitlines():
        if '<!--' in line:
            in_comment = True
        if in_comment:
            purged_lines.append(line)
            if '-->' in line:
                in_comment = False
        else:
            if sku_pkg_type in _SOLID_ORAL_TYPES:
                # Only for solid oral forms: normalize Capsules/Tablets → Pills
                line = re.sub(r'\b(?:Capsules?|Tablets?)\b', 'Pills', line)
                line = re.sub(r'\b(?:capsules?|tablets?)\b', 'pills', line)
            # else: do not touch — vials, tubes, etc. don't need this replacement
            purged_lines.append(line)
    md = "\n".join(purged_lines)

    return md

# =============================================
# MAIN PIPELINE
# =============================================

def main():
    if not INPUT_DIR.exists():
        print(f"[ERROR] Input directory {INPUT_DIR} not found.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    json_files = sorted(
        [f for f in INPUT_DIR.glob("*.json")],
        key=lambda f: int(f.stem.split("-")[0]) if f.stem.split("-")[0].isdigit() else 999999
    )
    
    # Statistics collection
    placeholder_counts = {}
    unsupported_families = set()
    absorption_mapping = {} # template_id -> set of families
    placeholder_skus_count = 0
    
    sub_brand_counts = {k: 0 for k, v in _SPECS_SUB_BRANDS.items() if isinstance(v, dict)}
    photosens_counts = {k: 0 for k, v in _SPECS_PHOTOSENS.items() if isinstance(v, dict)}
    photosens_missed = {k: 0 for k, v in _SPECS_PHOTOSENS.items() if isinstance(v, dict)}

    # Process all files
    total = len(json_files)
    print(f"\n[START] Processing {total} JSON passports for conversion to Markdown...")

    converted = 0
    failures  = []

    for json_path in json_files:
        md_path = OUTPUT_DIR / json_path.name.replace(".json", ".md")

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Ensure schema compatibility
            schema = data.get("schema_version", "")
            if schema not in ("2.0", "2.1"):
                continue

            # Enrich active ingredient and manufacturer from registry
            sku_id = data.get("sku_id", "")
            registry_entry = SSOT_SKU_REGISTRY.get(sku_id, {})
            if registry_entry:
                if data.get("active_ingredient") is None and registry_entry.get("active_ingredient"):
                    data["active_ingredient"] = registry_entry["active_ingredient"]
                if data.get("manufacturer") is None and registry_entry.get("manufacturer"):
                    data["manufacturer"] = registry_entry["manufacturer"]

            # Combo drug verification check
            active_ingredient = data.get("active_ingredient") or ""
            brand_name = data.get("brand_name") or data.get("product_name") or ""
            if ('+' in active_ingredient or '/' in active_ingredient) and brand_name.lower() != 'original test pack':
                parts = re.split(r'[/+]', active_ingredient)
                if any(not p.strip() for p in parts):
                    raise ValueError(f"[DATA ABORT] Incomplete API string for combo drug: '{brand_name}' -> '{active_ingredient}'")

            # Agent 1: Routing
            template_id, is_override = agent_1_router(data)

            # Packaging Resolution & Validation Fit
            primary = get_primary_package(data)
            secondary = resolve_secondary(primary)
            validate_fit(primary, secondary)

            # Agent 2: Verification
            verify = agent_2_verifier(data)

            if not verify["verified"]:
                entry = (
                    f"{json_path.name} | SKU: {sku_id} "
                    f"| confidence: {verify['confidence']} "
                    f"| {'; '.join(verify['warnings'])}"
                )
                failures.append(entry)

            # Agent 3: Architect Markdown Builder
            markdown = agent_3_passport_architect(data, template_id, is_override, secondary, verify)

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown)

            # Accumulate placeholder routing stats
            geom = str(data.get("packaging_geometry", "BOX"))
            product_name = str(data.get("product_name", ""))
            family = map_geometry_to_family(geom, product_name, data.get("package_type", ""))
            route = GEOMETRY_MAPPING.get(family, GEOMETRY_MAPPING[PackagingFamily.BOX_VERTICAL_STANDARD])
            
            if route["status"] == RouteStatus.PLACEHOLDER_ROUTE:
                placeholder_skus_count += 1
                placeholder_counts[family.value] = placeholder_counts.get(family.value, 0) + 1
                unsupported_families.add(family.value)
                t_id = route["template_id"]
                if t_id not in absorption_mapping:
                    absorption_mapping[t_id] = set()
                absorption_mapping[t_id].add(family.value)

            # Accumulate design overrides stats
            name_lower = product_name.lower()
            for rule_name, rule_data in _SPECS_SUB_BRANDS.items():
                if isinstance(rule_data, dict):
                    triggers = rule_data.get("triggers", [])
                    if triggers:
                        for t in triggers:
                            if re.search(rf'\b{re.escape(t)}\b', name_lower):
                                sub_brand_counts[rule_name] += 1
                                break
                                
            geom_upper = geom.upper().strip()
            light_protective_geom = {"BOTTLE", "VIAL", "AMPOULE", "DROPPER", "SPRAY"}
            for comp_name, comp_data in _SPECS_PHOTOSENS.items():
                if isinstance(comp_data, dict):
                    triggers = comp_data.get("triggers", [])
                    if triggers:
                        matched = False
                        for t in triggers:
                            if re.search(rf'\b{re.escape(t)}\b', name_lower):
                                matched = True
                                break
                        if matched:
                            if geom_upper in light_protective_geom:
                                photosens_counts[comp_name] += 1
                            else:
                                photosens_missed[comp_name] += 1
                            break

            converted += 1

        except ValueError as ve:
            print(f"  [BLOCKED] {json_path.name}: {ve}")
            failures.append(f"{json_path.name} | FIT_ERROR/ROUTING_BLOCK | {ve}")
        except Exception as e:
            print(f"  [ERROR] {json_path.name}: {e}")
            failures.append(f"{json_path.name} | EXCEPTION | {e}")

    # Write failures to log
    with open(FAILURES_LOG, "w", encoding="utf-8") as f_log:
        f_log.write(f"VERIFICATION FAILURES — {len(failures)} entries\n")
        f_log.write("=" * 60 + "\n")
        for entry in failures:
            f_log.write(entry + "\n")

    # Placeholder Routing Audit Report generation disabled per P10.0 requirements

    # Write Data-Driven Override Audit Report
    docs_dir = Path("docs")
    override_report_path = docs_dir / "DATA_DRIVEN_OVERRIDE_AUDIT.md"
    with open(override_report_path, "w", encoding="utf-8") as of:
        of.write("# DATA-DRIVEN OVERRIDE AUDIT REPORT\n\n")
        
        of.write("## SUB-BRAND SPECS OVERRIDES\n\n")
        of.write("| Sub-Brand Key | Triggers | Active Trigger Count | Status |\n")
        of.write("| --- | --- | --- | --- |\n")
        for k, v in sorted(_SPECS_SUB_BRANDS.items()):
            if isinstance(v, dict):
                triggers = ", ".join(f"`{t}`" for t in v.get("triggers", []))
                count = sub_brand_counts[k]
                status_str = "ACTIVE" if count > 0 else "ROADMAP_ONLY / UNUSED"
                of.write(f"| `{k}` | {triggers} | {count} | `{status_str}` |\n")
            
        of.write("\n## PHOTOSENSITIVE COMPOUNDS OVERRIDES\n\n")
        of.write("| Compound Key | Triggers | Active Trigger Count | Missed (wrong geom) | Material Spec | Status |\n")
        of.write("| --- | --- | --- | --- | --- | --- |\n")
        for k, v in sorted(_SPECS_PHOTOSENS.items()):
            if isinstance(v, dict):
                triggers = ", ".join(f"`{t}`" for t in v.get("triggers", []))
                count = photosens_counts[k]
                miss = photosens_missed[k]
                spec = v.get("material_render_spec", "")
                status_str = "ACTIVE" if count > 0 else "ROADMAP_ONLY / UNUSED"
                of.write(f"| `{k}` | {triggers} | {count} | {miss} | {spec} | `{status_str}` |\n")

    print(f"\n[DONE] Successfully converted {converted}/{total} passports.")
    print(f"       Failed/Warnings logged to: {FAILURES_LOG} ({len(failures)} entries)")

if __name__ == "__main__":
    main()