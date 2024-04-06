from typing import Optional
# import class ViaBotFilter, give me 3 variable, not from aiogram.filters.via_bot
from aiogram import F, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import DeleteCommon
from filters import HasLinkFilter
from storage import delete_image, delete_link


router = Router()

@router.message(
    DeleteCommon.waiting_for_delete_start,
    F.text,
    HasLinkFilter()
)
async def link_deletion_handler(message: Message, link: str, state: FSMContext):
    delete_link(message.from_user.id, link)
    await state.clear()
    await message.answer(
        text="Ссылка удалена! "
             "Выдача инлайн-режима обновится в течение нескольких минут.")

@router.message(
    DeleteCommon.waiting_for_delete_start,
    F.photo[-1].file_unique_id.as_("file_unique_id"),
)
async def image_deletion_handler(
        message: Message,
        state: FSMContext,
        file_unique_id: str
):
    delete_image(message.from_user.id, file_unique_id)
    await state.clear()
    await message.answer(
        text="Изображение удалено! "
             "Выдача инлайн-режима обновится в течение нескольких минут.")
