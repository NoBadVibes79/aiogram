from random import choice
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text)
async def my_text_handler(message: Message):
    phrases = [
        "Привет! Отлично выглядишь :)",
        "Хэллоу, сегодня будет отличный день!",
        "Здравствуй)) улыбнись :)"
    ]
    if message.from_user.id in (111, 777):
        await message.answer(choice(phrases))
    else:
        await message.answer("Я с тобой не разговариваю!")