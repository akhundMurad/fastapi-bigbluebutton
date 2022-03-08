from pydantic import BaseSettings

from src.core.settings import Settings


def settings_provider() -> BaseSettings:
    ...


def get_settings() -> Settings:
    return Settings()
