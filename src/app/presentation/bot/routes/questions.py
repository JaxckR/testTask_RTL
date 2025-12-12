from aiogram import Router
from aiogram.types import Message
from dishka import FromDishka

from app.application.handlers.nl2sql import NL2SQLHandler

router = Router()


@router.message()
async def root(
    message: Message,
    handler: FromDishka[NL2SQLHandler],
) -> None:
    await message.answer(text=f"{await handler.handle(message.text)}")
