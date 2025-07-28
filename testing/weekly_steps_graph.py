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

# date_data_a = ["01-01-2025", "02-01-2025", "03-01-2025", "04-01-2025", "05-01-2025", "06-01-2025", "07-01-2025", "08-01-2025", "09-01-2025", "10-01-2025", "11-01-2025", "12-01-2025", "13-01-2025", "14-01-2025", "15-01-2025","16-01-2025", "17-01-2025", "18-01-2025"]
# step_data_a = [5000, 7000, 9000, 2000, 4000, 3000, 5000, 6700, 9800, 9920, 4300, 4204, 2032, 6053, 6953, 5500, 4000, 9600]

# date_data_b = [
#     "01-02-2025", "02-02-2025", "03-02-2025", "04-02-2025", "05-02-2025", 
#     "06-02-2025", "07-02-2025", "08-02-2025", "09-02-2025", "10-02-2025",
#     "11-02-2025", "12-02-2025", "13-02-2025", "14-02-2025", "15-02-2025",
#     "16-02-2025", "17-02-2025", "18-02-2025"
# ]

# step_data_b = [
#     6200, 4800, 8500, 3100, 5300, 
#     2900, 7100, 5900, 8800, 9100,
#     4600, 3800, 2500, 6800, 7200,
#     5100, 4300, 9700
# ]

# def split_into_weeks(date_info, step_info): 
#     all_data = []
#     for i in range(len(date_info)):
#         all_data.append((date_info[i], step_info[i]))

#     dates = []
#     steps = []
#     counter = 0
#     dates_temp = []
#     steps_temp = []
#     for data in all_data:
#         if counter < 7:
#             dates_temp.append(data[0])
#             steps_temp.append(data[1])
#             counter += 1
#         else:
#             dates.append(dates_temp)
#             steps.append(steps_temp)
#             counter = 0
#             dates_temp = [data[0]]
#             steps_temp = [data[1]]
#     dates.append(dates_temp)
#     steps.append(steps_temp)
#     return (dates, steps)

# # ax1
# results = split_into_weeks(date_data_a, step_data_a)
# dates_a = results[0]
# steps_a = results[1]

# # ax2
# results = split_into_weeks(date_data_b, step_data_b)
# dates_b = results[0]
# steps_b = results[1]

# daily_goal = 5000

db_connection = sqlite3.connect("aeoncell_database.db")
db_cursor = db_connection.cursor()

current_month = datetime.now().month
current_year = datetime.now().year

if current_month < 10:
    current_month = f"0{current_month}"

# get all the dates of the current month and store as a list
def all_dates_current_month():
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    first_date = date(year, month, 1)
    last_date = date(year, month, number_of_days)
    delta = last_date - first_date

    return [(first_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(delta.days + 1)]

# get list of dates for the current month
dates_of_current_month = all_dates_current_month()
# populate dictionary with a key(date): value(steps_count)
steps_dict = {
    # defaulted to 0 steps_count
    i : 0
    for i in dates_of_current_month
}

# retrieve the steps entries (date and steps_count data) for the current month
get_steps_data = """
SELECT date, steps_taken FROM steps_tracker WHERE date LIKE ?
"""
db_cursor.execute(get_steps_data, (f'__-{current_month}-{current_year}',))
results = db_cursor.fetchall()

# loop through the entries retrieved from the database
for entry in results:
    # if any entry date matches a key in the steps_dict, then update the associated value (steps_count)
    if entry[0] in steps_dict:
        steps_dict[entry[0]] = entry[1]

# create a list of x and y values (dates and steps_count) which is split into subarrays of 7 (denoting a weekly count)
def split_by_week(steps_dictionary):
    dates = []
    values = []
    counter = 0
    dates_temp = []
    values_temp = []
    for key, val in steps_dictionary.items():
        dates_temp.append(key)
        values_temp.append(val)
        counter += 1

        if counter == 7:
            dates.append(dates_temp)
            values.append(values_temp)
            counter = 0
            dates_temp = []
            values_temp = []

    if dates_temp:
        dates.append(dates_temp)
        values.append(values_temp)

    return (dates, values)

results = split_by_week(steps_dict)

# root = ctk.CTk()

# # create the content frame
# content_frame = ctk.CTkFrame(root, border_width=3, border_color="red")
# content_frame.grid(row=0, column=0, sticky="nswe")
# content_frame.grid_rowconfigure(0, weight=1)
# content_frame.grid_columnconfigure(0, weight=1)

# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# # ax1
# ax1.plot(dates_a[0], steps_a[0], marker='o')
# ax1.axhline(y=daily_goal, color='r', linestyle='--')
# plt.xticks(rotation=45)

# # ax2
# ax2.plot(dates_b[0], steps_b[0], marker='o')
# ax2.axhline(y=daily_goal, color='b', linestyle='--')
# plt.xticks(rotation=45)

# canvas = FigureCanvasTkAgg(fig, master=content_frame)
# canvas.draw()
# canvas.get_tk_widget().pack(fill="both", expand=True)

# root.protocol("WM_DELETE_WINDOW", root.quit)

# root.mainloop()



