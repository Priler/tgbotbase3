"""
SQLite repository implementation.

Requires: pip install aiosqlite
"""
from typing import Any, Optional

try:
    import aiosqlite
except ImportError:
    aiosqlite = None

from .base import BaseRepository


class SQLiteRepository(BaseRepository):
    """
    SQLite repository implementation using aiosqlite.

    Usage:
        repo = SQLiteRepository("bot.db")
        await repo.init()
        # ... use repo ...
        await repo.close()
    """

    def __init__(self, db_path: str = "bot.db") -> None:
        if aiosqlite is None:
            raise ImportError("aiosqlite is required. Install with: pip install aiosqlite")

        self.db_path = db_path
        self._conn: Optional[aiosqlite.Connection] = None

    async def init(self) -> None:
        """Initialize database connection and create tables."""
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row

        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await self._conn.commit()

    async def get_user(self, user_id: int) -> Optional[dict[str, Any]]:
        if self._conn is None:
            raise RuntimeError("Database not initialized. Call init() first.")

        async with self._conn.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def save_user(self, user_id: int, data: dict[str, Any]) -> None:
        if self._conn is None:
            raise RuntimeError("Database not initialized. Call init() first.")

        columns = ["user_id"] + list(data.keys())
        placeholders = ", ".join(["?"] * len(columns))
        updates = ", ".join([f"{k} = ?" for k in data.keys()])

        values = [user_id] + list(data.values())
        update_values = list(data.values())

        await self._conn.execute(f"""
            INSERT INTO users ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT(user_id) DO UPDATE SET
            {updates}, updated_at = CURRENT_TIMESTAMP
        """, values + update_values)
        await self._conn.commit()

    async def delete_user(self, user_id: int) -> bool:
        if self._conn is None:
            raise RuntimeError("Database not initialized. Call init() first.")

        cursor = await self._conn.execute(
            "DELETE FROM users WHERE user_id = ?",
            (user_id,),
        )
        await self._conn.commit()
        return cursor.rowcount > 0

    async def get_all_users(self) -> list[dict[str, Any]]:
        if self._conn is None:
            raise RuntimeError("Database not initialized. Call init() first.")

        async with self._conn.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def count_users(self) -> int:
        if self._conn is None:
            raise RuntimeError("Database not initialized. Call init() first.")

        async with self._conn.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None
