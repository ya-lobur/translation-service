import logging
from typing import Any, Mapping, Self

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult, UpdateResult

from src.dependencies.resources import container
from src.enums.translations import WordsExpandEnum, WordsSortKeysEnum
from src.exceptions.translation import TranslationDbError
from src.models.translation import Word

logger = logging.getLogger(__name__)


class WordsRepository:
    __slots__ = (
        '_db',
        '_collection',
    )

    _instance: Self | None = None

    def __init__(self, db: AsyncIOMotorDatabase[Mapping[str, Any]]) -> None:
        self._db = db
        self._collection: AsyncIOMotorCollection[Mapping[str, Any]] = db.words

    async def get_word(self, word: str, language: str) -> Word | None:
        word_data = await self._collection.find_one({'_id': word})

        if word_data:
            model_word = Word(**word_data)
            translations = [t for t in model_word.translations if t.language == language]
            model_word.translations = translations
            return model_word
        return None

    async def upsert_word(self, word_data: Word) -> InsertOneResult | UpdateResult:
        logger.debug(f'Trying to upsert word "{word_data.word}"')
        existing_word = await self._collection.find_one({'_id': word_data.word})
        result: InsertOneResult | UpdateResult

        if existing_word is not None:
            result = await self._collection.update_one(
                filter={'_id': word_data.word},
                update={
                    '$addToSet': {
                        'translations': {
                            '$each': [translation.model_dump() for translation in word_data.translations]
                        }
                    }
                }
            )
        else:
            result = await self._collection.insert_one(word_data.model_dump(by_alias=True))
        logger.debug(f'"{word_data.word}" has been upserted')
        return result

    async def get_words(
        self,
        skip: int = 0,
        limit: int = 10,
        word_filter: str | None = None,
        sort_by: WordsSortKeysEnum | None = None,
        expands: list[WordsExpandEnum] | None = None,
    ) -> list[Word]:
        query = {}
        expands = expands or []
        projection: dict[str, Any] = {'_id': 1, 'original_language': 1}
        if expands:
            projection['translations'] = {expand.value: 1 for expand in expands}
            projection['translations']['language'] = 1

        if word_filter:
            query['_id'] = {'$regex': word_filter, '$options': 'i'}

        cursor = self._collection.find(query, projection).skip(skip).limit(limit)
        if sort_by:
            cursor = cursor.sort(sort_by.value)
        try:
            words = await cursor.to_list(length=limit)
        except OperationFailure as e:
            errmsg = e.details['errmsg'] if e.details else 'OperationFailure'
            raise TranslationDbError(f'Failed while getting words: {errmsg}')

        return [Word(**word) for word in words]

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls(container.mongodb)
        return cls._instance


__all__ = [
    'WordsRepository'
]
