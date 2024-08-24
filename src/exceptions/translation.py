from typing import Any


class TranslationBaseError(Exception):
    def __init__(
        self,
        message: str,
        extra: dict[str | int, Any] | None = None
    ) -> None:
        self.message: str = message
        self.extra: dict[str | int, Any] = extra or {}

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.message!r}, {self.extra!r})'


class TranslationClientError(TranslationBaseError):
    pass


__all__ = [
    'TranslationBaseError',
    'TranslationClientError'
]
