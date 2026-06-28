import os
import sys
from PIL import Image

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# === НАСТРОЙКИ КОНВЕРТАЦИИ (config.yaml via src/utils.py) ===
# Значения по умолчанию идентичны оригиналу (1600x1600, лимит 500KB);
# пути привязаны к корню проекта.
import argparse
from src.utils import load_config, resolve_path

_CFG = load_config()
_IMG = _CFG["image_processor"]

SOURCE_DIR = str(resolve_path(_IMG["source_dir"]))   # Папка с оригинальными PNG
_legacy_images = resolve_path("images")
if _legacy_images.exists():                          # legacy override (как в оригинале)
    SOURCE_DIR = str(_legacy_images)

OUTPUT_DIR = str(resolve_path(_IMG["output_dir"]))   # Целевая папка для готовых WebP
TARGET_SIZE = tuple(_IMG["target_size"])             # (1600, 1600) по умолчанию
MAX_FILE_SIZE_KB = _IMG["max_file_size_kb"]          # Жесткий лимит веса файла

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def save_webp_with_weight_limit(img, output_path, max_size_kb):
    """
    Динамически подбирает качество WebP, чтобы файл весил меньше max_size_kb
    """
    quality = 95  # Стартуем с отличного качества
    step = 4      # Шаг снижения качества при перевесе
    
    while quality > 15:
        # Пробуем сохранить во временный буфер/файл
        img.save(output_path, "WEBP", quality=quality, method=6) # method=6 включает самую глубокую оптимизацию WebP
        file_size_kb = os.path.getsize(output_path) / 1024
        
        # Если уложились в лимит — выходим из цикла
        if file_size_kb <= max_size_kb:
            print(f"[SUCCESS] {os.path.basename(output_path)} | Weight: {file_size_kb:.1f} KB | Quality: {quality}%")
            return True
        
        quality -= step
        
    print(f"[WARNING] File {os.path.basename(output_path)} could not be compressed below {max_size_kb} KB!")
    return False

def process_batch(resume: bool = False) -> bool:
    if not os.path.exists(SOURCE_DIR):
        print(f"[ERROR] Source directory '{SOURCE_DIR}' not found.")
        return False

    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"[START] Found {len(files)} files for conversion to {TARGET_SIZE[0]}x{TARGET_SIZE[1]} px...")
    
    success_count = 0
    for file_name in files:
        source_path = os.path.join(SOURCE_DIR, file_name)
        base_name, _ = os.path.splitext(file_name)
        
        # Сохраняем то же имя, но меняем расширение на .webp
        output_name = f"{base_name}.webp"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        # Resume: пропускаем уже сконвертированные файлы (без дублирования).
        if resume and os.path.exists(output_path):
            print(f"[SKIP] {output_name} — already exists (resume).")
            continue

        try:
            with Image.open(source_path) as img:
                # Проверяем пропорции (должно быть 1:1)
                if img.size[0] != img.size[1]:
                    print(f"[WARNING] File {file_name} has non-square proportions {img.size}. Forcing 1:1 aspect ratio.")
                
                # Апскейл с фильтром LANCZOS для сохранения читаемости текста фармацевтических шрифтов
                resized_img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                
                # Сохраняем с контролем веса
                if save_webp_with_weight_limit(resized_img, output_path, MAX_FILE_SIZE_KB):
                    success_count += 1
                    
        except Exception as e:
            print(f"[ERROR] Error processing {file_name}: {e}")
            
    print(f"\n[DONE] Conversion completed! Successfully processed: {success_count}/{len(files)} images.")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="PharmaGen PRO — Stage 3 image processor (raw PNG -> final WEBP)"
    )
    parser.add_argument("--resume", action="store_true",
                        help="Skip files whose .webp already exists in the output dir")
    args = parser.parse_args()
    ok = process_batch(resume=args.resume)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
