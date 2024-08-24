from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config import defaults
from src.config.log import make_log_config


class AppSettings(BaseSettings):
    DEBUG: bool = defaults.DEBUG
    ENVIRONMENT: str = defaults.ENVIRONMENT

    ROOT_PATH: str = defaults.ROOT_PATH

    SERVICE_NAME: str = defaults.SERVICE_NAME
    SERVICE_VERSION: str = defaults.SERVICE_VERSION
    HOST: str = defaults.HOST
    PORT: int = defaults.PORT

    model_config = SettingsConfigDict(env_file=('.env.template', '.env'), extra='ignore')

    @property
    def LOGGING(self) -> dict[str, Any]:  # noqa: N803
        return make_log_config(self.DEBUG)

    @property
    def SWAGGER_URL(self) -> str | None:  # noqa: N803
        if self.ENVIRONMENT != 'prod':
            return defaults.SWAGGER_URL
        return None

    @property
    def REDOC_URL(self) -> str | None:  # noqa: N803
        if self.ENVIRONMENT != 'prod':
            return defaults.REDOC_URL
        return None


__all__ = [
    'AppSettings'
]
