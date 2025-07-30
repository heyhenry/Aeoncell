import customtkinter as ctk
from PIL import Image
from widgets import Navbar
from datetime import date, timedelta, datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        #region [Main Frames]
        navbar = Navbar(self, self.controller)
        content = ctk.CTkScrollableFrame(self, corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(4, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)
        #endregion

        #region [PageFrames]
        page_title = ctk.CTkLabel(content, text="Statistics", font=("", 24))
        page_message = ctk.CTkLabel(content, text="View your statistics here", font=("", 14))
        statistics_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=1200, height=3200)

        statistics_section.grid_propagate(False)
        statistics_section.grid_rowconfigure(0, weight=1)
        statistics_section.grid_rowconfigure(2, weight=1)
        statistics_section.grid_columnconfigure(0, weight=1)
        statistics_section.grid_columnconfigure(2, weight=1)

        page_title.grid(row=1, column=1, pady=(30, 0), sticky="w", padx=(0, 1000))
        page_message.grid(row=2, column=1, pady=(0, 50), sticky="w")
        statistics_section.grid(row=3, column=1, pady=(0, 50))
        #endregion

        # ==================== [STATISTICS CONTENT] ====================
        #region [DailyStepsPerWeek]
        daily_steps_per_week_section = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        daily_steps_per_week_section.grid_rowconfigure(0, weight=1)
        daily_steps_per_week_section.grid_columnconfigure(0, weight=1)
        daily_steps_per_week_section.grid(row=0, column=0)

        # temp value storage
        steps_data_dict = self.create_data_dict("steps")
        steps_data = self.split_data_by_week(steps_data_dict)
        steps_weekly_data = self.get_current_week(steps_data)
        steps_daily_goal = self.get_daily_goal("steps")

        weekly_steps_graph = self.create_daily_plots(daily_steps_per_week_section, steps_weekly_data[0], steps_weekly_data[1], steps_daily_goal)
        weekly_steps_graph.grid(row=0, column=0, sticky="nswe")

        #endregion
        #region [DailyHydrationPerWeek]
        #endregion
        #region [DailySleepPerWeek]
        #endregion
        #region [DailyExerciseVolumePerWeek]
        #endregion
        #region [DailyRepsTotalPerWeek] & [DailySetsTotalPerWeek]
        #endregion

    def all_dates_current_month(self):
        month = datetime.now().month
        year = datetime.now().year
        number_of_days = calendar.monthrange(year, month)[1]
        first_date = date(year, month, 1)
        last_date = date(year, month, number_of_days)
        delta = last_date - first_date

        return [(first_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(delta.days + 1)]
            
    def create_data_dict(self, entry_type):
        current_month = self.controller.current_month
        current_year = self.controller.current_year

        # map entry type to daily tracking table 
        table_dict = {
            "hydration": ("hydration_tracker", "consumption_ml"),
            "sleep": ("sleep_tracker", "sleep_mins"),
            "steps": ("steps_tracker", "steps_taken")
        }

        # get list of all dates in the current month
        dates_of_current_month = self.all_dates_current_month()

        # determine if default value is set to integer or float
        if table_dict[entry_type] in (table_dict["hydration"], table_dict["sleep"]):
            default_value = 0.0
        else:
            default_value = 0

        # create initial data dictionary with dates as keys and values as defaulted values
        data_dict = {
            i : default_value
            for i in dates_of_current_month
        }

        # retrieve the daily tracker data 
        query = f"SELECT date, {table_dict[entry_type][1]} FROM {table_dict[entry_type][0]} WHERE date LIKE ?"
        self.controller.db_cursor.execute(query, (f'__-{current_month}-{current_year}',))
        found_entries = self.controller.db_cursor.fetchall()
        if found_entries:
            for entry in found_entries:
                if entry[0] in data_dict:
                    data_dict[entry[0]] = entry[1]

        return data_dict

    def split_data_by_week(self, data_dict):
        dates = []
        values = []
        counter = 0
        dates_temp = []
        values_temp = []
        for key, val in data_dict.items():
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
    
    def get_current_week(self, data_dict):
        # today = self.controller.today
        today = "01-07-2025"
        for week in range(len(data_dict[0])):
            if today in data_dict[0][week]:
                return (data_dict[0][week], data_dict[1][week])

    def get_daily_goal(self, entry_type):
        # map entry type to daily tracking table 
        table_dict = {
            "hydration": "daily_hydration_goal",
            "sleep": "daily_sleep_goal",
            "steps": "daily_steps_goal" 
        }
        self.controller.db_cursor.execute("SELECT ? FROM profile_details", (table_dict[entry_type],))
        daily_goal_value = self.controller.db_cursor.fetchone()[0]

        return daily_goal_value
    
    def create_daily_plots(self, parent_frame, dates, values, daily_goal):
        daily_plot_frame = ctk.CTkFrame(parent_frame)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.set_tight_layout(True)
        
        ax.plot(dates, values, marker='o', linestyle='-', color='#1f77b4')
        ax.axhline(y=daily_goal, color='red', linestyle='--', label='Daily Goal')
        ax.set_ylabel('Values')
        ax.set_title('Weekly Daily*steps for now* Progress')
        plt.xticks(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=daily_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        return daily_plot_frame