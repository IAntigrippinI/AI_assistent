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


def create_tables(db: CMySQLConnection):

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
                time_start DATE,
                time_finish DATE,
                discription VARCHAR(255))"""
    )

    db.commit()
    db.close()


def insert_user(db: CMySQLConnection, tg_id: int):

    cursor = db.cursor()

    cursor.execute(
        f"""INSERT INTO users (subscribe, time_zone, tg_id) VALUES ({0}, {0}, {tg_id})"""
    )

    db.commit()
    db.close()


def insert_user_task(
    db: CMySQLConnection,
    tg_id: int,
    task: str,
    time_start: float,
    time_finish: float,
    description: str,
):
    cursor = db.cursor()

    user_id = get_user_id(tg_id)

    cursor.execute(
        f"""INSERT INTO tasks (user_id, task, time_start, time_finish, description) VALUES ({user_id}, {task}, {time_start}, {time_finish}, {description})"""
    )

    db.commit()
    db.close()


def get_user_id(db: CMySQLConnection, tg_id: int) -> int:

    cursor = db.cursor()

    cursor.execute(f"""SELECT id FROM users WHERE tg_id = {tg_id}""")
    user_id = cursor.fetchall()

    db.close()

    return user_id


def get_user_task(db: CMySQLConnection, tg_id: int) -> list[tuple]:

    cursor = db.cursor()

    tasks = cursor.execute(
        f"""SELECT task, time_start, time_finish, description FROM tasks WHERE id = {get_user_id(tg_id)}"""
    )

    db.close()

    return tasks


def remove_task(db: CMySQLConnection, tg_id: int, time: float):

    cursor = db.cursor()

    cursor.execute(
        f"DELETE FROM tasks WHERE id = {get_user_id(tg_id)} AND time_start < {time}"
    )

    db.commit()
    db.close()


def get_gigachat_cred(db: CMySQLConnection) -> str:
    cursor = db.cursor()
    cursor.execute("SELECT cred FROM credentials WHERE id = 1")
    return cursor.fetchall()[0][0]


def get_telegram_bot_cred(db: CMySQLConnection) -> str:
    cursor = db.cursor()
    cursor.execute("SELECT cred FROM credentials WHERE id = 2")
    return cursor.fetchall()[0][0]
