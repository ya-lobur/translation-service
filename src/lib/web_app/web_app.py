from typing import Any, Type

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.lib.web_app.lifespan import FastApiCustomLifespan


def _make_lifespan(web_app: 'BaseWebApp') -> Type[FastApiCustomLifespan]:
    class Lifespan(FastApiCustomLifespan):
        @staticmethod
        async def setup(app: FastAPI) -> None:
            await web_app.setup(app)

        @staticmethod
        async def shutdown(app: FastAPI) -> None:
            await web_app.shutdown(app)

    return Lifespan


class BaseWebApp:
    __slots__ = (
        'app',
    )

    APP_NAME = 'APP'
    APP_DESC = ''
    APP_VERSION = '0.0.0'
    ROOT_PATH = ''
    DEBUG = False
    RESPONSE_CLASS = ORJSONResponse
    TIMEOUT_KEEP_ALIVE = 5
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None

    def __init__(self, **kwargs: Any) -> None:
        self.app = FastAPI(
            title=self.APP_NAME,
            description=self.APP_DESC,
            version=self.APP_VERSION,
            root_path=self.ROOT_PATH,
            docs_url=self.DOCS_URL,
            redoc_url=self.REDOC_URL,
            debug=self.DEBUG,
            lifespan=_make_lifespan(self),
            default_response_class=self.RESPONSE_CLASS,
            **kwargs
        )
        self.configure(self.app)

    def configure(self, app: FastAPI) -> None:
        pass

    async def setup(self, app: FastAPI) -> None:
        pass

    async def shutdown(self, app: FastAPI) -> None:
        pass

    def run(
        self,
        host: str,
        port: int,
    ) -> None:
        uvicorn.run(
            app=self.app,
            host=host,
            port=port,
        )


__all__ = [
    'BaseWebApp'
]
