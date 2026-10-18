from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    base_url: str = "https://qae-assignment-tau.vercel.app"
    user_id: str = Field(min_length=1)
    api_prefix: str = "/api"
    browser: Literal["chrome"] = "chrome"
    headless: bool = False

    log_level: Literal["DEBUG", "INFO", "WARNING"] = "INFO"
    log_format: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    log_datefmt: str = "%Y-%m-%d %H:%M:%S"

    currency: str = "EUR"

    @property
    def auth_url(self) -> str:
        return self.base_url.rstrip("/") + f"?user-id={self.user_id}"
