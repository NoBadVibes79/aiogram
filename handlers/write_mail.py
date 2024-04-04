from aiogram.enums import MessageEntityType
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
import time

router = Router()

@router.message(Command("write_mail"), flags={"long_operation": "upload_video_note"})
async def all_emails(message: Message):
    time.sleep(20)
    await message.answer("Отправила по видео хихик")


@router.message(F.entities[...].type == MessageEntityType.EMAIL)
async def any_emails(message: Message):
    await message.answer("At least one email!")