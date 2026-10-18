from http import HTTPStatus

import allure
import pytest

from api.models.bets import PlaceBetModel, SuccessBetModel
from api.models.error import ErrorMessageModel
from api.models.matches import MatchModel
from helpers.enums import Selection
from helpers.models import is_model_valid


@allure.issue(
    "BUG-005",
    "place-bet API accepts stake greater than user balance, balance goes negative",
)
@allure.severity(allure.severity_level.CRITICAL)
def test_bet_flow_over_balance(api_client, upcoming_match: MatchModel):
    balance = api_client.balance.get_balance()
    stake_1 = 50

    bet_1 = PlaceBetModel(
        match_id=upcoming_match.id, selection=Selection.HOME, stake=stake_1
    )
    bet_response_1 = api_client.bets.place_bet_raw(bet_1)

    assert bet_response_1.status_code == HTTPStatus.OK, (
        f"Bet within balance should be accepted. Expected: {HTTPStatus.OK}"
    )
    bet_response_1_json = bet_response_1.json()
    assert is_model_valid(SuccessBetModel, bet_response_1_json), (
        f"Response should match SuccessBetModel: {bet_response_1_json}"
    )

    balance_1 = api_client.balance.get_balance()
    expected_balance = balance.balance - stake_1
    assert balance_1.balance == pytest.approx(expected_balance), (
        f"Balance should decrease by stake. Expected: {expected_balance}"
    )

    bet_2 = PlaceBetModel(
        match_id=upcoming_match.id,
        selection=Selection.HOME,
        stake=balance_1.balance + 10,
    )
    bet_response_2 = api_client.bets.place_bet_raw(
        bet_2, validate_response=False
    )

    assert bet_response_2.status_code == HTTPStatus.CONFLICT, (
        f"Stake above balance should be rejected. "
        f"Expected: {HTTPStatus.CONFLICT}"
    )
    response_2_json = bet_response_2.json()
    assert is_model_valid(ErrorMessageModel, response_2_json), (
        f"Response should match ErrorMessageModel: {response_2_json}"
    )

    expected_message = "Insufficient balance"
    assert ErrorMessageModel(**response_2_json).message == expected_message, (
        f"Wrong error message. Expected: {expected_message}"
    )
    balance_2 = api_client.balance.get_balance()
    assert balance_2.balance == pytest.approx(balance_1.balance), (
        f"Balance should not change after rejected bet. "
        f"Expected: {balance_1.balance}"
    )
