"""Run Selenium checks and append a timestamped, human-readable log file."""
from __future__ import annotations

import argparse
import logging
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def build_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("website_tests")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    return logger


def browser_details(driver: webdriver.Chrome) -> str:
    capabilities = driver.capabilities
    browser = capabilities.get("browserName", "unknown")
    version = capabilities.get("browserVersion", "unknown")
    return f"{browser} {version}"


def run_test(logger: logging.Logger, driver: webdriver.Chrome, base_url: str, test_id: str, name: str, fragment: str, expected: str) -> bool:
    started = time.perf_counter()
    url = f"{base_url}{fragment}"
    logger.info("TEST_START id=%s test=%s url=%s expected=%s", test_id, name, url, expected)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(lambda current: current.execute_script("return document.readyState") == "complete")
        element = WebDriverWait(driver, 5).until(lambda current: current.find_element(By.ID, fragment.removeprefix("#")))
        actual = f"section id={element.get_attribute('id')} is visible"
        elapsed = time.perf_counter() - started
        if elapsed >= 1.0:
            logger.warning("TEST_WARNING id=%s test=%s message=slow test time_taken=%.3fs", test_id, name, elapsed)
        logger.info("TEST_RESULT id=%s test=%s expected=%s actual=%s status=PASS time_taken=%.3fs", test_id, name, expected, actual, elapsed)
        return True
    except Exception as exc:  # Keep running subsequent tests after failures.
        elapsed = time.perf_counter() - started
        error_message = " ".join(str(exc).split()) or type(exc).__name__
        logger.error("TEST_RESULT id=%s test=%s expected=%s actual=section not found status=FAIL time_taken=%.3fs error=%s failure_url=%s", test_id, name, expected, elapsed, error_message, driver.current_url or url)
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://itpacifique.github.io/mugishapacifique.github.com/index.html")
    args = parser.parse_args()

    run_started = time.perf_counter()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = LOG_DIR / f"website-test-{timestamp}.log"
    logger = build_logger(log_path)
    driver = None
    results: list[bool] = []

    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        logger.info("RUN_HEADER date_time=%s website=%s browser=%s operating_system=%s", datetime.now(timezone.utc).isoformat(), args.url, browser_details(driver), platform.platform())

        tests = [
            ("TEST-001", "Main content container", "#main-content", "Main content container is present and visible"),
            ("TEST-002", "About section", "#about", "About section is present and visible"),
            ("TEST-003", "Projects section", "#projects", "Projects section is present and visible"),
            ("TEST-004", "Contact section", "#contact", "Contact section is present and visible"),
            ("TEST-005", "Missing-section failure handling", "#skills", "Missing Skills section should be reported as a failure"),
        ]
        for test in tests:
            results.append(run_test(logger, driver, args.url, *test))
    except WebDriverException as exc:
        logger.error("RUN_SETUP_ERROR error=%s", exc)
        return 1
    finally:
        if driver is not None:
            driver.quit()
            logger.info("BROWSER_CLOSED browser_session=complete")
        total = len(results)
        passed = sum(results)
        failed = total - passed
        duration = time.perf_counter() - run_started
        logger.info("RUN_SUMMARY total_tests=%d passed=%d failed=%d total_duration=%.3fs", total, passed, failed, duration)
        for handler in logger.handlers:
            handler.flush()
            handler.close()
            logger.removeHandler(handler)

    print(f"Log written to {log_path}")
    print(f"Summary: total_tests={len(results)} passed={sum(results)} failed={len(results) - sum(results)}")
    return 0 if results and sum(results) == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
