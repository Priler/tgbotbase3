from aiogram import types
from dispatcher import dp, bot
from aiogram.filters import Command

from aiogram import F
from filters import IsOwnerFilter

import config
import utils


# Group events goes here ...
# In order to read group messages, bot group privacy must be disabled
@dp.message(F.content_type.in_({'new_chat_members', 'left_chat_member'}))
async def on_user_join_or_left(message: types.Message):
    """
    Removes "user joined" and "user left" messages.
    By the way, bots do not receive left_chat_member updates when the group has more than 50 members (otherwise use https://core.telegram.org/bots/api#chatmemberupdated)
    :param message: Service message "User joined group
    """

    await message.delete()
