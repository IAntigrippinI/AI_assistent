import re
import os
import logging.config
from langchain.schema import SystemMessage
from pathlib import Path


Path(os.getcwd() + "/logs").mkdir(parents=True, exist_ok=True)

Path(os.getcwd() + "/pict").mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


setup_logger("chat_logger", "logs/chat_logs.log")
chat_logger = logging.getLogger("chat_logger")
setup_logger("system_logger", "logs/sys_logs.log")
system_logger = logging.getLogger("system_logger")


DATE_PATTERN: re.Pattern = re.compile(r"\d\d\.\d\d")

PROMPTS_BASE_SYS = SystemMessage(
    content=""" Ты ИИ-ассистент, который помогает строить план действий для решение задачи. 
                             Если введенное сообщение похоже на запрос о создании плана, то напиши 'Да', иначе напиши 'Нет' """
)

PROMPT_FOR_QUASTION = SystemMessage(
    """Ты умный студент, расскажи подробнее об этой теме и не забудь выделить самое важное"""
)

PROMPT_BASE = """Ты ИИ-ассистент, который помогает строить план действий для решения задачи. 
                             Если введенное сообщение похоже на запрос о создании плана, то напиши 'Да', иначе напиши 'Нет'"""

PROMPT_FOR_ROADMAP = SystemMessage(
    content="""Представь, что ты умный студент. Разбей изучение введенной темы на уникальные пункты.
    Важное условие: Пункты не могут повторяться.
    Напиши каждый пункт и срок его выполнения в отдельной строке.
    Срок указывай только по образцу ДД.ММ.
    Сложи время выполнения всех пунктов и выведи в отдельную строку"""
)

PROMPT_FOR_GANT = SystemMessage(
    content="""Ты ИИ-ассистент, который помогает визуализировать задачи пользователя при помощи диаграммы Ганта.
                Ессли в ведённом сообщении тебя просят создать диаграмму Ганта, то напиши 'Да', иначе напиши 'Нет' """
)

PROMPT_FOR_COUNSELOR = SystemMessage(
    content="""Ты Ассистент по научной работе. Тебе сообщают задачу, котороую нужно сделать научному работнику.
            Твоя задача дать рекомендацию как сделать эту задачу.
            Так же ты должен посоветовать книги и научные статьи, которые помогут с решением задачи"""
)
