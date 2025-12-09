from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ConfirmCallback(CallbackData, prefix="confirm"):
    """Callback data for confirmation buttons."""
    action: str
    value: bool


def get_confirm_kb(
    confirm_text: str = "✅ Confirm",
    cancel_text: str = "❌ Cancel",
    action: str = "default",
) -> InlineKeyboardMarkup:
    """
    Create a confirmation keyboard with Confirm/Cancel buttons.

    Args:
        confirm_text: Text for confirm button
        cancel_text: Text for cancel button
        action: Action identifier for callback data

    Returns:
        InlineKeyboardMarkup with two buttons
    """
    builder = InlineKeyboardBuilder()

    builder.button(
        text=confirm_text,
        callback_data=ConfirmCallback(action=action, value=True),
    )
    builder.button(
        text=cancel_text,
        callback_data=ConfirmCallback(action=action, value=False),
    )

    builder.adjust(2)
    return builder.as_markup()
