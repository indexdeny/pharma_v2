"""
PharmaGen PRO — Automated Architecture Snapshot Generator
Version: 1.1 (2026-06-04) — P10.0

This script statically inspects the project's source code, configurations, 
and database states, producing:
  - docs/ARCHITECTURE_SNAPSHOT.md
  - docs/architecture_snapshot.json
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import os
import ast
import json
import csv
import re
from datetime import datetime
from pathlib import Path
from collections import Counter

ROOT_DIR = Path("c:/pharma_v2")
DOCS_DIR = ROOT_DIR / "docs"

# ─────────────────────────────────────────────────────────────────────────────
# 1. AST PYTHON FILE INSPECTOR
# ─────────────────────────────────────────────────────────────────────────────

def extract_python_file_info(filepath: Path) -> dict:
    """Statically parse a python file to extract metadata, classes, and functions."""
    try:
        content = filepath.read_text(encoding="utf-8")
        tree = ast.parse(content)
    except Exception as e:
        return {
            "file": str(filepath.relative_to(ROOT_DIR)).replace("\\", "/"),
            "size_bytes": filepath.stat().st_size,
            "error": str(e),
            "docstring": "Syntax Error / Parsing Failed",
            "functions": [],
            "classes": []
        }

    module_doc = ast.get_docstring(tree) or ""
    functions = []
    classes = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            # Reconstruct arguments signature
            args_str = ast.unparse(node.args)
            returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
            sig = f"def {node.name}({args_str}){returns}"
            func_doc = ast.get_docstring(node)
            doc_first_line = func_doc.split('\n')[0].strip() if func_doc else ""
            functions.append({
                "name": node.name,
                "signature": sig,
                "docstring": doc_first_line
            })
        elif isinstance(node, ast.ClassDef):
            class_doc = ast.get_docstring(node) or ""
            class_methods = []
            class_fields = []
            
            for subnode in node.body:
                if isinstance(subnode, ast.FunctionDef):
                    args_str = ast.unparse(subnode.args)
                    returns = f" -> {ast.unparse(subnode.returns)}" if subnode.returns else ""
                    sig = f"def {subnode.name}({args_str}){returns}"
                    m_doc = ast.get_docstring(subnode)
                    m_doc_first = m_doc.split('\n')[0].strip() if m_doc else ""
                    class_methods.append({
                        "name": subnode.name,
                        "signature": sig,
                        "docstring": m_doc_first
                    })
                elif isinstance(subnode, ast.AnnAssign):
                    target_name = ast.unparse(subnode.target)
                    type_name = ast.unparse(subnode.annotation)
                    class_fields.append(f"{target_name}: {type_name}")
                elif isinstance(subnode, ast.Assign):
                    for target in subnode.targets:
                        target_name = ast.unparse(target)
                        class_fields.append(target_name)
            
            classes.append({
                "name": node.name,
                "docstring": class_doc.split('\n')[0].strip() if class_doc else "",
                "methods": class_methods,
                "fields": class_fields
            })

    return {
        "file": str(filepath.relative_to(ROOT_DIR)).replace("\\", "/"),
        "size_bytes": filepath.stat().st_size,
        "docstring": module_doc.split('\n')[0].strip() if module_doc else "",
        "functions": functions,
        "classes": classes
    }


def scan_python_modules() -> list[dict]:
    """Scan all production python files in root, pharma_pkg/, and schemas/."""
    modules = []
    
    # Root python files
    root_py = ["gemini_image_generator.py", "image_postprocessor.py", "pass_tomd.py", "render_qa.py", "verification_agent.py"]
    for name in root_py:
        path = ROOT_DIR / name
        if path.exists():
            modules.append(extract_python_file_info(path))
            
    # pharma_pkg
    pkg_dir = ROOT_DIR / "pharma_pkg"
    if pkg_dir.exists():
        for path in sorted(pkg_dir.glob("*.py")):
            modules.append(extract_python_file_info(path))
            
    # schemas
    schema_dir = ROOT_DIR / "schemas"
    if schema_dir.exists():
        for path in sorted(schema_dir.glob("*.py")):
            modules.append(extract_python_file_info(path))
            
    return modules

# ─────────────────────────────────────────────────────────────────────────────
# 2. CONFIGURATION & STATE EXTRACTOR
# ─────────────────────────────────────────────────────────────────────────────

def extract_constants_from_generator() -> dict:
    """Statically parse constants from gemini_image_generator.py."""
    constants = {}
    path = ROOT_DIR / "gemini_image_generator.py"
    if not path.exists():
        return constants
        
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper() and len(target.id) > 2:
                        val_str = ast.unparse(node.value)
                        constants[target.id] = val_str
    except Exception as e:
        constants["error"] = str(e)
        
    return constants


def analyze_sku_csv() -> dict:
    """Parse SKU.csv database and summarize its package types and geometries."""
    path = ROOT_DIR / "SSOT" / "SKU.csv"
    info = {
        "exists": False,
        "total_rows": 0,
        "package_types": {},
        "unique_primary_geometries": []
    }
    if not path.exists():
        return info
        
    info["exists"] = True
    package_types = Counter()
    geometries = set()
    
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            info["total_rows"] += 1
            pkg = row.get("package_type", "").strip().lower()
            if pkg:
                package_types[pkg] += 1
            geom = row.get("primary_geometry", "").strip()
            if geom:
                geometries.add(geom)
                
    info["package_types"] = dict(package_types)
    info["unique_primary_geometries"] = sorted(list(geometries))
    return info


def analyze_passports() -> dict:
    """Dry-run router and verifier on JSON passports to count template, scene, and quality metrics."""
    from pass_tomd import agent_1_router
    from verification_agent import agent_2_verifier
    
    passports_dir = ROOT_DIR / "pipeline" / "passports"
    info = {
        "total_passports": 0,
        "template_distribution": {},
        "scene_archetypes": {},
        "empty_active_ingredient_count": 0,
        "empty_active_ingredient_stems": [],
        "low_confidence_stems": []
    }
    
    if not passports_dir.exists():
        return info
        
    passport_files = list(passports_dir.glob("*.json"))
    info["total_passports"] = len(passport_files)
    
    templates = Counter()
    scenes = Counter()
    empty_ai_count = 0
    empty_ai_stems = []
    low_confidence_stems = []
    
    for path in passport_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            # Determine template routing using the production router
            template_id, _ = agent_1_router(data)
            templates[template_id] += 1
            
            # Scene archetype
            scene = data.get("render_config", {}).get("scene_archetype", "")
            if scene:
                scenes[scene] += 1
            
            # Check empty active ingredient
            ai = data.get("active_ingredient") or ""
            if not ai.strip():
                empty_ai_count += 1
                empty_ai_stems.append(path.stem)
                
            # Run verifier to check confidence
            res = agent_2_verifier(data)
            if not res["verified"]:
                low_confidence_stems.append({
                    "stem": path.stem,
                    "confidence": res["confidence"],
                    "warnings": res["warnings"]
                })
        except Exception:
            pass
            
    info["template_distribution"] = dict(templates)
    info["scene_archetypes"] = dict(scenes)
    info["empty_active_ingredient_count"] = empty_ai_count
    info["empty_active_ingredient_stems"] = sorted(empty_ai_stems)
    info["low_confidence_stems"] = sorted(low_confidence_stems, key=lambda x: x["stem"])
    return info


def analyze_design_specs() -> dict:
    """Summarize sub-brands and photosensitive rules from master specs."""
    path = ROOT_DIR / "SSOT" / "master_pharma_design_specs.json"
    info = {
        "exists": False,
        "sub_brands": [],
        "photosensitive_compounds": []
    }
    if not path.exists():
        return info
        
    info["exists"] = True
    try:
        specs = json.loads(path.read_text(encoding="utf-8"))
        for k, v in specs.get("sub_brand_visual_rules", {}).items():
            if isinstance(v, dict):
                info["sub_brands"].append({
                    "key": k,
                    "triggers": v.get("triggers", []),
                    "finish_override": v.get("finish_override", ""),
                    "surface_treatment": v.get("surface_treatment", "")
                })
        for k, v in specs.get("photosensitive_compounds", {}).items():
            if isinstance(v, dict):
                info["photosensitive_compounds"].append({
                    "key": k,
                    "triggers": v.get("triggers", []),
                    "container_required": v.get("container_required", ""),
                    "material": v.get("material", "")
                })
    except Exception:
        pass
        
    return info


def get_failures_breakdown() -> dict:
    """Parse failures.log and count failures by stage."""
    log_path = ROOT_DIR / "render_output" / "failed_logs" / "failures.log"
    breakdown = Counter()
    if not log_path.exists():
        return {}
    try:
        content = log_path.read_text(encoding="utf-8")
        for match in re.finditer(r"stage:\s*(.*)", content):
            stage_val = match.group(1).strip()
            breakdown[stage_val] += 1
    except Exception:
        pass
    return dict(breakdown)


def get_render_state() -> dict:
    """Count files in render directories and calculate current completion progress."""
    raw_dir = ROOT_DIR / "render_output" / "raw"
    proc_dir = ROOT_DIR / "render_output" / "processed"
    fail_dir = ROOT_DIR / "render_output" / "failed"
    progress_path = ROOT_DIR / "gemini_rpa_progress_v23.txt"
    passports_dir = ROOT_DIR / "pipeline" / "passports"
    
    raw_count = len(list(raw_dir.glob("*.png"))) if raw_dir.exists() else 0
    proc_count = len(list(proc_dir.glob("*.png"))) if proc_dir.exists() else 0
    fail_count = len(list(fail_dir.glob("*.png"))) if fail_dir.exists() else 0
    
    passport_stems = set()
    if passports_dir.exists():
        passport_stems = {p.stem for p in passports_dir.glob("*.json")}
        
    processed_stems_raw = set()
    if proc_dir.exists():
        processed_stems_raw = {f.stem for f in proc_dir.glob("*.png")}
        
    got_stems = {stem.split("_dup")[0] for stem in processed_stems_raw}
    
    coverage_missing = sorted(list(passport_stems - got_stems))
    coverage_extra = sorted(list(got_stems - passport_stems))
    coverage_percentage = (len(passport_stems - set(coverage_missing)) / len(passport_stems) * 100) if passport_stems else 0.0
    
    progress_count = 0
    if progress_path.exists():
        try:
            skus_done = set()
            for line in progress_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    skus_done.add(line.strip())
            progress_count = len(skus_done)
        except Exception:
            pass
            
    return {
        "raw_images_count": raw_count,
        "processed_images_count": proc_count,
        "failed_images_count": fail_count,
        "progress_count": progress_count,
        "failure_breakdown": get_failures_breakdown(),
        "coverage_missing": coverage_missing,
        "coverage_extra": coverage_extra,
        "coverage_percentage": coverage_percentage
    }

# ─────────────────────────────────────────────────────────────────────────────
# 3. REPORT BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def build_markdown_report(data: dict) -> str:
    """Generate docs/ARCHITECTURE_SNAPSHOT.md markdown string."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines = [
        f"# PHARMAGEN PRO — ARCHITECTURE SNAPSHOT",
        f"> **Generated:** {now_str} | **Introspection Agent:** P10.0 Snapshot Engine",
        f"",
        f"---",
        f"",
        f"## 1. Pipeline Flow",
        f"",
        f"```",
        f"INPUT (389 source JPG images)",
        f"       │",
        f"       ▼",
        f"┌─────────────────────────────────────────────────────┐",
        f"│  STAGE 0: ANALYSIS (Manual / Workflow)              │",
        f"│  Workflow: /analyze-pharma                          │",
        f"│  Input:    input/{{sku_id}}.jpg + SSOT/master.json    │",
        f"│  Output:   pipeline/passports/{{sku_id}}.json (v2.1)  │",
        f"└─────────────────────────────────────────────────────┘",
        f"       │",
        f"       ▼",
        f"┌─────────────────────────────────────────────────────┐",
        f"│  STAGE 1: VERIFICATION (Deterministic QA)           │",
        f"│  Script:   verification_agent.py (v2.3)             │",
        f"│  Checks:   12 checks | Threshold: confidence ≥ 0.75  │",
        f"└─────────────────────────────────────────────────────┘",
        f"       │",
        f"       ▼",
        f"┌─────────────────────────────────────────────────────┐",
        f"│  STAGE 2: PASSPORT GENERATION (Production Core)     │",
        f"│  Script:   pass_tomd.py                             │",
        f"│  Input:    pipeline/passports/*.json (389 files)    │",
        f"│  Output:   pipeline/passports.markdown/*.md         │",
        f"└─────────────────────────────────────────────────────┘",
        f"       │",
        f"       ▼",
        f"┌─────────────────────────────────────────────────────┐",
        f"│  STAGE 3: IMAGE GENERATION (RPA Automation)         │",
        f"│  Script:   gemini_image_generator.py                │",
        f"│  Output:   render_output/raw/{{sku_id}}.png           │",
        f"└─────────────────────────────────────────────────────┘",
        f"       │",
        f"       ▼",
        f"┌─────────────────────────────────────────────────────┐",
        f"│  STAGE 4: POST-PROCESSING (Active Production)       │",
        f"│  Script:   image_postprocessor.py                   │",
        f"│  Output:   render_output/processed/{{sku_id}}.png     │",
        f"└─────────────────────────────────────────────────────┘",
        f"       │",
        f"       ▼",
        f"OUTPUT (389 PNG renders, 1024×1024px, normalized)",
        f"```",
        f"",
        f"---",
        f"",
        f"## 2. Active Code Modules",
        f"",
        f"| Module / File | Size (Bytes) | Description | Functions | Classes |",
        f"|---|---|---|---|---|",
    ]
    
    for mod in data["modules"]:
        fn_count = len(mod["functions"])
        cls_count = len(mod["classes"])
        lines.append(f"| [`{mod['file']}`](file:///{ROOT_DIR.as_posix()}/{mod['file']}) | {mod['size_bytes']:,} | {mod['docstring']} | {fn_count} | {cls_count} |")
        
    lines += [
        f"",
        f"---",
        f"",
        f"## 3. Function & Class Declarations",
    ]
    
    for mod in data["modules"]:
        lines.append(f"### File: `{mod['file']}`")
        if mod["docstring"]:
            lines.append(f"> {mod['docstring']}")
            lines.append("")
            
        if not mod["functions"] and not mod["classes"]:
            lines.append("*No class or function declarations found.*")
            lines.append("")
            continue
            
        if mod["classes"]:
            for cls in mod["classes"]:
                lines.append(f"#### class `{cls['name']}`")
                if cls["docstring"]:
                    lines.append(f"- *Docstring:* {cls['docstring']}")
                if cls["fields"]:
                    fields_str = ", ".join(cls["fields"])
                    lines.append(f"- *Fields:* `{fields_str}`")
                for method in cls["methods"]:
                    lines.append(f"  * ` {method['signature']} ` — *{method['docstring'] or 'No docstring'}*")
                lines.append("")
                
        if mod["functions"]:
            lines.append(f"#### Functions:")
            for fn in mod["functions"]:
                lines.append(f"- ` {fn['signature']} `")
                if fn["docstring"]:
                    lines.append(f"  * {fn['docstring']}")
            lines.append("")

    lines += [
        f"---",
        f"",
        f"## 4. Routing System (pass_tomd.py)",
        f"",
        f"**Available Templates (TEMPLATE_MAP):**",
    ]
    
    for t_id in data["routing"]["templates"]:
        lines.append(f"- `{t_id}`")
        
    lines += [
        f"",
        f"**Router Docstring (agent_1_router):**",
        f"> {data['routing']['router_doc']}",
        f"",
        f"**Actual Template Distribution (389 Passports):**",
        f"",
        f"| Template | Assigned SKU Count | Percentage |",
        f"|---|---|---|",
    ]
    
    total_p = data["passports"]["total_passports"]
    for t_id, count in sorted(data["passports"]["template_distribution"].items()):
        pct = (count / total_p * 100) if total_p else 0
        lines.append(f"| `{t_id}` | {count} | {pct:.1f}% |")
        
    lines += [
        f"",
        f"---",
        f"",
        f"## 5. Verification Rules (verification_agent.py)",
        f"",
        f"* **Production Confidence Threshold:** ` {data['verification']['threshold']} `",
        f"",
        f"| Check ID | Heuristic Rule | Weight / Penalty |",
        f"|---|---|---|",
    ]
    
    for check in data["verification"]["checks"]:
        lines.append(f"| CHECK {check['number']} | {check['description']} | **{check['weight']}** |")
        
    lines += [
        f"",
        f"---",
        f"",
        f"## 6. SSOT Databases & Design Specs",
        f"",
        f"### SSOT/SKU.csv Statistics",
        f"* **Total Rows:** {data['sku_csv']['total_rows']}",
        f"* **Unique Primary Geometries:**",
    ]
    
    for geom in data["sku_csv"]["unique_primary_geometries"]:
        lines.append(f"  - `{geom}`")
        
    lines += [
        f"",
        f"**Distribution of package_type:**",
        f"",
        f"| package_type | Count |",
        f"|---|---|",
    ]
    
    for pkg, count in sorted(data["sku_csv"]["package_types"].items()):
        lines.append(f"| `{pkg}` | {count} |")
        
    lines += [
        f"",
        f"### Sub-Brand Visual Rules (master_pharma_design_specs.json)",
        f"",
        f"| Sub-Brand | Finish Override | Triggers | Surface Treatment |",
        f"|---|---|---|---|",
    ]
    
    for sb in data["design_specs"]["sub_brands"]:
        triggers_str = ", ".join(sb["triggers"])
        lines.append(f"| `{sb['key']}` | `{sb['finish_override']}` | {triggers_str} | {sb['surface_treatment']} |")
        
    lines += [
        f"",
        f"### Photosensitive Compounds & Container Overrides",
        f"",
        f"| Compound Key | Required Container | Material | Triggers |",
        f"|---|---|---|---|",
    ]
    
    for pc in data["design_specs"]["photosensitive_compounds"]:
        triggers_str = ", ".join(pc["triggers"][:5])
        if len(pc["triggers"]) > 5:
            triggers_str += "..."
        lines.append(f"| `{pc['key']}` | `{pc['container_required']}` | `{pc['material']}` | {triggers_str} |")
        
    lines += [
        f"",
        f"---",
        f"",
        f"## 7. Current Render Output State",
        f"",
        f"| Output Directory | Image Count | Status |",
        f"|---|---|---|",
        f"| `render_output/raw/` | {data['render_state']['raw_images_count']} | Raw generator output |",
        f"| `render_output/processed/` | {data['render_state']['processed_images_count']} | Post-processed 1024x1024 RGB normalizations |",
        f"| `render_output/failed/` | {data['render_state']['failed_images_count']} | Screenshot logs on Selenium exception (current files in failed/ dir) |",
        f"",
        f"* **Progress Count (done SKUs):** `{data['render_state']['progress_count']}` / {total_p}",
        f"* **Coverage:** `{total_p - len(data['render_state']['coverage_missing'])}` / {total_p} unique SKU ({data['render_state']['coverage_percentage']:.1f}%)",
    ]
    
    if data['render_state']['coverage_missing']:
        lines.append(f"  - **Missing SKU Stems:** {', '.join(f'`{s}`' for s in data['render_state']['coverage_missing'])}")
    else:
        lines.append(f"  - **Missing SKU Stems:** *None (100% coverage)*")
        
    if data['render_state']['coverage_extra']:
        lines.append(f"  - **Extra/Unmatched Stems:** {', '.join(f'`{s}`' for s in data['render_state']['coverage_extra'])}")
        
    lines += [
        f"",
        f"### Failure Breakdown (from failures.log)",
        f"> *Note: failure_breakdown is a historical/cumulative log of all generation attempts (including recovered/retried ones).* ",
        f"",
        f"| Stage of Failure | Count |",
        f"|---|---|",
    ]
    
    breakdown = data["render_state"].get("failure_breakdown", {})
    if breakdown:
        for stage, count in sorted(breakdown.items()):
            lines.append(f"| `{stage}` | {count} |")
    else:
        lines.append(f"| *No failures logged* | 0 |")
        
    lines += [
        f"",
        f"### Diagnostic Alerts & Quality Issues",
        f"",
        f"* **Empty Active Ingredients Count:** `{data['passports']['empty_active_ingredient_count']}`",
    ]
    
    empty_stems = data["passports"].get("empty_active_ingredient_stems", [])
    if empty_stems:
        lines.append(f"  - **Empty Stems:** {', '.join(f'`{s}`' for s in empty_stems)}")
        
    lines += [
        f"* **Low Confidence Passports (< 0.75):** `{len(data['passports'].get('low_confidence_stems', []))}`",
    ]
    
    low_stems = data["passports"].get("low_confidence_stems", [])
    if low_stems:
        lines.append(f"")
        lines.append(f"| SKU Stem | Confidence | Warnings |")
        lines.append(f"|---|---|---|")
        for ls in low_stems:
            warnings_str = " · ".join(ls["warnings"])
            lines.append(f"| `{ls['stem']}` | `{ls['confidence']:.2f}` | {warnings_str} |")
            
    lines += [
        f"",
        f"---",
        f"",
        f"## 8. Runtime Constants (gemini_image_generator.py)",
        f"",
        f"| Constant | Value | Description |",
        f"|---|---|---|",
    ]
    
    for c_name, c_val in sorted(data["constants"].items()):
        if c_name == "error":
            continue
        lines.append(f"| `{c_name}` | `{c_val}` | Static AST value |")
        
    lines += [
        f"",
        f"---",
        f"",
        f"## 9. Known Technical Debt & Backlog",
        f"",
        f"| Technical Debt Issue | Severity | Target Remediation |",
        f"|---|---|---|",
        f"| `schemas/analysis_passport.py` is a stub (477 bytes), not integrated | Low | Backlog |",
        f"| `pharma_pkg/package_mapping.yaml` (351 bytes) superseded by Python code | Low | Backlog |",
        f"| `protocol.md` v3.0 schema is roadmap, not implemented | Low | Roadmap |",
        f"| `_freeze_legacy/` contains 4 legacy subdirs never referenced | Info | Archive |",
        f"",
        f"---",
        f"*Architecture Snapshot generated automatically by generate_architecture_snapshot.py*",
    ]
    
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 4. MAIN ORCHESTRATION
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("[START] Building architecture snapshot...")
    
    modules = scan_python_modules()
    constants = extract_constants_from_generator()
    sku_csv = analyze_sku_csv()
    passports = analyze_passports()
    design_specs = analyze_design_specs()
    render_state = get_render_state()
    
    from pass_tomd import TEMPLATE_MAP, agent_1_router
    from verification_agent import agent_2_verifier, PRODUCTION_CONFIDENCE_THRESHOLD
    
    routing_info = {
        "templates": list(TEMPLATE_MAP.keys()),
        "router_doc": (agent_1_router.__doc__ or "").strip()
    }
    
    verifier_doc = (agent_2_verifier.__doc__ or "").strip()
    checks = []
    for match in re.finditer(r"CHECK\s+(\d+):\s+(.*?)\s+->\s+(-?\d+\.\d+)", verifier_doc):
        checks.append({
            "number": int(match.group(1)),
            "description": match.group(2).strip(),
            "weight": float(match.group(3))
        })
        
    verification_info = {
        "threshold": PRODUCTION_CONFIDENCE_THRESHOLD,
        "checks": checks
    }
    
    # Bundle all JSON data
    snapshot_data = {
        "modules": modules,
        "constants": constants,
        "sku_csv": sku_csv,
        "passports": passports,
        "design_specs": design_specs,
        "render_state": render_state,
        "routing": routing_info,
        "verification": verification_info
    }
    
    # Write JSON snapshot
    json_path = DOCS_DIR / "architecture_snapshot.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(snapshot_data, jf, indent=4)
    print(f"[DONE] Wrote JSON: {json_path}")
    
    # Build and Write Markdown snapshot
    markdown_report = build_markdown_report(snapshot_data)
    md_path = DOCS_DIR / "ARCHITECTURE_SNAPSHOT.md"
    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write(markdown_report)
    print(f"[DONE] Wrote Markdown: {md_path}")
    
    print("[SUCCESS] Architecture snapshot generated cleanly.")

if __name__ == "__main__":
    main()
