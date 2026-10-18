from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from helpers.enums import Selection

if TYPE_CHECKING:
    from pages.main_page.main_page import MainPage


class MatchItem:
    ODDS_BUTTON_VALUE = (By.CSS_SELECTOR, ".oddsButtonValue")
    TEAMS = (By.CSS_SELECTOR, ".teamName")
    STATUS_BADGE = (By.CSS_SELECTOR, ".matchMeta .badge")

    STATUS_UPCOMING = "UPCOMING"

    def __init__(self, page: MainPage, element: WebElement):
        self.page = page
        self.element = element

    @staticmethod
    def _odds_locator(selection: Selection) -> tuple[str, str]:
        value = selection.value.lower()
        return By.CSS_SELECTOR, f'[id^="odds-"][id$="-{value}"]'

    def click_odd(self, selection: Selection):
        self.element.find_element(*self._odds_locator(selection)).click()

    def get_odds_value(self, selection: Selection) -> float:
        button = self.element.find_element(*self._odds_locator(selection))
        return float(button.find_element(*self.ODDS_BUTTON_VALUE).text)

    def get_teams(self) -> list[str]:
        return [team.text for team in self.element.find_elements(*self.TEAMS)]

    def get_status(self) -> str:
        return self.element.find_element(*self.STATUS_BADGE).text
