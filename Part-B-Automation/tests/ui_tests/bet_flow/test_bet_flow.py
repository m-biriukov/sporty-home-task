from datetime import datetime, timedelta

import allure
import pytest

from helpers.enums import Selection
from pages.main_page.main_page import MainPage


@allure.issue(
    "BUG-001", "Past events are shown in 'Upcoming' match list and accept bets"
)
@allure.issue(
    "BUG-002",
    "Potential payout in bet confirmation does not match stake × odds",
)
@allure.issue("BUG-003", "Home and away teams are swapped in bet confirmation")
@allure.issue(
    "BUG-006",
    "Balance in UI is not updated after bet placement until page refresh",
)
@allure.severity(allure.severity_level.CRITICAL)
def test_bet_flow(main_page: MainPage):
    """
    End-to-end happy path: select odds, place a bet, verify confirmation and balance.
    """
    stake = 5.5
    selection = Selection.HOME
    expected_stake = f"€{stake:.2f}"

    initial_balance = main_page.get_header_balance()
    upcoming_matches = main_page.get_upcoming_matches()
    assert upcoming_matches, "At least one upcoming match should be listed"
    match = upcoming_matches[0]
    teams = match.get_teams()
    odds_value = match.get_odds_value(selection)
    match.click_odd(selection)

    assert main_page.is_bet_slip_visible(), (
        "Bet slip should be visible after odds selection"
    )
    bet_slip = main_page.bet_slip
    assert bet_slip.get_count() == 1, "Bet count should be 1"

    expected_slip_title = "Bet Slip"
    assert bet_slip.get_title() == expected_slip_title, (
        f"Wrong slip title. Expected: {expected_slip_title}"
    )
    expected_selection_teams = f"{teams[0]} vs {teams[1]}"
    assert bet_slip.get_selection_teams() == expected_selection_teams, (
        f"Wrong selection teams. Expected: {expected_selection_teams}"
    )
    expected_market = f"Match Winner: {selection.label}"
    assert bet_slip.get_selection_market() == expected_market, (
        f"Wrong selection market. Expected: {expected_market}"
    )
    expected_odds = f"Odds: {odds_value:.2f}"
    assert bet_slip.get_selection_odd() == expected_odds, (
        f"Wrong selection odds. Expected: {expected_odds}"
    )

    bet_slip.fill_stake_input(str(stake))

    assert bet_slip.get_total_stake() == expected_stake, (
        f"Wrong total stake in bet slip. Expected: {expected_stake}"
    )
    expected_potential_payout = f"€{stake * odds_value:.2f}"
    assert bet_slip.get_potential_payout() == expected_potential_payout, (
        f"Wrong potential payout in bet slip. Expected: {expected_potential_payout}"
    )
    assert bet_slip.is_place_bet_button_enabled(), (
        "Place bet button should be enabled after entering stake"
    )

    # Lower bound of the placement window, floored to the minute because the
    # modal shows HH:MM only
    placed_after = datetime.now().replace(second=0, microsecond=0)
    bet_slip.click_place_bet_button()
    bet_slip.wait_place_bet_placing()

    modal_success = main_page.modal_success
    assert modal_success.is_present(), (
        "Success modal should be shown after placing bet"
    )
    expected_modal_title = "Bet Placed Successfully!"
    assert modal_success.get_title() == expected_modal_title, (
        f"Wrong modal title. Expected: {expected_modal_title}"
    )

    assert modal_success.is_bet_id_present(), (
        "Bet ID should be present in modal"
    )
    assert modal_success.is_match_details_present(), (
        "Match details should be present in modal"
    )
    assert modal_success.get_match_details() == expected_selection_teams, (
        f"Wrong match details in modal. Expected: {expected_selection_teams}"
    )

    assert modal_success.is_stake_present(), "Stake should be present in modal"
    assert modal_success.get_stake() == expected_stake, (
        f"Wrong stake in modal. Expected: {expected_stake}"
    )

    assert modal_success.is_odds_present(), "Odds should be present in modal"
    assert modal_success.get_odds() == f"{odds_value:.2f}", (
        f"Wrong odds in modal. Expected: {odds_value:.2f}"
    )

    assert modal_success.is_potential_payout_present(), (
        "Potential payout should be present in modal"
    )
    assert modal_success.get_potential_payout() == expected_potential_payout, (
        f"Wrong potential payout in modal. Expected: {expected_potential_payout}"
    )

    assert modal_success.is_placed_at_present(), (
        "Placed at time should be present in modal"
    )
    # The backend stamps the bet between the click and the modal appearing,
    # so a single now() can be off by a minute if that span crosses a
    # minute boundary. Accept every minute in [click, modal] instead of a
    # fixed +/-1 min tolerance, which would also accept genuinely wrong
    # times.
    placed_before = datetime.now()
    expected_placed_at = []
    minute = placed_after
    while minute <= placed_before:
        expected_placed_at.append(minute.strftime("TODAY, %H:%M"))
        minute += timedelta(minutes=1)

    assert modal_success.get_placed_at() in expected_placed_at, (
        f"Wrong placed at time in modal. Expected one of: {expected_placed_at}"
    )

    assert modal_success.is_close_button_enabled(), (
        "Close button should be enabled in modal"
    )
    modal_success.click_close_button()
    assert modal_success.is_closed(), (
        "Success modal should be closed after clicking close"
    )

    assert main_page.bet_slip.is_empty(), (
        "Bet slip should have no active selection after closing modal"
    )
    expected_balance = initial_balance - stake
    assert main_page.get_header_balance() == pytest.approx(expected_balance), (
        f"Balance should decrease by stake. Expected: {expected_balance}"
    )
