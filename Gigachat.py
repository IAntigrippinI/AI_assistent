import sys

import logging
import queue

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from db import connect, get_gigachat_cred, get_user_id, insert_user


logging.getLogger(__name__)
db = connect()
if not db:
    sys.exit()
credentials = get_gigachat_cred(db)

chat = GigaChat(
    credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_CORP"
)

prompts_base = SystemMessage(
    content="""Ты ассистент. Пользователи тебе отправляют сообщения. 
            Тебе необходимо определить является сообщение задачей пользователя, вопросом к тебе или просьбой что-то сделать.
            Ты должен определить является ли сообщение задачей или нет.
            Ты должен отвечать на сообщение 'Задачи с указанным сроком' и добавить срок выполнения задачи,
            если сообщение похоже на задачу для которой указан срок.
            Ты должен отвечать на сообщение 'Задача без срока', если соощение похоже на задачу, но для нее не указан срок выполнения.
            Ты должен ответить на вопрос, если сообщение похоже на вопрос.
            Ты должен сделать то, что указано в сообщении, если сообщение похоже на просьбу\n"""
    # "Ты таск-менеджер, который получает информацию о сроках выполнения задачи, получает ее описание и дает ей название\n"
)

messages = {}


def message_processing(user_id: int, message: str) -> str:

    error_message = "Произошла техническая ошибка, попробуйте снова"
    quastion = "Дай ответ на следующее сообщение:\n" + message
    # if user_id in messages:
    #     if len(messages[user_id]) >= 10:
    #         last_messages = messages[user_id][2:]
    #         messages[user_id] = [prompts_base] + last_messages
    #     messages[user_id].append(HumanMessage(content=quastion))
    # else:
    #     messages[user_id] = [prompts_base]
    #     messages[user_id].append(HumanMessage(content=quastion))
    # res = chat(messages[user_id]).content
    res = chat([prompts_base, HumanMessage(content=quastion)]).content

    return res
