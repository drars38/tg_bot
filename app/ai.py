"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat



def robot_answer(user_question):
    print(user_question)
    # Авторизация в сервисе GigaChat
    chat = GigaChat(
        credentials='NDcxZmQ3YjMtMGQ2Mi00MTFmLWEyMjEtZmQ4NDA5N2FmNzBhOmMyNzhiY2M4LTg4YzgtNDA5NC1iOTQyLTNhZjdlMjJiMTliZQ==',
        model='GigaChat-Pro',
        verify_ssl_certs=False)

    messages = [
        SystemMessage(
            content="Ты бот тех.поддержки ООО Транснефть-Восток - дочерняя компания Транснефти, который помогает пользователю решить его проблемы,"
                    "Старайся отвечать кратко и лаконично, строго по делу. Не задавай вопросов в ответ, "
                    "только утвердительные предложения. Можешь так же воспользоваться сайтом Транснефть-Восток"
        )
    ]
    # Ввод пользователя
    user_input = user_question
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
   # print("Bot: ", res.content)
    return str(res.content)
