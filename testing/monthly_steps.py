from datetime import date, timedelta, datetime
import calendar
import sqlite3
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def all_dates_current_month():
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    first_date = date(year, month, 1)
    last_date = date(year, month, number_of_days)
    delta = last_date - first_date

    return [(first_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(delta.days + 1)]

def number_of_days():
    month = datetime.now().month
    year = datetime.now().year
    return calendar.monthrange(year, month)[1]

db_connection = sqlite3.connect("aeoncell_database.db")
db_cursor = db_connection.cursor()

get_all_dates_and_steps = """
SELECT date, steps_taken FROM steps_tracker
"""
db_cursor.execute(get_all_dates_and_steps)
results = db_cursor.fetchall()

dates = []
steps = [i for i in range(number_of_days())]

# for i in range(len(results)):
#     # dates.append(results[i][0])
#     steps.append(results[i][1])

dates = all_dates_current_month()

get_daily_steps_goal = """
SELECT daily_steps_goal FROM profile_details
"""
db_cursor.execute(get_daily_steps_goal)
daily_goal = db_cursor.fetchone()[0]

root = ctk.CTk()

content_frame = ctk.CTkFrame(root, border_width=3, border_color="red")
content_frame.grid(row=0, column=0)
content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

# create graph figure
fig, ax = plt.subplots(figsize=(12, 8))

# adjust the margins for the bottom of the figure to ensure space for the slider
plt.subplots_adjust(bottom=0.3)

# plot data to figure
ax.plot(dates, steps, marker='o')
ax.axhline(y=daily_goal, color='r', linestyle='--')
# 45 degree rotatation of the x axis values (dates) to fit better due to its length
plt.xticks(rotation=45)

# adjust slider location
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
# create the slider
slider = Slider(ax_slider, 'Day', 0, len(dates)-1, valinit=0, valstep=1)

# create tkinter compatible canvas to host the figure
canvas = FigureCanvasTkAgg(fig, master=content_frame)
canvas.draw()
canvas.get_tk_widget().pack()

# update the displayed data based on user slider actions
def update(val):
    i = int(slider.val)
    n = len(dates)

    start = max(0, i-3)
    end = min(n-1, i+4)

    ax.set_xlim(dates[start], dates[end])
    fig.canvas.draw_idle()

# trigger the update() upon slider action being made
slider.on_changed(update)

# cleanup to deal with ghost callbacks
def cleanup():
    slider.disconnect_events()
    root.quit()

# embed cleanup function upon app window close for a clean exit (no lingering terminals)
root.protocol("WM_DELETE_WINDOW", cleanup)

root.mainloop()