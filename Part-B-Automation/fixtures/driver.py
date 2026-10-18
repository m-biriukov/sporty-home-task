import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from helpers.exceptions import WrongBrowserNameException


def create_chrome_driver(headless: bool) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    # Fixed size so layout is the same headed and headless; the headless
    # default (800x600) overlaps the bet slip and intercepts clicks
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument("--headless=new")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


@pytest.fixture(scope="function")
def driver(settings):
    driver_item = None
    if settings.browser == "chrome":
        driver_item = create_chrome_driver(settings.headless)

    if driver_item is None:
        raise WrongBrowserNameException()

    yield driver_item

    driver_item.quit()
