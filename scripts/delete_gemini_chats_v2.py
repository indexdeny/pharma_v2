import os, sys, time, logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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

print("[START] Launching Chrome driver...")
driver = webdriver.Chrome(options=options)
try:
    driver.get("https://gemini.google.com/app")
    time.sleep(5)
    
    # Check if expand sidebar button needs to be clicked
    try:
        expand_btns = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='Expand'], button[aria-label*='Main menu'], button[aria-label*='Меню']")
        for b in expand_btns:
            if b.is_displayed():
                b.click()
                time.sleep(2)
                break
    except Exception:
        pass

    # Inspect DOM structure of conversation history items
    inspect_script = """
    const items = Array.from(document.querySelectorAll('a[href*="/app/"], conversation-item, [data-test-id*="conversation"]'));
    const info = items.map(el => {
        return {
            tag: el.tagName,
            href: el.getAttribute('href'),
            text: el.innerText.slice(0, 30),
            innerHTML: el.innerHTML.slice(0, 200)
        };
    });
    return info.slice(0, 10);
    """
    sample_items = driver.execute_script(inspect_script)
    print(f"[INSPECT] Sample items found ({len(sample_items)}):")
    for s in sample_items:
        print("  ", s)

    # Let's inspect all buttons in the left navigation sidebar
    buttons_script = """
    const nav = document.querySelector('side-navigation, [role="navigation"], nav, .side-nav-container') || document.body;
    const btns = Array.from(nav.querySelectorAll('button, [role="button"]'));
    return btns.map(b => ({
        aria: b.getAttribute('aria-label'),
        txt: b.innerText,
        html: b.outerHTML.slice(0, 150)
    })).filter(b => b.aria || b.txt || b.html.includes('svg') || b.html.includes('mat-icon'));
    """
    nav_buttons = driver.execute_script(buttons_script)
    print(f"[INSPECT] Nav buttons sample ({len(nav_buttons)}):")
    for b in nav_buttons[:15]:
        print("  ", b)

    # Clean loop: for each conversation item, hover and click 3-dots, then click Delete, then confirm Delete.
    deleted_count = 0
    while True:
        # Script to trigger hover and find option button
        find_and_click_menu_js = """
        // Find recent conversation links/items in sidebar
        const convLinks = Array.from(document.querySelectorAll('a[href*="/app/"]')).filter(a => {
            const h = a.getAttribute('href') || '';
            // Only actual conversation IDs (e.g. /app/12345 or /app/abcde)
            return h.match(/\\/app\\/[a-z0-9_-]{5,}/i);
        });

        if (convLinks.length === 0) return 'NO_CONVERSATIONS';

        const firstConv = convLinks[0];
        // Scroll into view & dispatch mouseover
        firstConv.scrollIntoView({block: 'center'});
        firstConv.dispatchEvent(new MouseEvent('mouseover', { bubbles: true, cancelable: true }));
        firstConv.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true, cancelable: true }));

        // Check if there is a parent container holding the 3 dots button
        let parent = firstConv.parentElement;
        while (parent && parent.tagName !== 'SIDE-NAVIGATION' && parent !== document.body) {
            const btn = parent.querySelector('button[aria-label*="options"], button[aria-label*="More"], button[aria-label*="меню"], button[aria-label*="Параметры"], button[mat-menu-trigger-for], [data-test-id*="menu"]');
            if (btn) {
                btn.click();
                return 'CLICKED_MENU_BTN';
            }
            parent = parent.parentElement;
        }

        // Try querySelectorAll across document for any newly visible menu trigger button
        const allMenuBtns = Array.from(document.querySelectorAll('button[aria-label*="options"], button[aria-label*="More"], button[aria-label*="меню"], button[aria-label*="Параметры"], button[mat-menu-trigger-for], [data-test-id*="menu"]'));
        if (allMenuBtns.length > 0) {
            allMenuBtns[0].click();
            return 'CLICKED_ANY_MENU_BTN';
        }

        return 'MENU_BTN_NOT_FOUND';
        """

        res = driver.execute_script(find_and_click_menu_js)
        print(f"[LOOP] Menu click attempt: {res}")

        if res == 'NO_CONVERSATIONS':
            print("[DONE] No more conversations found in sidebar.")
            break
        elif res in ['CLICKED_MENU_BTN', 'CLICKED_ANY_MENU_BTN']:
            time.sleep(1.2)
            # Click Delete option in popup menu
            click_delete_js = """
            const items = Array.from(document.querySelectorAll('[role="menuitem"], button, div, span')).filter(el => {
                const txt = (el.innerText || '').trim().toLowerCase();
                return txt === 'delete' || txt === 'удалить' || txt.includes('delete chat') || txt.includes('удалить чат');
            });
            if (items.length > 0) {
                items[0].click();
                return 'CLICKED_DELETE_OPTION';
            }
            return 'DELETE_OPTION_NOT_FOUND';
            """
            del_res = driver.execute_script(click_delete_js)
            print(f"[LOOP] Delete option attempt: {del_res}")

            if del_res == 'CLICKED_DELETE_OPTION':
                time.sleep(1.2)
                # Confirm in modal dialog if present
                confirm_js = """
                const confirmBtns = Array.from(document.querySelectorAll('mat-dialog-container button, [role="dialog"] button, [data-test-id*="confirm"] button')).filter(el => {
                    const txt = (el.innerText || '').trim().toLowerCase();
                    return txt === 'delete' || txt === 'удалить';
                });
                if (confirmBtns.length > 0) {
                    confirmBtns[0].click();
                    return 'CONFIRMED_DELETE';
                }
                return 'NO_CONFIRM_MODAL';
                """
                conf_res = driver.execute_script(confirm_js)
                print(f"[LOOP] Modal confirm attempt: {conf_res}")
                deleted_count += 1
                time.sleep(2)
            else:
                # Click somewhere else to close menu and avoid stuck loop
                driver.execute_script("document.body.click();")
                time.sleep(1)
        else:
            time.sleep(1)
            # Try alternative hover via ActionChains
            try:
                conv_elems = driver.find_elements(By.CSS_SELECTOR, "a[href*='/app/']")
                if conv_elems:
                    ActionChains(driver).move_to_element(conv_elems[0]).perform()
                    time.sleep(1)
            except Exception:
                pass

    print(f"[COMPLETE] Total deleted chats: {deleted_count}")

finally:
    print("[INFO] Pausing 5s before closing...")
    time.sleep(5)
    driver.quit()
