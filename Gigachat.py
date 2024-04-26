from src.setting import (
    PROMPTS_BASE_SYS,
    PROMPT_FOR_ROADMAP,
    PROMPT_FOR_QUASTION,
    PROMPT_BASE,
    PROMPT_FOR_GANT,
)

import logging
import logging.config

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from db import get_gigachat_cred, insert_user_task
from processing_data_for_db import processing_for_add_in_db
from gant import Gant_Diagram

logging.getLogger(__name__)
credentials = get_gigachat_cred()

chat = GigaChat(
    credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_CORP"
)

messages = {}


def message_processing(tg_id: int, message: str) -> str:

    quastion = PROMPT_BASE + "\n" + message

    try:
        res = chat([HumanMessage(content=quastion)]).content

        if res.lower() == "да":
            plan = chat([PROMPT_FOR_ROADMAP, HumanMessage(content=message)]).content
            # try:
            #     send = tg.bot.send_message(
            #         tg_id, "В какие сроки вы планируете это сделать?"
            #     )

            #     period = tg.bot.register_next_step_handler(send, get_period)
            #     logging.info(f"GOT PERIOD: {period}")
            # except:
            #     logging.critical("Bad code")
            logging.info(plan)

            list_tasks_for_db = processing_for_add_in_db(plan, message)

            for el in list_tasks_for_db:
                insert_user_task(tg_id, el[0], el[1], el[2])
            return plan

        res = chat([PROMPT_FOR_GANT, HumanMessage(content=message)]).content

        if res.lower() == "да":
            way = Gant_Diagram(tg_id)
            return way
        else:
            if tg_id in messages:
                if len(messages[tg_id]) >= 10:
                    last_messages = messages[tg_id][2:]
                    messages[tg_id] = [PROMPT_FOR_QUASTION] + last_messages
                    messages[tg_id].append(HumanMessage(content=message))
            else:
                messages[tg_id] = [PROMPT_FOR_QUASTION]
                messages[tg_id].append(HumanMessage(content=message))
            answer = chat(messages[tg_id]).content
            return answer
    except Exception as e:
        logging.critical(f"Failed in message_processing: {e}", exc_info=True)
        return "Произошла ошибка, попробуйте снова"


def get_recomindation(user_id: int, message: str) -> str:
    pass


# def get_plan(tg_id: int, message: str):
#     plan = chat([prompts_for_roadmap, HumanMessage(content=message)]).content
#     try:
#         send = tg.bot.send_message(tg_id, "В какие сроки вы планируете это сделать?")

#         period = tg.bot.register_next_step_handler(send, get_period)
#         logging.info(f"GOT PERIOD: {period}")
#     except:
#         logging.critical("Bad code")

#     list_tasks_for_db = processing_for_add_in_db(plan, message)

#     for el in list_tasks_for_db:
#         insert_user_task(tg_id, el)
#     return plan
