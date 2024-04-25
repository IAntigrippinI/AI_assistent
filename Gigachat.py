import sys
import time

import logging
import queue

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from db import connect, get_gigachat_cred, get_user_id, insert_user, insert_user_task
from processing_data_for_db import processing_for_add_in_db


logging.getLogger(__name__)
credentials = get_gigachat_cred()

chat = GigaChat(
    credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_CORP"
)

prompts_base_sys = SystemMessage(
    content=""" Ты ИИ-ассистент, который помогает строить план действий для решение задачи. 
                             Если введенное сообщение похоже на запрос о создании плана, то напиши 'Да', иначе напиши 'Нет' """
)

prompts_base = """Ты ИИ-ассистент, который помогает строить план действий для решения задачи. 
                             Если введенное сообщение похоже на запрос о создании плана, то напиши 'Да', иначе напиши 'Нет'"""

prompts_for_roadmap = SystemMessage(
    content="""Представь, что ты умный студент. Разбей изучение введенной темы на пункты\n
    Напиши каждый пункт в отдельной строке"""
    # "Ты таск-менеджер, который получает информацию о сроках выполнения задачи, получает ее описание и дает ей название\n"
)

messages = {}


def message_processing(tg_id: int, message: str) -> str:

    quastion = prompts_base + "\n" + message

    try:
        res = chat([HumanMessage(content=quastion)]).content

        if res.lower() == "да":
            plan = chat([prompts_for_roadmap, HumanMessage(content=message)]).content

            list_tasks_for_db = processing_for_add_in_db(plan, message)

            for el in list_tasks_for_db:
                insert_user_task(tg_id, el)

            return "Данные успешно добавлены"
        else:
            if tg_id in messages:
                if len(messages[tg_id]) >= 10:
                    last_messages = messages[tg_id][2:]
                    messages[tg_id] = [prompts_base] + last_messages
                    messages[tg_id].append(HumanMessage(content=quastion))
            else:
                messages[tg_id] = [prompts_base]
                messages[tg_id].append(HumanMessage(content=quastion))
            res = chat(messages[tg_id]).content
            return res
    except Exception as e:
        logging.critical(f"Failed in message_processing: {e}", exc_info=True)
        return "Произошла ошибка, попробуйте снова"


def get_recomindation(user_id: int, message: str) -> str:
    pass
