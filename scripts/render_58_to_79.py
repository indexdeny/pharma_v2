import os, sys, time, glob, re, logging, shutil, subprocess
sys.path.insert(0, os.path.abspath("."))

from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

# Import PharmaGen PRO modules and config
from src.utils import load_config, get_path
from src.rpa_orchestrator import (
    create_driver,
    send_message,
    wait_for_chat_idle,
    wait_for_image_generation,
    download_blob_image,
    IMAGE_GENERATION_TIMEOUT,
    GEMINI_URL,
    MD_DIR,
    RAW_DIR,
    FAILED_DIR
)

# Custom log file path matching user reference log
LOG_FILENAME = f"gemini_rpa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG_FILEPATH = os.path.join("logs", LOG_FILENAME)

os.makedirs("logs", exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(FAILED_DIR, exist_ok=True)

# Configure logger to mirror the exact format of gemini_rpa_20260611_194525.log
file_handler = logging.FileHandler(LOG_FILEPATH, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))

log = logging.getLogger("pharma_rpa_render")
log.setLevel(logging.INFO)
log.handlers = [file_handler, console_handler]

# Target stems 58 to 79
TARGET_IDS = ['58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79']
TARGET_STEMS = [f"{i}-min" for i in TARGET_IDS]

def delete_sidebar_chats(driver: webdriver.Chrome):
    """
    Deletes all conversation items from Gemini sidebar before each new rendering session.
    """
    try:
        js_cleanup = """
        function deleteNextChat() {
            const links = Array.from(document.querySelectorAll('a[href*="/app/"]')).filter(a => {
                const h = a.getAttribute('href') || '';
                return h.match(/\\/app\\/[a-z0-9_-]{5,}/i);
            });
            if (links.length === 0) return false;

            const item = links[0];
            item.scrollIntoView({ block: 'center' });
            let p = item;
            for (let i = 0; i < 4 && p; i++) {
                p.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                p.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                p = p.parentElement;
            }

            let btn = null;
            p = item.parentElement;
            for (let i = 0; i < 5 && p; i++) {
                btn = p.querySelector('button[aria-label*="option"], button[aria-label*="Option"], button[aria-label*="More"], button[aria-label*="more"], button[aria-label*="меню"], button[aria-label*="Параметры"], button[aria-label*="Действия"], button[mat-menu-trigger-for], [data-test-id*="menu"]');
                if (btn) break;
                p = p.parentElement;
            }

            if (!btn) {
                const icons = Array.from(document.querySelectorAll('mat-icon[svgicon="more_vert"], mat-icon[svgicon*="more"]'));
                if (icons.length > 0) btn = icons[0].closest('button') || icons[0];
            }

            if (!btn) return false;
            btn.click();
            return true;
        }
        return deleteNextChat();
        """

        js_click_delete = """
        const candidates = Array.from(document.querySelectorAll('[role="menuitem"], button, div, span, a')).filter(el => {
            const txt = (el.innerText || '').trim().toLowerCase();
            const aria = (el.getAttribute('aria-label') || '').toLowerCase();
            return txt === 'delete' || txt === 'удалить' || txt.includes('delete chat') || txt.includes('удалить чат') || aria.includes('delete') || aria.includes('удалить');
        });
        if (candidates.length > 0) {
            candidates[0].click();
            return true;
        }
        return false;
        """

        js_confirm_modal = """
        const confirmBtns = Array.from(document.querySelectorAll('mat-dialog-container button, [role="dialog"] button, button[data-test-id*="confirm"]')).filter(el => {
            const txt = (el.innerText || '').trim().toLowerCase();
            return txt === 'delete' || txt === 'удалить';
        });
        if (confirmBtns.length > 0) {
            confirmBtns[0].click();
            return true;
        }
        return false;
        """

        deleted = 0
        while True:
            clicked = driver.execute_script(js_cleanup)
            if not clicked:
                break
            time.sleep(1.2)
            del_click = driver.execute_script(js_click_delete)
            if del_click:
                time.sleep(1.2)
                driver.execute_script(js_confirm_modal)
                deleted += 1
                time.sleep(1.5)
            else:
                driver.execute_script("document.body.click();")
                time.sleep(1)
                break

        if deleted > 0:
            log.info(f"Sidebar cleanup check: Deleted {deleted} chat(s) from sidebar.")
        else:
            log.info("Sidebar cleanup check: Sidebar is clean (0 chats).")
    except Exception as e:
        log.warning(f"Sidebar cleanup warning: {e}")

