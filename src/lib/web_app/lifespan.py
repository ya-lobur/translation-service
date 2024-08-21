from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Type

from fastapi import FastAPI


class FastApiCustomLifespan(AbstractAsyncContextManager[None]):
    __slots__ = (
        'app',
    )

    def __init__(self, app: FastAPI) -> None:
        self.app = app

    async def __aenter__(self) -> None:
        await self.setup(self.app)

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        await self.shutdown(self.app)

    @staticmethod
    async def setup(app: FastAPI) -> None:
        pass

    @staticmethod
    async def shutdown(app: FastAPI) -> None:
        pass


__all__ = [
    'FastApiCustomLifespan'
]
