import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from app.bootstrap.config import config, PostgresConfig, Config, LLMConfig
from app.bootstrap.ioc import providers
from app.bootstrap.logging import setup_logging
from app.infrastructure.persistence.tables import map_tables
from app.presentation.bot.routes import setup_routes

logger = logging.getLogger(__name__)


async def app() -> None:
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    setup_logging()
    container = make_async_container(
        *providers(),
        context={
            PostgresConfig: config.postgres,
            LLMConfig: config.llm,
            Config: config,
        },
    )
    setup_dishka(container, router=dp, auto_inject=True)

    map_tables()
    setup_routes(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(app())
    except (KeyboardInterrupt, SystemExit):
        logger.info("The bot was turned off")
