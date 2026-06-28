"""
PHARMAGEN PRO: Image Post-Processor
Performs clean post-processing on generated images.
Converts to WEBP, exactly 2048x2048, maintaining aspect ratio.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
import argparse
import shutil
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    print("[ERROR] Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# Configuration
DEFAULT_INPUT_DIR = Path("render_output/raw")
DEFAULT_OUTPUT_DIR = Path("render_output/processed")
DEFAULT_FAILED_DIR = Path("render_output/failed")

def process_image(input_path: Path, output_dir: Path, failed_dir: Path = DEFAULT_FAILED_DIR) -> tuple[bool, str]:
    """
    Process a single image:
    1. Open the original PNG.
    2. Apply EXIF orientation normalization.
    3. Resize to exactly 1024x1024 px (LANCZOS, square 1:1).
    4. Save as PNG — format PNG, dimensions 1024x1024, no metadata.
    5. If failure occurs, preserve in failed_dir.
    """
    try:
        if not input_path.exists():
            return False, f"File not found: {input_path}"

        img = Image.open(input_path)

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Force WEBP output filename (Rule 15 constraint)
        output_stem = input_path.stem
        output_path = output_dir / f"{output_stem}.webp"

        # Step 1: EXIF orientation normalisation
        img_normalized = ImageOps.exif_transpose(img)

        # Step 2: Convert to RGB (handles RGBA, P, L modes safely)
        if img_normalized.mode != "RGB":
            img_normalized = img_normalized.convert("RGB")

        # Step 3: Resize to exactly 2048x2048 (Rule 15 constraint)
        img_resized = img_normalized.resize((2048, 2048), Image.LANCZOS)

        # Step 4: Save as WEBP — quality 85 to keep <= 500 KB
        img_resized.save(output_path, format="WEBP", quality=85)

        return True, f"{input_path.name} -> {output_path.name} (2048x2048 WEBP)"

    except Exception as e:
        # Save failed image copy to failed directory
        try:
            failed_dir.mkdir(parents=True, exist_ok=True)
            failed_path = failed_dir / input_path.name
            shutil.copy2(input_path, failed_path)
            error_msg = f"Saved to failed: {failed_path.name} | Error: {e}"
        except Exception as copy_err:
            error_msg = f"Could not copy to failed: {copy_err} | Original error: {e}"
            
        return False, f"{input_path.name}: ERROR - {error_msg}"


def main():
    parser = argparse.ArgumentParser(description="Clean PNG renders without destructive compression or forced resizing")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_DIR,
                        help=f"Input directory (default: {DEFAULT_INPUT_DIR})")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR,
                        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--failed", type=Path, default=DEFAULT_FAILED_DIR,
                        help=f"Failed directory (default: {DEFAULT_FAILED_DIR})")
    parser.add_argument("--file", type=str, default=None,
                        help="Process a single file instead of directory")
    args = parser.parse_args()
    
    args.output.mkdir(parents=True, exist_ok=True)
    
    if args.file:
        files = [args.input / args.file]
    else:
        files = sorted(args.input.glob("*.png"))
    
    if not files:
        print(f"[WARN] No PNG files found in {args.input}")
        return
    
    print(f"\n[START] Processing {len(files)} images -> PNG (Preserving original dimensions/quality)")
    print(f"        Output: {args.output}/\n")
    
    success_count = 0
    fail_count = 0
    
    for f in files:
        if not f.exists():
            print(f"  [SKIP] {f.name} — file not found")
            continue
            
        ok, msg = process_image(f, args.output, args.failed)
        if ok:
            success_count += 1
            print(f"  [OK] {msg}")
        else:
            fail_count += 1
            print(f"  [FAIL] {msg}")
    
    print(f"\n[DONE] Success: {success_count} | Failed: {fail_count}")


if __name__ == "__main__":
    main()
