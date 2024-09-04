from aiogram import types
from dispatcher import dp, bot
from aiogram.filters import Command

from aiogram import F
from filters import IsOwnerFilter

import config
import utils

@dp.message(
    Command(commands=["start"]),
)
async def cmd_start_bot(message: types.Message):
    await bot.send_message(message.chat.id, "<b>👊 Hello, world!</b>")


# Here is some example !ping command ...
@dp.message(
    IsOwnerFilter(is_owner=True),
    Command(commands=["ping"]),
)
async def cmd_ping_bot(message: types.Message):
    await message.reply("<b>👊 Up & Running!</b>\n\n")


# Here is some example content types command ...
@dp.message(F.content_type.in_({'photo', 'video'}))
async def cmd_media_react_bot(message: types.message):
    await message.reply("<b>🫡 Nice media (I guess)!</b>\n\n")
