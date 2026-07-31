# -*- coding: utf-8 -*-
"""
Диагностика реального DOM сайдбара Gemini. НИЧЕГО НЕ УДАЛЯЕТ.

Задача: выяснить, почему clean_old_chats находит 0 чатов при непустом
сайдбаре, и снять фактические селекторы для фикса.

Установлено первым прогоном:
  * <side-navigation-content class="... rail ...">  — сайдбар свёрнут в
    узкую полосу; список диалогов в DOM НЕ отрисован;
  * раскрытие: <button data-test-id="side-nav-sparkle-button">
    (aria "Открыть боковую панель"). ВНИМАНИЕ: тот же data-test-id носит
    <a> «Новый чат» — различать по тегу button;
  * в сайдбаре есть <infinite-scroller> и data-test-id="loading-content-spinner",
    то есть список догружается асинхронно.

Отчёты пишутся в 00_PROJECT_STATE/dom_dump/ в UTF-8: консоль Windows
(cp1251) ломает кириллицу, поэтому результаты читаются из файлов.

Запуск:  python scripts/diagnose_sidebar_dom.py
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
from selenium.webdriver.common.action_chains import ActionChains

from src import rpa_orchestrator as rpa

OUT_DIR = os.path.join(ROOT, "00_PROJECT_STATE", "dom_dump")

EXPAND_BTN = "button[data-test-id='side-nav-sparkle-button']"
SPINNER = "[data-test-id='loading-content-spinner']"

# Широкая сеть на строку диалога — какой сработает, тот и пойдёт в фикс
ROW_CANDIDATES = [
    "div[data-test-id='conversation']",
    "[data-test-id='conversation']",
    "div.conversation",
    "conversation-items-container div.conversation",
    "conversation-item",
    "a[href*='/app/c/']",
    "[jslog][role='button'].conversation",
]

MENU_CANDIDATES = [
    "button.gem-conversation-actions-menu-button",      # текущий боевой
    "[data-test-id='actions-menu-button']",
    "button[data-test-id='actions-menu-button']",
    "span[data-test-id='actions-menu-button']",
    "button[aria-label*='ptions']",
    "mat-icon[fonticon='more_vert']",
]


def probe(driver, selectors, label, report):
    res = {}
    for sel in selectors:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            res[sel] = {"total": len(els),
                        "visible": sum(1 for e in els if e.is_displayed())}
        except Exception as e:
            res[sel] = {"error": e.__class__.__name__}
    report[label] = res
    return res


def dump_testids(driver, label, report):
    """Все data-test-id внутри раскрытого сайдбара."""
    try:
        el = driver.find_element(By.CSS_SELECTOR, "side-navigation-content")
        html = el.get_attribute("outerHTML")
    except Exception as e:
        report[label] = {"error": str(e)}
        return ""
    ids = Counter(re.findall(r'data-test-id="([^"]+)"', html))
    report[label] = {
        "sidebar_html_len": len(html),
        "class": (re.search(r'<side-navigation-content[^>]*class="([^"]*)"', html) or [None, ""])[1],
        "test_ids": dict(ids.most_common(60)),
    }
    return html


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    report = {}
    driver = rpa.create_driver()
    try:
        driver.get(rpa.GEMINI_URL)
        time.sleep(6)
        report["url"] = driver.current_url

        # ── Состояние 1: как загрузилось (сайдбар свёрнут) ──────────────
        probe(driver, ROW_CANDIDATES, "s1_rows_collapsed", report)
        probe(driver, MENU_CANDIDATES, "s1_menus_collapsed", report)
        dump_testids(driver, "s1_sidebar_collapsed", report)

        # ── Раскрываем сайдбар ─────────────────────────────────────────
        expanded = False
        btns = [b for b in driver.find_elements(By.CSS_SELECTOR, EXPAND_BTN) if b.is_displayed()]
        report["expand_buttons_found"] = len(btns)
        if btns:
            report["expand_aria"] = btns[0].get_attribute("aria-label")
            driver.execute_script("arguments[0].click();", btns[0])
            expanded = True
            time.sleep(3)
        report["expanded"] = expanded

        # ── Ждём, пока список догрузится ───────────────────────────────
        waited = 0
        while waited < 30:
            spinners = [e for e in driver.find_elements(By.CSS_SELECTOR, SPINNER) if e.is_displayed()]
            hits = 0
            for sel in ROW_CANDIDATES:
                hits += len([e for e in driver.find_elements(By.CSS_SELECTOR, sel) if e.is_displayed()])
            if hits > 0 and not spinners:
                break
            time.sleep(1.5)
            waited += 1.5
        report["wait_for_list_seconds"] = waited

        # ── Состояние 2: сайдбар раскрыт, список загружен ──────────────
        s2_rows = probe(driver, ROW_CANDIDATES, "s2_rows_expanded", report)
        probe(driver, MENU_CANDIDATES, "s2_menus_expanded", report)
        html = dump_testids(driver, "s2_sidebar_expanded", report)
        if html:
            io.open(os.path.join(OUT_DIR, "sidebar_expanded.html"), "w",
                    encoding="utf-8").write(html)

        # ── Состояние 3: наведение на первую строку ────────────────────
        row_sel = next((s for s, v in s2_rows.items()
                        if v.get("visible", 0) > 0), None)
        report["row_selector_used"] = row_sel
        if row_sel:
            rows = [e for e in driver.find_elements(By.CSS_SELECTOR, row_sel) if e.is_displayed()]
            report["rows_visible"] = len(rows)
            report["first_row_text"] = (rows[0].text or "")[:80]
            ActionChains(driver).move_to_element(rows[0]).perform()
            time.sleep(2)
            probe(driver, MENU_CANDIDATES, "s3_menus_after_hover", report)
            io.open(os.path.join(OUT_DIR, "row_hovered.html"), "w",
                    encoding="utf-8").write(rows[0].get_attribute("outerHTML"))
            ids = Counter(re.findall(r'data-test-id="([^"]+)"',
                                     rows[0].get_attribute("outerHTML")))
            report["hovered_row_test_ids"] = dict(ids)

        # ── Вердикт ────────────────────────────────────────────────────
        cur = "button.gem-conversation-actions-menu-button"
        report["verdict"] = {
            "боевой_селектор": cur,
            "свёрнутый_сайдбар": report.get("s1_menus_collapsed", {}).get(cur),
            "раскрытый_сайдбар": report.get("s2_menus_expanded", {}).get(cur),
            "после_наведения": report.get("s3_menus_after_hover", {}).get(cur),
        }
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        p = os.path.join(OUT_DIR, "diagnosis.json")
        io.open(p, "w", encoding="utf-8").write(
            json.dumps(report, ensure_ascii=False, indent=1))
        print("REPORT_WRITTEN " + p)


if __name__ == "__main__":
    main()
