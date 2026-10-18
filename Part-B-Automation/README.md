# Part B – Automation

UI end-to-end tests for the betting app (https://qae-assignment-tau.vercel.app), built with pytest, Selenium and Allure.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Google Chrome (chromedriver is downloaded automatically)
- [Allure CLI](https://allurereport.org/docs/install/) to view reports (`brew install allure`)

## Setup

```bash
uv sync
cp .env.example .env
```

Set `USER_ID` in `.env` to your user ID. It is required; the run stops with a validation error if it's missing.

## Configuration

Settings come from `.env` (or environment variables) and can be overridden with CLI options:

| Setting | CLI option | Default |
|---|---|---|
| `BASE_URL` | `--base-url` | `https://qae-assignment-tau.vercel.app` |
| `USER_ID` | `--user-id` | none (required) |
| `API_PREFIX` | `--api-prefix` | `/api` |
| `BROWSER` | `--browser` | `chrome` (only option) |
| `HEADLESS` | `--headless` | `false` |
| `LOG_LEVEL` | `--log-level` | `INFO` (`DEBUG`, `INFO`, `WARNING`) |

## Running tests

```bash
uv run pytest                 # headed Chrome
uv run pytest --headless      # headless, e.g. for CI
uv run pytest --user-id=<id>  # without .env
```

## Project structure

```
api/                  API client
  api_session.py      requests session with base URL and x-user-id header
  client.py           ApiClient: entry point, exposes endpoint groups as properties
  balance.py          /balance, /reset-balance
  bets.py             /place-bet
  matches.py          /matches
  models/             pydantic request/response models
fixtures/             pytest fixtures, registered automatically as plugins
  api_fixtures.py     API client, balance reset before each test, upcoming match
  driver.py           Chrome driver setup and teardown
  pages.py            page object fixtures
helpers/              logging setup, failure screenshots, model validation, exceptions
pages/                page objects
  base_page.py        BasePage: open, find, click, waits
  main_page/          MainPage and its components (bet slip, match item, success modal)
tests/
  api_tests/          API tests
  ui_tests/           UI end-to-end tests
conftest.py           CLI options, settings loading, loggers, screenshot-on-failure hook
settings.py           pydantic settings model (.env + CLI overrides)
```

A new fixture module in `fixtures/` is picked up without changes to `conftest.py`.

## Project convention:
### - Common
- Assertion should be part of test, not a method.
- Use allure decorators to indicate bugs, severity, etc.
- Use [Ruff](https://docs.astral.sh/ruff/) as formatter and linter.
### - UI
- Each page should have its own implementation based on BasePage.
- Each page should have its own fixture that uses driver fixture.
- Each component should be as separate class without any parent. This prevents page class from enormous size and makes page interaction smoother.
- Project has a lot of ids, so use it. If no id, use CSS selectors, only then XPATH
### - Api
- Api client split their functionality into multiple subclasses as property
- It should be raw request that returns bare response, and method that returns object (Pydantic). List of models: [models](api/models)


## Reports and artifacts

| Path | Contents |
|---|---|
| `allure-results/` | Allure raw results, cleaned on every run |
| `screenshots/` | PNG of the browser when a test body fails, also attached to the Allure report |
| `logs/driver.log`, `logs/api.log` | Selenium and API logs |

View the Allure report:

```bash
allure serve allure-results
```