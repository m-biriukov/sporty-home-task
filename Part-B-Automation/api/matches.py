from __future__ import annotations

from typing import TYPE_CHECKING

from requests import Response

from api.models.matches import MatchModel

if TYPE_CHECKING:
    from api.api_session import ApiSession


class MatchesApi:
    def __init__(self, session: ApiSession):
        self.session = session

    def list_matches_raw(self) -> Response:
        return self.session.request("get", "/matches")

    def list_matches(self) -> list[MatchModel]:
        response = self.list_matches_raw().json()
        return [MatchModel.model_validate(match) for match in response]
