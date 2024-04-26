import telebot
import logging
import requests

from db import get_telegram_bot_cred, create_tables, remove_task
from Gigachat import message_processing

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
    logging.info(got_message.text)
    try:
        if got_message.text == "/del":
            remove_task(got_message.from_user.id, 1)
            send_message(got_message.from_user.id, "Удалено")

        else:
            answer, source = message_processing(
                got_message.from_user.id, got_message.text
            )
            logging.info(answer)
            send_message(got_message.from_user.id, answer)
            if source != "":
                bot.send_photo(
                    got_message.from_user.id, open("pict/gantt_chart.png", "rb")
                )
    except requests.exceptions.ReadTimeout as e:
        logging.critical(f"Read timed out: {e}", exc_info=True)
    except telebot.apihelper.ApiTelegramException as e:
        logging.critical(f"Failed to give an answer: {e}", exc_info=True)
        send_message(
            got_message.from_user.id, "Извините, не удалось обработать Ваш запрос"
        )


bot.polling(none_stop=True, interval=0)
