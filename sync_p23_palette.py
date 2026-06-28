import csv
import json
import re
import shutil
from pathlib import Path

sku_path = Path("SSOT/SKU.csv")
master_path = Path("SSOT/master.json")
prices_path = Path("SSOT/full_prices - Sheet1.csv")
passports_dir = Path("pipeline/passports")
output_json_path = Path("SSOT/audit_categories.json")

# 1. Load category mapping data from prices
group_to_category = {}
name_to_category = {}
active_to_category = {}

with open(prices_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat = row.get("category", "").strip()
        grp = row.get("group", "").strip()
        nm = row.get("name", "").strip()
        
        if cat:
            if grp:
                group_to_category[grp.lower()] = cat
                match = re.search(r'\((.*?)\)', grp)
                if match:
                    active_to_category[match.group(1).lower().strip()] = cat
            if nm:
                name_to_category[nm.lower()] = cat

# Manual fallback mappings for known SKUs that don't match directly
manual_fallbacks = {
    "1-min.jpg": "ADHD",
    "18-min.jpg": "Anti-Viral",
    "30-min.jpg": "Antipsychotic Treatment",
    "51-min.jpg": "Hepatitis C",
    "82-min.jpg": "General Health",
    "89-min.jpg": "Arthritis",
    "94-min.jpg": "Women's Health",
    "102-min.jpg": "Heart & Cholesterol",
    "111-min.jpg": "Skin Care & Dermatology",
    "117-min.jpg": "Weight Loss",
    "122-min.jpg": "Women's Health",
    "124-min.jpg": "Women's Sexual Health",
    "127-min.jpg": "Skin Care & Dermatology",
    "229-min.jpg": "Men's Sexual Health",
    "317-min.jpg": "Skin Care & Dermatology",
    "359-min.jpg": "Anti-Anxiety",
    "360-min.jpg": "Sleep Aid",
    "369-min.jpg": "Allergy Relief",
    "379-min.jpg": "Men's Sexual Health",
    "393-min.jpg": "Asthma Relief & Management"
}

def clean_name(n):
    n = re.sub(r'\b(generic|cream|gel|oral|jelly|chewable|soft|strips|original|test|pack|drops|spray|nasal)\b', '', n, flags=re.IGNORECASE)
    n = re.sub(r'\(.*?\)', '', n)
    return n.strip().lower()

# Get category for SKU
def get_sku_category(pic, name, active):
    name_lower = name.lower()
    active_lower = active.lower().strip()
    
    # 1. Try direct matches
    if name_lower in group_to_category:
        return group_to_category[name_lower]
    elif name_lower in name_to_category:
        return name_to_category[name_lower]
    elif active_lower in active_to_category:
        return active_to_category[active_lower]
    
    # 2. Try clean matching
    cleaned = clean_name(name)
    for grp, cat in group_to_category.items():
        grp_clean = clean_name(grp)
        if cleaned and grp_clean and (cleaned in grp_clean or grp_clean in cleaned):
            return cat
            
    for nm, cat in name_to_category.items():
        nm_clean = clean_name(nm)
        if cleaned and nm_clean and (cleaned in nm_clean or nm_clean in cleaned):
            return cat
            
    # 3. Fallback matching
    if pic in manual_fallbacks:
        return manual_fallbacks[pic]
        
    return "NOT_FOUND"

# Load is_generic values from master.json
is_generic_map = {}
if master_path.exists():
    with open(master_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)
    for pic, entry in master_data.get("sku_registry", {}).items():
        is_generic_map[pic] = entry.get("is_generic", True)

# Premium Color Palette Configuration
COLOR_PALETTE_CONFIG = {
    "BRANDS": {
        "Cialis": {
            "badge": "#006A4E",        # Pharma Green
            "row_6": "#C9A227"         # Muted Gold
        },
        "Viagra": {
            "badge": "#003366",        # Navy
            "row_6": "#C9A227"         # Muted Gold
        },
        "Kamagra": {
            "badge": "#6B2D5C",        # Bordeaux (P23.3 fix — CR 4.02 vs Gold stripe)
            "row_6": "#C9A227"         # Muted Gold
        }
    },
    "CATEGORIES": {
        "ED Generic": {
            "badge": "#005A9C",        # Medical Blue
            "row_6": "#C9A227"         # Muted Gold
        },
        "ED Brand": {
            "badge": "#005A9C",        # Medical Blue
            "row_6": "#C9A227"         # Muted Gold
        },
        "Smart Pills (Nootropics)": {
            "badge": "#DDA7A5",        # Rose
            "row_6": "#6B2D5C"         # Bordeaux
        },
        "Beauty & Skin Care": {
            "badge": "#E2583E",        # Poppy
            "row_6": "#4B4632"         # Tapenade
        },
        "DEFAULT": {
            "badge": "#003366",        # Navy
            "row_6": "#0D5FB8"         # North Star Cobalt
        }
    }
}

# Resolve target category and color pair
def get_sku_colors_and_category(pic, name, original_cat):
    first_word = name.split()[0]
    is_gen = is_generic_map.get(pic, True)
    
    # 1. Resolve category
    if original_cat in ("Men's Sexual Health", "Women's Sexual Health"):
        mapped_cat = "ED Generic" if is_gen else "ED Brand"
    elif original_cat == "ADHD":
        mapped_cat = "Smart Pills (Nootropics)"
    elif original_cat in ("Skin Care & Dermatology", "Hair Loss Treatment"):
        mapped_cat = "Beauty & Skin Care"
    else:
        mapped_cat = original_cat

    # 2. Resolve colors
    if first_word in COLOR_PALETTE_CONFIG["BRANDS"]:
        colors = COLOR_PALETTE_CONFIG["BRANDS"][first_word]
    else:
        cat_key = mapped_cat
        if cat_key not in COLOR_PALETTE_CONFIG["CATEGORIES"]:
            cat_key = "DEFAULT"
        colors = COLOR_PALETTE_CONFIG["CATEGORIES"][cat_key]
        
    return colors["badge"], colors["row_6"], mapped_cat

# 2. Process all SKUs and build maps
sku_colors_map = {}
sku_category_map = {}
sku_original_category_map = {}

categories_report = {}

with open(sku_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pic = row.get("picture", "").strip()
        name = row.get("name", "").strip()
        active = row.get("active_ingredient", "").strip()
        
        orig_cat = get_sku_category(pic, name, active)
        badge_hex, row_6_hex, final_cat = get_sku_colors_and_category(pic, name, orig_cat)
        
        sku_category_map[pic] = final_cat
        sku_original_category_map[pic] = orig_cat
        sku_colors_map[pic] = {
            "primary": badge_hex,
            "accent": row_6_hex
        }
        
        # Determine group for audit report
        first_word = name.split()[0]
        if first_word in COLOR_PALETTE_CONFIG["BRANDS"]:
            group_key = first_word
        else:
            group_key = final_cat if final_cat in COLOR_PALETTE_CONFIG["CATEGORIES"] else "DEFAULT"
            
        # Add to audit report structure
        entry_str = f"{pic} | {name} ({active}) | Badge: {badge_hex}, Stripe: {row_6_hex}"
        if group_key in COLOR_PALETTE_CONFIG["BRANDS"]:
            categories_report.setdefault(f"Brand Family: {group_key}", []).append(entry_str)
        else:
            categories_report.setdefault(group_key, []).append(entry_str)

# 3. Write Phase 1 Audit Report
with open(output_json_path, "w", encoding="utf-8") as jf:
    json.dump({
        "summary": {
            "total_skus": 389,
            "color_config": COLOR_PALETTE_CONFIG
        },
        "categories": categories_report
    }, jf, ensure_ascii=False, indent=2)
print(f"Phase 1 Audit Report written to {output_json_path}")

# 4. Phase 2: Write modified palettes and categories to master.json
if master_path.exists():
    with open(master_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)
        
    sku_registry = master_data.get("sku_registry", {})
    updated_master_count = 0
    for pic, entry in sku_registry.items():
        if pic in sku_colors_map:
            cat = sku_category_map[pic]
            colors = sku_colors_map[pic]
            
            # Update category
            entry["category"] = cat
            
            # Update palette
            branding = entry.setdefault("branding", {})
            palette = branding.setdefault("palette", {})
            palette["primary"] = colors["primary"]
            palette["accent"] = colors["accent"]
            palette["background"] = "#FFFFFF"
            branding["palette_source"] = "Canonical/Official_DB"
            
            updated_master_count += 1
            
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
    print(f"Phase 2: Updated {updated_master_count} SKUs in master.json")
else:
    print("Error: master.json not found!")

# 5. Phase 2: Write modified palettes and categories to individual passport JSON files
updated_json_count = 0
for pic, colors in sku_colors_map.items():
    cat = sku_category_map[pic]
    json_name = pic.replace(".jpg", ".json")
    json_path = passports_dir / json_name
    
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        data["category"] = cat
        branding = data.setdefault("branding", {})
        palette = branding.setdefault("palette", {})
        palette["primary"] = colors["primary"]
        palette["accent"] = colors["accent"]
        palette["background"] = "#FFFFFF"
        branding["palette_source"] = "Canonical/Official_DB"
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        updated_json_count += 1
    else:
        print(f"Warning: {json_name} passport file not found!")

print(f"Phase 2: Updated {updated_json_count} individual passport JSON files.")
