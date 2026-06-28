"""
PHARMAGEN PRO — Render QA (OCR Post-Render Quality Assurance)
Version: 1.0 (2026-06-04) — P8.0

PURPOSE:
    Non-blocking diagnostic module. Runs after image generation.
    For each PNG in render_output/processed/, extracts text via OCR
    and cross-references the corresponding passport JSON to verify:
      1. brand_name is present in the rendered image
      2. brand_name does NOT appear more than 2 times (duplication guard)
      3. Dosage numeric value appears in image
      4. Unit count number appears in image

    Outputs a Markdown report to docs/RENDER_QA_REPORT.md.
    NEVER blocks the pipeline. Gracefully handles missing Tesseract.

USAGE:
    python render_qa.py
    python render_qa.py --dir render_output/processed
    python render_qa.py --passports pipeline/passports
    python render_qa.py --limit 20

DEPENDENCIES:
    pip install pytesseract Pillow
    Tesseract binary: https://github.com/UB-Mannheim/tesseract/wiki
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import json
import re
import os
import argparse
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_PROCESSED_DIR = Path("render_output/processed")
DEFAULT_PASSPORTS_DIR = Path("pipeline/passports")
DEFAULT_REPORT_PATH   = Path("docs/RENDER_QA_REPORT.md")

# Maximum allowed occurrences of brand_name in OCR text before flagging duplicate
MAX_BRAND_OCCURRENCES = 2

# Minimum OCR text length to consider extraction valid
MIN_OCR_TEXT_LENGTH = 20

# ─────────────────────────────────────────────────────────────────────────────
# OCR BACKEND
# ─────────────────────────────────────────────────────────────────────────────

_TESSERACT_AVAILABLE = False
_TESSERACT_ERROR = ""

try:
    import pytesseract
    from PIL import Image
    import shutil

    # Quick check if tesseract is in PATH, if not try default Windows paths
    if not shutil.which("tesseract"):
        possible_paths = [
            Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Tesseract-OCR" / "tesseract.exe",
            Path(os.environ.get("LocalAppData", "")) / "Programs" / "Tesseract-OCR" / "tesseract.exe",
        ]
        for p in possible_paths:
            if p.exists():
                pytesseract.pytesseract.tesseract_cmd = str(p)
                break

    # Quick sanity check
    pytesseract.get_tesseract_version()
    _TESSERACT_AVAILABLE = True
except ImportError:
    _TESSERACT_ERROR = "pytesseract not installed. Run: pip install pytesseract"
except Exception as e:
    _TESSERACT_ERROR = f"Tesseract binary not found or not configured: {e}"


def extract_text(image_path: Path) -> tuple[bool, str]:
    """
    Run OCR on a single image.
    Returns (success, text_or_error).
    """
    if not _TESSERACT_AVAILABLE:
        return False, _TESSERACT_ERROR
    try:
        img = Image.open(image_path)
        # Use both standard and --psm 6 (uniform text block) for better coverage
        text = pytesseract.image_to_string(img, config="--psm 6")
        return True, text
    except Exception as e:
        return False, str(e)


# ─────────────────────────────────────────────────────────────────────────────
# PASSPORT LOADER
# ─────────────────────────────────────────────────────────────────────────────

def load_passport(sku_stem: str, passports_dir: Path) -> dict | None:
    """Load the JSON passport for a given SKU stem."""
    path = passports_dir / f"{sku_stem}.json"
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# QA CHECKS
# ─────────────────────────────────────────────────────────────────────────────

def extract_numeric(s: str) -> str:
    """Extract the first numeric value (including decimals) from a string."""
    m = re.search(r"\d+(?:[.,]\d+)?", s or "")
    return m.group(0).replace(",", ".") if m else ""


def check_image(image_path: Path, passport: dict) -> dict:
    """
    Run OCR and perform QA checks against passport data.
    Returns a result dict with check outcomes.
    """
    result = {
        "sku": image_path.stem,
        "ocr_ok": False,
        "ocr_error": "",
        "brand_found": None,
        "brand_duplicated": None,
        "dosage_found": None,
        "count_found": None,
        "status": "UNKNOWN",
        "flags": [],
    }

    # Extract expected values from passport
    brand_name        = (passport.get("brand_name") or "").strip()
    active_ingredient = (passport.get("active_ingredient") or "").strip()
    product_name      = (passport.get("product_name") or "").strip()
    
    label         = passport.get("label_content", {})
    dosage_raw    = (label.get("dosage_display") or "").strip()
    unit_raw      = (label.get("unit_count_display") or "").strip()

    dosage_num = extract_numeric(dosage_raw)
    unit_num   = extract_numeric(unit_raw)

    # OCR
    ok, text = extract_text(image_path)
    result["ocr_ok"] = ok

    if not ok:
        result["ocr_error"] = text
        result["status"] = "UNAVAILABLE"
        result["flags"].append(f"OCR unavailable: {text[:80]}")
        return result

    text_lower = text.lower()

    # Collect all possible brand/ingredient names to check
    name_targets = set()
    for name in [brand_name, active_ingredient, product_name]:
        if name:
            clean_name = name.split("(")[0].strip()
            if clean_name:
                name_targets.add(clean_name.lower())

    # Check 1: brand/ingredient present
    if name_targets:
        brand_found = False
        brand_duplicated = False
        counts_found = []
        for target in name_targets:
            count = len(re.findall(re.escape(target), text_lower))
            if count >= 1:
                brand_found = True
            if count > MAX_BRAND_OCCURRENCES:
                brand_duplicated = True
            counts_found.append(f"'{target}': {count}x")
            
        result["brand_found"] = brand_found
        result["brand_duplicated"] = brand_duplicated
        
        if not brand_found:
            result["flags"].append(f"MISSING brand/ingredient from {sorted(list(name_targets))}")
        if brand_duplicated:
            result["flags"].append(f"DUPLICATE brand/ingredient ({', '.join(counts_found)}) — text duplication risk")

    # Check 2: dosage numeric present
    if dosage_num:
        result["dosage_found"] = bool(re.search(rf"\b{re.escape(dosage_num)}\b", text))
        if not result["dosage_found"]:
            result["flags"].append(f"MISSING dosage value '{dosage_num}' (from '{dosage_raw}')")

    # Check 3: unit count numeric present
    if unit_num:
        result["count_found"] = bool(re.search(rf"\b{re.escape(unit_num)}\b", text))
        if not result["count_found"]:
            result["flags"].append(f"MISSING unit count value '{unit_num}' (from '{unit_raw}')")

    # Overall status: OK, SOFT_FAIL, or HARD_FAIL
    # HARD_FAIL if critical numbers are missing or OCR is empty
    critical_missing = (
        result["dosage_found"] is False
        or result["count_found"] is False
    )
    
    brand_missing_or_dup = (
        result["brand_found"] is False
        or result["brand_duplicated"] is True
    )

    if len(text) < MIN_OCR_TEXT_LENGTH:
        result["status"] = "HARD_FAIL"
        result["flags"].append("EMPTY_OCR: OCR returned very little text - image may be blank or purely graphical")
    elif critical_missing:
        result["status"] = "HARD_FAIL"
    elif brand_missing_or_dup:
        result["status"] = "SOFT_FAIL"
    else:
        result["status"] = "OK"

    return result


# ─────────────────────────────────────────────────────────────────────────────
# REPORT WRITER
# ─────────────────────────────────────────────────────────────────────────────

def bool_icon(value) -> str:
    """Convert bool/None to a readable icon for Markdown."""
    if value is None:
        return "—"
    return "OK" if value else "FAIL"


def dup_icon(value) -> str:
    """Convert brand_duplicated bool/None to a readable icon for Markdown. True means FAIL (DUPLICATE)."""
    if value is None:
        return "—"
    return "DUPLICATE" if value else "OK"


def write_report(results: list[dict], report_path: Path):
    """Write a Markdown QA report."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    total      = len(results)
    ok_count   = sum(1 for r in results if r["status"] == "OK")
    soft_fails = sum(1 for r in results if r["status"] == "SOFT_FAIL")
    hard_fails = sum(1 for r in results if r["status"] == "HARD_FAIL")
    unavail    = sum(1 for r in results if r["status"] == "UNAVAILABLE")

    flagged = [r for r in results if r["flags"]]
    hard_flagged = [r for r in results if r["status"] == "HARD_FAIL"]

    lines = [
        f"# RENDER QA REPORT",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Pipeline: P12.0",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Total images checked | {total} |",
        f"| OK (all checks pass) | {ok_count} |",
        f"| SOFT_FAIL (brand missing/duplicated only) | {soft_fails} |",
        f"| HARD_FAIL (critical numbers missing / empty) | {hard_fails} |",
        f"| OCR UNAVAILABLE | {unavail} |",
        f"",
    ]

    if not _TESSERACT_AVAILABLE:
        lines += [
            f"> [!WARNING]",
            f"> Tesseract OCR is not available: {_TESSERACT_ERROR}",
            f"> Install Tesseract and pytesseract to enable OCR checks.",
            f"",
        ]

    if hard_flagged:
        lines += [
            f"## HARD_FAIL — Prioritized Manual Review List",
            f"These SKUs failed critical numeric checks (dosage or unit count) or returned empty OCR text.",
            f"",
            f"| SKU | Dosage Found | Count Found | Details |",
            f"|---|---|---|---|",
        ]
        for r in hard_flagged:
            flags_str = " · ".join(r["flags"]) if r["flags"] else ""
            lines.append(
                f"| {r['sku']} "
                f"| {bool_icon(r['dosage_found'])} "
                f"| {bool_icon(r['count_found'])} "
                f"| {flags_str} |"
            )
        lines.append("")

    lines += [
        f"## Results",
        f"",
        f"| SKU | Brand/Ingr Found | Brand Dup | Dosage Found | Count Found | Status |",
        f"|---|---|---|---|---|---|",
    ]

    for r in results:
        flags_str = " · ".join(r["flags"]) if r["flags"] else ""
        status_cell = f"**{r['status']}** — {flags_str}" if r["flags"] else r["status"]
        lines.append(
            f"| {r['sku']} "
            f"| {bool_icon(r['brand_found'])} "
            f"| {dup_icon(r['brand_duplicated'])} "
            f"| {bool_icon(r['dosage_found'])} "
            f"| {bool_icon(r['count_found'])} "
            f"| {status_cell} |"
        )

    if flagged:
        lines += [
            f"",
            f"## Flagged SKUs (Manual Review Recommended)",
            f"",
        ]
        for r in flagged:
            lines.append(f"### {r['sku']} ({r['status']})")
            for flag in r["flags"]:
                lines.append(f"- {flag}")
            lines.append("")

    lines += [
        f"",
        f"---",
        f"*render_qa.py v1.1 — PharmaGen PRO P12.0*",
    ]

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[DONE] Report written to: {report_path}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OCR post-render QA for PharmaGen PRO. Non-blocking diagnostic."
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=DEFAULT_PROCESSED_DIR,
        help=f"Directory of processed PNG images (default: {DEFAULT_PROCESSED_DIR})",
    )
    parser.add_argument(
        "--passports",
        type=Path,
        default=DEFAULT_PASSPORTS_DIR,
        help=f"Directory of JSON passports (default: {DEFAULT_PASSPORTS_DIR})",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help=f"Output report path (default: {DEFAULT_REPORT_PATH})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of images to check (default: all)",
    )
    args = parser.parse_args()

    if not _TESSERACT_AVAILABLE:
        print(f"[WARN] {_TESSERACT_ERROR}")
        print("[WARN] Proceeding — report will mark all as UNAVAILABLE.")

    if not args.dir.exists():
        print(f"[WARN] Processed images directory not found: {args.dir}")
        print(f"       No images to check. Writing empty report.")
        write_report([], args.report)
        return

    images = sorted(args.dir.glob("*.png"))
    if not images:
        print(f"[WARN] No PNG files found in {args.dir}")
        write_report([], args.report)
        return

    if args.limit:
        images = images[:args.limit]

    print(f"\n[START] Render QA — checking {len(images)} images in {args.dir}")
    print(f"        OCR backend: {'pytesseract OK' if _TESSERACT_AVAILABLE else 'UNAVAILABLE'}")
    print(f"        Passports:   {args.passports}")
    print(f"        Report:      {args.report}\n")

    results = []
    ok_count = 0

    for img_path in images:
        sku_stem = img_path.stem
        passport = load_passport(sku_stem, args.passports)

        if passport is None:
            result = {
                "sku": sku_stem,
                "ocr_ok": False,
                "ocr_error": "Passport JSON not found",
                "brand_found": None,
                "brand_duplicated": None,
                "dosage_found": None,
                "count_found": None,
                "status": "NO_PASSPORT",
                "flags": [f"Passport JSON not found: {args.passports / sku_stem}.json"],
            }
        else:
            result = check_image(img_path, passport)

        status = result["status"]
        icon = "[OK]       " if status == "OK" else f"[{status}]"
        flags_display = " | ".join(result["flags"][:2]) if result["flags"] else ""
        print(f"  {icon} {sku_stem:20s} {flags_display}")

        if status == "OK":
            ok_count += 1

        results.append(result)

    soft_count = sum(1 for r in results if r["status"] == "SOFT_FAIL")
    hard_count = sum(1 for r in results if r["status"] == "HARD_FAIL")
    print(f"\n  Total: {len(results)} | OK: {ok_count} | SOFT_FAIL: {soft_count} | HARD_FAIL: {hard_count}")
    write_report(results, args.report)


if __name__ == "__main__":
    main()
