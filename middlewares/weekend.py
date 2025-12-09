from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


def is_weekend() -> bool:
    """Check if today is Saturday (5) or Sunday (6)."""
    return datetime.now(timezone.utc).weekday() in (5, 6)


class WeekendMessageMiddleware(BaseMiddleware):
    """
    Middleware that blocks message processing on weekends.

    Usage:
        dp.message.middleware(WeekendMessageMiddleware())
    """

    def __init__(self, message: str = "Bot does not work on weekends!") -> None:
        """
        Args:
            message: Message to show when bot is disabled
        """
        self.message = message

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if is_weekend():
            await event.answer(self.message)
            return None

        return await handler(event, data)


class WeekendCallbackMiddleware(BaseMiddleware):
    """
    Middleware that blocks callback query processing on weekends.

    Usage:
        dp.callback_query.middleware(WeekendCallbackMiddleware())
    """

    def __init__(self, message: str = "Bot does not work on weekends!") -> None:
        """
        Args:
            message: Alert message to show when bot is disabled
        """
        self.message = message

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        if is_weekend():
            await event.answer(self.message, show_alert=True)
            return None

        return await handler(event, data)
