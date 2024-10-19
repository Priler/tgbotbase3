import structlog
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message

from fluent.runtime import FluentLocalization

from filters.is_owner import IsOwnerFilter

# Declare router
router = Router()
router.message.filter(F.chat.type == "private", IsOwnerFilter(is_owner=True)) # allow bot admin actions only for bot owner

# Declare handlers
logger = structlog.get_logger()

# Handlers:
@router.message(Command("start"))
async def cmd_owner_hello(message: Message, l10n: FluentLocalization):
    await message.answer(
        l10n.format_value("hello-owner")
    )


# Here is some example !ping command ...
@router.message(
    IsOwnerFilter(is_owner=True),
    Command(commands=["ping"]),
)
async def cmd_ping_bot(message: Message, l10n: FluentLocalization):
    await message.reply(l10n.format_value("ping-msg"))
