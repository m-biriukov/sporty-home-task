import logging
import pkgutil

import pytest
from _pytest.config import Config
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Item

import fixtures
from helpers.logging_helper import configure_logger
from helpers.screenshot import save_failure_screenshot
from settings import TestSettings

pytest_plugins = [
    f"{fixtures.__name__}.{module.name}"
    for module in pkgutil.iter_modules(fixtures.__path__)
    if not module.ispkg
]


def _load_settings(config: Config) -> TestSettings:
    overrides = {
        "base_url": config.getoption("--base-url"),
        "user_id": config.getoption("--user-id"),
        "api_prefix": config.getoption("--api-prefix"),
        "browser": config.getoption("--browser"),
        "headless": config.getoption("--headless"),
        # Reuses pytest's built-in --log-level option
        "log_level": config.getoption("--log-level"),
    }
    overrides = {
        key: value for key, value in overrides.items() if value is not None
    }
    return TestSettings(**overrides)


def pytest_addoption(parser):
    parser.addoption("--base-url", default=None)
    parser.addoption("--user-id", default=None)
    parser.addoption("--api-prefix", default=None)
    parser.addoption("--browser", default=None)
    parser.addoption("--headless", action="store_true", default=None)


def pytest_configure(config: Config):
    settings_item = _load_settings(config)
    for name, file in (("driver", "logs/driver.log"), ("api", "logs/api.log")):
        configure_logger(
            name,
            settings_item.log_level,
            settings_item.log_format,
            settings_item.log_datefmt,
            file,
        )


@pytest.fixture(scope="session")
def settings(request: FixtureRequest) -> TestSettings:
    return _load_settings(request.config)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item: Item, call):
    # Capture in the call phase (not fixture teardown) so the screenshot is
    # attached to the test body in Allure while the browser still shows the
    # failing state
    report = yield
    driver = item.funcargs.get("driver")
    if report.when == "call" and report.failed and driver is not None:
        # Never let a dead browser mask the original test failure
        try:
            save_failure_screenshot(driver, item.name)
        except Exception:
            logging.getLogger("driver").warning(
                "Failed to capture screenshot", exc_info=True
            )
    return report
