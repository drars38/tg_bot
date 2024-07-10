from environs import Env
import re

env = Env()
env.read_env()

ADMIN_USER_ID = env.list("ADMINS")
DATABASE = 'support_bot.db'


def escape_markdown_v2(text: str) -> str:
    escape_chars = r'([_*\[\]()~>#+\-=|{}.!])'
    text = re.sub(escape_chars, r'\\\1', text)
    #text = text.replace('`', '\\`')
    return text


def wrap_code_blocks(text: str) -> str:
    # Проверяем, есть ли в тексте тройные обратные кавычки
    if '```' in text:
        # Если есть, оставляем текст как есть и экранируем символы внутри блоков кода
        return escape_markdown_v2(text)
    else:
        # Если нет, экранируем текст и добавляем тройные кавычки вокруг всего текста
        escaped_text = escape_markdown_v2(text)
        return f'```\n{escaped_text}\n```'
