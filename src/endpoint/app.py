from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.config import settings
from src.endpoint.routers import setup_routes
from src.lib.web_app import BaseWebApp


class WebApp(BaseWebApp):
    APP_NAME = settings.SERVICE_NAME
    APP_VERSION = settings.SERVICE_VERSION
    ROOT_PATH = settings.ROOT_PATH
    DEBUG = settings.DEBUG
    RESPONSE_CLASS = ORJSONResponse
    TIMEOUT_KEEP_ALIVE = 5
    DOCS_URL = settings.SWAGGER_URL
    REDOC_URL = settings.REDOC_URL

    def configure(self, app: FastAPI) -> None:  # noqa: PLR6301
        setup_routes(app)

    async def setup(self, app: FastAPI) -> None:
        pass

    async def shutdown(self, app: FastAPI) -> None:
        pass


web_app = WebApp()

__all__ = [
    'web_app',
]
