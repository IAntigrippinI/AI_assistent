import logging

from datetime import datetime, timedelta

from src.setting import DATE_PATTERN, system_logger


def get_timestamp(date: str) -> float:
    year = datetime.now().year
    month, day = date.split(".")[1], date.split(".")[0]
    return datetime(year, int(month), int(day)).timestamp()


def get_timestamp_plus_day(date: str) -> float:
    year = datetime.now().year
    month, day = date.split(".")[1], date.split(".")[0]
    return (datetime(year, int(month), int(day)) + timedelta(2)).timestamp()


def processing_for_add_in_db(plan: str, handle: str) -> list:
    list_tasks = plan.split("\n")
    tuple_tasks = []
    for el in list_tasks:
        dates = DATE_PATTERN.findall(el)
        system_logger.info(" ".join(dates))
        if len(dates) == 2:
            task = el[2 : el.find(dates[0])].replace("-", "")
            time_start = get_timestamp(dates[0])
            time_finish = get_timestamp(dates[1])
            tuple_tasks.append(tuple([task, time_start, time_finish]))
        elif len(dates) == 1:
            task = el[2 : el.find(dates[0])].replace("-", "")
            time_start = get_timestamp(dates[0])
            time_finish = get_timestamp_plus_day(dates[0])
            tuple_tasks.append(tuple([task, time_start, time_finish]))
        else:
            pass
    return tuple_tasks
