import mysql.connector
import logging
from datetime import datetime
from mysql.connector.connection_cext import CMySQLConnection

import src.setting

logging.getLogger(__name__)


def connect():
    try:
        db = mysql.connector.connect(
            host="localhost", user="root", passwd="", database="assistent"
        )
        logging.info("Connection success")

        return db
    except mysql.connector.errors.ProgrammingError as e:
        logging.critical(f"Failed to connect to database: {e}", exc_info=True)
        return False


def create_tables():
    db = connect()
    cursor = db.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(
                id int AUTO_INCREMENT PRIMARY KEY,
                subscribe BLOB,
                time_zone int,
                tg_id int UNIQUE)"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
                id int AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                task VARCHAR(255),
                time_start float,
                time_finish float,
                discription VARCHAR(255))"""
    )

    db.commit()
    db.close()


def check_user_in_db(tg_id: int):
    db = connect()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    result = cursor.fetchall()
    db.close()

    if len(result) == 0:
        logging.info("NOT EXISTS")
        insert_user(tg_id)
    else:

        logging.info("EXISTS")


def insert_user(tg_id: int):
    db = connect()

    cursor = db.cursor()

    cursor.execute(
        f"""INSERT INTO users (subscribe, time_zone, tg_id) VALUES ({0}, {0}, {tg_id})"""
    )

    db.commit()
    db.close()


def insert_user_task(
    # db: CMySQLConnection,
    tg_id: int,
    task: str,
    time_start: float = 0,
    time_finish: float = 0,
    description: str = "Desc",
):
    check_user_in_db(tg_id)

    user_id = get_user_id(tg_id)

    db = connect()
    cursor = db.cursor()
    cursor.execute(
        f"""INSERT INTO tasks (user_id, task, time_start, time_finish, discription) VALUES ({user_id},'{task}', {time_start}, {time_finish}, '{description}')"""
    )

    db.commit()
    db.close()


def get_user_id(tg_id: int) -> int:
    check_user_in_db(tg_id)
    db = connect()
    cursor = db.cursor()

    cursor.execute(f"""SELECT id FROM users WHERE tg_id = '{tg_id}'""")
    user_id = cursor.fetchall()[0][0]

    db.close()
    logging.info(f"GOT USER ID = {user_id}")
    return user_id


def get_all_users_id() -> list:
    db = connect()
    cursor = db.cursor()

    cursor.execute("""SELECT tg_id FROM users""")

    users_id = cursor.fetchall()
    db.close()
    return users_id[0]


def get_user_task(tg_id: int) -> list[tuple]:
    user_id = get_user_id(tg_id)
    db = connect()
    cursor = db.cursor()

    cursor.execute(
        f"""SELECT task, time_start, time_finish FROM tasks WHERE user_id = {user_id}"""
    )

    tasks = cursor.fetchall()

    db.close()

    return tasks


def remove_task(tg_id: int, time: float):
    db = connect()
    cursor = db.cursor()

    cursor.execute(f"DELETE FROM tasks WHERE user_id = {get_user_id(tg_id)}")

    db.commit()
    db.close()


def get_gigachat_cred() -> str:
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT cred FROM credentials WHERE id = 1")
    cred = cursor.fetchall()[0][0]
    db.close()
    return cred


def get_telegram_bot_cred() -> str:
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT cred FROM credentials WHERE id = 2")
    cred = cursor.fetchall()[0][0]
    db.close()
    return cred
