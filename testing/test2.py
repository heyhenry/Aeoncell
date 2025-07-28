from datetime import date, timedelta, datetime
import calendar
import sqlite3

def all_dates_current_month():
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    first_date = date(year, month, 1)
    last_date = date(year, month, number_of_days)
    delta = last_date - first_date

    return [(first_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(delta.days + 1)]

# print(all_dates_current_month())

db_connection = sqlite3.connect("aeoncell_database.db")
db_cursor = db_connection.cursor()

current_month = datetime.now().month
current_year = datetime.now().year

get_all_dates_and_steps = """
SELECT date, steps_taken FROM steps_tracker WHERE date LIKE ?
"""
db_cursor.execute(get_all_dates_and_steps, (f'__-{current_month}-{current_year}',))
results = db_cursor.fetchall()

print(current_month, current_year)

def all_dates_current_month():
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    first_date = date(year, month, 1)
    last_date = date(year, month, number_of_days)
    delta = last_date - first_date

    return [(first_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(delta.days + 1)]

# dict with dates:steps
date_steps_dict = {
    i : 0
    for i in all_dates_current_month()
}

for entry in results:
    date_steps_dict[entry[0]] = entry[1]

# for key, val in date_steps_dict.items():
    # print(f"{key}: {val}")


