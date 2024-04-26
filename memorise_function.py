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
        print(
            f" day_now {day_now} ? {day_start}\n month_now {month_now} ? {month_start}"
        )
        if (
            day_now == day_start - 1
            or day_now == day_start - 2
            or day_now == day_start + 1
        ) and month_now == month_start:
            near_tasks.append(tuple([task[0], (str(day_start) + "." + str(month_now))]))

    return near_tasks


tasks = [
    ("Помыть посуду", 1712670000, 1713100000),
    ("Сделать дз", 1714050000, 1714830000),
]

print(find_near_date(tasks))
