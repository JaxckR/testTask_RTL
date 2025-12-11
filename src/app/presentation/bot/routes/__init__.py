__all__ = ["setup_routes"]

from typing import Final

from aiogram import Dispatcher, Router

from .questions import router as questions_router

ROUTES: Final[list[Router]] = [questions_router]


def setup_routes(dp: Dispatcher) -> None:
    dp.include_routers(*ROUTES)
