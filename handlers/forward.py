from aiogram import F, Router
from aiogram.types import Message, Chat

router = Router()
# No work
@router.message(F.forward_from_chat[F.type == "channel"].as_("channel"))
async def forwarded_from_channel(message: Message, channel: Chat):
    await message.answer(f"This channel's ID is {channel.id}")