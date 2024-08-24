from typing import Any, Mapping, Self

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from pymongo.results import InsertOneResult, UpdateResult

from src.dependencies.resources import container
from src.models.translation import Word


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

    async def add_word(self, word_data: Word) -> InsertOneResult | UpdateResult:
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

        return result

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls(container.mongodb)
        return cls._instance
