import structlog
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from filters import IsOwnerFilter


router = Router(name="personal")
router.message.filter(F.chat.type == "private", IsOwnerFilter(is_owner=False))

logger = structlog.get_logger()


@router.message(Command("start"))
async def cmd_start(message: Message, l10n: FluentLocalization) -> None:
    """Handle /start command for regular users."""
    await logger.ainfo(
        "User started bot",
        user_id=message.from_user.id if message.from_user else None,
        username=message.from_user.username if message.from_user else None,
    )
    await message.answer(l10n.format_value("hello-msg"))


@router.message(Command("help"))
async def cmd_help(message: Message, l10n: FluentLocalization) -> None:
    """Handle /help command."""
    await message.answer(l10n.format_value("help-msg"))


@router.message(F.content_type.in_({"photo", "video"}))
async def on_media(message: Message, l10n: FluentLocalization) -> None:
    """React to photo and video messages."""
    await message.reply(l10n.format_value("media-msg"))
