from aiogram import types
from aiogram.filters import BaseFilter
import config


class IsOwnerFilter(BaseFilter):
    """
    Custom filter "is_owner".
    """
    key = "is_owner"

    def __init__(self, is_owner):
        self.is_owner = is_owner

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in config.BOT_OWNERS


class IsAdminFilter(BaseFilter):
    """
    Filter that checks for admin rights existence
    """
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def __call__(self, message: types.Message) -> bool:
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin() == self.is_admin


class MemberCanRestrictFilter(BaseFilter):
    """
    Filter that checks member ability for restricting
    """
    key = 'member_can_restrict'

    def __init__(self, member_can_restrict: bool) -> bool:
        self.member_can_restrict = member_can_restrict

    async def __call__(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

        # I don't know why, but telegram thinks, if member is chat creator, he cant restrict member
        return (member.is_chat_creator() or member.can_restrict_members) == self.member_can_restrict
