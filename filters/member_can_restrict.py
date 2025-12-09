from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class MemberCanRestrictFilter(BaseFilter):
    """
    Filter that checks if user can restrict other members.

    Note: Chat creators always have restrict permissions, even if
    Telegram API doesn't explicitly report it.

    Usage:
        @router.message(MemberCanRestrictFilter())  # Can restrict
        @router.message(MemberCanRestrictFilter(can_restrict=False))  # Cannot restrict
    """

    def __init__(self, can_restrict: bool = True) -> None:
        """
        Args:
            can_restrict: If True, only users who can restrict pass.
        """
        self.can_restrict = can_restrict

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

        user_can_restrict = (
            member.is_chat_creator() or
            getattr(member, "can_restrict_members", False)
        )

        if self.can_restrict:
            return user_can_restrict
        return not user_can_restrict
