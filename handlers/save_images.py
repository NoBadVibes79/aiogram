from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PhotoSize
from aiogram.filters.command import Command
from states import SaveCommon
from storage import add_photo

router = Router()

# @router.message(Command("save"))
# async def save_start(message: Message, state: FSMContext):
#     await state.set_state(SaveCommon.waiting_for_save_start)
#     await message.answer("Отправь мне сообщение со ссылкой или фото для сохранения.")

@router.message(SaveCommon.waiting_for_save_start, F.photo[-1].as_("photo"))
async def save_image(message: Message, photo: PhotoSize, state: FSMContext):
    add_photo(message.from_user.id, photo.file_id, photo.file_unique_id)
    await message.answer("Изображение сохранено!")
    await state.clear()