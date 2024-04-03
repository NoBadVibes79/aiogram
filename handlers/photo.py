from aiogram import Router, F
from aiogram.types import Message, PhotoSize

router = Router()

@router.message(F.photo[-1].as_("largest_photo"))
async def forward_from_channel_handler(message: Message, largest_photo: PhotoSize) -> None:
    print(largest_photo.width, largest_photo.height)