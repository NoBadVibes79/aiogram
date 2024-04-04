import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config_reader import config
from handlers import \
    admin_changes_in_group, bot_in_group, email, checkin, events_in_group, write_mail, in_pm
from middlewares.standart import \
    SomeMiddleware, UserInternalIdMiddleware, HappyMonthMiddleware
from middlewares.weekend import WeekendCallbackMiddleware
from middlewares.long_operation import ChatActionMiddleware

# Запуск бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    default = DefaultBotProperties(parse_mode="HTML")
    bot = Bot(token=config.bot_token.get_secret_value(), default=default)
    dp = Dispatcher()
    
    checkin.router.message.middleware(WeekendCallbackMiddleware())
    
    
    dp.update.outer_middleware(UserInternalIdMiddleware())
    email.router.message.middleware(SomeMiddleware())
    email.router.message.middleware(HappyMonthMiddleware())
    dp.callback_query.outer_middleware(WeekendCallbackMiddleware())
    write_mail.router.message.outer_middleware(ChatActionMiddleware())
    
    dp.include_routers(
        in_pm.router, events_in_group.router,
        bot_in_group.router, admin_changes_in_group.router
        )
    
    
    admins = await bot.get_chat_administrators(config.main_chat_id.get_secret_value())
    admin_ids = {admin.user.id for admin in admins}
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, admins=admin_ids) # allowed_updates=["message", "inline_query", "chat_member"]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())