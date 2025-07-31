import sqlite3
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
from datetime import datetime, date, timedelta

db_connection = sqlite3.connect("aeoncell_database.db")
db_cursor = db_connection.cursor()

current_month = datetime.now().month
current_year = datetime.now().year

if current_month < 10:
    current_month = f"0{current_month}"

def all_dates_current_month():
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    first_date = date(year, month, 1)
    last_date = date(year, month, number_of_days)
    delta = last_date - first_date

    return [(first_date + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(delta.days + 1)]

def create_data_dict(entry_type):
    table_dict = {
        "hydration": ("hydration_tracker", "consumption_ml"),
        "sleep": ("sleep_tracker", "sleep_mins"),
        "steps": ("steps_tracker", "steps_taken")
    }

    dates_of_current_month = all_dates_current_month()

    if table_dict[entry_type] in (table_dict["hydration"], table_dict["sleep"]):
        default_value = 0.0
    else:
        default_value = 0

    data_dict = {
        i : default_value
        for i in dates_of_current_month
    }

    query = f"SELECT date, {table_dict[entry_type][1]} FROM {table_dict[entry_type][0]} WHERE date LIKE ?"
    db_cursor.execute(query, (f"__-{current_month}-{current_year}",))
    found_entries = db_cursor.fetchall()

    if found_entries:
        for entry in found_entries:
            if entry[0] in data_dict:
                data_dict[entry[0]] = entry[1]

    return data_dict

def split_data_by_week(data_dict):
    dates = []
    values = []
    counter = 0
    temp_dates = []
    temp_values = []

    for key, val in data_dict.items():
        temp_dates.append(key)
        temp_values.append(val)
        counter += 1
        if counter == 7:
            dates.append(temp_dates)
            values.append(temp_values)
            counter = 0
            temp_dates = []
            temp_values = []
    
    if temp_dates:
        dates.append(temp_dates)
        values.append(temp_values)

    return (dates, values)

def get_current_week(data_dict):
    today = "01-07-2025"
    for week in range(len(data_dict[0])):
        if today in data_dict[0][week]:
            return (data_dict[0][week], data_dict[1][week])

def get_daily_goal(entry_type):
    table_dict = {
        "hydration": "daily_hydration_goal",
        "sleep": "daily_sleep_goal",
        "steps": "daily_steps_goal"
    }

    query = f"SELECT {table_dict[entry_type]} FROM profile_details"
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    daily_goal_value = result[0]

    return daily_goal_value

def create_per_week_daily_tracker_chart(parent_frame, entry_type, dates, values, daily_goal):
    table_dict = {
        "Hydration": 2000.0,
        "Sleep": 108.0,
        "Steps": 2000
    }
    largest_stored_value = max(values)
    
    daily_plot_frame = ctk.CTkFrame(parent_frame)

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.set_tight_layout(True)

    ax.plot(dates, values, marker="o")
    ax.axhline(y=daily_goal, color="r", linestyle="--", label=f"Daily {entry_type} Goal")
    ax.set_ylim(0, (largest_stored_value+table_dict[entry_type]))
    ax.set_ylabel(entry_type, fontsize=14, labelpad=30)
    ax.set_xlabel(f"Dates (Per Week of Current Month)", fontsize=14, labelpad=30)
    ax.set_title(f"Daily {entry_type} Per Week", fontsize=20, pad=30)
    plt.xticks(rotation=45)
    fig.tight_layout(pad=5.0)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=daily_plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return daily_plot_frame

def create_per_week_daily_tracker_bar_chart(parent_frame, entry_type, dates, values, daily_goal):
    table_dict = {
        "Hydration": 2000.0,
        "Sleep": 108.0,
        "Steps": 2000
    }
    largest_stored_value = max(values)
    
    daily_plot_frame = ctk.CTkFrame(parent_frame)

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.set_tight_layout(True)

    ax.bar(dates, values, width=1, edgecolor="white", linewidth=0.7)
    ax.axhline(y=daily_goal, color="r", linestyle="--", label=f"Daily {entry_type} Goal")
    ax.set_ylim(0, (largest_stored_value+table_dict[entry_type]))
    ax.set_ylabel(entry_type, fontsize=14, labelpad=30)
    ax.set_xlabel(f"Dates (Per Week of Current Month)", fontsize=14, labelpad=30)
    ax.set_title(f"Daily {entry_type} Per Week", fontsize=20, pad=30)
    plt.xticks(rotation=45)
    fig.tight_layout(pad=5.0)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=daily_plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return daily_plot_frame

root = ctk.CTk()
root.geometry("1400x900")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

scroll_content = ctk.CTkScrollableFrame(root, corner_radius=0)
scroll_content.grid_rowconfigure(0, weight=1)
scroll_content.grid_rowconfigure(2, weight=1)
scroll_content.grid_columnconfigure(0, weight=1)
scroll_content.grid_columnconfigure(2, weight=1)
scroll_content.grid(row=0, column=0, sticky="nswe")

main_content = ctk.CTkFrame(scroll_content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, width=1200, height=3200)
main_content.grid_propagate(False)
main_content.grid_rowconfigure(0, weight=1)
main_content.grid_rowconfigure(2, weight=1)
main_content.grid_columnconfigure(0, weight=1)
main_content.grid_columnconfigure(2, weight=1)
main_content.grid(row=1, column=1, pady=20)

# ----- [Daily Steps Per Week] -----
daily_steps_per_week_section = ctk.CTkFrame(main_content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
daily_steps_per_week_section.grid_rowconfigure(0, weight=1)
daily_steps_per_week_section.grid_columnconfigure(0, weight=1)
daily_steps_per_week_section.grid(row=1, column=1, pady=10)

steps_data_dict = create_data_dict("steps")
grouped_steps_data = split_data_by_week(steps_data_dict)
steps_current_week_data = get_current_week(grouped_steps_data)
steps_daily_goal_value = get_daily_goal("steps")

weekly_steps_chart = create_per_week_daily_tracker_bar_chart(daily_steps_per_week_section, "Steps", steps_current_week_data[0], steps_current_week_data[1], steps_daily_goal_value)
weekly_steps_chart.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

root.protocol("WM_DELETE_WINDOW", root.quit)

root.mainloop()



