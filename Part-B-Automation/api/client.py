from api.api_session import ApiSession
from api.balance import BalanceApi
from api.bets import BetsApi
from api.matches import MatchesApi


class ApiClient:
    def __init__(self, base_url: str, user_id: str):
        self.session = ApiSession(base_url, user_id)

    @property
    def matches(self) -> MatchesApi:
        return MatchesApi(self.session)

    @property
    def balance(self) -> BalanceApi:
        return BalanceApi(self.session)

    @property
    def bets(self) -> BetsApi:
        return BetsApi(self.session)
