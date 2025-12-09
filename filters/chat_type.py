from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class ChatTypeFilter(BaseFilter):
    """
    Filter that checks chat type.

    Usage:
        @router.message(ChatTypeFilter("private"))
        @router.message(ChatTypeFilter(["group", "supergroup"]))
    """

    def __init__(self, chat_type: Union[str, list[str], set[str]]) -> None:
        """
        Args:
            chat_type: Single chat type or collection of allowed types.
                       Valid types: 'private', 'group', 'supergroup', 'channel'
        """
        if isinstance(chat_type, str):
            self.chat_types = {chat_type}
        else:
            self.chat_types = set(chat_type)

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        if isinstance(event, CallbackQuery):
            if event.message is None:
                return False
            chat_type = event.message.chat.type
        else:
            chat_type = event.chat.type

        return chat_type in self.chat_types
