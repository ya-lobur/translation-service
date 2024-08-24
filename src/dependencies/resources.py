import logging
from asyncio import Lock
from typing import TYPE_CHECKING, Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import settings

if TYPE_CHECKING:
    from collections.abc import Mapping

logger = logging.getLogger(__name__)


class ResourceContainer:

    def __init__(self) -> None:
        self._lock = Lock()

    async def setup(self) -> None:
        logger.info('Container is setting up...')
        async with self._lock:
            self.mongodb_client: AsyncIOMotorClient[Mapping[str, Any]] = AsyncIOMotorClient(
                settings.MONGO_DSN.unicode_string()
            )
            self.mongodb: AsyncIOMotorDatabase[Mapping[str, Any]] = self.mongodb_client['word_service']
        logger.info('Container is set up.')

    async def cleanup(self) -> None:
        logger.info('Container is cleaning up...')
        async with self._lock:
            self.mongodb_client.close()
        logger.info('Container is cleaned up.')


container = ResourceContainer()

__all__ = [
    'container'
]
