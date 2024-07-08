from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# Основная клавиатура
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Написать коллеге')],
    [KeyboardButton(text='О компании'), KeyboardButton(text='Задать вопрос')],
    [KeyboardButton(text='Инвесторам и акционерам'), KeyboardButton(text='Клиентам')],
    [KeyboardButton(text='Войти в аккаунт', request_contact=True)]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')


# Клавиатура для внутреннего меню
inner_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Тех. поддержка'), KeyboardButton(text='Развлечения')],
    [KeyboardButton(text='Написать коллеге')],
    [KeyboardButton(text='Назад')]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню.')

# Клавиатура подтверждения отправки сообщения
message_confirm = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить сообщение")],
    [KeyboardButton(text='Назад')]
], input_field_placeholder='Выберите пункт меню.')

# Inline клавиатура для настроек
company_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ознакомиться', url='https://example.com')],
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
        [KeyboardButton(text='Инвесторам и акционерам'), KeyboardButton(text='Клиентам')],
        [KeyboardButton(text='Войти в аккаунт', request_contact=True)]
        ],
    resize_keyboard=True , input_field_placeholder='Выберите пункт меню.'
)

user_keyboard_after_login = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Помощь')], [KeyboardButton(text='История запросов')],
        [KeyboardButton(text='О компании')],
        [KeyboardButton(text='Инвесторам и акционерам'), KeyboardButton(text='Клиентам')]
        ],
    resize_keyboard=True , input_field_placeholder='Выберите пункт меню.'
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
        [KeyboardButton(text = 'Узнать время до окончания бана')]
    ],
    resize_keyboard=True
)

def unban_user_keyboard(user_id):
    unban_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Разбанить', callback_data=f'unban_{user_id}')],
            [InlineKeyboardButton(text='Установить временные рамки бана',callback_data=f'time_{user_id}')]
        ]
    )
    return unban_kb
