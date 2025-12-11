from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def root(message: Message) -> None:
    print(message.text)
