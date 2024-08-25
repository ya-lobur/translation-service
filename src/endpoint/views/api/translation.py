import logging

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from more_itertools import first
from typing_extensions import Annotated

from src.enums.translations import WordsExpandEnum, WordsSortKeysEnum
from src.exceptions.translation import TranslationDbError, TranslationServiceError
from src.schemas.translation import WordDetails
from src.services.translation.translation import TranslationService

router = APIRouter(
    prefix='/translation',
    tags=['translation'],
)

logger = logging.getLogger(__name__)


@router.get('/translate/{word}')
async def get_word_translation(
    service: Annotated[TranslationService, Depends(TranslationService.get_instance)],
    word: str,
    dest_language: str,  # todo: validation
    src_language: str = 'auto',  # todo: validation + auto
) -> WordDetails:
    """Get the details about the given word."""
    try:
        result = await service.get_word_translation(word, dest_language, src_language)
    except TranslationServiceError as e:
        logger.exception(e.message)
        raise HTTPException(status_code=499, detail=e.message)

    return WordDetails(
        word=result.word,
        original_language=result.original_language,
        translation_details=first(result.translations),
    )


@router.delete('/word/{word}')
async def delete_word(word: str) -> WordDetails:  # type: ignore
    """Delete a word from the database."""


@router.get('/words/')
async def get_words(
    # todo: PLR0913
    service: Annotated[TranslationService, Depends(TranslationService.get_instance)],

    skip: int = 0,
    limit: int = 10,

    word_filter: str | None = None,
    sort_by: WordsSortKeysEnum | None = None,
    expands: Annotated[list[WordsExpandEnum] | None, Query()] = None,

) -> list[WordDetails]:
    """Get the list of the words stored in the database."""
    result = []
    try:
        words = await service.get_words(
            skip=skip,
            limit=limit,
            word_filter=word_filter,
            sort_by=sort_by,
            expands=expands,
        )
    except TranslationDbError as e:
        logger.exception(e.message)
        raise HTTPException(status_code=400, detail=e.message)

    for word in words:
        result.append(WordDetails(
            word=word.word,
            original_language=word.original_language,
            translation_details=word.translations,
        ))

    return result


__all__ = [
    'router'
]
