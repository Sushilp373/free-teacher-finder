from flask import Flask
import pandas as pd
from datetime import datetime, time
import os

app = Flask(__name__)

# Period Timings
periods = {
    1:  (time(7,35),  time(8,10)),
    2:  (time(8,10),  time(8,45)),
    3:  (time(9,5),   time(9,40)),
    4:  (time(9,40),  time(10,15)),
    5:  (time(10,15), time(10,50)),
    6:  (time(10,50), time(11,25)),
    7:  (time(11,55), time(12,30)),
    8:  (time(12,30), time(13,5)),
    9:  (time(13,5),  time(13,40)),
    10: (time(13,40), time(14,15)),
}

lunch_start = time(11,25)
lunch_end   = time(11,55)

def get_current_period():
    now = datetime.now()
    current_time = now.time()

    if lunch_start <= current_time <= lunch_end:
        return "LUNCH"

    for period, (start, end) in periods.items():
        if start <= current_time <= end:
            return period

    return None

@app.route("/")
def home():
    file_path = os.path.join(os.getcwd(), "timetable.xlsx")
    df = pd.read_excel(file_path)

    today = datetime.now().strftime("%A")

    if today not in ["Monday","Tuesday","Wednesday","Thursday","Friday"]:
        return f"<h2>Today is {today}. No school today.</h2>"

    current_period = get_current_period()

    if current_period is None:
        return "<h2>School is not running right now.</h2>"

    if current_period == "LUNCH":
        return "<h2>It is Lunch Break.</h2>"

    today_data = df[df["Day"] == today]
    period_column = f"P{current_period}"

    free_teachers = []

    for index, row in today_data.iterrows():
        cell_value = row[period_column]
        if pd.isna(cell_value) or str(cell_value).strip().upper() == "FREE":
            free_teachers.append(row["Teacher"])

    html = f"<h1>Free Teachers - {today} Period {current_period}</h1><ul>"
    for teacher in sorted(free_teachers):
        html += f"<li>{teacher}</li>"
    html += "</ul>"

    return html

if __name__ == "__main__":
    app.run()
