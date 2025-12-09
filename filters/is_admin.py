from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from typing import Union


class IsAdminFilter(BaseFilter):
    """
    Filter that checks if user has admin rights in the chat.

    Usage:
        @router.message(IsAdminFilter())  # Only admins
        @router.message(IsAdminFilter(is_admin=False))  # Only non-admins
    """

    def __init__(self, is_admin: bool = True) -> None:
        """
        Args:
            is_admin: If True, only admins pass. If False, only non-admins pass.
        """
        self.is_admin = is_admin

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        if event.from_user is None:
            return False

        if isinstance(event, CallbackQuery):
            if event.message is None:
                return False
            chat_id = event.message.chat.id
        else:
            chat_id = event.chat.id

        member = await event.bot.get_chat_member(chat_id, event.from_user.id)
        user_is_admin = member.is_chat_admin()

        if self.is_admin:
            return user_is_admin
        return not user_is_admin
