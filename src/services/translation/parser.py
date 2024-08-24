from typing import Any

from googletrans.models import Translated
from more_itertools import first

from src.models.translation import PartOfSpeechAndSamples, Translation, Word


class GoogleTranslateApiDataParser:
    __slots__ = ()

    @staticmethod
    def _extract_definitions(data: Translated) -> list[PartOfSpeechAndSamples]:
        definitions = []
        raw_definitions = data.extra_data.get('definitions') or []

        for part_of_speech, *samples_data in raw_definitions:
            samples = [first(sample) for sample in first(samples_data, [])]
            definitions.append(PartOfSpeechAndSamples(
                part_of_speech=part_of_speech,
                samples=samples,
            ))

        return definitions

    @staticmethod
    def _extract_synonyms(data: Translated) -> list[PartOfSpeechAndSamples]:
        synonyms = []
        raw_synonyms = data.extra_data.get('synonyms') or []

        for part_of_speech, *samples_data in raw_synonyms:
            samples: list[str] = []
            for item in first(samples_data, [])[1:]:
                samples.extend(first(item, []))

            synonyms.append(PartOfSpeechAndSamples(
                part_of_speech=part_of_speech,
                samples=samples,
            ))

        return synonyms

    @staticmethod
    def _extract_possible_translations(data: Translated) -> list[PartOfSpeechAndSamples]:
        possible_translations = []
        raw_possible_translations = data.extra_data.get('all-translations') or []

        for part_of_speech, *samples_data in raw_possible_translations:
            samples: list[str] = first(samples_data, [])
            possible_translations.append(PartOfSpeechAndSamples(
                part_of_speech=part_of_speech,
                samples=samples,
            ))

        return possible_translations

    @staticmethod
    def _extract_examples(data: Translated) -> list[str]:
        examples = []
        raw_examples: list[Any] = first(data.extra_data.get('examples') or [], [])

        for example, *_ in raw_examples:
            examples.append(example)

        return examples

    @classmethod
    def parse(cls, data: Translated) -> Word:
        word_translation = Translation(
            language=data.dest,
            definitions=cls._extract_definitions(data),
            synonyms=cls._extract_synonyms(data),
            possible_translations=cls._extract_possible_translations(data),
            examples=cls._extract_examples(data),
        )

        return Word(_id=data.origin, original_language=data.src, translations=[word_translation])


__all__ = [
    'GoogleTranslateApiDataParser'
]
