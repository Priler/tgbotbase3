import structlog
from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from fluent.runtime import FluentLocalization

# Declare router
router = Router()
router.message.filter(F.chat.type == "group") # process group events only

# Declare logger
logger = structlog.get_logger()

# Declare handlers
@router.message(F.content_type.in_({'new_chat_members', 'left_chat_member'}))
async def on_user_join_or_left(message: Message):
    """
    Removes "user joined" and "user left" messages.
    By the way, bots do not receive left_chat_member updates when the group has more than 50 members (otherwise use https://core.telegram.org/bots/api#chatmemberupdated)
    :param message: Service message "User joined group
    """

    await message.delete()
