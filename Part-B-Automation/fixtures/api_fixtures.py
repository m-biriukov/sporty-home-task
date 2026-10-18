import datetime
import random

import pytest

from api.client import ApiClient
from api.models.matches import MatchModel
from helpers.exceptions import NoUpcomingMatchesException


@pytest.fixture
def api_client(settings) -> ApiClient:
    url = settings.base_url.rstrip("/") + settings.api_prefix
    return ApiClient(url, settings.user_id)


@pytest.fixture(scope="function", autouse=True)
def reset_user_balance(api_client):
    api_client.balance.reset_balance()


@pytest.fixture
def upcoming_match(api_client) -> MatchModel:
    # TODO: Workaround until BUG-001 will be fixed
    upcoming_matches = [
        item
        for item in api_client.matches.list_matches()
        if item.kickoff_date > datetime.date.today()
    ]
    if not upcoming_matches:
        raise NoUpcomingMatchesException()
    return random.choice(upcoming_matches)
