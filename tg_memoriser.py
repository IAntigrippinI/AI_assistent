import time
import telebot
import datetime
import schedule

import logging

from db import get_all_users_id, get_user_task
from memorise_function import find_near_date

bot = telebot.TeleBot("6771849352:AAFiFk-Ri4E9oVYkRdSFkCO4ge329kczfmI")


def send_mesage(tg_id: int, message: str):
    bot.send_message(tg_id, message)


def send_remember():

    # print(users_data)

    users_id = get_all_users_id()
    print(users_id)
    for tg_id in users_id:
        user_tasks = get_user_task(tg_id)
        near_tasks = find_near_date(user_tasks)
        for task in near_tasks:
            memorise = "Напоминаю, что вам нужно выполнить:\n"
            send_mesage(tg_id, memorise + " ".join(task))
        logging.info(f"User {tg_id} was remembered")


schedule.every(15).seconds.do(send_remember)

while True:
    schedule.run_pending()
    time.sleep(1)
