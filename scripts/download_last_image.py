"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              GEMINI IMAGE EXTRACTOR — RPA Utility Script                     ║
║              Extracts generated image from open Gemini chat                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

This utility script opens Chrome with the existing Gemini session profile,
automatically opens the latest chat from the sidebar, and extracts the last
generated image using canvas.toDataURL() to preserve the smaller file size.
"""

import os
import re
import time
import base64
import logging
import argparse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration matching gemini_image_generator.py
BROWSER_PROFILE_DIR = r"LOCAL_HOME\.gemini\antigravity-browser-profile\Profile 1"
BROWSER_PROFILE_NAME = "Profile 1"
RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "render_output", "raw")
DOWNLOADS_DIR = r"LOCAL_HOME\Downloads"
GEMINI_URL = "https://gemini.google.com/app"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

def create_driver() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={BROWSER_PROFILE_DIR}")
    chrome_options.add_argument(f"--profile-directory={BROWSER_PROFILE_NAME}")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--lang=en-US")

    prefs = {
        "download.default_directory": DOWNLOADS_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.content_settings.exceptions.clipboard": {
            "[*.]google.com,*": {"setting": 1},
            "https://gemini.google.com:443,*": {"setting": 1}
        }
    }
    chrome_options.add_experimental_option("prefs", prefs)

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        log.info("ChromeDriver installed/located via webdriver-manager.")
    except ImportError:
        service = Service()
        log.warning("webdriver-manager not found. Using ChromeDriver from PATH.")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Hide automation traces
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            """
        },
    )
    return driver

def open_latest_chat(driver: webdriver.Chrome) -> bool:
    log.info("Locating the latest chat link in the sidebar...")
    try:
        # Wait up to 5s for anchor tags to load
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/app/']"))
        )
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/app/']")
        chat_links = []
        for link in links:
            href = link.get_attribute("href") or ""
            if href.endswith("/app") or href.endswith("/app/") or "new_chat" in href:
                continue
            chat_links.append(link)
        
        if chat_links:
            log.info(f"Found {len(chat_links)} chat link(s) in sidebar. Clicking the first one...")
            driver.execute_script("arguments[0].click();", chat_links[0])
            log.info("Clicked sidebar chat link successfully.")
            return True
    except Exception as e:
        log.warning(f"Could not locate or click sidebar chat link: {e}")
    return False

def wait_for_chat_idle(driver: webdriver.Chrome, timeout: int = 90) -> bool:
    log.info("Waiting for chat to become idle (Stop button and progress bars gone)...")
    deadline = time.time() + timeout

    stop_selectors = [
        "button[aria-label*='Stop']",
        "button[aria-label*='stop']",
        "mat-progress-bar",
        ".progress-bar",
        "response-container.loading",
        ".response-loading",
        "[data-pending='true']",
    ]

    poll_interval = 1.0
    while time.time() < deadline:
        is_busy = False
        for selector in stop_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed():
                        is_busy = True
                        break
                if is_busy:
                    break
            except Exception:
                continue

        if not is_busy:
            time.sleep(0.5)
            is_busy_double = False
            for selector in stop_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for el in elements:
                        if el.is_displayed():
                            is_busy_double = True
                            break
                    if is_busy_double:
                        break
                except Exception:
                    continue
            if not is_busy_double:
                log.info("Chat is idle.")
                return True

        time.sleep(poll_interval)

    log.warning("Timeout waiting for chat to become idle.")
    return False

