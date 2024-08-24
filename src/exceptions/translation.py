from typing import Any


class TranslationBaseError(Exception):
    def __init__(
        self,
        message: str,
        extra: dict[str | int, Any] | None = None
    ) -> None:
        self.message: str = message
        self.extra: dict[str | int, Any] = extra or {}


class TranslationClientError(TranslationBaseError):
    pass
