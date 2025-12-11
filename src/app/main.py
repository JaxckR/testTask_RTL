import asyncio
import logging

from aiogram import Bot, Dispatcher
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from app.bootstrap.config import config, PostgresConfig
from app.bootstrap.ioc import providers
from app.bootstrap.logging import setup_logging
from app.presentation.bot.routes import setup_routes

logger = logging.getLogger(__name__)


async def app() -> None:
    bot = Bot(token=config.token)
    dp = Dispatcher()

    setup_logging()
    container = make_async_container(
        *providers(), context={PostgresConfig: config.postgres}
    )
    setup_dishka(container, router=dp, auto_inject=True)
    setup_routes(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(app())
    except (KeyboardInterrupt, SystemExit):
        logger.info("The bot was turned off")
