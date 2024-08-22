from pydantic import BaseModel, Field


class Translation(BaseModel):
    language: str
    definitions: list[str] = []
    synonyms: list[str] = []
    translations: list[str] = []
    examples: list[str] = []


class Word(BaseModel):
    word: str = Field(..., alias='_id')
    original_language: str
    translations: list[Translation]
