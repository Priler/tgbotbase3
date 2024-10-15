from aiogram.filters import BaseFilter
from aiogram.types import Message

from config_reader import get_config, BotConfig

class IsOwnerFilter(BaseFilter):
    def __init__(self, is_owner):
        self.is_owner = is_owner

    async def __call__(self, message: Message) -> bool:
        bot_config: BotConfig = get_config(model=BotConfig, root_key="bot")
        return message.from_user.id in bot_config.owners
