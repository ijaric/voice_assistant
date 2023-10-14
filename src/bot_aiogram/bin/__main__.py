import asyncio
import logging

import aiogram
import aiogram.contrib.fsm_storage.memory as fsm_storage_memory

import tgbot.handlers as tgbot_handlers
import tgbot.middlewares as tgbot_middlewares
import tgbot.settings as tgbot_settings

logger = logging.getLogger(__name__)


def register_all_middlewares(dp: aiogram.Dispatcher):
    dp.setup_middleware(tgbot_middlewares.environment.EnvironmentMiddleware())


def register_all_handlers(dp: aiogram.Dispatcher):
    tgbot_handlers.register_user(dp)
    tgbot_handlers.register_echo(dp)
    tgbot_handlers.register_voice_response(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = tgbot_settings.Settings()

    storage = fsm_storage_memory.MemoryStorage()
    bot = aiogram.Bot(token=config.tgbot.token.get_secret_value(), parse_mode="HTML")
    dp = aiogram.Dispatcher(bot, storage=storage)

    bot["config"] = config

    register_all_middlewares(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        if bot.session:
            await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
