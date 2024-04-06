from typing import Optional

from aiogram import F, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import SaveCommon, TextSave
from filters import HasLinkFilter
from storage import add_link

router = Router()

@router.message(Command("save"))
async def save_start(message: Message, state: FSMContext):
    await state.set_state(SaveCommon.waiting_for_save_start)
    await message.answer("Отправь мне сообщение со ссылкой для сохранения.")

# Ловим сообщение где есть ссылка
@router.message(SaveCommon.waiting_for_save_start, F.text, HasLinkFilter())
async def save_text_has_link(message: Message, link: str, state: FSMContext):
    await state.update_data(link=link)
    await state.set_state(TextSave.waiting_for_title)
    await message.answer(
        text=f"Окей, я нашёл в сообщении ссылку {link}. "
             f"Теперь отправь мне заголовок (не больше 30 символов)"
    )

@router.message(SaveCommon.waiting_for_save_start, F.text)
async def save_text_no_link(message: Message):
    await message.answer(
        text="Эмм.. я не нашёл в твоём сообщении ссылку. "
             "Попробуй ещё раз или нажми /cancel, чтобы отменить."
    )
# заголовок записи
@router.message(TextSave.waiting_for_title, F.text.func(len) <= 30)
async def title_entered_ok(message: Message, state: FSMContext):
    await state.update_data(title=message.text, description=None)
    await state.set_state(TextSave.waiting_for_description)
    await message.answer(
        text="Так, заголовок вижу. Теперь введи описание "
             "(тоже не больше 30 символов) "
             "или нажми /skip, чтобы пропустить этот шаг"
    )

# Эта функция должна быть ПЕРЕД text_too_long() !
@router.message(TextSave.waiting_for_description, F.text.func(len) <= 30)
@router.message(TextSave.waiting_for_description, Command("skip"))
async def last_step(
        message: Message,
        state: FSMContext,
        command: Optional[CommandObject] = None
):
    if not command:
        await state.update_data(description=message.text)
    # Сохраняем данные в нашу ненастоящую БД
    data = await state.get_data()
    add_link(message.from_user.id, data["link"], data["title"], data["description"])

    await message.answer("Ссылка сохранена!")
    await state.clear()

@router.message(TextSave.waiting_for_title, F.text)
@router.message(TextSave.waiting_for_description, F.text)
async def text_too_long(message: Message):  # бывш. too_long_title()
    await message.answer("Слишком длинный заголовок. Попробуй ещё раз")
    return