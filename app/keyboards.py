from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Inline клавиатура для настроек
company_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ознакомиться', url='https://vostok.transneft.ru/about/information/')],
])

login_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить контакт', request_contact=True)]
    ]
)

# Основная клавиатура для обычных пользователей
user_keyboard = ReplyKeyboardMarkup(
    keyboard=[

        [KeyboardButton(text='Зарегистрироваться', request_contact=True)],
        [KeyboardButton(text='Помощь')],
        [KeyboardButton(text='О компании')],
        [KeyboardButton(text='Новости сообщества'), KeyboardButton(text='Клиентам')],
        [KeyboardButton(text='Войти в аккаунт', request_contact=True)]
    ],
    resize_keyboard=True, input_field_placeholder='Выберите пункт меню.'
)

user_keyboard_after_login = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Помощь')], [KeyboardButton(text='История запросов')],
        [KeyboardButton(text='О компании')],
        [KeyboardButton(text='Новости сообщества'), KeyboardButton(text='Клиентам')]
    ],
    resize_keyboard=True, input_field_placeholder='Выберите пункт меню.'
)

# Основная клавиатура для администраторов
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Список пользователей')], [KeyboardButton(text='Список бан-пользователей')],
        [KeyboardButton(text='Неотвеченные сообщения')]
    ],
    resize_keyboard=True
)


# Inline-клавиатура для админов
def create_admin_inline_keyboard(message_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Ответить', callback_data=f'reply_{message_id}')],
            [InlineKeyboardButton(text='Забанить', callback_data=f'ban_{message_id}')]
        ]
    )
    return keyboard


banned_user = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Админ, сжалься😢')]
    ],
    resize_keyboard=True
)


def unban_user_keyboard(user_id):
    unban_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Разбанить', callback_data=f'unban_{user_id}')],
            [InlineKeyboardButton(text='Установить временные рамки бана', callback_data=f'time_{user_id}')]
        ]
    )
    return unban_kb
