from environs import Env

env = Env()
env.read_env()
ADMIN_USER_ID = env.list("ADMINS")

DATABASE = 'support_bot.db'
