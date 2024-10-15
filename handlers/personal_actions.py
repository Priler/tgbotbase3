import structlog
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from fluent.runtime import FluentLocalization

# Declare router
router = Router()
router.message.filter(F.chat.type == "private")

# Declare logger
logger = structlog.get_logger()

# Declare handlers
@router.message(Command("start"))
async def cmd_owner_hello(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("hello-msg"))


# Here is some example content types command ...
@router.message(F.content_type.in_({'photo', 'video'}))
async def cmd_media_react_bot(message: Message, l10n: FluentLocalization):
    await message.reply(l10n.format_value("media-msg"))
