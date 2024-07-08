from aiogram.fsm.state import State, StatesGroup


class HelpMessage(StatesGroup):
    message_id = State()
    chat_id = State()
    message_send = State()


class AnswerMessage(StatesGroup):
    waiting_for_reply = State()
