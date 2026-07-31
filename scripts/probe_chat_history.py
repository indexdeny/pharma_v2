# -*- coding: utf-8 -*-
"""Проверяет, есть ли в аккаунте диалоги, и как они выглядят в DOM.
НИЧЕГО НЕ УДАЛЯЕТ и НИЧЕГО НЕ ОТПРАВЛЯЕТ в Gemini.

Открывает панель «Поиск по чатам» (data-test-id='search-chats-button') —
единственное место в новом ia-redesign сайдбаре, где виден список истории.
"""
import io
import json
import os
import re
import sys
import time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from selenium.webdriver.common.by import By
from src import rpa_orchestrator as rpa

OUT = os.path.join(ROOT, "00_PROJECT_STATE", "dom_dump")


def main():
    os.makedirs(OUT, exist_ok=True)
    rep = {}
    driver = rpa.create_driver()
    try:
        driver.get(rpa.GEMINI_URL)
        time.sleep(8)

        # раскрыть сайдбар
        for b in driver.find_elements(By.CSS_SELECTOR,
                                      "button[data-test-id='side-nav-sparkle-button']"):
            if b.is_displayed():
                b.click()
                time.sleep(3)
                break

        # открыть «Поиск по чатам»
        opened = False
        for b in driver.find_elements(By.CSS_SELECTOR,
                                      "[data-test-id='search-chats-button']"):
            if b.is_displayed():
                b.click()
                opened = True
                time.sleep(4)
                break
        rep["search_panel_opened"] = opened
        driver.save_screenshot(os.path.join(OUT, "04_search_chats.png"))

        body = driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
        io.open(os.path.join(OUT, "search_panel.html"), "w",
                encoding="utf-8").write(body)
        rep["all_test_ids"] = dict(
            Counter(re.findall(r'data-test-id="([^"]+)"', body)).most_common(60))
        rep["href_app_c"] = len(re.findall(r'href="[^"]*/app/c/', body))

        # текст видимой области
        try:
            rep["dialog_text"] = (driver.find_element(
                By.CSS_SELECTOR, "[role='dialog'], mat-dialog-container").text or "")[:800]
        except Exception:
            rep["dialog_text"] = None
        rep["body_text_sample"] = (driver.find_element(
            By.TAG_NAME, "body").text or "")[:800]
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        io.open(os.path.join(OUT, "history_probe.json"), "w",
                encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1))
        print("WRITTEN")


if __name__ == "__main__":
    main()
