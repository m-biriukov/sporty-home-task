from __future__ import annotations

from typing import TYPE_CHECKING

from requests import Response

from api.models.bets import PlaceBetModel, SuccessBetModel

if TYPE_CHECKING:
    from api.api_session import ApiSession


class BetsApi:
    def __init__(self, session: ApiSession):
        self.session = session

    def place_bet_raw(self, bet: PlaceBetModel, **kwargs) -> Response:
        return self.session.request(
            "post", "/place-bet", json=bet.model_dump(by_alias=True), **kwargs
        )

    def place_bet(self, bet: PlaceBetModel) -> SuccessBetModel:
        return SuccessBetModel.model_validate(self.place_bet_raw(bet).json())
