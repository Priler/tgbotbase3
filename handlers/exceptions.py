import logging
from aiogram.handlers import ErrorHandler
from dispatcher import dp


@dp.errors()
class MyHandler(ErrorHandler):
    async def handle(self) -> any:
        logging.debug(
            "Cause unexpected exception %s: %s",
            self.exception_name,
            self.exception_message
        )
