from fastapi import APIRouter

from src.schemas.translation import WordDetails, WordList

router = APIRouter(
    prefix='/translation',
    tags=['translation'],
)


@router.get('/translate/{word}')
async def get_word_translation(  # type: ignore
    word: str,
    dest_language: str,  # todo: validation
    src_language: str,  # todo: validation + auto
) -> WordDetails:
    """Get the details about the given word."""


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
