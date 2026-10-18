import re

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.main_page.bet_slip import BetSlip
from pages.main_page.match_item import MatchItem
from pages.main_page.modal_success import ModalSuccess


class MainPage(BasePage):
    MATCH_LIST = (By.CSS_SELECTOR, ".card.matchCard")
    BET_SLIP = (By.ID, "bet-slip")
    HEADER_BALANCE = (By.CSS_SELECTOR, "#header-balance span:last-of-type")

    def open(self, url: str | None = None):
        super().open(url)
        self.wait_to_be_visible(*self.MATCH_LIST)

    @property
    def bet_slip(self) -> BetSlip:
        return BetSlip(self, self.find_element(*self.BET_SLIP))

    @property
    def modal_success(self) -> ModalSuccess:
        return ModalSuccess(self)

    def get_matches(self) -> list[MatchItem]:
        return [
            MatchItem(self, element)
            for element in self.find_elements(*self.MATCH_LIST)
        ]

    def get_upcoming_matches(self) -> list[MatchItem]:
        return [
            match
            for match in self.get_matches()
            if match.get_status() == MatchItem.STATUS_UPCOMING
        ]

    def is_bet_slip_visible(self) -> bool:
        return self.is_visible(*self.BET_SLIP)

    def get_header_balance(self) -> float:
        text = self.find_element(*self.HEADER_BALANCE).text.replace(",", "")
        return float(re.findall(r"\d+(?:\.\d+)?", text)[0])
