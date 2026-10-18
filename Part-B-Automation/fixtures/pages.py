import pytest

from pages.main_page.main_page import MainPage


@pytest.fixture(scope="function")
def main_page(driver, settings) -> MainPage:
    page = MainPage(driver, settings.auth_url)
    page.open()
    return page
