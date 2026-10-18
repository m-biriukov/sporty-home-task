from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

if TYPE_CHECKING:
    from pages.main_page.main_page import MainPage


class ModalSuccess:
    MAIN = (By.ID, "modal-success")
    TITLE = (By.CSS_SELECTOR, ".modalTitle")
    BET_ID = (By.ID, "modal-success-bet-id")
    MATCH = (By.ID, "modal-success-match")
    STAKE = (By.ID, "modal-success-stake")
    ODDS = (By.ID, "modal-success-odds")
    PAYOUT = (By.ID, "modal-success-payout")
    PLACED_AT = (By.ID, "modal-success-placed-at")
    CLOSE = (By.ID, "modal-success-close")

    def __init__(self, page: MainPage):
        self.page = page

    @property
    def element(self) -> WebElement:
        return self.page.find_element(*self.MAIN)

    def is_present(self) -> bool:
        return self.page.is_visible(*self.MAIN)

    def is_closed(self) -> bool:
        return self.page.is_invisible(*self.MAIN)

    def get_title(self) -> str:
        return self.element.find_element(*self.TITLE).text

    def is_bet_id_present(self) -> bool:
        return self.page.is_visible(*self.BET_ID)

    def is_match_details_present(self) -> bool:
        return self.page.is_visible(*self.MATCH)

    def get_match_details(self) -> str:
        return self.element.find_element(*self.MATCH).text

    def is_stake_present(self) -> bool:
        return self.page.is_visible(*self.STAKE)

    def get_stake(self) -> str:
        return self.element.find_element(*self.STAKE).text

    def is_odds_present(self) -> bool:
        return self.page.is_visible(*self.ODDS)

    def get_odds(self) -> str:
        return self.element.find_element(*self.ODDS).text

    def is_potential_payout_present(self) -> bool:
        return self.page.is_visible(*self.PAYOUT)

    def get_potential_payout(self) -> str:
        return self.element.find_element(*self.PAYOUT).text

    def is_placed_at_present(self) -> bool:
        return self.page.is_visible(*self.PLACED_AT)

    def get_placed_at(self) -> str:
        return self.element.find_element(*self.PLACED_AT).text

    def is_close_button_enabled(self) -> bool:
        return self.element.find_element(*self.CLOSE).is_enabled()

    def click_close_button(self):
        self.element.find_element(*self.CLOSE).click()
