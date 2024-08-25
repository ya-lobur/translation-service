import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.config import settings
from src.dependencies.resources import container
from src.endpoint.routers import setup_routes
from src.lib.web_app import BaseWebApp

logger = logging.getLogger(__name__)


# todo: exception handlers
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
        logger.info('App is configuring...')
        setup_routes(app)
        logger.info('App is configured.')

    async def setup(self, app: FastAPI) -> None:  # noqa: PLR6301
        logger.info('App setting up...')
        await container.setup()
        logger.info('App is set up.')

    async def shutdown(self, app: FastAPI) -> None:  # noqa: PLR6301
        logger.info('App shutting down...')
        await container.cleanup()
        logger.info('App is shut down.')


web_app = WebApp()

__all__ = [
    'web_app',
]
