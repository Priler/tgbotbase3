from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class HasUsernamesFilter(BaseFilter):
    """
    Filter that extracts mentioned usernames from message.

    If usernames are found, they are passed to the handler as 'usernames' argument.

    Usage:
        @router.message(HasUsernamesFilter())
        async def handler(message: Message, usernames: list[str]):
            for username in usernames:
                await message.answer(f"Found: {username}")
    """

    async def __call__(self, message: Message) -> Union[bool, dict[str, list[str]]]:
        entities = message.entities or []

        if not message.text:
            return False

        found_usernames = [
            item.extract_from(message.text)
            for item in entities
            if item.type == "mention"
        ]

        if found_usernames:
            return {"usernames": found_usernames}

        return False
