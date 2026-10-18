## Tests for automation

I automated two tests.

1. **Place bet, happy path (UI, TC-1).** This is the main money flow: the user selects odds, enters a stake, places the bet and sees the confirmation and the new balance. If it breaks, nobody can bet, so it should run as a smoke test on every build.
2. **Stake above balance is rejected (API, TC-6).** The backend has to refuse a bet the user can't cover. Checking only the UI isn't enough, because anyone can call the API directly. A bug here means financial and regulatory risk. API tests are fast and stable, so this one is cheap to run often.

So one test covers the most important user path end to end, and the other covers the most important business rule on the layer that has to enforce it.

## Left as manual only

- **Stake boundary (TC-2).** High priority, but a bug here costs less. It's a good next candidate as a data-driven API test.
- **Max bet in UI (TC-3).** The risky part, backend validation, is already covered by TC-6. The UI error message and blocked button are quick to check by hand.
- **Duplicate submission (TC-4).** It depends on click timing, so in Selenium it would be flaky. I'd automate it next, but as an API test that sends parallel `/place-bet` calls rather than through the UI.
- **Failed bet placement (TC-5).** It needs the backend or network to fail on demand (a mock server or proxy), and the project doesn't have that yet.

## Recommendations for scaling

1. **CI/CD.** Run API tests on every PR and the UI smoke test (TC-1) on every deploy in headless mode. Publish Allure reports with history so flaky tests are easy to spot, and use Ruff as a quality gate.
2. **Test layers and data.** Business rules (stake limits, balance, payout, currency) belong in API tests, which are fast. UI tests should cover only a few critical journeys. Each run or worker should get its own test user, state should be reset through the API, and match data should be controlled so tests don't depend on live events or dates.
3. **Spec and TMS.** Test cases can live in a test management system as the single source of truth, linked to the spec, with automated tests linked to test case IDs through Allure.

## Notice about AI Usage
According to the rules, AI usage is not forbidden, but I want to be honest about the places where it is used:
- Test Case creation: Tests were written manually, but rewritten by AI to make them as clear as possible.
- Bugs: Bugs were found and filed manually, AI was used for formatting.
- Automation: Code review and implementation of some methods for the base page.