import os, sys, time, logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PROFILE_DIR = r"LOCAL_HOME\.gemini\antigravity-browser-profile"
PROFILE_NAME = "Profile 1"

options = Options()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument(f"--profile-directory={PROFILE_NAME}")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--window-size=1920,1080")

print("[START] Launching Chrome driver with Gemini profile...")
driver = webdriver.Chrome(options=options)
try:
    driver.get("https://gemini.google.com/app")
    time.sleep(5)
    
    # Check if left sidebar expand button needs to be clicked
    try:
        expand_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Expand menu'], button[aria-label*='Main menu'], button[mattooltip*='Main menu']")
        if expand_btn.is_displayed():
            expand_btn.click()
            time.sleep(2)
    except Exception:
        pass
        
    print("[INFO] Looking for conversation history items in sidebar...")
    
    deleted_count = 0
    while True:
        # Find all chat items in the sidebar
        # In Gemini UI, chat history items are typically in side-nav / conversation history list
        chat_items = driver.find_elements(By.CSS_SELECTOR, "conversation-item, a[href*='/app/'], div[data-test-id='conversation-item']")
        
        # Filter for actual chat links (excluding 'New Chat' button or navigation links)
        chats = []
        for item in chat_items:
            try:
                # Find options menu button inside or adjacent to chat item (3 dots / option menu)
                menu_btn = item.find_elements(By.CSS_SELECTOR, "button[aria-label*='options'], button[aria-label*='More'], button[aria-label*='menu'], [mat-menu-trigger-for]")
                if menu_btn or 'app/' in (item.get_attribute('href') or ''):
                    chats.append(item)
            except Exception:
                pass
                
        print(f"[FOUND] {len(chats)} chat items in history.")
        
        # If no chats found, try broader selectors for Gemini sidebar
        if not chats:
            # Try finding buttons with 3-dots in sidebar
            menu_btns = driver.find_elements(By.CSS_SELECTOR, "mat-icon[svgicon='more_vert'], button[aria-label*='Chat options'], button[aria-label*='options']")
            if not menu_btns:
                print("[DONE] No more chats found in sidebar history.")
                break
                
        # Delete chats one by one
        # JS script to find options menu and click delete
        deleted_in_loop = 0
        
        # Execute JS to find all 3-dots menus in sidebar and click delete
        js_code = """
        const findAndDeleteOne = async () => {
            // Find all chat item menu buttons (more_vert / options)
            const btns = Array.from(document.querySelectorAll('button')).filter(b => {
                const label = (b.getAttribute('aria-label') || '').toLowerCase();
                const text = b.innerText.toLowerCase();
                return label.includes('option') || label.includes('more') || label.includes('chat') || b.querySelector('mat-icon[svgicon="more_vert"]');
            });
            return btns.length;
        };
        return findAndDeleteOne();
        """
        
        count = driver.execute_script(js_code)
        print(f"[JS CHECK] Found {count} option menu buttons.")
        if count == 0:
            break
            
        # Click the first option menu button
        try:
            # Use Selenium or JS to hover over first chat item and click options menu
            js_delete_first = """
            let btns = Array.from(document.querySelectorAll('button[aria-label*="options"], button[aria-label*="More"], button[aria-label*="Chat options"]'));
            if (btns.length === 0) {
                // Try hovering over conversation links
                const links = Array.from(document.querySelectorAll('a[href*="/app/"]'));
                if (links.length > 0) {
                    links[0].dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                    btns = Array.from(document.querySelectorAll('button[aria-label*="options"], button[aria-label*="More"], button[aria-label*="Chat options"]'));
                }
            }
            if (btns.length > 0) {
                btns[0].click();
                return true;
            }
            return false;
            """
            clicked = driver.execute_script(js_delete_first)
            time.sleep(1.5)
            
            if clicked:
                # Click 'Delete' or 'Remove' in the opened menu
                js_click_delete_confirm = """
                // Find popup menu item for Delete
                const menuItems = Array.from(document.querySelectorAll('[role="menuitem"], button, div')).filter(el => {
                    const txt = el.innerText.trim().toLowerCase();
                    return txt === 'delete' || txt.includes('delete chat') || txt === 'удалить' || txt.includes('удалить чат');
                });
                if (menuItems.length > 0) {
                    menuItems[0].click();
                    return 'deleted_menu_clicked';
                }
                return 'not_found';
                """
                res = driver.execute_script(js_click_delete_confirm)
                print(f"[ACTION] Menu click result: {res}")
                time.sleep(1.5)
                
                # Check for confirm modal / dialog ('Delete' button in modal)
                js_confirm_modal = """
                const confirmBtns = Array.from(document.querySelectorAll('mat-dialog-container button, [role="dialog"] button')).filter(el => {
                    const txt = el.innerText.trim().toLowerCase();
                    return txt === 'delete' || txt.includes('delete') || txt === 'удалить';
                });
                if (confirmBtns.length > 0) {
                    confirmBtns[0].click();
                    return 'modal_confirmed';
                }
                return 'no_modal';
                """
                res_modal = driver.execute_script(js_confirm_modal)
                print(f"[ACTION] Modal confirm result: {res_modal}")
                time.sleep(2)
                deleted_count += 1
            else:
                print("[INFO] Could not click options menu. Stopping loop.")
                break
        except Exception as e:
            print(f"[ERROR] Loop error: {e}")
            break
            
    print(f"[DONE] Successfully deleted {deleted_count} chats from sidebar history.")
    
finally:
    print("[INFO] Driver active. Pausing 10s for inspection...")
    time.sleep(10)
    driver.quit()
