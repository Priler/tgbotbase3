import asyncio
from dispatcher import dp, bot
import handlers

async def main():
    await dp.start_polling(bot, skip_updates=False) # Don't skip updates, if your bot will process payments or other important stuff

if __name__ == "__main__":
    asyncio.run(main())
