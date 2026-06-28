import csv
import json
import re
from pathlib import Path

sku_path = Path("SSOT/SKU.csv")
percent_skus_path = Path("SSOT/percent_skus.csv")
master_path = Path("SSOT/master.json")
passports_dir = Path("pipeline/passports")

# 1. Load percent_skus.csv targets
percent_targets = {}
with open(percent_skus_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        pic = row.get("picture", "").strip()
        if pic:
            # Extract percentage from active ingredient
            ai = row.get("active_ingredient", "")
            pct_match = re.search(r'(\d+(?:\.\d+)?%)', ai)
            pct = pct_match.group(1) if pct_match else None
            
            # Format minimal dosage
            dosage_val = float(row.get("minimal_dosage", 0))
            dosage_str = str(int(dosage_val)) if dosage_val.is_integer() else str(dosage_val)
            unit = row.get("dosage_type", "").strip()
            
            # Combined dosage display
            if pct:
                percent_targets[pic] = f"{dosage_str}{unit}/{pct}"

print(f"Loaded {len(percent_targets)} percent dosage targets.")

# 2. Update passport JSON files
json_files = list(passports_dir.glob("*.json"))
updated_json_count = 0

for jf_path in json_files:
    pic_name = jf_path.name.replace(".json", ".jpg")
    with open(jf_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    disp = data.get("label_content", {}).get("dosage_display", "")
    new_disp = None
    
    if pic_name in percent_targets:
        new_disp = percent_targets[pic_name]
    elif disp:
        # Remove space between number and letters
        new_disp = re.sub(r'(\d+(?:\.\d+)?)\s+([a-zA-Z]+)', r'\1\2', disp)
        
    if new_disp and new_disp != disp:
        data.setdefault("label_content", {})["dosage_display"] = new_disp
        with open(jf_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        updated_json_count += 1

print(f"Updated {updated_json_count} JSON passport files.")

# 3. Update master.json
if master_path.exists():
    with open(master_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)
        
    sku_registry = master_data.get("sku_registry", {})
    updated_master_count = 0
    
    for pic, entry in sku_registry.items():
        disp = entry.get("dosage_display")
        # If it was null or had space, let's get the target dosage_display from the updated JSON passport
        json_path = passports_dir / pic.replace(".jpg", ".json")
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
            new_disp = json_data.get("label_content", {}).get("dosage_display")
            
            # Update entry in master.json
            if new_disp and new_disp != disp:
                entry["dosage_display"] = new_disp
                updated_master_count += 1
                
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
        
    print(f"Updated {updated_master_count} entries in master.json.")
else:
    print("Warning: master.json not found!")

print("Sync completed successfully.")