def download_blob_image(driver: webdriver.Chrome, passport_stem: str) -> str | None:
    """
    Saves the generated image via canvas.toDataURL() in original PNG format.
    """
    import base64
    os.makedirs(RAW_DIR, exist_ok=True)

    # Find the last response
    response_selector = "model-response, [data-testid='model-response']"
    try:
        responses = driver.find_elements(By.CSS_SELECTOR, response_selector)
        if not responses:
            log.error("No model-response elements found.")
            return None
        latest_response = responses[-1]
    except Exception as e:
        log.error(f"Failed to find latest response: {e}")
        return None

    # Search for the last loaded blob image inside the last response
    blob_selectors = [
        "img.image.animate.loaded",
        "button.image-button img",
        "img[src^='blob:']",
    ]
    img_element = None
    for sel in blob_selectors:
        try:
            imgs = latest_response.find_elements(By.CSS_SELECTOR, sel)
            blob_imgs = [
                el for el in imgs
                if (el.get_attribute("src") or "").startswith("blob:")
            ]
            if blob_imgs:
                for candidate in reversed(blob_imgs):
                    is_loaded = driver.execute_script(
                        "return arguments[0].complete && arguments[0].naturalWidth > 0;",
                        candidate
                    )
                    if is_loaded:
                        img_element = candidate
                        break
                if img_element:
                    log.info(f"Target img found in latest response: {sel}, src={img_element.get_attribute('src')[:60]}...")
                    break
        except Exception:
            continue

    if not img_element:
        for sel in blob_selectors:
            try:
                imgs = latest_response.find_elements(By.CSS_SELECTOR, sel)
                blob_imgs = [
                    el for el in imgs
                    if (el.get_attribute("src") or "").startswith("blob:")
                ]
                if blob_imgs:
                    img_element = blob_imgs[-1]
                    log.warning(f"Using fallback not-fully-loaded img: {sel}")
                    break
            except Exception:
                continue

    if not img_element:
        log.error("No blob img element found in the latest response container.")
        return None

    log.info("Extracting image via canvas.toDataURL()...")
    try:
        b64_data = driver.execute_script(
            """
            var img = arguments[0];
            try {
                var canvas = document.createElement('canvas');
                canvas.width  = img.naturalWidth  || img.width  || 512;
                canvas.height = img.naturalHeight || img.height || 512;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                var dataURL = canvas.toDataURL('image/png');
                canvas.remove();
                return dataURL;
            } catch(e) {
                return 'ERROR:' + e.toString();
            }
            """,
            img_element,
        )
    except Exception as e:
        log.error(f"canvas.toDataURL() JS call failed: {e}")
        return None

    if not b64_data or b64_data.startswith("ERROR:"):
        log.error(f"canvas.toDataURL() returned error: {b64_data}")
        log.info("Trying XHR sync fallback...")
        try:
            blob_url = img_element.get_attribute("src")
            b64_data = driver.execute_script(
                """
                var url = arguments[0];
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('GET', url, false);
                    xhr.responseType = 'blob';
                    xhr.send();
                    var reader = new FileReaderSync();
                    return reader.readAsDataURL(xhr.response);
                } catch(e) {
                    return 'ERROR:' + e.toString();
                }
                """,
                blob_url,
            )
        except Exception as e2:
            log.error(f"XHR sync fallback failed: {e2}")
            return None

    if not b64_data or b64_data.startswith("ERROR:") or b64_data == "data:,":
        log.error("All extraction methods failed.")
        return None

    try:
        header, encoded = b64_data.split(",", 1)
    except Exception:
        encoded = b64_data

    target_filename = f"{passport_stem}.png"
    target_path = os.path.join(RAW_DIR, target_filename)

    try:
        img_bytes = base64.b64decode(encoded)
        if len(img_bytes) < 1000:
            log.error(f"Decoded image too small ({len(img_bytes)} bytes). Skipping.")
            return None
        
        with open(target_path, "wb") as f:
            f.write(img_bytes)
        return target_path
    except Exception as e:
        log.error(f"Failed to save image bytes: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Extract last generated image from Gemini chat UI.")
    parser.add_argument("--stem", type=str, default="421-min", help="Target filename stem (default: 421-min)")
    args = parser.parse_args()

    log.info(f"Starting Gemini Image Extractor for SKU stem: {args.stem}")
    log.info("⚠️  IMPORTANT: Please close any open Chrome instances using this profile before running.")

    driver = create_driver()
    try:
        log.info(f"Navigating to: {GEMINI_URL}")
        driver.get(GEMINI_URL)

        log.info("Waiting for interface to load...")
        try:
            # Wait up to 30s for standard chat input elements
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'], textarea, rich-textarea"))
            )
            log.info("Interface loaded successfully.")
        except Exception:
            log.warning("Timeout waiting for input elements. Make sure you are logged in.")

        # Check if we are already inside a chat (by checking for model-response)
        has_chat = False
        try:
            responses = driver.find_elements(By.CSS_SELECTOR, "model-response, [data-testid='model-response']")
            if responses:
                log.info("Already inside an active chat. Skipping sidebar navigation.")
                has_chat = True
        except Exception:
            pass

        if not has_chat:
            # Click the latest chat link in the sidebar
            chat_opened = open_latest_chat(driver)
            if chat_opened:
                log.info("Chat link clicked. Waiting for content to load...")
                time.sleep(3.0)

        # Wait up to 15s for chat responses to be loaded in the DOM
        log.info("Waiting for chat responses (model-response) to appear...")
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "model-response, [data-testid='model-response']"))
            )
            log.info("Chat responses found.")
            time.sleep(2.0)
            
            # Wait for chat idle
            wait_for_chat_idle(driver, timeout=30)
            
            log.info("Attempting image extraction...")
            saved_path = download_blob_image(driver, args.stem)
            if saved_path:
                print("\n" + "="*80)
                print(f"  🎉 SUCCESS! Automatically extracted and saved image to:")
                print(f"  {saved_path}")
                print(f"  Size: {os.path.getsize(saved_path) / 1024:.1f} KB")
                print("="*80 + "\n")
                
                # Check if we should exit or keep open
                confirm = input("Press ENTER to close Chrome and exit (or type 'keep' to keep Chrome open): ").strip().lower()
                if confirm != 'keep':
                    return
        except Exception as e:
            log.error(f"Failed to detect loaded chat responses: {e}")

        print("\n" + "="*80)
        print("  MANUAL FALLBACK MODE:")
        print("  If automatic opening failed or you want to extract a different chat:")
        print("  1. In the Chrome window, click the correct chat or navigate to it.")
        print("  2. Ensure the target image is fully visible on screen.")
        print(f"  3. Press [ENTER] here in the terminal to extract the image as '{args.stem}.png'.")
        print("="*80 + "\n")

        while True:
            user_input = input("Press ENTER to extract (or type 'exit' to quit): ").strip().lower()
            if user_input == 'exit':
                log.info("Exiting script.")
                break
            
            log.info("Extracting...")
            saved_path = download_blob_image(driver, args.stem)
            if saved_path:
                print(f"\n🎉 SUCCESS! Saved image to: {saved_path}")
                print(f"Size: {os.path.getsize(saved_path) / 1024:.1f} KB")
                
                confirm = input("\nWould you like to close Chrome and exit? (y/n, default: y): ").strip().lower()
                if confirm != 'n':
                    break
            else:
                print("\n❌ EXTRACTION FAILED. Please make sure the chat is open and the image is visible on the screen.")
                retry = input("Try again? (y/n, default: y): ").strip().lower()
                if retry == 'n':
                    break
    finally:
        log.info("Closing Chrome browser...")
        try:
            driver.quit()
        except Exception:
            pass
        log.info("Done.")

if __name__ == "__main__":
    main()
