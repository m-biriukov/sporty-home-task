from datetime import datetime
from pathlib import Path

import allure
from selenium import webdriver

SCREENSHOTS_DIR = Path("screenshots")


def save_failure_screenshot(driver: webdriver.Remote, test_name: str) -> None:
    png = driver.get_screenshot_as_png()
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    (SCREENSHOTS_DIR / f"{test_name}-{timestamp}.png").write_bytes(png)
    allure.attach(
        png, name="screenshot", attachment_type=allure.attachment_type.PNG
    )
