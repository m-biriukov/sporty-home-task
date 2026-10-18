# QA Engineer Assignment – Betting App

QA assignment for the betting app at https://qae-assignment-tau.vercel.app. The repository has three parts: manual test strategy, test automation and strategy recommendations.

## Repository structure

| Folder | Contents |
|---|---|
| [Part-A-Manual-QA-Test-Strategy](Part-A-Manual-QA-Test-Strategy) | Test plan (6 test cases), bug reports (7 bugs) and screenshots |
| [Part-B-Automation](Part-B-Automation) | pytest + Selenium + Allure framework with UI and API tests |
| [Part-C-Strategy-Recommendations](Part-C-Strategy-Recommendations) | Why these tests were automated, what stays manual, how to scale |

## Part A – Manual QA test strategy

### Test plan

| ID | Test case | Priority |
|---|---|---|
| 1 | [Successful bet placement](Part-A-Manual-QA-Test-Strategy/Test%20plan/1-place-bet.md) | Critical |
| 2 | [Validate stake boundary](Part-A-Manual-QA-Test-Strategy/Test%20plan/2-stake-boundary.md) | High |
| 3 | [Stake exceeding available balance is rejected](Part-A-Manual-QA-Test-Strategy/Test%20plan/3-max-bet.md) | Critical |
| 4 | [Duplicate submission does not create two bets](Part-A-Manual-QA-Test-Strategy/Test%20plan/4-duplicate-submission.md) | Critical |
| 5 | [Failed placement shows error modal, Rebet, Close and X behave correctly](Part-A-Manual-QA-Test-Strategy/Test%20plan/5-failed-bet-placement.md) | High |
| 6 | [POST /api/place-bet rejects invalid requests with correct error classes](Part-A-Manual-QA-Test-Strategy/Test%20plan/6-place-bet-via-api.md) | High |

### Bugs found

| ID | Bug | Severity |
|---|---|---|
| BUG-001 | [Past events are shown in "Upcoming" match list and accept bets](Part-A-Manual-QA-Test-Strategy/Bugs/Past-events-displayed-in-match-list.md) | Critical |
| BUG-002 | [Potential payout in bet confirmation does not match stake × odds](Part-A-Manual-QA-Test-Strategy/Bugs/Wrong-potential-payout-in-bet-confirmation.md) | High |
| BUG-003 | [Home and away teams are swapped in bet confirmation](Part-A-Manual-QA-Test-Strategy/Bugs/Teams-swapped-in-bet-confirmation.md) | Medium |
| BUG-004 | [place-bet API response returns currency "USD" instead of "EUR"](Part-A-Manual-QA-Test-Strategy/Bugs/Place-bet-api-returns-wrong-currency.md) | High |
| BUG-005 | [place-bet API accepts stake greater than user balance, balance goes negative](Part-A-Manual-QA-Test-Strategy/Bugs/Bet-stake-above-balance-accepted-via-api.md) | Critical |
| BUG-006 | [Balance in UI is not updated after bet placement until page refresh](Part-A-Manual-QA-Test-Strategy/Bugs/Balance-not-updated-after-bet-placement.md) | Medium |
| BUG-007 | [Repeated clicks on Place bet create multiple bets, balance goes negative](Part-A-Manual-QA-Test-Strategy/Bugs/Multiple-bets-on-repeated-place-bet-click.md) | Critical |

## Part B – Automation

Two automated tests:

- **UI:** place bet happy path (TC-1)
- **API:** stake above balance is rejected (TC-6)

Quick start:

```bash
cd Part-B-Automation
uv sync
cp .env.example .env   # set USER_ID
uv run pytest
allure serve allure-results
```

Requirements, configuration, project structure and conventions are in the [Part B README](Part-B-Automation/README.md).

## Part C – Strategy recommendations

The [Part C README](Part-C-Strategy-Recommendations/README.md) covers why these two tests were automated, which tests stay manual, recommendations for scaling (CI/CD, test layers and data, TMS) and a note on AI usage.
