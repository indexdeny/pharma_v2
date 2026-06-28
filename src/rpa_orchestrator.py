"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          GEMINI IMAGE GENERATOR — RPA Automation Script v2.0               ║
║          Senior Python RPA Engineer · Selenium WebDriver                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

ОПИСАНИЕ:
    Скрипт автоматизирует отправку Markdown-паспортов в Gemini Chat,
    ожидает генерацию изображения, скачивает и переименовывает его.

ЗАВИСИМОСТИ:
    pip install selenium webdriver-manager

ЗАПУСК:
    python gemini_image_generator.py
"""

import os
import re
import glob
import time
import shutil
import logging
import argparse
from pathlib import Path
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                      БЛОК КОНФИГУРАЦИИ (EDIT HERE)                     ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# ──────────────────────────────────────────────────────────────────────────
# ПУТЬ К ПРОФИЛЮ БРАУЗЕРА (КРИТИЧЕСКИ ВАЖНО для доступа к сессии Google)
# ──────────────────────────────────────────────────────────────────────────
# КАК НАЙТИ ПУТЬ:
#   1. Откройте встроенный браузер Antigravity IDE.
#   2. В адресной строке введите:  chrome://version
#   3. Найдите строку "Profile Path" — она выглядит примерно так:
#      LOCAL_HOME\AppData\Local\Google\Chrome\User Data\Default
#   4. Скопируйте путь БЕЗ последнего сегмента "\Default"
#      То есть укажите родительскую папку: ...\User Data
#   5. Вставьте этот путь в переменную BROWSER_PROFILE_DIR ниже.
#
# ПРИМЕР (стандартный Chrome):
#   BROWSER_PROFILE_DIR = r"LOCAL_HOME\AppData\Local\Google\Chrome\User Data"
#
# ПРИМЕР (Antigravity / встроенный браузер):
#   Путь может быть нестандартным — проверьте chrome://version в самом браузере IDE.
#   Обычно что-то вроде:
#   r"LOCAL_HOME\.gemini\antigravity\browser\profile"
#
# ⚠️  ВАЖНО: Закройте встроенный браузер Antigravity ПЕРЕД запуском скрипта!
#   Chrome не позволяет двум процессам использовать один профиль одновременно.
# ──────────────────────────────────────────────────────────────────────────
# ── Centralised configuration (config.yaml via src/utils.py) ────────────────
# Defaults mirror the original constants but FIX the stale absolute paths:
# the project moved away from the old hard-coded c:\pharma_v2 location.
from src.utils import load_config, get_path

_CFG = load_config()
_RPA = _CFG["rpa"]

# Pre-authenticated Chrome profile (the Google/Gemini session lives here).
BROWSER_PROFILE_DIR = _RPA["browser_profile_dir"]
BROWSER_PROFILE_NAME = _RPA["browser_profile_name"]

# ── DIRECTORIES (anchored to project root, never the stale c:\pharma_v2) ─────
MD_DIR = str(get_path(_CFG, "passports_md"))        # .md passports (input)
DOWNLOADS_DIR = _RPA["downloads_dir"]                # Chrome download folder
RAW_DIR = str(get_path(_CFG, "renders_raw"))         # raw PNG output
FAILED_DIR = str(get_path(_CFG, "renders_failed"))   # failure screenshots

# ── AUTOMATION PARAMETERS ────────────────────────────────────────────────────
BATCH_SIZE = _RPA["batch_size"]                              # passports per chat before reset
IMAGE_GENERATION_TIMEOUT = _RPA["image_generation_timeout"] # seconds
DOWNLOAD_TIMEOUT = _RPA["download_timeout"]                  # seconds
READY_TIMEOUT = _RPA["ready_timeout"]                        # seconds
POST_CLICK_DELAY = _RPA["post_click_delay"]                  # seconds
GEMINI_URL = _RPA["gemini_url"]                              # Gemini chat URL

# Системный промпт для инициализации ИИ (Role Priming)
SYSTEM_PROMPT = (
    "You are a silent image generation engine. "
    "Rules: Accept incoming text prompts and generate images immediately. "
    "No commentary, no questions, no explanations before or after generation. "
    "Do not modify, interpret, or summarize the prompt. "
    "Do not add elements not specified in the prompt. "
    "If the prompt is accepted, generate the image silently. "
    "Treat every incoming message as a direct image generation instruction. "
    "Confirm readiness with one word: READY"
)

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                         НАСТРОЙКА ЛОГИРОВАНИЯ                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

_LOGS_DIR = get_path(_CFG, "logs")
_LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = str(_LOGS_DIR / f"gemini_rpa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=getattr(logging, str(_CFG["logging"]["level"]).upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def log_failure(filename: str, stage: str, error: str, recovery_attempted: str, result: str):
    """
    Append-only deterministic failure log.
    No telemetry frameworks. No analytics. No observability.
    Just a visible text log file.
    """
    failed_logs_dir = str(get_path(_CFG, "renders_failed_logs"))
    os.makedirs(failed_logs_dir, exist_ok=True)
    log_file_path = os.path.join(failed_logs_dir, "failures.log")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}]\n"
        f"file: {filename}\n"
        f"stage: {stage}\n"
        f"error: {error}\n"
        f"recovery_attempted: {recovery_attempted}\n"
        f"result: {result}\n\n"
    )
    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
        log.info(f"💾 Failure recorded in visibility log for {filename} ({stage})")
    except Exception as e:
        log.error(f"Failed to write to visibility log: {e}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                          ИНИЦИАЛИЗАЦИЯ ДРАЙВЕРА                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def create_driver() -> webdriver.Chrome:
    """
    Создаёт и возвращает Chrome WebDriver в headless-режиме
    с подключением к существующему профилю браузера.

    Headless = фоновый режим, не перехватывает фокус мыши.
    User-agent = имитация обычного десктопного Chrome (обход блокировок Google).
    """
    chrome_options = Options()

    # ── Headless режим ──────────────────────────────────────────────────
    # Gemini блокирует генерацию изображений в headless-режиме, поэтому по
    # умолчанию headless ВЫКЛЮЧЕН. Включается через config.yaml (rpa.headless)
    # или флаг main.py --headless, но это, как правило, ломает генерацию.
    if _RPA.get("headless"):
        log.warning("⚠️  HEADLESS включён — Gemini обычно БЛОКИРУЕТ генерацию изображений в headless!")
        chrome_options.add_argument("--headless=new")

    # ── Профиль браузера (доступ к сессии Google) ─────────────────────────
    chrome_options.add_argument(f"--user-data-dir={BROWSER_PROFILE_DIR}")
    chrome_options.add_argument(f"--profile-directory={BROWSER_PROFILE_NAME}")

    # ── Кастомный User-Agent (критично для headless!) ─────────────────────
    # В headless-режиме Chrome отправляет маркер "HeadlessChrome",
    # который Google обнаруживает и блокирует. Заменяем на обычный UA.
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )

    # ── Антидетект и стабильность ─────────────────────────────────────────
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--lang=en-US")

    # ── Папка загрузок (направляем скачивание в DOWNLOADS_DIR) ───────────
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

    # ── Автоматическое управление ChromeDriver ────────────────────────────
    # Если webdriver-manager не установлен: pip install webdriver-manager
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        log.info("ChromeDriver установлен через webdriver-manager.")
    except ImportError:
        # Fallback: Chrome и ChromeDriver уже в PATH
        service = Service()
        log.warning("webdriver-manager не найден. Используется ChromeDriver из PATH.")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Скрываем следы автоматизации через JavaScript
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

    log.info("Chrome WebDriver успешно инициализирован (видимый режим, headless ОТКЛЮЧЁН).")
    return driver


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                        ФУНКЦИИ РАБОТЫ С GEMINI                         ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def find_chat_input(driver: webdriver.Chrome) -> object:
    """
    Ищет поле ввода текста в чате Gemini.
    Gemini использует contenteditable div или textarea.
    """
    wait = WebDriverWait(driver, 20)

    # Селекторы поля ввода Gemini (в порядке приоритета)
    selectors = [
        (By.CSS_SELECTOR, "div.ql-editor[contenteditable='true']"),
        (By.CSS_SELECTOR, "rich-textarea div[contenteditable='true']"),
        (By.CSS_SELECTOR, "[data-testid='user-input'] textarea"),
        (By.CSS_SELECTOR, "textarea.input-area"),
        (By.XPATH, "//div[@role='textbox' and @contenteditable='true']"),
        (By.CSS_SELECTOR, "div[contenteditable='true']"),
    ]

    for by, selector in selectors:
        try:
            element = wait.until(EC.element_to_be_clickable((by, selector)))
            log.debug(f"Поле ввода найдено по селектору: {selector}")
            return element
        except TimeoutException:
            continue

    raise NoSuchElementException("Не удалось найти поле ввода чата Gemini.")


def send_message(driver: webdriver.Chrome, text: str) -> None:
    """
    Отправляет текстовое сообщение в чат Gemini.

    Стратегия вставки (3 уровня fallback):
    1. Clipboard API (navigator.clipboard.writeText) → Ctrl+A → Ctrl+V
       Полностью обходит Trusted Types: не трогаем innerHTML/innerText.
    2. DataTransfer paste event (синтетическая вставка plaintext).
    3. send_keys посимвольно (медленно, но надёжно).
    """
    input_box = find_chat_input(driver)
    input_box.click()
    time.sleep(2.5)  # Задержка 2.5 сек после клика по полю ввода перед вставкой текста

    inserted = False

    # ── Метод 1: Clipboard API + Ctrl+A + Ctrl+V ──────────────────────────
    # Записываем текст в системный буфер через async clipboard и сразу вставляем.
    # innerHTML не используется — Trusted Types не срабатывает.
    try:
        driver.execute_script(
            """
            const text = arguments[0];
            navigator.clipboard.writeText(text).then(() => {}).catch(() => {});
            """,
            text,
        )
        time.sleep(0.3)
        # Выделяем всё существующее содержимое и заменяем вставкой
        input_box.send_keys(Keys.CONTROL, "a")
        time.sleep(0.1)
        input_box.send_keys(Keys.CONTROL, "v")
        time.sleep(0.5)

        # Проверяем, что что-то появилось
        current_text = driver.execute_script(
            "return arguments[0].innerText || arguments[0].value || '';",
            input_box,
        )
        if current_text and len(current_text.strip()) > 10:
            inserted = True
            log.debug("send_message: вставка через Clipboard API успешна.")
    except Exception as e:
        log.debug(f"send_message: Clipboard API недоступен: {e}")

    # ── Метод 2: DataTransfer paste event ────────────────────────────────
    if not inserted:
        try:
            driver.execute_script(
                """
                const el = arguments[0];
                const text = arguments[1];
                el.focus();
                const dt = new DataTransfer();
                dt.setData('text/plain', text);
                const pasteEvent = new ClipboardEvent('paste', {
                    clipboardData: dt,
                    bubbles: true,
                    cancelable: true
                });
                el.dispatchEvent(pasteEvent);
                el.dispatchEvent(new Event('input', {bubbles: true}));
                """,
                input_box,
                text,
            )
            time.sleep(0.5)
            current_text = driver.execute_script(
                "return arguments[0].innerText || arguments[0].value || '';",
                input_box,
            )
            if current_text and len(current_text.strip()) > 10:
                inserted = True
                log.debug("send_message: вставка через DataTransfer paste event успешна.")
        except Exception as e:
            log.debug(f"send_message: DataTransfer метод не сработал: {e}")

    # ── Метод 3: send_keys посимвольно (fallback) ─────────────────────────
    if not inserted:
        log.debug("send_message: fallback — send_keys.")
        # Split by newlines and send using Shift+Enter to avoid triggering submission
        lines = text.split("\n")
        for idx, line in enumerate(lines):
            if idx > 0:
                input_box.send_keys(Keys.SHIFT, Keys.ENTER)
            if line:
                # Type line in chunks of 100 characters to prevent lags
                CHUNK = 100
                for i in range(0, len(line), CHUNK):
                    input_box.send_keys(line[i:i + CHUNK])
                    time.sleep(0.02)

    time.sleep(2.5)  # Задержка 2.5 сек после вставки текста перед отправкой

    # ── Отправка: Клик по кнопке Send или Enter ───────────────────────────
    sent = False
    try:
        sent = driver.execute_script("""
            let buttons = Array.from(document.querySelectorAll('button'));
            // 1. Try finding by aria-label
            let sendBtn = buttons.find(b => {
                let aria = (b.getAttribute('aria-label') || '').toLowerCase();
                if (aria.includes('send') || aria.includes('отправить') || aria.includes('сообщение')) {
                    if (b.getAttribute('aria-haspopup') === 'true') return false;
                    return b.offsetHeight > 0 && b.offsetWidth > 0;
                }
                return false;
            });
            // 2. Try finding by mat-icon content
            if (!sendBtn) {
                sendBtn = buttons.find(b => {
                    let icon = b.querySelector('mat-icon');
                    if (icon) {
                        let text = icon.textContent.trim().toLowerCase();
                        if (text === 'arrow_upward' || text === 'send') {
                            if (b.getAttribute('aria-haspopup') === 'true') return false;
                            return b.offsetHeight > 0 && b.offsetWidth > 0;
                        }
                    }
                    return false;
                });
            }
            if (sendBtn) {
                sendBtn.focus();
                sendBtn.click();
                return true;
            }
            return false;
        """)
        if sent:
            log.info("Sent message via robust JS send button click.")
    except Exception as e:
        log.warning(f"JS send button click failed: {e}")

    # Fallback to python selectors if JS failed
    if not sent:
        send_btn_selectors = [
            (By.CSS_SELECTOR, "button[aria-label='Send message']"),
            (By.CSS_SELECTOR, "button[aria-label='Отправить сообщение']"),
            (By.CSS_SELECTOR, "button[aria-label*='Send']"),
            (By.CSS_SELECTOR, "button[aria-label*='send']"),
            (By.CSS_SELECTOR, "button[aria-label*='Отправить']"),
            (By.CSS_SELECTOR, "button[aria-label*='отправить']"),
            (By.CSS_SELECTOR, "button[aria-label*='сообщение']"),
            (By.CSS_SELECTOR, "button[data-testid='send-button']"),
            (By.XPATH, "//button[contains(@aria-label,'Send') or contains(@aria-label,'Отправить')]"),
            (By.CSS_SELECTOR, "button.send-button"),
        ]
        for by, sel in send_btn_selectors:
            try:
                btn = driver.find_element(by, sel)
                if btn.get_attribute("aria-haspopup") == "true":
                    continue
                if btn.is_displayed() and btn.is_enabled():
                    btn.click()
                    sent = True
                    log.info(f"Clicked send button found by selector: {sel}")
                    break
                else:
                    driver.execute_script("arguments[0].click();", btn)
                    sent = True
                    log.info(f"JS Clicked send button found by selector: {sel}")
                    break
            except Exception:
                continue

    if not sent:
        try:
            input_box.send_keys(Keys.ENTER)
            log.info("Sent message via Keys.ENTER")
            sent = True
        except Exception as e:
            log.error(f"Failed to send message: {e}")

    log.info(f"Сообщение отправлено ({len(text)} символов).")
    time.sleep(2.5)  # Задержка 2.5 сек после отправки сообщения


def wait_for_ready_response(driver: webdriver.Chrome) -> bool:
    """
    Ждёт ответ 'READY' от Gemini после отправки системного промпта.
    Возвращает True при успехе, False при таймауте.
    """
    log.info("Ожидание ответа READY от Gemini...")
    wait = WebDriverWait(driver, READY_TIMEOUT)

    try:
        # Ищем последнее сообщение модели, содержащее READY
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "model-response, .model-response-text, [data-testid='model-response']"),
                "READY",
            )
        )
        log.info("✅ Gemini ответил READY. Начинаем обработку паспортов.")
        return True
    except TimeoutException:
        # Fallback: проверяем наличие READY в любом тексте страницы
        try:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            if "READY" in page_text:
                log.info("✅ READY найден в тексте страницы.")
                return True
        except Exception:
            pass

        log.warning("⚠️  Таймаут ожидания READY. Продолжаем без подтверждения.")
        return False


def clean_old_chats(driver: webdriver.Chrome, keep_last: int = 2, force: bool = False):
    """
    Cleans up old chats in the Gemini sidebar to avoid UI lag.
    Keep the most recent `keep_last` chats, delete the rest.
    Only runs if total target chats >= 5, unless force is True.
    """
    try:
        # We find all menu buttons in the sidebar
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.gem-conversation-actions-menu-button")
        
        # Target all chat menu buttons in the sidebar
        target_buttons = buttons
                
        total_targets = len(target_buttons)
        log.info(f"Sidebar cleanup check: Found {total_targets} total chats.")
        
        if not force and total_targets < 5:
            log.info("Fewer than 5 chats in sidebar. Skipping cleanup.")
            return

        # Keep the newest `keep_last` chats (at the top) and delete the rest
        to_delete_count = total_targets - keep_last
        log.info(f"Targeting {to_delete_count} old chats for deletion...")

        deleted = 0
        while deleted < to_delete_count:
            # Re-fetch because DOM updates after deletion
            buttons = driver.find_elements(By.CSS_SELECTOR, "button.gem-conversation-actions-menu-button")
            curr_targets = buttons
            
            if len(curr_targets) <= keep_last:
                break
                
            # Delete the oldest target chat first (at the bottom, index -1)
            target_btn = curr_targets[-1]
            label_summary = (target_btn.get_attribute("aria-label") or "")[:50].replace("\n", " ")
            log.info(f"Deleting old chat: '{label_summary}...'")
            
            try:
                driver.execute_script("arguments[0].click();", target_btn)
                time.sleep(2.5)  # Задержка 2.5 сек после открытия меню
                
                menu_items = driver.find_elements(By.CSS_SELECTOR, "button.mat-mdc-menu-item")
                delete_item = None
                for item in menu_items:
                    txt = item.text.lower()
                    if any(x in txt for x in ["удалить", "delete", "remove"]) or "delete-outline" in item.get_attribute("outerHTML"):
                        delete_item = item
                        break
                        
                if not delete_item and len(menu_items) >= 3:
                    delete_item = menu_items[2]
                    
                if delete_item:
                    driver.execute_script("arguments[0].click();", delete_item)
                    time.sleep(2.5)  # Задержка 2.5 сек после выбора Delete
                    
                    dialog_buttons = driver.find_elements(By.CSS_SELECTOR, "mat-dialog-container button, [role='dialog'] button")
                    confirm_btn = None
                    for db in dialog_buttons:
                        db_txt = db.text.lower()
                        if any(x in db_txt for x in ["удалить", "delete", "confirm"]):
                            confirm_btn = db
                            break
                            
                    if not confirm_btn and dialog_buttons:
                        confirm_btn = dialog_buttons[-1]
                        
                    if confirm_btn:
                        log.info(f"Confirming deletion: clicking '{confirm_btn.text.strip()}' button")
                        driver.execute_script("arguments[0].click();", confirm_btn)
                        deleted += 1
                        time.sleep(2.5)  # Задержка 2.5 сек после подтверждения
                    else:
                        log.warning("Could not find confirmation button in dialog.")
                        driver.find_element(By.TAG_NAME, "body").send_keys("\ue00c") # Escape
                        time.sleep(2.5)
                        break
                else:
                    log.warning("Could not find Delete option in menu.")
                    driver.find_element(By.TAG_NAME, "body").send_keys("\ue00c") # Escape
                    time.sleep(2.5)
                    break
            except Exception as e:
                log.error(f"Error during automatic sidebar deletion step: {e}")
                try:
                    driver.find_element(By.TAG_NAME, "body").send_keys("\ue00c")
                except Exception:
                    pass
                time.sleep(2.5)
                break
                
        log.info(f"Sidebar cleanup completed. Deleted {deleted} chats.")
    except Exception as e:
        log.error(f"Failed to clean old chats from sidebar: {e}")


def get_timeout_stems_from_log() -> list[str]:
    """
    Parses failures.log and extracts stems of passports that failed with wait_for_image_generation (timeout).
    """
    log_file_path = os.path.join(str(get_path(_CFG, "renders_failed_logs")), "failures.log")
    if not os.path.exists(log_file_path):
        return []
    stems = []
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = content.strip().split("\n\n")
        for block in blocks:
            lines = block.strip().split("\n")
            file_val = None
            stage_val = None
            for line in lines:
                if line.startswith("file:"):
                    file_val = line.split("file:", 1)[1].strip()
                elif line.startswith("stage:"):
                    stage_val = line.split("stage:", 1)[1].strip()
            if file_val and stage_val == "wait_for_image_generation":
                stem = Path(file_val).stem
                if stem not in stems:
                    stems.append(stem)
    except Exception as e:
        log.error(f"Error parsing failures.log: {e}")
    return stems


def print_estimate():
    """
    Dry-run output estimating remaining SKUs and execution ETA.
    """
    processed = load_progress()
    try:
        passports = get_passport_files()
    except Exception as e:
        log.error(f"Could not load passports: {e}")
        return
    total = len(passports)
    completed = len(processed)
    remaining = total - completed
    
    success_rate = 0.70
    avg_success_time = 40  # seconds
    avg_fail_time = 90     # seconds
    
    if remaining <= 0:
        print(f"\nAll {total} SKUs are already processed!")
        return
        
    expected_attempts = remaining / success_rate
    expected_failures = expected_attempts * (1 - success_rate)
    
    total_seconds = (remaining * avg_success_time) + (expected_failures * avg_fail_time)
    total_seconds += (remaining / BATCH_SIZE) * 20  # 20s per batch reset
    
    eta_hours = total_seconds / 3600
    
    print(f"\n==================================================")
    print(f"  PHARMAGEN PRO — ESTIMATED EXECUTION TIME")
    print(f"==================================================")
    print(f"  Total Passports: {total}")
    print(f"  Processed:       {completed}")
    print(f"  Remaining:       {remaining}")
    print(f"  Estimated Rate:  {success_rate*100:.0f}% success rate")
    print(f"  Avg Success:     {avg_success_time}s")
    print(f"  Avg Timeout:     {avg_fail_time}s")
    print(f"  ETA:             {eta_hours:.1f} hours ({eta_hours*60:.0f} mins)")
    print(f"==================================================\n")


def prime_gemini(driver: webdriver.Chrome) -> None:
    """
    Role Priming: загружает страницу и отправляет системный промпт.
    Вызывается в начале каждого нового пакета (batch).
    """
    log.info("🔄 Загрузка нового чата Gemini...")
    driver.get(GEMINI_URL)

    # Ожидание полной загрузки интерфейса
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[contenteditable='true'], textarea, rich-textarea")
        )
    )
    time.sleep(2.5)  # Задержка 2.5 сек для инициализации Angular/React

    # Auto-cleanup old chats in sidebar to prevent lag
    clean_old_chats(driver, keep_last=2)

    log.info("📨 Пропускаем отправку системного промпта по требованию пользователя.")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                    ФУНКЦИИ СКАЧИВАНИЯ И МОНИТОРИНГА                    ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def get_current_files_in_downloads() -> set:
    """
    Возвращает множество полных путей к файлам в папке Downloads,
    исключая временные файлы Chrome (.crdownload, .tmp).
    """
    all_files = glob.glob(os.path.join(DOWNLOADS_DIR, "*"))
    return {
        f for f in all_files
        if not f.endswith(".crdownload")
        and not f.endswith(".tmp")
        and os.path.isfile(f)
    }


def wait_for_new_download(files_before: set, timeout: int = DOWNLOAD_TIMEOUT) -> str | None:
    """
    Мониторит папку Downloads и ждёт появления нового полностью
    скачанного файла (не .crdownload / .tmp).

    Args:
        files_before: Множество файлов ДО начала скачивания.
        timeout: Максимальное время ожидания в секундах.

    Returns:
        Полный путь к новому файлу или None при таймауте.
    """
    log.info(f"⏳ Мониторинг папки Downloads (таймаут: {timeout}с)...")
    deadline = time.time() + timeout

    while time.time() < deadline:
        files_after = get_current_files_in_downloads()
        new_files = files_after - files_before

        if new_files:
            # Ждём завершения записи файла (размер стабилизируется)
            new_file = max(new_files, key=os.path.getmtime)
            prev_size = -1
            stable_count = 0

            while time.time() < deadline:
                try:
                    curr_size = os.path.getsize(new_file)
                    if curr_size == prev_size and curr_size > 0:
                        stable_count += 1
                        if stable_count >= 2:  # Размер стабилен 2 итерации подряд
                            log.info(f"✅ Файл скачан: {os.path.basename(new_file)} ({curr_size} байт)")
                            return new_file
                    else:
                        stable_count = 0
                    prev_size = curr_size
                except FileNotFoundError:
                    pass
                time.sleep(0.5)

        time.sleep(0.5)

    log.error("❌ Таймаут скачивания файла.")
    return None


def find_download_button(driver: webdriver.Chrome) -> object | None:
    """
    Ищет кнопку скачивания изображения в интерфейсе Gemini.
    Gemini рендерит изображения с кнопкой download внутри карточки.
    """
    # Различные варианты кнопки скачивания в Gemini
    selectors = [
        (By.XPATH, "//button[contains(@aria-label,'Download')]"),
        (By.XPATH, "//button[contains(@aria-label,'download')]"),
        (By.CSS_SELECTOR, "button[aria-label*='Download']"),
        (By.CSS_SELECTOR, "button[aria-label*='download']"),
        (By.XPATH, "//button[.//mat-icon[text()='download']]"),
        (By.CSS_SELECTOR, "[data-testid='download-button']"),
        # Кнопка на изображении (появляется при hover)
        (By.XPATH, "//div[contains(@class,'image')]//button[contains(@class,'download')]"),
    ]

    for by, selector in selectors:
        try:
            elements = driver.find_elements(by, selector)
            if elements:
                # Берём последнюю кнопку (последнее сгенерированное изображение)
                return elements[-1]
        except Exception:
            continue

    return None


def get_all_blob_images(driver: webdriver.Chrome) -> list:
    """
    Returns all generated image elements with a blob URL.
    """
    image_selectors = [
        "img.image.animate.loaded",
        "button.image-button img",
        "img[src^='blob:']",
    ]
    for selector in image_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            blob_imgs = [
                el for el in elements
                if (el.get_attribute("src") or "").startswith("blob:")
            ]
            if blob_imgs:
                return blob_imgs
        except Exception:
            continue
    return []


def wait_for_chat_idle(driver: webdriver.Chrome, timeout: int = 90) -> bool:
    """
    Waits for the Gemini chat to become idle (no longer generating, input ready).
    """
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
        # Check if stop button or loading indicator is visible
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
            # Let's do a double check: wait 0.5s and check again to ensure stability
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


def wait_for_image_generation(driver: webdriver.Chrome, responses_before: int, timeout: int = IMAGE_GENERATION_TIMEOUT) -> bool:
    """
    Ждёт генерации нового изображения в чате Gemini.

    Стратегия:
    1. Ждём появления нового model-response элемента.
    2. Ждём окончания генерации (idle статус).
    3. Ждём загрузки blob-изображения внутри последнего model-response.
    """
    log.info(f"Waiting for new response container (responses before: {responses_before}, timeout: {timeout}s)...")
    deadline = time.time() + timeout

    # 1. Ждём появления нового model-response элемента
    new_response_found = False
    response_selector = "model-response, [data-testid='model-response']"

    while time.time() < deadline:
        try:
            responses = driver.find_elements(By.CSS_SELECTOR, response_selector)
            if len(responses) > responses_before:
                new_response_found = True
                log.info(f"New model response detected (total responses: {len(responses)}).")
                break
        except Exception:
            pass
        time.sleep(1.0)

    if not new_response_found:
        log.error("Timeout: New model-response container did not appear.")
        return False

    # 2. Ждём завершения генерации (чат станет idle)
    time.sleep(1.0)  # Даём секунду на инициализацию
    remaining_time = max(5, int(deadline - time.time()))
    wait_for_chat_idle(driver, timeout=remaining_time)

    # 3. Ищем blob-изображение в последнем ответе
    image_selectors = [
        "img.image.animate.loaded",
        "button.image-button img",
        "img[src^='blob:']",
    ]

    log.info("Checking for generated images inside the latest response...")
    poll_interval = 1.5
    while time.time() < deadline:
        try:
            responses = driver.find_elements(By.CSS_SELECTOR, response_selector)
            if not responses:
                time.sleep(poll_interval)
                continue
            latest_response = responses[-1]
            for selector in image_selectors:
                elements = latest_response.find_elements(By.CSS_SELECTOR, selector)
                blob_imgs = [
                    el for el in elements
                    if (el.get_attribute("src") or "").startswith("blob:")
                ]
                if blob_imgs:
                    # Проверяем, что картинка загрузилась и имеет ненулевой размер
                    is_loaded = driver.execute_script(
                        "return arguments[0].complete && arguments[0].naturalWidth > 0;",
                        blob_imgs[-1]
                    )
                    if is_loaded:
                        log.info(f"Successfully found {len(blob_imgs)} generated image(s) in the latest response (and loaded).")
                        return True
        except Exception as e:
            log.debug(f"Exception while checking images in latest response: {e}")
        time.sleep(poll_interval)

    log.error("Timeout: No blob image found in the latest response container.")
    return False


def save_raw_image(image_bytes: bytes, target_path: str) -> str | None:
    """
    Сохраняет исходные байты изображения без изменений.
    """
    try:
        with open(target_path, "wb") as f:
            f.write(image_bytes)
        size_kb = os.path.getsize(target_path) / 1024
        log.info(f"Raw image saved: {os.path.basename(target_path)} ({size_kb:.1f} KB)")
        return target_path
    except Exception as e:
        log.error(f"Error saving raw image: {e}")
        return None


def download_blob_image(driver: webdriver.Chrome, passport_stem: str) -> str | None:
    """
    Сохраняет сгенерированное изображение через canvas.toDataURL() в исходном формате PNG.
    """
    import base64
    os.makedirs(RAW_DIR, exist_ok=True)

    # Находим последний ответ
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

    # Ищем последний загруженный blob img внутри последнего ответа
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
                # Берем последний, но также проверяем, чтобы он был загружен
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

    # Если не нашли полностью загруженный, берем просто последний найденный
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

    # Canvas approach: рисуем img на canvas → toDataURL (все в page context)
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
        # Fallback: XHR синхронный в page context (альтернативный метод)
        log.info("Trying XHR sync fallback...")
        try:
            blob_url = img_element.get_attribute("src")
            b64_data = driver.execute_script(
                """
                var url = arguments[0];
                try {
                    var xhr = new XMLHttpRequest();
                    xhr.open('GET', url, false);  // false = synchronous
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
            log.error(f"XHR sync fallback also failed: {e2}")
            return None

    if not b64_data or b64_data.startswith("ERROR:") or b64_data == "data:,":
        log.error(f"All extraction methods failed. Last result: {str(b64_data)[:100]}")
        return None

    # Парсим data URI
    try:
        header, encoded = b64_data.split(",", 1)
    except Exception:
        encoded = b64_data

    os.makedirs(RAW_DIR, exist_ok=True)
    target_filename = f"{passport_stem}.png"
    target_path = os.path.join(RAW_DIR, target_filename)

    # Дедупликация
    if os.path.exists(target_path):
        base_p, extension = os.path.splitext(target_path)
        target_path = f"{base_p}_dup{int(time.time())}{extension}"

    try:
        img_bytes = base64.b64decode(encoded)
        if len(img_bytes) < 1000:
            log.error(f"Decoded image too small ({len(img_bytes)} bytes) — likely blank canvas. Skipping.")
            return None
        
        final_path = save_raw_image(img_bytes, target_path)
        return final_path
    except Exception as e:
        log.error(f"Failed to save raw image: {e}")
        return None



# ╔══════════════════════════════════════════════════════════════════════════╗

# ║                      ФУНКЦИИ ФАЙЛОВОЙ СИСТЕМЫ                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def get_passport_files() -> list[Path]:
    """
    Возвращает отсортированный список .md файлов из MD_DIR.
    """
    md_path = Path(MD_DIR)
    if not md_path.exists():
        raise FileNotFoundError(f"Папка с паспортами не найдена: {MD_DIR}")

    files = sorted(
        md_path.glob("*.md"),
        key=lambda f: int(f.stem.split("-")[0]) if f.stem.split("-")[0].isdigit() else 999999
    )
    log.info(f"📁 Найдено {len(files)} .md паспортов в {MD_DIR}")
    return files


def read_passport(filepath: Path) -> str:
    """
    Читает содержимое .md файла и возвращает строку.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def rename_and_move_image(downloaded_file: str, passport_stem: str) -> str:
    """
    Переименовывает скачанный файл согласно имени паспорта и
    перемещает его в TARGET_DIR.

    Пример: скачан 'gemini_image.jpg', паспорт '1-min.md'
            → результат: TARGET_DIR/1-min.jpg

    Args:
        downloaded_file: Полный путь к скачанному файлу.
        passport_stem: Имя паспорта без расширения (Path.stem).

    Returns:
        Полный путь к финальному файлу.
    """
    os.makedirs(RAW_DIR, exist_ok=True)

    # Force .png — canvas.toDataURL always returns PNG data.
    # Never use the downloaded file's extension (may be .jpg due to browser fallback).
    ext = ".png"

    # Формируем целевое имя файла
    target_filename = f"{passport_stem}{ext}"
    target_path = os.path.join(RAW_DIR, target_filename)

    # Если файл с таким именем уже существует — добавляем суффикс
    if os.path.exists(target_path):
        base, extension = os.path.splitext(target_path)
        target_path = f"{base}_dup{int(time.time())}{extension}"

    shutil.move(downloaded_file, target_path)
    log.info(f"📦 Файл перемещён: {os.path.basename(downloaded_file)} → {target_filename}")
    return target_path


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                           ЗАГРУЗКА ПРОГРЕССА                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝

PROGRESS_FILE = str(get_path(_CFG, "progress_file"))


def load_progress() -> set:
    """
    Загружает список уже обработанных паспортов из файла прогресса,
    но считает завершенными только те, у которых есть файл изображения в RAW_DIR.
    Также добавляет к пропущенным все файлы, фактически присутствующие в RAW_DIR.
    """
    progress_stems = set()
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            progress_stems = set(line.strip() for line in f if line.strip())

    completed_stems = set()
    for stem in progress_stems:
        img_path = os.path.join(RAW_DIR, f"{stem}.png")
        if os.path.exists(img_path):
            completed_stems.add(stem)

    if os.path.exists(RAW_DIR):
        for f in os.listdir(RAW_DIR):
            if f.endswith(".png"):
                stem = os.path.splitext(f)[0]
                stem = re.sub(r'_dup\d+', '', stem)
                completed_stems.add(stem)

    log.info(f"Progress check: {len(completed_stems)} items are present in {RAW_DIR} and will be skipped.")
    return completed_stems


def save_progress(passport_stem: str) -> None:
    """
    Записывает имя обработанного паспорта в файл прогресса.
    """
    with open(PROGRESS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{passport_stem}\n")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                           ГЛАВНАЯ ФУНКЦИЯ                              ║
# ╚══════════════════════════════════════════════════════════════════════════╝

def main():
    # ── CLI ARGUMENTS ─────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="PharmaGen PRO — Gemini RPA Image Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python gemini_image_generator.py                  # default: first 20 unprocessed\n"
            "  python gemini_image_generator.py --limit 50       # first 50 unprocessed\n"
            "  python gemini_image_generator.py --all            # all unprocessed\n"
            "  python gemini_image_generator.py --from 50-min    # start from stem '50-min'\n"
            "  python gemini_image_generator.py --all --from 21-min\n"
        )
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Max number of passports to process (default: 20 for safety)"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Process ALL remaining unprocessed passports (overrides --limit)"
    )
    parser.add_argument(
        "--from", dest="from_stem", type=str, default=None,
        help="Start processing from a specific passport stem (e.g. '50-min')"
    )
    parser.add_argument(
        "--estimate", action="store_true",
        help="Show dry-run remaining SKUs and ETA without opening browser"
    )
    args = parser.parse_args()

    if args.estimate:
        print_estimate()
        return

    log.info("=" * 70)
    log.info("  GEMINI IMAGE GENERATOR — Запуск")
    log.info(f"  MD_DIR:       {MD_DIR}")
    log.info(f"  DOWNLOADS_DIR:{DOWNLOADS_DIR}")
    log.info(f"  RAW_DIR:      {RAW_DIR}")
    log.info(f"  FAILED_DIR:   {FAILED_DIR}")
    log.info(f"  BATCH_SIZE:   {BATCH_SIZE}")
    log.info(f"  CLI --limit:  {'ALL' if args.all else args.limit}")
    log.info(f"  CLI --from:   {args.from_stem or '(start)'}")
    log.info("=" * 70)

    # Создаём целевые папки если не существуют
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)

    # Загружаем список уже обработанных файлов
    processed = load_progress()
    if processed:
        log.info(f"♻️  Возобновление: уже обработано {len(processed)} паспортов.")

    # Получаем список паспортов
    passports = get_passport_files()

    # Фильтруем уже обработанные
    passports = [p for p in passports if p.stem not in processed]

    # --from: skip to the specified stem
    if args.from_stem:
        found_idx = None
        for i, p in enumerate(passports):
            if p.stem == args.from_stem:
                found_idx = i
                break
        if found_idx is not None:
            passports = passports[found_idx:]
            log.info(f"⏩ --from {args.from_stem}: skipping to index {found_idx}, {len(passports)} remaining.")
        else:
            log.warning(f"⚠️  --from '{args.from_stem}' not found in unprocessed list. Processing from start.")

    # --limit / --all
    if not args.all:
        passports = passports[:args.limit]
    log.info(f"📋 Обрабатываем: {len(passports)} паспортов{' (ALL mode)' if args.all else f' (limit={args.limit})'}")

    if not passports:
        log.info("✅ Все паспорты уже обработаны!")
        return

    # Статистика
    stats = {"success": 0, "failed": 0, "skipped": 0}
    failed_files = []
    need_reset = False
    consecutive_timeouts = 0

    # Инициализируем WebDriver
    driver = create_driver()

    try:
        # ── ГЛАВНЫЙ ЦИКЛ ──────────────────────────────────────────────────
        for index, passport_path in enumerate(passports):
            passport_stem = passport_path.stem
            log.info(f"\n{'─'*60}")
            log.info(f"  [{index + 1}/{len(passports)}] Обработка: {passport_path.name}")
            log.info(f"{'─'*60}")

            # ── BATCH CHUNKING: сброс контекста каждые BATCH_SIZE файлов ──
            # При index == 0 — всегда инициализируем (первый запуск)
            # При index % BATCH_SIZE == 0 — сброс после каждой пятёрки
            if index == 0 or (index > 0 and index % BATCH_SIZE == 0) or need_reset:
                if need_reset and consecutive_timeouts > 0:
                    sleep_time = min(30 * consecutive_timeouts, 120)
                    if consecutive_timeouts >= 3:
                        log.warning(f"⚠️ Gemini backend throttling detected, sleeping 3min (180s)")
                        sleep_time = 180
                    else:
                        log.info(f"Sleeping {sleep_time}s backoff before reset due to {consecutive_timeouts} consecutive timeouts...")
                    time.sleep(sleep_time)

                log.info(f"🔁 BATCH RESET: начало нового пакета (индекс {index}, reset={need_reset}).")
                try:
                    prime_gemini(driver)
                except Exception as e:
                    log.error(f"❌ WebDriver exception during BATCH RESET: {e}. Re-initializing driver...")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    time.sleep(5)
                    driver = create_driver()
                    try:
                        prime_gemini(driver)
                    except Exception as e2:
                        log.error(f"❌ Failed to prime re-initialized driver: {e2}")
                        need_reset = True
                        continue
                need_reset = False

            # ── Читаем содержимое паспорта ────────────────────────────────
            try:
                passport_text = read_passport(passport_path)
                log.info(f"📄 Паспорт прочитан: {len(passport_text)} символов.")
            except Exception as e:
                log.error(f"❌ Ошибка чтения файла {passport_path.name}: {e}")
                stats["skipped"] += 1
                log_failure(passport_path.name, "read_passport", str(e), "None", "SKIPPED")
                continue

            # ── Запоминаем текущие файлы в Downloads ─────────────────────
            files_before_download = get_current_files_in_downloads()

            # Ожидаем готовности чата перед отправкой нового запроса
            try:
                wait_for_chat_idle(driver, timeout=30)
            except Exception as e:
                log.error(f"❌ WebDriver error during wait_for_chat_idle: {e}")
                stats["failed"] += 1
                failed_files.append(str(passport_path))
                need_reset = True
                log_failure(passport_path.name, "wait_for_chat_idle", str(e), "Force Session Reset on next batch", "FAILED")
                continue

            # Подсчёт количества ответов перед отправкой
            try:
                responses_before = len(driver.find_elements(By.CSS_SELECTOR, "model-response, [data-testid='model-response']"))
            except Exception:
                responses_before = 0
            log.info(f"Текущее количество ответов в чате: {responses_before}.")

            # ── Отправляем паспорт в Gemini ───────────────────────────────
            try:
                send_message(driver, passport_text)
                log.info("📤 Паспорт отправлен в Gemini.")
            except Exception as e:
                log.error(f"❌ Ошибка отправки паспорта: {e}")
                stats["failed"] += 1
                failed_files.append(str(passport_path))
                need_reset = True
                log_failure(passport_path.name, "send_message", str(e), "Force Session Reset on next batch", "FAILED")
                continue

            # ── Ждём генерации изображения (Explicit Wait) ────────────────
            try:
                image_ready = wait_for_image_generation(driver, responses_before, IMAGE_GENERATION_TIMEOUT)
            except Exception as e:
                log.error(f"❌ WebDriver error during wait_for_image_generation: {e}")
                stats["failed"] += 1
                failed_files.append(str(passport_path))
                need_reset = True
                log_failure(passport_path.name, "wait_for_image_generation_exception", str(e), "Force Session Reset on next batch", "FAILED")
                continue

            if not image_ready:
                log.error(
                    f"TIMEOUT: Image for '{passport_path.name}' "
                    f"not generated in {IMAGE_GENERATION_TIMEOUT}s. Skipping."
                )
                try:
                    screenshot_name = os.path.join(FAILED_DIR, f"error_gen_{passport_stem}.png")
                    driver.save_screenshot(screenshot_name)
                    log.info(f"📸 Saved error screenshot to: {screenshot_name}")
                except Exception as ex:
                    log.error(f"Failed to save screenshot: {ex}")
                stats["failed"] += 1
                consecutive_timeouts += 1
                failed_files.append(str(passport_path))
                need_reset = True
                log_failure(
                    passport_path.name,
                    "wait_for_image_generation",
                    f"Timeout after {IMAGE_GENERATION_TIMEOUT}s",
                    "Screenshot saved, Force Session Reset on next batch",
                    "FAILED"
                )
                continue

            # ── Скачиваем blob изображение напрямую через JS ──────────────
            # Gemini не имеет кнопки Download — изображение живёт в blob: URL.
            # Извлекаем через fetch() → FileReader → base64 → файл на диске.
            time.sleep(POST_CLICK_DELAY)  # Пауза для стабилизации blob URL
            try:
                final_path = download_blob_image(driver, passport_stem)
            except Exception as e:
                log.error(f"❌ WebDriver error during download_blob_image: {e}")
                stats["failed"] += 1
                failed_files.append(str(passport_path))
                need_reset = True
                log_failure(passport_path.name, "download_blob_image_exception", str(e), "Force Session Reset on next batch", "FAILED")
                continue

            if not final_path:
                log.error(f"Failed to download image for '{passport_path.name}'. Skipping.")
                try:
                    screenshot_name = os.path.join(FAILED_DIR, f"error_dl_{passport_stem}.png")
                    driver.save_screenshot(screenshot_name)
                    log.info(f"📸 Saved download failure screenshot to: {screenshot_name}")
                except Exception as ex:
                    log.error(f"Failed to save screenshot: {ex}")
                stats["failed"] += 1
                failed_files.append(str(passport_path))
                need_reset = True
                log_failure(
                    passport_path.name,
                    "download_blob_image",
                    "Blob extraction failed or file could not be written",
                    "Screenshot saved, Force Session Reset on next batch",
                    "FAILED"
                )
                continue

            log.info(f"SUCCESS: {passport_path.name} -> {os.path.basename(final_path)}")
            stats["success"] += 1
            consecutive_timeouts = 0

            # Post-process disabled as per P17.0 Stage 1 specifications
            save_progress(passport_stem)

            # Scheduled cleanup every 10 iterations
            if (index + 1) % 10 == 0:
                log.info(f"🧹 {index + 1} iterations completed. Triggering scheduled sidebar chat cleanup...")
                try:
                    clean_old_chats(driver, keep_last=2, force=True)
                except Exception as clean_err:
                    log.warning(f"⚠️ Scheduled sidebar cleanup failed: {clean_err}")

        # ── RETRY PASS FOR TIMEOUT SKUs ───────────────────────────────────
        retry_stems = get_timeout_stems_from_log()
        current_progress = load_progress()
        retry_stems = [s for s in retry_stems if s not in current_progress]

        if retry_stems:
            log.info("\n" + "=" * 70)
            log.info(f"🔄 Starting retry pass for {len(retry_stems)} failed SKU(s)...")
            log.info(f"Failed SKUs to retry: {', '.join(retry_stems)}")
            log.info("=" * 70)
            
            consecutive_timeouts = 0
            for r_idx, stem in enumerate(retry_stems):
                passport_path = Path(MD_DIR) / f"{stem}.md"
                if not passport_path.exists():
                    log.warning(f"Passport file {passport_path} not found for retry. Skipping.")
                    continue
                    
                log.info(f"\n[Retry {r_idx + 1}/{len(retry_stems)}] Processing: {passport_path.name}")
                if r_idx > 0:
                    log.info("Sleeping 60s between retry attempts...")
                    time.sleep(60)
                    
                log.info("🔁 Force session reset for retry attempt.")
                try:
                    prime_gemini(driver)
                except Exception as e:
                    log.error(f"❌ WebDriver error in retry prime_gemini: {e}. Re-initializing driver...")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    time.sleep(5)
                    driver = create_driver()
                    try:
                        prime_gemini(driver)
                    except Exception as e2:
                        log.error(f"❌ Failed to prime re-initialized driver in retry: {e2}")
                        continue
                
                try:
                    passport_text = read_passport(passport_path)
                except Exception as e:
                    log.error(f"❌ Error reading file {passport_path.name}: {e}")
                    continue
                    
                files_before_download = get_current_files_in_downloads()
                try:
                    wait_for_chat_idle(driver, timeout=30)
                except Exception as e:
                    log.error(f"❌ WebDriver error in retry wait_for_chat_idle: {e}")
                    continue
                
                try:
                    responses_before = len(driver.find_elements(By.CSS_SELECTOR, "model-response, [data-testid='model-response']"))
                except Exception:
                    responses_before = 0
                    
                try:
                    send_message(driver, passport_text)
                except Exception as e:
                    log.error(f"❌ Error sending message in retry: {e}")
                    continue
                    
                try:
                    image_ready = wait_for_image_generation(driver, responses_before, IMAGE_GENERATION_TIMEOUT)
                except Exception as e:
                    log.error(f"❌ WebDriver error in retry wait_for_image_generation: {e}")
                    continue
                
                if not image_ready:
                    log.error(f"Retry TIMEOUT for '{passport_path.name}'.")
                    try:
                        screenshot_name = os.path.join(FAILED_DIR, f"error_gen_{stem}.png")
                        driver.save_screenshot(screenshot_name)
                        log.info(f"📸 Saved error screenshot to: {screenshot_name}")
                    except Exception as ex:
                        log.error(f"Failed to save screenshot: {ex}")
                    continue
                    
                time.sleep(POST_CLICK_DELAY)
                try:
                    final_path = download_blob_image(driver, stem)
                except Exception as e:
                    log.error(f"❌ WebDriver error in retry download_blob_image: {e}")
                    continue
                
                if not final_path:
                    log.error(f"Retry download failed for '{passport_path.name}'.")
                    try:
                        screenshot_name = os.path.join(FAILED_DIR, f"error_dl_{stem}.png")
                        driver.save_screenshot(screenshot_name)
                        log.info(f"📸 Saved error screenshot to: {screenshot_name}")
                    except Exception as ex:
                        log.error(f"Failed to save screenshot: {ex}")
                    continue
                    
                log.info(f"RETRY SUCCESS: {passport_path.name} -> {os.path.basename(final_path)}")
                stats["success"] += 1
                
                # Post-process disabled as per P17.0 Stage 1 specifications
                save_progress(stem)
                log.info(f"✅ Retry SKU {stem} successfully saved to progress.")

    except KeyboardInterrupt:
        log.info("\n⚠️  Прерывание пользователем (Ctrl+C). Сохраняем прогресс...")

    finally:
        try:
            driver.quit()
        except Exception:
            pass
        log.info("\n" + "=" * 70)
        log.info("  ИТОГИ ОБРАБОТКИ")
        log.info(f"  ✅ Успешно:   {stats['success']}")
        log.info(f"  ❌ Ошибки:    {stats['failed']}")
        log.info(f"  ⏭️  Пропущено: {stats['skipped']}")
        log.info(f"  📋 Лог:       {LOG_FILE}")
        if failed_files:
            log.info(f"\n  Файлы с ошибками:")
            for f in failed_files:
                log.info(f"    - {f}")
        try:
            print_estimate()
        except Exception:
            pass
        log.info("=" * 70)


if __name__ == "__main__":
    main()
