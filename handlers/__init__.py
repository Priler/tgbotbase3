from aiogram import Dispatcher

from . import admin_actions, group_events, personal_actions


def register_all_handlers(dp: Dispatcher) -> None:
    """
    Register all handler routers with the dispatcher.

    Args:
        dp: Aiogram Dispatcher instance
    """
    dp.include_router(admin_actions.router)
    dp.include_router(group_events.router)
    dp.include_router(personal_actions.router)


__all__ = [
    "register_all_handlers",
    "admin_actions",
    "group_events",
    "personal_actions",
]