def run_render():
    log.info("=" * 70)
    log.info("  GEMINI IMAGE GENERATOR — Запуск (ID 58–79)")
    log.info(f"  MD_DIR:       {MD_DIR}")
    log.info("  DOWNLOADS_DIR:%s", load_config()["rpa"]["downloads_dir"])
    log.info(f"  RAW_DIR:      {RAW_DIR}")
    log.info(f"  FAILED_DIR:   {FAILED_DIR}")
    log.info(f"  BATCH_SIZE:   1")
    log.info(f"  CLI --limit:  {len(TARGET_STEMS)}")
    log.info(f"  CLI --from:   58-min")
    log.info("=" * 70)

    stats = {"success": 0, "failed": 0, "skipped": 0}
    
    log.info("====== WebDriver manager ======")
    driver = create_driver()

    try:
        total_items = len(TARGET_STEMS)
        for idx, stem in enumerate(TARGET_STEMS):
            passport_path = Path(MD_DIR) / f"{stem}.md"
            if not passport_path.exists():
                log.warning(f"File not found: {passport_path}")
                stats["skipped"] += 1
                continue

            # SKIP CHECK: If raw PNG already exists in RAW_DIR, skip re-generation!
            raw_png_path = os.path.join(RAW_DIR, f"{stem}.png")
            if os.path.exists(raw_png_path) and os.path.getsize(raw_png_path) > 1000:
                log.info(f"⏭️  Пропускаем {stem}.md — качественная картинка уже присутствует в {RAW_DIR}")
                stats["skipped"] += 1
                continue

            success = False
            attempts = 0
            max_attempts = 2  # Retry once if first render attempt is bad/failed

            while not success and attempts < max_attempts:
                attempts += 1
                log.info("\n" + "─" * 60)
                log.info(f"  [{idx + 1}/{total_items}] Обработка: {passport_path.name} (попытка {attempts}/{max_attempts})")
                log.info("─" * 60)

                # 1. Open new chat
                log.info(f"🔁 BATCH RESET: начало нового пакета (индекс {idx}, stem={stem}).")
                log.info("🔄 Загрузка нового чата Gemini...")
                driver.get(GEMINI_URL)
                time.sleep(4)

                # 2. Delete existing chats from sidebar before proceeding
                delete_sidebar_chats(driver)
                log.info("📨 Пропускаем отправку системного промпта по требованию пользователя.")

                # Read passport
                with open(passport_path, "r", encoding="utf-8") as f:
                    passport_text = f.read()
                log.info(f"📄 Паспорт прочитан: {len(passport_text)} символов.")

                # Wait idle
                wait_for_chat_idle(driver, timeout=30)

                # Send message
                send_message(driver, passport_text)
                log.info("📤 Паспорт отправлен в Gemini.")

                # Wait for response container
                log.info(f"Waiting for new response container (responses before: 0, timeout: {IMAGE_GENERATION_TIMEOUT}s)...")
                
                try:
                    img_found = wait_for_image_generation(driver, 0, IMAGE_GENERATION_TIMEOUT)
                except Exception as e:
                    img_found = False
                    log.error(f"Image generation exception: {e}")

                if img_found:
                    raw_saved = download_blob_image(driver, stem)
                    if raw_saved and os.path.exists(raw_saved) and os.path.getsize(raw_saved) > 1000:
                        size_kb = os.path.getsize(raw_saved) / 1024
                        log.info(f"Raw image saved: {os.path.basename(raw_saved)} ({size_kb:.1f} KB)")
                        log.info(f"SUCCESS: {stem}.md -> {os.path.basename(raw_saved)}")
                        stats["success"] += 1
                        success = True
                    else:
                        img_found = False

                if not success:
                    log.error(f"❌ Ошибка генерации для {stem}.md (попытка {attempts}).")
                    stats["failed"] += 1
                    # Save error screenshot to failed directory
                    err_ss_path = os.path.join(FAILED_DIR, f"error_gen_{stem}_attempt{attempts}.png")
                    try:
                        driver.save_screenshot(err_ss_path)
                        log.info(f"📸 Saved error screenshot to: {err_ss_path}")
                    except Exception:
                        pass
                    
                    # Delete the bad chat before retrying or moving on
                    delete_sidebar_chats(driver)
                    time.sleep(3)

        log.info("\n" + "=" * 70)
        log.info("  ИТОГИ ОБРАБОТКИ")
        log.info(f"  ✅ Успешно:   {stats['success']}")
        log.info(f"  ❌ Ошибки:    {stats['failed']}")
        log.info(f"  ⏭️  Пропущено: {stats['skipped']}")
        log.info(f"  📋 Лог:       {LOG_FILEPATH}")
        log.info("=" * 70)

    finally:
        try:
            driver.quit()
        except Exception:
            pass

    # Run Stage 3 image processor to convert new raw PNGs to WEBP
    if stats["success"] > 0:
        log.info("🔄 Running Stage 3 image conversion to WEBP...")
        try:
            subprocess.run([sys.executable, "main.py", "--process-images-only"], check=True)
        except Exception as e:
            log.error(f"Stage 3 error: {e}")

if __name__ == "__main__":
    run_render()
