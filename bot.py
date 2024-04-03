import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config_reader import config
from handlers import group_games, usernames, photo, forward, email
from middlewares.standart import SomeMiddleware

# Запуск бота
async def main():
    default = DefaultBotProperties(parse_mode="HTML")
    bot = Bot(token=config.bot_token.get_secret_value(), default=default)
    dp = Dispatcher()
    
    email.router.message.middleware(SomeMiddleware())
    
    dp.include_routers(email.router, group_games.router, usernames.router, photo.router)
    
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())