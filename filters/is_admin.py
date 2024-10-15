from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdminFilter(BaseFilter):
    """
    Filter that checks for admin rights existence
    """
    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def __call__(self, message: Message) -> bool:
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin() == self.is_admin
