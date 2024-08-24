from pydantic import BaseModel, Field


class PartOfSpeechAndSamples(BaseModel):
    part_of_speech: str
    samples: list[str] = []


class Translation(BaseModel):
    language: str
    definitions: list[PartOfSpeechAndSamples] = []
    synonyms: list[PartOfSpeechAndSamples] = []
    possible_translations: list[PartOfSpeechAndSamples] = []
    examples: list[str] = []


class Word(BaseModel):
    word: str = Field(..., alias='_id')
    original_language: str
    translations: list[Translation] = []


__all__ = [
    'Word',
    'PartOfSpeechAndSamples',
    'Translation',
]
