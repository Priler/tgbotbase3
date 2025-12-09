import structlog
from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest


router = Router(name="groups")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

logger = structlog.get_logger()


@router.message(F.content_type.in_({"new_chat_members", "left_chat_member"}))
async def on_user_join_or_left(message: Message) -> None:
    """
    Delete 'user joined' and 'user left' service messages.

    Note: Bots don't receive left_chat_member updates when the group
    has more than 50 members. Use ChatMemberUpdated for larger groups.
    """
    try:
        await message.delete()
    except TelegramBadRequest as e:
        await logger.awarning(
            "Failed to delete service message",
            chat_id=message.chat.id,
            error=str(e),
        )


@router.message(F.content_type == "new_chat_title")
async def on_chat_title_changed(message: Message) -> None:
    """Log when chat title is changed."""
    await logger.ainfo(
        "Chat title changed",
        chat_id=message.chat.id,
        new_title=message.chat.title,
    )


@router.message(F.content_type == "pinned_message")
async def on_message_pinned(message: Message) -> None:
    """Handle pinned message events."""
    await logger.ainfo(
        "Message pinned",
        chat_id=message.chat.id,
        pinned_message_id=message.pinned_message.message_id if message.pinned_message else None,
    )
