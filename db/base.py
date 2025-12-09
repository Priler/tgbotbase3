from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseRepository(ABC):
    """
    Abstract base class for data repositories.

    Implement this class to create database-specific repositories
    (SQLite, PostgreSQL, Redis, etc.)
    """

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[dict[str, Any]]:
        """
        Get user data by ID.

        Args:
            user_id: Telegram user ID

        Returns:
            User data dict or None if not found
        """
        ...

    @abstractmethod
    async def save_user(self, user_id: int, data: dict[str, Any]) -> None:
        """
        Save or update user data.

        Args:
            user_id: Telegram user ID
            data: User data to save
        """
        ...

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete user data.

        Args:
            user_id: Telegram user ID

        Returns:
            True if user was deleted, False if not found
        """
        ...

    @abstractmethod
    async def get_all_users(self) -> list[dict[str, Any]]:
        """
        Get all users.

        Returns:
            List of user data dicts
        """
        ...

    @abstractmethod
    async def count_users(self) -> int:
        """
        Get total user count.

        Returns:
            Number of users
        """
        ...

    async def close(self) -> None:
        """Close database connection."""
        pass
