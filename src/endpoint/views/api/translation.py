import logging

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path, Query
from googletrans import LANGUAGES
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
    word: Annotated[str, Path(description='The word you want to translate')],
    dest_language: Annotated[str, Query(description='The destination language code', example='en')],
    src_language: Annotated[str, Query(description='The source language code (`auto` for auto detection)')] = 'auto',
) -> WordDetails:
    """Get the details about the given word."""
    if dest_language not in LANGUAGES:
        raise HTTPException(status_code=400, detail='Invalid `dest_language` language')

    if src_language not in {*LANGUAGES.keys(), 'auto'}:
        raise HTTPException(status_code=400, detail='Invalid `src_language` language')

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
async def delete_word(
    service: Annotated[TranslationService, Depends(TranslationService.get_instance)],
    word: str
) -> WordDetails:
    """Delete a word from the database."""
    result = await service.delete_word(word)
    if not result:
        raise HTTPException(status_code=404, detail='Word does not exist')

    return WordDetails(
        word=result.word,
        original_language=result.original_language,
        translation_details=result.translations,
    )


@router.get('/words/')
async def get_words(
    service: Annotated[TranslationService, Depends(TranslationService.get_instance)],
    skip: int = 0,
    limit: int = 10,
    word_filter: str | None = None,
    sort_by: WordsSortKeysEnum | None = None,
    expands: Annotated[
        list[WordsExpandEnum] | None,
        Query(description='Fields of `Translation` you want to be included in the response')
    ] = None,
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
