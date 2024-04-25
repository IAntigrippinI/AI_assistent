import sys
import time

import telebot
import logging
import requests

import src.setting
from db import connect, get_telegram_bot_cred, create_tables
from Gigachat import message_processing
from tg_function import split_answer

logging.getLogger(__name__)

try:
    create_tables()
except Exception as e:
    logging.critical(f"Failed create tables: {e}", exc_info=True)


try:
    credentials = get_telegram_bot_cred()
    bot = telebot.TeleBot(credentials)
except telebot.apihelper.ApiTelegramException as e:
    logging.critical(f"Failed to run telegram bot: {e}", exc_info=True)


def send_message(tg_id: int, message: str):
    bot.send_message(tg_id, message)


@bot.message_handler(content_types=["text"])
def get_text_messages(got_message):
    try:
        logging.info(got_message.text)
        answer = message_processing(got_message.from_user.id, got_message.text)
        logging.info(answer)
        send_message(got_message.from_user.id, answer)
    except requests.exceptions.ReadTimeout as e:
        logging.critical(f"Read timed out: {e}", exc_info=True)


bot.polling(none_stop=True, interval=0)