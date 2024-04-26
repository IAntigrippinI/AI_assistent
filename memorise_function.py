import datetime


def get_date(date_timestamp: float) -> int:
    date = datetime.datetime.fromtimestamp(date_timestamp)
    return date.day, date.month


def find_near_date(tasks: list[tuple]) -> list[tuple]:
    near_tasks = []
    today = datetime.datetime.now()
    day_now, month_now = today.day, today.month
    for task in tasks:
        day_start, month_start = get_date(task[1])
        if (
            day_now == day_start - 1
            or day_now == day_start - 2
            or day_now == day_start + 1
        ) and month_now == month_start:
            near_tasks.append(tuple([task[0], (str(day_start) + "." + str(month_now))]))

    return near_tasks
