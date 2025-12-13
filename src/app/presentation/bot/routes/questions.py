from aiogram import Router
from aiogram.types import Message
from dishka import FromDishka

from app.application.exceptions import TokensExpiredError
from app.application.handlers import NL2SQLHandler

router = Router()


@router.message()
async def root(
    message: Message,
    handler: FromDishka[NL2SQLHandler],
) -> None:
    try:
        await message.answer(text=f"{await handler.handle(message.text)}")
    except TokensExpiredError as e:
        await message.answer(text=str(e))
