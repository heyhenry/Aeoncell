from datetime import date, timedelta, datetime
import calendar
import sqlite3
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# def get_current_week():
#     month = datetime.now().month
#     year = datetime.now().year
#     number_of_days = calendar.monthrange(year, month)[1]
#     first_date = date(year, month, 1)

date_data_a = ["01-01-2025", "02-01-2025", "03-01-2025", "04-01-2025", "05-01-2025", "06-01-2025", "07-01-2025", "08-01-2025", "09-01-2025", "10-01-2025", "11-01-2025", "12-01-2025", "13-01-2025", "14-01-2025", "15-01-2025","16-01-2025", "17-01-2025", "18-01-2025"]
step_data_a = [5000, 7000, 9000, 2000, 4000, 3000, 5000, 6700, 9800, 9920, 4300, 4204, 2032, 6053, 6953, 5500, 4000, 9600]

date_data_b = [
    "01-02-2025", "02-02-2025", "03-02-2025", "04-02-2025", "05-02-2025", 
    "06-02-2025", "07-02-2025", "08-02-2025", "09-02-2025", "10-02-2025",
    "11-02-2025", "12-02-2025", "13-02-2025", "14-02-2025", "15-02-2025",
    "16-02-2025", "17-02-2025", "18-02-2025"
]

step_data_b = [
    6200, 4800, 8500, 3100, 5300, 
    2900, 7100, 5900, 8800, 9100,
    4600, 3800, 2500, 6800, 7200,
    5100, 4300, 9700
]

def split_into_weeks(date_info, step_info): 
    all_data = []
    for i in range(len(date_info)):
        all_data.append((date_info[i], step_info[i]))

    dates = []
    steps = []
    counter = 0
    dates_temp = []
    steps_temp = []
    for data in all_data:
        if counter < 7:
            dates_temp.append(data[0])
            steps_temp.append(data[1])
            counter += 1
        else:
            dates.append(dates_temp)
            steps.append(steps_temp)
            counter = 0
            dates_temp = [data[0]]
            steps_temp = [data[1]]
    dates.append(dates_temp)
    steps.append(steps_temp)
    return (dates, steps)

# ax1
results = split_into_weeks(date_data_a, step_data_a)
dates_a = results[0]
steps_a = results[1]

# ax2
results = split_into_weeks(date_data_b, step_data_b)
dates_b = results[0]
steps_b = results[1]

daily_goal = 5000

root = ctk.CTk()

# create the content frame
content_frame = ctk.CTkFrame(root, border_width=3, border_color="red")
content_frame.grid(row=1, column=1)
content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_rowconfigure(2, weight=1)
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(2, weight=1)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# ax1
ax1.plot(dates_a[0], steps_a[0], marker='o')
ax1.axhline(y=daily_goal, color='r', linestyle='--')
plt.xticks(rotation=45)

# ax2
ax2.plot(dates_b[0], steps_b[0], marker='o')
ax2.axhline(y=daily_goal, color='b', linestyle='--')
plt.xticks(rotation=45)

canvas = FigureCanvasTkAgg(fig, master=content_frame)
canvas.draw()
canvas.get_tk_widget().pack()

root.protocol("WM_DELETE_WINDOW", root.quit)

root.mainloop()



