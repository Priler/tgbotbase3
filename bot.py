import asyncio
import signal
from typing import Optional

import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from structlog.typing import FilteringBoundLogger

from config_reader import get_config, BotConfig, LogConfig, L10nConfig
from logs import get_structlog_config
from fluent_loader import get_fluent_localization
from middlewares import L10nMiddleware, ThrottlingMiddleware
from handlers import register_all_handlers


async def on_startup(bot: Bot, logger: FilteringBoundLogger) -> None:
    """Actions to perform on bot startup."""
    bot_info = await bot.get_me()
    await logger.ainfo(
        "Bot started",
        username=bot_info.username,
        bot_id=bot_info.id,
    )


async def on_shutdown(bot: Bot, logger: FilteringBoundLogger) -> None:
    """Actions to perform on bot shutdown."""
    await logger.ainfo("Bot stopped")


def setup_middlewares(dp: Dispatcher, l10n_config: L10nConfig) -> None:
    """Register all middlewares."""
    locale = get_fluent_localization(
        locale=l10n_config.default_locale,
        locales_dir=l10n_config.locales_path,
    )

    dp.message.outer_middleware(ThrottlingMiddleware(rate_limit=0.5))
    dp.message.outer_middleware(L10nMiddleware(locale))
    dp.callback_query.outer_middleware(L10nMiddleware(locale))
    dp.pre_checkout_query.outer_middleware(L10nMiddleware(locale))


async def main() -> None:
    """Main entry point."""
    log_config = get_config(model=LogConfig, root_key="logs")
    structlog.configure(**get_structlog_config(log_config))

    logger: FilteringBoundLogger = structlog.get_logger()

    bot_config = get_config(model=BotConfig, root_key="bot")
    l10n_config = get_config(model=L10nConfig, root_key="localization")

    bot = Bot(
        token=bot_config.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    setup_middlewares(dp, l10n_config)
    register_all_handlers(dp)

    stop_event = asyncio.Event()

    def signal_handler() -> None:
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, signal_handler)
        except NotImplementedError:
            pass

    await on_startup(bot, logger)

    try:
        polling_task = asyncio.create_task(
            dp.start_polling(bot, skip_updates=False)
        )

        await stop_event.wait()
        await logger.ainfo("Shutdown signal received...")

        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass

    finally:
        await on_shutdown(bot, logger)
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
