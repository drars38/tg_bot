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
settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ознакомиться', url='https://example.com')],
])

login = ReplyKeyboardMarkup(

    keyboard=[
        [KeyboardButton(text='Отправить контакт', request_contact=True)]
    ]

)


# Основная клавиатура для обычных пользователей
user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Помощь')],
        [KeyboardButton(text='Зарегистрироваться', request_contact=True)]
    ],
    resize_keyboard=True
)

# Основная клавиатура для администраторов
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Список пользователей')],
        [KeyboardButton(text='Неотвеченные сообщения')]
    ],
    resize_keyboard=True
)


# Inline-клавиатура для админов
def create_admin_inline_keyboard(message_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Ответить', callback_data=f'reply_{message_id}')]
        ]
    )
    return keyboard



