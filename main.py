import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from config import env
from handlers import common, user, admin

logging.basicConfig(level=logging.INFO)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Получить помощь"),
    ]
    await bot.set_my_commands(commands)


async def main():
    bot_token = env.str("BOT_TOKEN")
    bot = Bot(token=bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(common.router)
    dp.include_router(admin.router)
    dp.include_router(user.router)

    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
