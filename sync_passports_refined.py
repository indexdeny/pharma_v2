import json
from pathlib import Path

passports_dir = Path("pipeline/passports")
master_path = Path("SSOT/master.json")

targets = {
    "11-min.jpg": {"layout": "10 pills per blister, 3 blisters"},
    "36-min.jpg": {"layout": "10 pills per blister, 3 blisters"},
    "277-min.jpg": {"layout": "10 pills per blister, 6 blisters"}
}

# 1. Update individual JSON files
for pic, cfg in targets.items():
    json_name = pic.replace(".jpg", ".json")
    json_path = passports_dir / json_name
    
    if json_path.exists():
        print(f"Updating {json_path}...")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        data["packaging_geometry"] = "BLISTER"
        data["render_priority"] = "secondary_box"
        
        # render_config
        rc = data.setdefault("render_config", {})
        rc["primary_render_target"] = "carton_box"
        rc["future_dual_shot_enabled"] = False
        rc["scene_archetype"] = "thick_blister_carton"
        
        # secondary_packaging
        sp = data.setdefault("secondary_packaging", {})
        sp["dimensions"] = "115x55x48mm"
        
        # internal_unit
        iu = data.setdefault("internal_unit", {})
        iu["type"] = "Pills"
        iu["material"] = "Blister (PVC/Aluminium)"
        iu["layout"] = cfg["layout"]
        iu["leaflet"] = None
        iu["min_pills_per_unit"] = 10
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print(f"Warning: {json_path} not found!")

# 2. Update master.json
if master_path.exists():
    print(f"Updating {master_path}...")
    with open(master_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)
        
    sku_registry = master_data.setdefault("sku_registry", {})
    
    for pic, cfg in targets.items():
        if pic in sku_registry:
            entry = sku_registry[pic]
            entry["packaging_geometry"] = "BLISTER"
            
            # render_config
            rc = entry.setdefault("render_config", {})
            rc["primary_render_target"] = "carton_box"
            rc["future_dual_shot_enabled"] = False
            rc["scene_archetype"] = "thick_blister_carton"
            
            # secondary_packaging
            sp = entry.setdefault("secondary_packaging", {})
            sp["dimensions"] = "115x55x48mm"
            
            # internal_unit
            iu = entry.setdefault("internal_unit", {})
            iu["type"] = "Pills"
            iu["material"] = "Blister (PVC/Aluminium)"
            iu["layout"] = cfg["layout"]
            iu["leaflet"] = None
            iu["min_pills_per_unit"] = 10
            
            sku_registry[pic] = entry
            print(f"Updated {pic} in master.json")
        else:
            print(f"Warning: {pic} not found in master.json sku_registry!")
            
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
else:
    print(f"Warning: {master_path} not found!")

print("Refined sync completed successfully.")
