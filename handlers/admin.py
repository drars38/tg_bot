from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.database import (
    get_unanswered_messages, get_chat_id, get_message,
    get_all_users, get_blocked_user_message, unban_user, get_first_name, add_to_black_list,
    get_black_list, get_username
)
from app.keyboards import (
    create_admin_inline_keyboard, unban_user_keyboard, user_keyboard_after_login,
    banned_user
)
from config import ADMIN_USER_ID
from handlers.help import AnswerMessage

router = Router()


@router.message(F.text == 'Список пользователей')
async def list_users_button(message: Message):
    if str(message.from_user.id) in ADMIN_USER_ID:
        await list_users(message)
    else:
        await message.reply('❌❌❌У вас нет доступа к этой команде.❌❌❌')


@router.message(F.text == 'Список бан-пользователей')
async def black_list_users_button(message: Message):
    black_list = await get_black_list()
    if not black_list:
        await message.answer('Забаненных пользователей нет')
    else:
        for i in black_list:
            msg = str(await get_blocked_user_message(str(i)))
            first_name = await get_first_name(str(i))
            username = await get_username(str(i))
            keyboard = unban_user_keyboard(str(i))
            if username[0] is not None:
                await message.answer(
                    f'🏴Забаненный пользователь: {first_name[0]} (@{username[0]}) из-за сообщения - <b>{msg}</b>',
                    parse_mode='HTML', reply_markup=keyboard)
            else:
                await message.answer(
                    f'🏴Забаненный пользователь: <a href="tg://user?id={msg[1]}">{first_name[0]}</a> из-за сообщения '
                    f'- <b>{msg}</b>',
                    parse_mode='HTML', reply_markup=keyboard)


@router.message(F.text == 'Неотвеченные сообщения')
async def list_unanswered_button(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN_USER_ID:
        await list_unanswered(message, state)
    else:
        await message.reply('❌❌❌У вас нет доступа к этой команде.❌❌❌')


@router.message(Command("Список пользователей"))
async def list_users(message: Message):
    if str(message.from_user.id) not in ADMIN_USER_ID:
        await message.answer('Вы не админ')
        return
    users = await get_all_users()
    user_list = ' '
    for user in users:
        if user[1] is not None:
            user_list += "\n".join([f'@{user[1]}: <a href="tg://user?id={user[0]}">{user[2]}</a> {user[3]}\n'])
        else:
            user_list += "\n".join([f'<a href="tg://user?id={user[0]}">{user[2]}</a> {user[3]}\n'])
    await message.reply(f'Зарегистрированные пользователи:\n{user_list}', parse_mode='HTML')


@router.message(Command("Неотвеченные сообщения"))
async def list_unanswered(message: Message):
    if str(message.from_user.id) not in ADMIN_USER_ID:
        return
    unanswered = await get_unanswered_messages()
    if not unanswered:
        await message.reply('Нет необработанных сообщений.')
        return
    for msg in unanswered:
        keyboard = create_admin_inline_keyboard(msg[0])
        first_name = await get_first_name(str(msg[1]))
        username = await get_username(str(msg[1]))
        if username[0] is not None:
            await message.reply(
                f'Сообщение от пользователя <a href="tg://user?id={msg[1]}">{first_name[0]}</a>'
                f' (@{username[0]}) :\n"{msg[2]}"',
                reply_markup=keyboard, parse_mode='HTML')
        else:
            await message.reply(
                f'Сообщение от пользователя <a href="tg://user?id={msg[1]}">{first_name[0]}</a>:\n"{msg[2]}"',
                reply_markup=keyboard, parse_mode='HTML')


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


@router.callback_query(F.data.startswith('unban_'))
async def handle_unban_callback(callback_query: CallbackQuery, bot: Bot):
    if str(callback_query.from_user.id) not in ADMIN_USER_ID:
        await callback_query.answer('У вас нет доступа к этой функции.', show_alert=True)
        return
    user_id = callback_query.data.split('_')[1]
    await unban_user(user_id)
    await callback_query.answer(f'Пользователь {user_id} разбанен.')
    await bot.send_message(str(user_id), 'Вы были разбанены🎉', reply_markup=user_keyboard_after_login)


@router.callback_query(F.data.startswith('ban_'))
async def handle_ban_callback(callback_query: CallbackQuery, bot: Bot):
    if str(callback_query.from_user.id) not in ADMIN_USER_ID:
        await callback_query.answer('У вас нет доступа к этой функции.', show_alert=True)
        return
    message_id = callback_query.data.split('_')[1]
    user = await get_chat_id(message_id, 0)
    msg = await get_message(message_id, 0)
    await add_to_black_list(user[0], msg[0])
    await callback_query.answer(f'🏴Пользователь {user[0]} добавлен в черный список🏴')
    await bot.send_message(user[0], f'🏴Вы были забанены за сообщение <b>{msg[0]}</b>', parse_mode='HTML',
                           reply_markup=banned_user)
