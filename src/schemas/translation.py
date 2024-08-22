from pydantic import BaseModel


class TranslationDetails(BaseModel):
    language: str
    definitions: list[str] = []
    synonyms: list[str] = []
    translations: list[str] = []
    examples: list[str] = []


class WordDetails(BaseModel):
    word: str
    original_language: str
    translation_details: TranslationDetails | list[TranslationDetails]


class WordList(BaseModel):
    words: list[WordDetails]
    total: int
