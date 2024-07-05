import datetime
import logging
from environs import Env
from dotenv import dotenv_values
from aiogram import Bot,  F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from app.database import (add_message, get_unanswered_messages, respond_to_message, get_chat_id, get_message, \
    get_all_users, check_user_or_registr, get_history,
                          get_black_list, add_user, get_blocked_user_message,
                          add_to_black_list)
from app.keyboards import (login_keyboard, user_keyboard, admin_keyboard,
                           create_admin_inline_keyboard, user_keyboard_after_login)


config = dotenv_values()

logging.basicConfig(level=logging.INFO)
env = Env()
env.read_env()
ADMIN_USER_ID = env.list("ADMINS")
black_list = []

router = Router()


class HelpMessage(StatesGroup):
    message_id = State()
    chat_id = State()
    message_send = State()


class AnswerMessage(StatesGroup):
    waiting_for_reply = State()


@router.message(Command("start"))
async def start(message: Message):
    black_list = await get_black_list()
    user_id = str(message.from_user.id)
    print(ADMIN_USER_ID)
    print(black_list)
    print(user_id)

    if user_id in map(str, ADMIN_USER_ID):
        keyboard = admin_keyboard
    elif user_id in black_list:
        await message.reply('Увы, вы в черном списке :(')
    else:
        keyboard = user_keyboard

    await message.reply('Привет! Вас приветствует служба поддержки Транснефть.', reply_markup=keyboard)


@router.message(F.contact)
async def login(message: Message):
    check = await check_user_or_registr(message.from_user.id)
    id = str(message.from_user.id)
    msg = await get_blocked_user_message(id)
    if check:
        if id in ADMIN_USER_ID:
            await message.answer('Рады вас видеть снова, <b>'+ message.from_user.full_name +'</b>', parse_mode='HTML', reply_markup=admin_keyboard)
        elif id in black_list:
            await message.reply(f'Увы, вы в черном списке :(\n'
                                f'за следующее сообщение: {msg}' )
            return
        else:
            await message.answer('Рады вас видеть снова, <b>'+ message.from_user.full_name +'</b>', parse_mode='HTML', reply_markup=user_keyboard_after_login)
    else:
        if id in ADMIN_USER_ID:
            await add_user(message.from_user.id,message.from_user.username, message.contact.phone_number, message.from_user.full_name)
            await message.answer(f'✔️Вы успешно зарегестрировались, <b>{message.from_user.full_name}</b>!',
                                 parse_mode='HTML', reply_markup=admin_keyboard)
        else:
            await add_user(message.from_user.id, message.contact.phone_number, message.from_user.full_name)
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
        await message.answer('Вы не писали обращений :(', parse_mode='HTML')

@router.message(Command("help"))
async def help_command(message: Message, state: FSMContext):
    await state.set_state(HelpMessage.message_send)
    await message.reply('Задайте ваш вопрос, и наша поддержка скоро свяжется с вами.')


@router.message(F.text == 'Помощь')
async def help_button(message: Message, state: FSMContext):
    await help_command(message, state)


@router.message(F.text == 'Список пользователей')
async def list_users_button(message: Message):
    if str(message.from_user.id) in ADMIN_USER_ID:
        await list_users(message)
    else:
        await message.reply('❌❌❌У вас нет доступа к этой команде.❌❌❌')


@router.message(F.text == 'Неотвеченные сообщения')
async def list_unanswered_button(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN_USER_ID:
        await list_unanswered(message, state)
    else:
        await message.reply('❌❌❌У вас нет доступа к этой команде.❌❌❌')


@router.message(Command("Список пользователей"))
async def list_users(message: Message):
    if str(message.from_user.id) not in ADMIN_USER_ID:
        return
    users = await get_all_users()
    user_list = "\n".join([f'{user[1]}: {user[2]} {user[3]}' for user in users])
    await message.reply(f'Зарегистрированные пользователи:\n{user_list}')


@router.message(Command("Неотвеченные сообщения"))
async def list_unanswered(message: Message, state: FSMContext):
    if str(message.from_user.id) not in ADMIN_USER_ID:
        return
    unanswered = await get_unanswered_messages()
    if not unanswered:
        await message.reply('Нет необработанных сообщений.')
        return
    for msg in unanswered:
        keyboard = create_admin_inline_keyboard(msg[0])
        await message.reply(f'Сообщение от пользователя {msg[1]}:\n"{msg[2]}"', reply_markup=keyboard)


@router.callback_query(F.data.startswith('reply_'))
async def handle_reply_callback(callback_query: CallbackQuery, state: FSMContext):
    if str(callback_query.from_user.id) not in ADMIN_USER_ID:
        await callback_query.answer('У вас нет доступа к этой функции.', show_alert=True)
        return
    message_id = callback_query.data.split('_')[1]
    await state.update_data(message_id=message_id)
    await state.set_state(AnswerMessage.waiting_for_reply)
    await callback_query.message.reply(f'Введите ответ на сообщение {message_id}.')
    await callback_query.answer()


@router.callback_query(F.data.startswith('ban_'))
async def handle_ban_callback(callback_query: CallbackQuery, bot: Bot):
    if str(callback_query.from_user.id) not in ADMIN_USER_ID:
        await callback_query.answer('У вас нет доступа к этой функции.', show_alert=True)
        return

    message_id = callback_query.data.split('_')[1]
    user = await get_chat_id(message_id, 0)
    msg = await get_message(message_id, 0)
    await add_to_black_list(user[0], msg[0])

    await callback_query.answer(f'Пользователь {user[0]} добавлен в черный список')
    await bot.send_message(user[0], 'Вы были забанены (')



@router.message(F.text)
async def handle_message(message: Message, state: FSMContext, bot: Bot):
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
            await bot.send_message(user_chat_id[0],
                                   f'❓ Ваше обращение:\n <b>{original_message[0]}</b>\n\n'
                                   f'🗣 Ответ от поддержки:\n <b><i>{message.text}</i></b>',
                                   parse_mode='HTML')
            await state.clear()
        else:
            print('Ошибка: текущее состояние - ожидание ответа, но сообщение не от администратора.')
    else:
        if str(user_id) not in map(str, ADMIN_USER_ID):
            if current_state == HelpMessage.message_send.state:
                user_message = message.text
                db_message_id = await add_message(user_id, user_message)
                await state.update_data(message_id=db_message_id, chat_id=message.chat.id, message_send=True)
                await message.reply(f'✅Ваше сообщение: "{user_message}" получено. Ожидайте ответа.')
                await state.clear()
            else:
                await message.answer('Сначала нажмите кнопку Помощь❗️❗️❗️')
