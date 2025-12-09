from typing import Any, Awaitable, Callable, Dict, Optional, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from cachetools import TTLCache


EventType = Union[Message, CallbackQuery]


class ThrottlingMiddleware(BaseMiddleware):
    """
    Rate limiting middleware to prevent spam.

    Limits how often a user can send messages to the bot.

    Usage:
        dp.message.outer_middleware(ThrottlingMiddleware(rate_limit=0.5))
    """

    def __init__(
        self,
        rate_limit: float = 0.5,
        max_users: int = 10000,
        throttle_message: Optional[str] = None,
    ) -> None:
        """
        Args:
            rate_limit: Minimum seconds between messages per user
            max_users: Maximum number of users to track
            throttle_message: Optional message to send when throttled
        """
        self.cache: TTLCache = TTLCache(maxsize=max_users, ttl=rate_limit)
        self.throttle_message = throttle_message

    async def __call__(
        self,
        handler: Callable[[EventType, Dict[str, Any]], Awaitable[Any]],
        event: EventType,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user is None:
            return await handler(event, data)

        user_id = event.from_user.id

        if user_id in self.cache:
            if self.throttle_message and isinstance(event, Message):
                await event.answer(self.throttle_message)
            return None

        self.cache[user_id] = True
        return await handler(event, data)
