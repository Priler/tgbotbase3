from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PaginationCallback(CallbackData, prefix="page"):
    """Callback data for pagination buttons."""
    action: str
    page: int


def get_pagination_kb(
    current_page: int,
    total_pages: int,
    action: str = "list",
) -> InlineKeyboardMarkup:
    """
    Create a pagination keyboard.

    Args:
        current_page: Current page number (1-indexed)
        total_pages: Total number of pages
        action: Action identifier for callback data

    Returns:
        InlineKeyboardMarkup with navigation buttons
    """
    builder = InlineKeyboardBuilder()

    if current_page > 1:
        builder.button(
            text="« First",
            callback_data=PaginationCallback(action=action, page=1),
        )
        builder.button(
            text="‹ Prev",
            callback_data=PaginationCallback(action=action, page=current_page - 1),
        )

    builder.button(
        text=f"{current_page}/{total_pages}",
        callback_data=PaginationCallback(action=action, page=current_page),
    )

    if current_page < total_pages:
        builder.button(
            text="Next ›",
            callback_data=PaginationCallback(action=action, page=current_page + 1),
        )
        builder.button(
            text="Last »",
            callback_data=PaginationCallback(action=action, page=total_pages),
        )

    builder.adjust(5)
    return builder.as_markup()
