import logging
from typing import Self, Type

from src.clients import TranslationClient
from src.dependencies.resources import container
from src.enums.translations import WordsExpandEnum, WordsSortKeysEnum
from src.exceptions.translation import TranslationClientError, TranslationParseError, TranslationServiceError
from src.models.translation import Word
from src.repositories.words import WordsRepository
from src.services.translation.parser import GoogleTranslateApiDataParser

logger = logging.getLogger(__name__)


class TranslationService:
    __slots__ = (
        '_word_crud',
        '_parser',
        '_client'
    )

    _instance: Self | None = None

    def __init__(
        self,
        word_crud: WordsRepository,
        parser: Type[GoogleTranslateApiDataParser],
        client: TranslationClient
    ) -> None:
        self._word_crud = word_crud
        self._parser = parser
        self._client = client

    async def get_word_translation(
        self,
        word: str,
        dest_language: str,
        src_language: str = 'auto',
    ) -> Word:
        result: Word
        existing_word = await self._word_crud.get_word(word, language=dest_language)

        if not (existing_word and existing_word.translations):
            logger.debug(f'Cannot find word "{word}", trying to fetch translation...')
            try:
                translated = await self._client.translate_word(
                    word,
                    dest=dest_language,
                    src=src_language
                )
                parsed = self._parser.parse(translated)
                result = parsed
                await self._word_crud.upsert_word(result)
            except (TranslationClientError, TranslationParseError) as e:
                logger.error(e.message)
                raise TranslationServiceError(e.message)
        else:
            logger.debug(f'Word "{word}" got from db')
            result = existing_word

        return result

    async def get_words(
        self,
        skip: int = 0,
        limit: int = 10,
        word_filter: str | None = None,
        sort_by: WordsSortKeysEnum | None = None,
        expands: list[WordsExpandEnum] | None = None,
    ) -> list[Word]:
        return await self._word_crud.get_words(
            skip=skip,
            limit=limit,
            word_filter=word_filter,
            sort_by=sort_by,
            expands=expands
        )

    async def delete_word(self, word: str) -> Word | None:
        return await self._word_crud.delete_word(word)

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls(
                word_crud=WordsRepository(container.mongodb),
                parser=GoogleTranslateApiDataParser,
                client=container.translation_client
            )
        return cls._instance


__all__ = [
    'TranslationService'
]
