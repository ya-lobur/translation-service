from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from more_itertools import first
from typing_extensions import Annotated

from src.exceptions.translation import TranslationServiceError
from src.schemas.translation import WordDetails, WordList
from src.services.translation.translation import TranslationService

router = APIRouter(
    prefix='/translation',
    tags=['translation'],
)


@router.get('/translate/{word}')
async def get_word_translation(
    service: Annotated[TranslationService, Depends(TranslationService.get_instance)],
    word: str,
    dest_language: str,  # todo: validation
    src_language: str = 'auto',  # todo: validation + auto
) -> WordDetails:
    """Get the details about the given word."""
    try:
        word_data = await service.get_word_translation(word, dest_language, src_language)
    except TranslationServiceError as e:
        raise HTTPException(status_code=499, detail=e.message)

    return WordDetails(
        word=word_data.word,
        original_language=word_data.original_language,
        translation_details=first(word_data.translations),
    )


@router.delete('/word/{word}')
async def delete_word(word: str) -> WordDetails:  # type: ignore
    """Delete a word from the database."""


@router.get('/words/')
async def get_words(  # type: ignore
    # todo: PLR0913
    skip: int = 0,
    limit: int = 10,
    sort_by: str = 'word',
    word_filter: str | None = None,
    include_definitions: bool = False,
    include_synonyms: bool = False,
    include_translations: bool = False,
    include_examples: bool = False,
) -> WordList:
    """Get the list of the words stored in the database."""


__all__ = [
    'router'
]
