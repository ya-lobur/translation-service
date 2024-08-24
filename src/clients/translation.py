import asyncio
from typing import Any

import httpcore
from googletrans import Translator
from googletrans.constants import DEFAULT_SERVICE_URLS
from googletrans.models import Translated
from httpx import Timeout

from src.exceptions.translation import TranslationClientError


class TranslationClient:
    def __init__(
        self,
        service_urls: list[str] | tuple[str] | None = None,
        raise_exception: bool = True,
        proxies: dict[str, httpcore._sync.interfaces.RequestInterface] | None = None,
        timeout: Timeout | None = None,
        **kwargs: Any,
    ) -> None:
        self._client = Translator(
            service_urls=service_urls or DEFAULT_SERVICE_URLS,
            raise_exception=raise_exception,
            proxies=proxies,
            timeout=timeout,
            **kwargs,
        )

    async def translate_word(
        self,
        word: str,
        dest: str = 'en',
        src: str = 'auto'
    ) -> Translated:
        try:
            result: Translated = await asyncio.to_thread(
                self._client.translate_legacy,
                text=word,
                dest=dest,
                src=src
            )
        except Exception as e:
            raise TranslationClientError(message=str(e))

        return result


__all__ = [
    'TranslationClient'
]
