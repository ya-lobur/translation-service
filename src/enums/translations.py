from enum import StrEnum


class WordsExpandEnum(StrEnum):
    DEFINITIONS = 'definitions'
    SYNONYMS = 'synonyms'
    TRANSLATIONS = 'possible_translations'
    EXAMPLES = 'examples'


class WordsSortKeysEnum(StrEnum):
    WORD = '_id'
    LANGUAGE = 'original_language'
