# -*- coding: utf-8 -*-
"""Снимает скриншот Gemini с раскрытым сайдбаром. НИЧЕГО НЕ УДАЛЯЕТ.

Нужен, чтобы визуально убедиться, есть ли вообще диалоги в аккаунте:
DOM-зонд показал 0 строк, но это может значить как «селектор не тот»,
так и «история действительно пуста».
"""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from selenium.webdriver.common.by import By
from src import rpa_orchestrator as rpa

OUT = os.path.join(ROOT, "00_PROJECT_STATE", "dom_dump")


def main():
    os.makedirs(OUT, exist_ok=True)
    driver = rpa.create_driver()
    try:
        driver.get(rpa.GEMINI_URL)
        time.sleep(8)
        driver.save_screenshot(os.path.join(OUT, "01_loaded.png"))

        # Раскрытие сайдбара — сначала настоящий клик мышью, затем JS-клик
        for attempt, use_js in enumerate([False, True], 1):
            btns = [b for b in driver.find_elements(
                By.CSS_SELECTOR, "button[data-test-id='side-nav-sparkle-button']")
                if b.is_displayed()]
            if not btns:
                break
            try:
                if use_js:
                    driver.execute_script("arguments[0].click();", btns[0])
                else:
                    btns[0].click()
            except Exception as e:
                print(f"attempt{attempt} click failed: {e}")
            time.sleep(4)
            cls = driver.find_element(
                By.CSS_SELECTOR, "side-navigation-content").get_attribute("class")
            print(f"attempt{attempt} js={use_js} class={cls}")
            driver.save_screenshot(os.path.join(OUT, f"02_after_expand_{attempt}.png"))
            if "rail" not in cls:
                break

        time.sleep(3)
        driver.save_screenshot(os.path.join(OUT, "03_final.png"))
        el = driver.find_element(By.CSS_SELECTOR, "side-navigation-content")
        print("SIDEBAR_TEXT_START")
        print((el.text or "")[:600])
        print("SIDEBAR_TEXT_END")
    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
