from pathlib import Path
import os, sys, time, logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

PROFILE_DIR = str(Path.home().joinpath('.gemini', 'antigravity-browser-profile'))
PROFILE_NAME = "Profile 1"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

options = Options()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument(f"--profile-directory={PROFILE_NAME}")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--window-size=1920,1080")

logging.info("Starting Gemini Chat History Cleanup Driver...")
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://gemini.google.com/app")
    time.sleep(5)

    # 1. Expand sidebar if collapsed
    try:
        expand_btns = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='Expand'], button[aria-label*='Main menu'], button[aria-label*='Меню'], button[aria-label*='Главное меню']")
        for b in expand_btns:
            if b.is_displayed():
                b.click()
                time.sleep(2)
                break
    except Exception as e:
        logging.warning(f"Sidebar expand check: {e}")

    deleted_count = 0
    consecutive_failures = 0

    while True:
        # JS script to find first conversation item, hover/focus it, click options button, click delete, click modal confirm
        js_step = """
        function deleteNextChat() {
            // Find all conversation links in side navigation
            const links = Array.from(document.querySelectorAll('a[href*="/app/"]')).filter(a => {
                const h = a.getAttribute('href') || '';
                return h.match(/\\/app\\/[a-z0-9_-]{5,}/i);
            });

            if (links.length === 0) {
                return { status: 'NO_CHATS' };
            }

            const item = links[0];
            item.scrollIntoView({ block: 'center' });

            // Trigger mouseover and mouseenter on item and its parent tree
            let p = item;
            for (let i = 0; i < 4 && p; i++) {
                p.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                p.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                p = p.parentElement;
            }

            // Look for options button in the item's DOM branch or nearby
            let btn = null;
            p = item.parentElement;
            for (let i = 0; i < 5 && p; i++) {
                btn = p.querySelector('button[aria-label*="option"], button[aria-label*="Option"], button[aria-label*="More"], button[aria-label*="more"], button[aria-label*="меню"], button[aria-label*="Параметры"], button[aria-label*="Действия"], button[mat-menu-trigger-for], [data-test-id*="menu"]');
                if (btn) break;
                p = p.parentElement;
            }

            // Fallback: search across document for visible mat-icon more_vert
            if (!btn) {
                const icons = Array.from(document.querySelectorAll('mat-icon[svgicon="more_vert"], mat-icon[svgicon*="more"]'));
                if (icons.length > 0) {
                    btn = icons[0].closest('button') || icons[0];
                }
            }

            if (!btn) {
                return { status: 'BTN_NOT_FOUND', total_links: links.length };
            }

            btn.click();
            return { status: 'CLICKED_MENU_BTN', total_links: links.length };
        }
        return deleteNextChat();
        """

        res = driver.execute_script(js_step)
        logging.info(f"[STEP 1] Menu click result: {res}")

        status = res.get('status')
        if status == 'NO_CHATS':
            logging.info("No more conversation links found in sidebar. Cleanup complete!")
            break

        if status == 'CLICKED_MENU_BTN':
            time.sleep(1.5)
            # Step 2: Click 'Delete' in popup menu
            js_click_delete = """
            function clickDeleteOption() {
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
            }
            return clickDeleteOption();
            """
            deleted_clicked = driver.execute_script(js_click_delete)
            logging.info(f"[STEP 2] Delete menu option clicked: {deleted_clicked}")

            if deleted_clicked:
                time.sleep(1.5)
                # Step 3: Confirm in modal dialog
                js_confirm_modal = """
                function confirmDeleteModal() {
                    const confirmBtns = Array.from(document.querySelectorAll('mat-dialog-container button, [role="dialog"] button, button[data-test-id*="confirm"]')).filter(el => {
                        const txt = (el.innerText || '').trim().toLowerCase();
                        return txt === 'delete' || txt === 'удалить';
                    });
                    if (confirmBtns.length > 0) {
                        confirmBtns[0].click();
                        return true;
                    }
                    return false;
                }
                return confirmDeleteModal();
                """
                confirmed = driver.execute_script(js_confirm_modal)
                logging.info(f"[STEP 3] Modal confirm clicked: {confirmed}")

                deleted_count += 1
                consecutive_failures = 0
                time.sleep(2)
            else:
                consecutive_failures += 1
                driver.execute_script("document.body.click();")
                time.sleep(1)
        else:
            consecutive_failures += 1
            # Try Selenium ActionChains hover as fallback
            try:
                links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/app/']")
                if links:
                    ActionChains(driver).move_to_element(links[0]).perform()
                    time.sleep(1)
            except Exception:
                pass

        if consecutive_failures >= 5:
            logging.info(f"Reached {consecutive_failures} consecutive unhandled items. Stopping cleanup.")
            break

    logging.info(f"=== CLEANUP FINISHED: Successfully deleted {deleted_count} chats ===")

finally:
    try:
        driver.quit()
    except Exception:
        pass
