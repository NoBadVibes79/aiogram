from typing import Optional

from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PhotoSize, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from states import SaveCommon
from storage import add_photo, get_links_by_id


router = Router()


@router.inline_query(F.query == "links")
async def show_user_links(inline_query: InlineQuery):

    # Эта функция просто собирает текст, который будет
    # отправлен при нажатии на вариант в инлайн-режиме
    def get_message_text(
            link: str,
            title: str,
            description: Optional[str]
    ) -> str:
        text_parts = [f'{html.bold(html.quote(title))}']
        if description:
            text_parts.append(html.quote(description))
        text_parts.append("")  # добавим пустую строку
        text_parts.append(link)
        return "\n".join(text_parts)

    results = []
    for link, link_data in get_links_by_id(inline_query.from_user.id).items():
        # В итоговый массив запихиваем каждую запись
        results.append(InlineQueryResultArticle(
            id=link,  # ссылки у нас уникальные, потому проблем не будет
            title=link_data["title"],
            description=link_data["description"],
            input_message_content=InputTextMessageContent(
                message_text=get_message_text(
                    link=link,
                    title=link_data["title"],
                    description=link_data["description"]
                ),
                parse_mode="HTML"
            )
        ))
    # Важно указать is_personal=True!
    await inline_query.answer(results, is_personal=True)