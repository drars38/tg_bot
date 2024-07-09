from environs import Env
import re
env = Env()
env.read_env()

ADMIN_USER_ID = env.list("ADMINS")
DATABASE = 'support_bot.db'
def escape_markdown_v2(text: str) -> str:
    return re.sub(r'([_*\[\]()~>#+\-=|{}.!])', r'\\\1', text)