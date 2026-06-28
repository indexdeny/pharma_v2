import os
import sys
from PIL import Image

# Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# === НАСТРОЙКИ КОНВЕРТАЦИИ ===
SOURCE_DIR = "render_output/raw"  # Папка с оригинальными PNG 1024x1024
if os.path.exists("images"):
    SOURCE_DIR = "images"

OUTPUT_DIR = "output"       # Целевая папка для готовых WebP
TARGET_SIZE = (1600, 1600)  # Меняй на (1200, 1200), если 1600 выйдет плохо
MAX_FILE_SIZE_KB = 500     # Жесткий лимит веса файла

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

def process_batch():
    if not os.path.exists(SOURCE_DIR):
        print(f"[ERROR] Source directory '{SOURCE_DIR}' not found.")
        return

    files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"[START] Found {len(files)} files for conversion to {TARGET_SIZE[0]}x{TARGET_SIZE[1]} px...")
    
    success_count = 0
    for file_name in files:
        source_path = os.path.join(SOURCE_DIR, file_name)
        base_name, _ = os.path.splitext(file_name)
        
        # Сохраняем то же имя, но меняем расширение на .webp
        output_name = f"{base_name}.webp"
        output_path = os.path.join(OUTPUT_DIR, output_name)
        
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

if __name__ == "__main__":
    process_batch()
