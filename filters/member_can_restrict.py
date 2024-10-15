from aiogram.filters import BaseFilter
from aiogram.types import Message

class MemberCanRestrictFilter(BaseFilter):
    """
    Filter that checks member ability for restricting
    """
    def __init__(self, member_can_restrict: bool):
        self.member_can_restrict = member_can_restrict

    async def __call__(self, message: Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

        # I don't know why, but telegram thinks, if member is chat creator, he cant restrict member
        return (member.is_chat_creator() or member.can_restrict_members) == self.member_can_restrict
