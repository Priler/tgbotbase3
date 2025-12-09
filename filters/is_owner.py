from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from typing import Union

from config_reader import get_config, BotConfig


class IsOwnerFilter(BaseFilter):
    """
    Filter that checks if user is a bot owner.

    Usage:
        @router.message(IsOwnerFilter())  # Only owners
        @router.message(IsOwnerFilter(is_owner=False))  # Only non-owners
    """

    def __init__(self, is_owner: bool = True) -> None:
        """
        Args:
            is_owner: If True, only owners pass. If False, only non-owners pass.
        """
        self.is_owner = is_owner

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        bot_config = get_config(model=BotConfig, root_key="bot")

        if event.from_user is None:
            return False

        user_is_owner = event.from_user.id in bot_config.owners

        if self.is_owner:
            return user_is_owner
        return not user_is_owner
