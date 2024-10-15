from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


def _is_weekend() -> bool:
    # 5 - Saturday, 6 - Sunday
    return datetime.utcnow().weekday() in (5, 6)


# This will be inner-middleware for messages
class WeekendMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # If today is not Saturday or Sunday,
        # then we continue processing.
        if not _is_weekend():
            return await handler(event, data)
        # Otherwise it will simply return None
        # and processing will stop


# This will be outer-middleware for messages
class WeekendCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # If today is not Saturday or Sunday,
        # then we continue processing.
        if not _is_weekend():
            return await handler(event, data)
        # Otherwise it will simply return None
        # and processing will stop
        await event.answer(
            "Bot does not work on weekends!",
            show_alert=True
        )
        return