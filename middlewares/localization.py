from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from fluent.runtime import FluentLocalization


EventType = Union[Message, CallbackQuery, PreCheckoutQuery]


class L10nMiddleware(BaseMiddleware):
    """
    Middleware that injects localization into handler data.

    The FluentLocalization object will be available as 'l10n' in handlers.

    Usage:
        @router.message()
        async def handler(message: Message, l10n: FluentLocalization):
            await message.answer(l10n.format_value("hello-msg"))
    """

    def __init__(self, locale: FluentLocalization) -> None:
        """
        Args:
            locale: FluentLocalization instance to inject
        """
        self.locale = locale

    async def __call__(
        self,
        handler: Callable[[EventType, Dict[str, Any]], Awaitable[Any]],
        event: EventType,
        data: Dict[str, Any],
    ) -> Any:
        data["l10n"] = self.locale
        return await handler(event, data)
