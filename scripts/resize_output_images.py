"""
PHARMAGEN: Output Image Resizer
Resizes .webp images from output/ into output/m_size/ (400x400) and
output/s_size/ (100x100) using crop-to-fill (cover), preserving originals.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("[ERROR] Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

SOURCE_DIR = Path("output")
M_DIR = Path("output/m_size")
S_DIR = Path("output/s_size")
M_SIZE = (400, 400)
S_SIZE = (100, 100)


def resize_cover(img: Image.Image, target_size: tuple[int, int]) -> Image.Image:
    """Scale to fully cover target_size preserving aspect ratio, then center-crop."""
    target_w, target_h = target_size
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = round(src_w * scale), round(src_h * scale)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def main() -> None:
    if not SOURCE_DIR.is_dir():
        print(f"[ERROR] Source folder not found: {SOURCE_DIR.resolve()}")
        sys.exit(1)

    M_DIR.mkdir(parents=True, exist_ok=True)
    S_DIR.mkdir(parents=True, exist_ok=True)

    source_files = sorted(SOURCE_DIR.glob("*.webp"))

    if not source_files:
        print(f"[WARN] No .webp files found directly in {SOURCE_DIR.resolve()}")
        return

    processed = 0
    for src_path in source_files:
        stem = src_path.stem
        with Image.open(src_path) as img:
            img = img.convert("RGBA") if img.mode not in ("RGB", "RGBA") else img

            m_img = resize_cover(img, M_SIZE)
            m_img.save(M_DIR / f"{stem}-m.webp", format="WEBP")

            s_img = resize_cover(img, S_SIZE)
            s_img.save(S_DIR / f"{stem}-s.webp", format="WEBP")

        processed += 1

    print(f"[DONE] Processed {processed} images.")
    print(f"  M ({M_SIZE[0]}x{M_SIZE[1]}) -> {M_DIR.resolve()}")
    print(f"  S ({S_SIZE[0]}x{S_SIZE[1]}) -> {S_DIR.resolve()}")


if __name__ == "__main__":
    main()
