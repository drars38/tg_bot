from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.database import (add_user, check_user_or_registr, get_history,
                          get_blocked_user_message, get_black_list,
                          respond_to_message, get_chat_id, get_message, add_message)
from app.keyboards import user_keyboard_after_login, banned_user, admin_keyboard, company_info
from config import ADMIN_USER_ID
from handlers.help import HelpMessage, AnswerMessage

black_list = []
router = Router()


@router.message(F.contact)
async def login(message: Message):
    user_id = message.from_user.id
    check = await check_user_or_registr(user_id)
    id = str(user_id)
    msg = await get_blocked_user_message(id)
    black_list = await get_black_list()
    if check:
        if id in ADMIN_USER_ID:
            await message.answer('👋Рады вас видеть снова, <b>' + message.from_user.full_name + '</b>',
                                 parse_mode='HTML', reply_markup=admin_keyboard)
        elif id in black_list:
            await message.reply(f'🏴Увы, вы в черном списке :(\nза следующее сообщение: {msg}')
            return
        else:
            await message.answer('👋Рады вас видеть снова, <b>' + message.from_user.full_name + '</b>',
                                 parse_mode='HTML', reply_markup=user_keyboard_after_login)
    else:
        await add_user(user_id, message.from_user.username, message.contact.phone_number, message.from_user.full_name)
        await message.answer(f'✔️Вы успешно зарегестрировались, <b>{message.from_user.full_name}</b>!',
                             parse_mode='HTML', reply_markup=user_keyboard_after_login)


@router.message(F.text == 'История запросов')
async def history(message: Message):
    user = message.from_user.id
    history = await get_history(user)
    if history:
        user_history = "\n".join([f'❓: <b>{messages[0]}</b>\n🔎: <i>{messages[1]}</i> \n \n' for messages in history])
        await message.answer(user_history, parse_mode='HTML')
    else:
        await message.answer('😭Вы еще не получили ответов на ваши обращения\n🦾уже разбираемся <b>:(</b>',
                             parse_mode='HTML')


@router.message(Command("help"))
async def help_command(message: Message, state: FSMContext):
    await state.set_state(HelpMessage.message_send)
    await message.reply('Задайте ваш вопрос, поддержка скоро свяжется с вами. 🛠')


@router.message(F.text == 'Помощь')
async def help_button(message: Message, state: FSMContext):
    user_id = message.from_user.id
    black_list = await get_black_list()
    if user_id in black_list:
        await message.answer('Вы забанены', reply_markup=banned_user)
    else:
        await help_command(message, state)


@router.message(F.text == 'О компании')
async def info(message: Message):
    await message.reply('Тут большая история', reply_markup=company_info)


@router.message(F.text == 'Новости "Транснефти"')
async def investors(message: Message):
    await message.reply('Новости')


@router.message(F.text == 'Клиентам')
async def clients(message: Message, bot: Bot):
    await message.reply('Контактная информация\n'
                        'Отдел делопроизводства\n'
                        'Телефоны: +7 (3953) 300-701, +7 (3953) 300-709\n'
                        'Email: vsmn@vsmn.transneft.ru')
    await bot.send_location(message.from_user.id, 56.313259, 101.739587)


@router.message(F.text)
async def handle_message(message: Message, state: FSMContext, bot: Bot):
    await bot.send_chat_action(message.from_user.id, action="typing")
    data = await state.get_data()
    current_state = await state.get_state()
    user_id = message.from_user.id
    black_list = await get_black_list()

    if str(user_id) in black_list:
        await message.reply('Вы заблокированы и не можете отправлять сообщения.')
        return

    if current_state == AnswerMessage.waiting_for_reply.state:
        if str(user_id) in map(str, ADMIN_USER_ID):
            db_message_id = data['message_id']
            await respond_to_message(db_message_id, message.text)
            await message.reply(f'✅Ответ на сообщение {db_message_id} отправлен.')
            user_chat_id = await get_chat_id(db_message_id, 1)
            original_message = await get_message(db_message_id, 1)
            await bot.send_message(
                user_chat_id[0],
                f'❓ Ваше обращение:\n <b>{original_message[0]}</b>\n\n'
                f'🗣 Ответ от поддержки:\n <b><i>{message.text}</i></b>',
                parse_mode='HTML'
            )
            await state.clear()
    elif str(user_id) not in map(str, ADMIN_USER_ID):
        if current_state == HelpMessage.message_send.state:
            user_message = message.text
            db_message_id = await add_message(user_id, user_message)
            await state.update_data(message_id=db_message_id, chat_id=message.chat.id, message_send=True)
            await message.reply(f'✅Ваше сообщение: "{user_message}" получено. Ожидайте ответа.')
            await state.clear()
        else:
            await message.answer('Сначала нажмите кнопку Помощь❗️❗️❗️')
