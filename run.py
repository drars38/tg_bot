import asyncio
from app.bot import router

from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher

from app.database import create_table


# Загрузка токена из .env файла
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

# Инициализация бота и диспетчера
async def main():
    await create_table()  # Инициализация базы данных
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):

    await create_table()
    print('Starting up...')
async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
