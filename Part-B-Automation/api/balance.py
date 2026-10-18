from __future__ import annotations

from typing import TYPE_CHECKING

from requests import Response

from api.models.balance import BalanceModel, BalanceResetModel

if TYPE_CHECKING:
    from api.api_session import ApiSession


class BalanceApi:
    def __init__(self, session: ApiSession):
        self.session = session

    def get_balance_raw(self) -> Response:
        return self.session.request("get", "/balance")

    def get_balance(self) -> BalanceModel:
        return BalanceModel.model_validate(self.get_balance_raw().json())

    def reset_balance_raw(self) -> Response:
        return self.session.request("post", "/reset-balance")

    def reset_balance(self) -> BalanceResetModel:
        return BalanceResetModel.model_validate(self.reset_balance_raw().json())
