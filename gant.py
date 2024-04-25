import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num, DateFormatter, DayLocator
from matplotlib.ticker import AutoMinorLocator
from matplotlib.patches import Patch
from db import connect, get_user_task


def Gant_Diagram(tg_id):

    user_id = get_user_task(tg_id)
    list_of_touples = get_task(user_id)
    df = pd.DataFrame(list_of_touples, columns=["Task", "Start", "Finish"])

    df = df["Task", "Start", "Finish"]

    df["Start"] = pd.to_datetime(df["Start"], unit="s")
    df["Finish"] = pd.to_datetime(df["Finish"], unit="s")

    df["Start"] = df["Start"].dt.strftime("%Y-%m-%d")
    df["Finish"] = df["Finish"].dt.strftime("%Y-%m-%d")

    tasks = df["Task"].tolist()
    start_dates = df["Start"].tolist()
    end_dates = df["Finish"].tolist()

    start_dates = [datestr2num(d) for d in start_dates]
    end_dates = [datestr2num(d) for d in end_dates]

    durations = [
        (end - start) for start, end in zip(start_dates, end_dates)
    ]  # Длительность таска

    fig, ax = plt.subplots(figsize=(15, 8), facecolor="#25253c")

    ax.set_facecolor("#25253c")

    colors = ["#7a5195", "#ef5675", "#ffa600"]
    task_colors = [colors[0]] * 3 + [colors[1]] * 4 + [colors[2]] * 3

    ax.barh(
        y=tasks, width=durations, left=start_dates, height=0.8, color=task_colors
    )  # Вывод столбцов

    ax.invert_yaxis()  # метод инвертирует направление оси y

    ax.set_xlim(start_dates[0], end_dates[-1])  # Пределы оси x

    date_form = DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(date_form)  # Формат делений на оси x

    ax.xaxis.set_major_locator(
        DayLocator(interval=10)
    )  # местоположение делений на оси x
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    # местоположение вспомогательных делений
    ax.tick_params(
        axis="x", which="minor", length=2, color="white", labelsize=6
    )  # параметры делений

    ax.get_yaxis().set_visible(False)  #  метод скрывает ось y.

    # Установка параметров сетки
    ax.grid(True, axis="x", linestyle="-", color="#FFFFFF", alpha=0.2, which="major")
    # ax.grid(True, axis="x", linestyle="-", color="#FFFFFF", alpha=0.05, which="minor")

    ax.set_axisbelow(True)
    # все элементы графика (такие как линии, метки и т. д.) будут нарисованы под сеткой графика, что обеспечит более четкое отображение сетки и ее линий над графическими элементами. Это может быть полезно, если вы хотите, чтобы сетка была легко видимой и не загораживалась элементами графика.

    # подписи тасков
    for i, task in enumerate(tasks):
        ax.text(
            start_dates[i],
            i,
            f"  {task}",
            ha="left",
            va="center",
            color="white",
            fontsize=12,
            fontweight="bold",
        )

    # текущая дата
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_num = datestr2num(today)
    ax.axvline(today_num, color="red", alpha=0.8)

    ax.tick_params(axis="both", colors="white")

    ax.set_title("Диаграмма ганта", color="white", fontsize=14)

    fig.savefig("pict\gantt_chart.png", dpi=300, bbox_inches="tight")

    return "pict\gantt_chart.png"
