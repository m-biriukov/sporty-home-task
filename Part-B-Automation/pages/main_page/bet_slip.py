from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

if TYPE_CHECKING:
    from pages.main_page.main_page import MainPage


class BetSlip:
    SLIP_COUNT = (By.ID, "bet-slip-count")
    SLIP_TITLE = (By.ID, "bet-slip-title")
    REMOVE_ALL = (By.ID, "bet-slip-remove-all")

    SELECTION_TEAMS = (By.CSS_SELECTOR, ".betSelectionTeams")
    SELECTION_MARKET = (By.CSS_SELECTOR, ".betSelectionMarket")
    SELECTION_ODD = (By.CSS_SELECTOR, ".betSelectionOdds")

    STAKE_CURRENCY = (By.CSS_SELECTOR, ".stakeCurrency")
    STAKE_INPUT = (By.ID, "bet-slip-stake-input")

    TOTAL_STAKE = (By.ID, "bet-slip-total-stake")
    POTENTIAL_PAYOUT = (By.ID, "bet-slip-potential-payout")

    PLACE_BET = (By.ID, "bet-slip-place-bet")
    EMPTY_BODY = (By.CSS_SELECTOR, ".betSlipBodyEmpty")

    def __init__(self, page: MainPage, element: WebElement):
        self.page = page
        self.element = element

    def get_count(self) -> int:
        return int(self.element.find_element(*self.SLIP_COUNT).text)

    def get_title(self) -> str:
        return self.element.find_element(*self.SLIP_TITLE).text

    def get_selection_teams(self) -> str:
        return self.element.find_element(*self.SELECTION_TEAMS).text

    def get_selection_odd(self) -> str:
        return self.element.find_element(*self.SELECTION_ODD).text

    def get_selection_market(self) -> str:
        return self.element.find_element(*self.SELECTION_MARKET).text

    def fill_stake_input(self, value: str, timeout: int = 10):
        element = self.element.find_element(*self.STAKE_INPUT)
        if element.get_attribute("value") == value:
            return
        total_before = self.get_total_stake()
        element.clear()
        element.send_keys(value)
        # Totals re-render asynchronously; wait so callers don't read stale
        WebDriverWait(self.page.driver, timeout).until(
            lambda _: self.get_total_stake() != total_before
        )

    def get_total_stake(self) -> str:
        return self.element.find_element(*self.TOTAL_STAKE).text

    def get_potential_payout(self) -> str:
        return self.element.find_element(*self.POTENTIAL_PAYOUT).text

    def is_place_bet_button_enabled(self):
        return self.element.find_element(*self.PLACE_BET).is_enabled()

    def click_place_bet_button(self):
        self.element.find_element(*self.PLACE_BET).click()

    def wait_place_bet_placing(self):
        self.page.wait_to_have_text(*self.PLACE_BET, "PLACING...")

    def is_empty(self) -> bool:
        return (
            self.get_count() == 0
            and len(self.element.find_elements(*self.EMPTY_BODY)) == 1
        )
