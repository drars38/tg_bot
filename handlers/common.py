from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.keyboards import login_keyboard

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.reply('👋Вас приветствует служба поддержки Транснефть. Пройдите регистрацию',
                        reply_markup=login_keyboard)
