from typing import Any, Optional

from .base import BaseRepository


class MemoryRepository(BaseRepository):
    """
    In-memory repository implementation.

    Useful for testing or small bots that don't need persistence.
    Data is lost when the bot restarts.
    """

    def __init__(self) -> None:
        self._users: dict[int, dict[str, Any]] = {}

    async def get_user(self, user_id: int) -> Optional[dict[str, Any]]:
        return self._users.get(user_id)

    async def save_user(self, user_id: int, data: dict[str, Any]) -> None:
        if user_id in self._users:
            self._users[user_id].update(data)
        else:
            self._users[user_id] = {"user_id": user_id, **data}

    async def delete_user(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    async def get_all_users(self) -> list[dict[str, Any]]:
        return list(self._users.values())

    async def count_users(self) -> int:
        return len(self._users)
