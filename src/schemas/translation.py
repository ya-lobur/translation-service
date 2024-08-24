from pydantic import BaseModel

from src.models.translation import Translation


class WordDetails(BaseModel):
    word: str
    original_language: str
    translation_details: Translation | list[Translation]


class WordList(BaseModel):
    words: list[WordDetails]
    total: int
