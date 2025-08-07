import customtkinter as ctk
from PIL import Image
from widgets import Navbar
from datetime import date, timedelta, datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # data for graphs and charts
        self.current_month = self.controller.current_month
        self.current_year = self.controller.current_year
        self.today = self.controller.today

        steps_data_dict = self.create_data_dict("steps")
        grouped_steps_data = self.split_data_by_week(steps_data_dict)
        self.steps_current_week_data = self.get_current_week(grouped_steps_data)
        self.steps_daily_goal_value = self.get_daily_goal("steps")

        hydration_data_dict = self.create_data_dict("hydration")
        grouped_hydration_data = self.split_data_by_week(hydration_data_dict)
        self.hydration_current_week_data = self.get_current_week(grouped_hydration_data)
        self.hydration_daily_goal_value = self.get_daily_goal("hydration")

        sleep_data_dict = self.create_data_dict("sleep")
        grouped_sleep_data = self.split_data_by_week(sleep_data_dict)
        self.sleep_current_week_data = self.get_current_week(grouped_sleep_data)
        self.sleep_daily_goal_value = self.get_daily_goal("sleep")

        monthly_steps_data_dict = self.create_data_dict("steps")
        self.monthly_steps_dates = list(monthly_steps_data_dict.keys())
        self.monthly_steps_values = list(monthly_steps_data_dict.values())
        self.monthly_steps_daily_goal_value = self.get_daily_goal("steps")

        monthly_hydration_data_dict = self.create_data_dict("hydration")
        self.monthly_hydration_dates = list(monthly_hydration_data_dict.keys())
        self.monthly_hydration_values = list(monthly_hydration_data_dict.values())
        self.monthly_hydration_daily_goal_value = self.get_daily_goal("hydration")

        monthly_sleep_data_dict = self.create_data_dict("sleep")
        self.monthly_sleep_dates = list(monthly_sleep_data_dict.keys())
        self.monthly_sleep_values = list(monthly_sleep_data_dict.values())
        self.monthly_sleep_daily_goal_value = self.get_daily_goal("sleep")

        monthly_exercise_daily_volume_dict = self.create_exercise_volume_dict()
        self.monthly_exercise_daily_volume_dates = list(monthly_exercise_daily_volume_dict.keys())
        self.monthly_exercise_daily_volume_values = list(monthly_exercise_daily_volume_dict.values())

        self.create_widgets()

    def create_widgets(self):
        #region [Main Frames]
        navbar = Navbar(self, self.controller)
        content = ctk.CTkScrollableFrame(self, corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(5, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)
        #endregion

        #region [PageFrames]
        page_title = ctk.CTkLabel(content, text="Statistics", font=("", 24))
        page_message = ctk.CTkLabel(content, text="View your statistics here", font=("", 14))
        statistics_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=1200, height=6200)

        statistics_section.grid_propagate(False)
        statistics_section.grid_rowconfigure(0, weight=1)
        statistics_section.grid_rowconfigure(8, weight=1)
        statistics_section.grid_columnconfigure(0, weight=1)
        statistics_section.grid_columnconfigure(2, weight=1)

        page_title.grid(row=1, column=1, pady=(30, 0), sticky="w", padx=(0, 1000))
        page_message.grid(row=2, column=1, pady=(0, 50), sticky="w")
        statistics_section.grid(row=3, column=1, pady=(0, 50))
        #endregion

        # ==================== [STATISTICS CONTENT] ====================
        #region [Daily Steps Per Week]
        daily_steps_per_week_section = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        daily_steps_per_week_section.grid_rowconfigure(0, weight=1)
        daily_steps_per_week_section.grid_columnconfigure(0, weight=1)
        daily_steps_per_week_section.grid(row=1, column=1, pady=10)

        weekly_steps_graph = self.create_per_week_daily_tracker_bar_chart(daily_steps_per_week_section, "Steps", self.steps_current_week_data[0], self.steps_current_week_data[1], self.steps_daily_goal_value)
        weekly_steps_graph.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        #endregion

        #region [Daily Hydration Per Week]
        daily_hydration_per_week_section = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        daily_hydration_per_week_section.grid_rowconfigure(0, weight=1)
        daily_hydration_per_week_section.grid_columnconfigure(0, weight=1)
        daily_hydration_per_week_section.grid(row=2, column=1, pady=10)

        weekly_hydration_graph = self.create_per_week_daily_tracker_bar_chart(daily_hydration_per_week_section, "Hydration", self.hydration_current_week_data[0], self.hydration_current_week_data[1], self.hydration_daily_goal_value)
        weekly_hydration_graph.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        #endregion

        #region [Daily Sleep Per Week]
        daily_sleep_per_week_section = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        daily_sleep_per_week_section.grid_rowconfigure(0, weight=1)
        daily_sleep_per_week_section.grid_columnconfigure(0, weight=1)
        daily_sleep_per_week_section.grid(row=3, column=1, pady=10)

        weekly_sleep_graph = self.create_per_week_daily_tracker_bar_chart(daily_sleep_per_week_section, "Sleep", self.sleep_current_week_data[0], self.sleep_current_week_data[1], self.sleep_daily_goal_value)
        weekly_sleep_graph.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        #endregion

        #region [Daily Steps Per Month]
        daily_steps_per_month_section = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        daily_steps_per_month_section.grid_rowconfigure(0, weight=1)
        daily_steps_per_month_section.grid_columnconfigure(0, weight=1)
        daily_steps_per_month_section.grid(row=4, column=1, pady=10)

        monthly_steps_chart = self.create_per_month_daily_tracker_line_chart(daily_steps_per_month_section, "Steps", self.monthly_steps_dates, self.monthly_steps_values, self.monthly_steps_daily_goal_value)
        monthly_steps_chart.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        #endregion

        #region [Daily Hydration Per Month]
        daily_hydration_per_month_section = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        daily_hydration_per_month_section.grid_rowconfigure(0, weight=1)
        daily_hydration_per_month_section.grid_columnconfigure(0, weight=1)
        daily_hydration_per_month_section.grid(row=5, column=1, pady=10)

        monthly_hydration_chart = self.create_per_month_daily_tracker_line_chart(daily_hydration_per_month_section, "Hydration", self.monthly_hydration_dates, self.monthly_hydration_values, self.monthly_hydration_daily_goal_value)
        monthly_hydration_chart.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        #endregion

        #region [Daily Sleep Per Month]
        daily_sleep_per_month_section = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        daily_sleep_per_month_section.grid_rowconfigure(0, weight=1)
        daily_sleep_per_month_section.grid_columnconfigure(0, weight=1)
        daily_sleep_per_month_section.grid(row=6, column=1, pady=10)

        monthly_sleep_chart = self.create_per_month_daily_tracker_line_chart(daily_sleep_per_month_section, "Sleep", self.monthly_sleep_dates, self.monthly_sleep_values, self.monthly_sleep_daily_goal_value)
        monthly_sleep_chart.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
        #endregion    

        #region [Daily Exercise Volume Per Month]
        daily_exercise_per_month_section = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        daily_exercise_per_month_section.grid_rowconfigure(0, weight=1)
        daily_exercise_per_month_section.grid_columnconfigure(0, weight=1)
        daily_exercise_per_month_section.grid(row=7, column=1, pady=10)
        
        monthly_exercise_volume_chart = self.create_per_month_daily_exercise_weight_volume_bar_chart(daily_exercise_per_month_section, self.monthly_exercise_daily_volume_dates, self.monthly_exercise_daily_volume_values)
        monthly_exercise_volume_chart.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
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
        for week in range(len(data_dict[0])):
            if self.today in data_dict[0][week]:
                return (data_dict[0][week], data_dict[1][week])

    def get_daily_goal(self, entry_type):
        # map entry type to daily tracking table 
        table_dict = {
            "hydration": "daily_hydration_goal",
            "sleep": "daily_sleep_goal",
            "steps": "daily_steps_goal" 
        }

        get_daily_goal_query = f"SELECT {table_dict[entry_type]} FROM profile_details"
        self.controller.db_cursor.execute(get_daily_goal_query)
        results = self.controller.db_cursor.fetchone()
        daily_goal_value = results[0]

        return daily_goal_value
    
    def create_per_week_daily_tracker_bar_chart(self, parent_frame, entry_type, dates, values, daily_goal):
        table_dict = {
            "Hydration": (2000.0, "(Ml)"),
            "Sleep": (108.0, "(Mins)"),
            "Steps": (2000,"")
        }
        largest_stored_value = max(values)
        
        daily_plot_frame = ctk.CTkFrame(parent_frame)

        fig, ax = plt.subplots(figsize=(10, 8))
        fig.set_tight_layout(True)

        ax.bar(dates, values, width=1, edgecolor="white", linewidth=0.7)
        ax.axhline(y=daily_goal, color="r", linestyle="--", label=f"Daily {entry_type} Goal")
        ax.set_ylim(0, (largest_stored_value+table_dict[entry_type][0]))
        ax.set_ylabel(f"{entry_type} {table_dict[entry_type][1]}", fontsize=14, labelpad=30)
        ax.set_xlabel("Dates (Per Week of Current Month)", fontsize=14, labelpad=30)
        ax.set_title(f"Daily {entry_type} Per Week", fontsize=20, pad=30)
        plt.xticks(rotation=45)
        fig.tight_layout(pad=5.0)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=daily_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        return daily_plot_frame
    
    def create_per_month_daily_tracker_line_chart(self, parent_frame, entry_type, dates, values, daily_goal):
        table_dict = {
            "Hydration": (2000.0, "(Ml)"),
            "Sleep": (108.0, "(Mins)"),
            "Steps": (2000,"")
        }
        largest_stored_value = max(values)

        monthly_plot_frame = ctk.CTkFrame(parent_frame)

        fig, ax = plt.subplots(figsize=(10, 8))
        fig.set_tight_layout(True)

        plt.subplots_adjust(bottom=0.6)

        ax.plot(dates, values, marker="o")
        ax.axhline(y=daily_goal, color="r", linestyle="--", label=f"Daily {entry_type} Goal")
        ax.set_ylim(0, (largest_stored_value+table_dict[entry_type][0]))
        ax.set_ylabel(f"{entry_type} {table_dict[entry_type][1]}", fontsize=14, labelpad=30)
        ax.set_xlabel("Dates for the Current Month", fontsize=14, labelpad=30)
        ax.set_title(f"Daily {entry_type} Per Month", fontsize=20, pad=30)
        plt.xticks(rotation=45)
        fig.tight_layout(pad=5.0)
        ax.legend()

        ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
        slider = Slider(ax_slider, "Day", 0, len(dates)-1, valinit=0, valstep=1)
        
        # reference to fig and slider due to auto garbage collection
        monthly_plot_frame.fig = fig
        monthly_plot_frame.slider = slider

        def update(val):
            i = int(slider.val)
            n = len(dates)

            start = max(0, i-3)
            end = min(n-1, i+3)

            ax.set_xlim(dates[start], dates[end])
            fig.canvas.draw_idle()

        canvas = FigureCanvasTkAgg(fig, master=monthly_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        slider.on_changed(update)
        slider.set_val(0)

        return monthly_plot_frame
    
    def create_exercise_volume_dict(self):
        # get all dates of the current month
        dates_of_current_month = self.all_dates_current_month()
        
        # initialise a dictionary with the keys being the dates of the current month
        data_dict = {
            i : []
            for i in dates_of_current_month
        }
        
        # retrieve all relevant exericse entries data for the current month
        query = f"SELECT date, sets_count, reps_count, weight_value FROM exercise_entries WHERE date LIKE ?"
        self.controller.db_cursor.execute(query, (f"__-{self.current_month}-{self.current_year}",))
        found_entries = self.controller.db_cursor.fetchall()

        # update the dictionary with weight volume data

        if found_entries:
            for entry in found_entries:
                if entry[0] in data_dict:
                    # calculate weight volume per entry
                    total_volume = (entry[1] * entry[2]) * entry[3]
                    data_dict[entry[0]].append(total_volume)

        sum_volume_dict = {
            i : 0
            for i in dates_of_current_month
        }

        for key, val in data_dict.items():
            # if the list isn't empty
            if val:
                # add total sum of all weight volumes for each day to respective date key
                sum_volume_dict[key] = sum(val)

        return sum_volume_dict

    def create_per_month_daily_exercise_weight_volume_bar_chart(self, parent_frame, dates, values):
        monthly_chart_frame = ctk.CTkFrame(parent_frame)

        current_month_str = datetime.now().strftime("%B")
        largest_stored_value = max(values)+2000

        fig, ax = plt.subplots(figsize=(10, 8))
        fig.set_tight_layout(True)

        ax.bar(dates, values, width=1, edgecolor="white", linewidth=0.7)
        ax.set_ylim(0, largest_stored_value)
        ax.set_ylabel("Volume (KG)", fontsize=14, labelpad=30)
        ax.set_xlabel("Dates (Everday of the Month)", fontsize=14, labelpad=30)
        ax.set_title(f"Daily Exercise Volume for {current_month_str}", pad=30)
        plt.xticks(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=monthly_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        return monthly_chart_frame

    def create_per_month_daily_exercise_tracker_histogram(self, parent_frame, values):
        monthly_chart_frame = ctk.CTkFrame(parent_frame)

        fig, ax = plt.subplots(figsize=(10, 8))
        fig.set_tight_layout(True)

        ax.hist(values, bins=5, color="skyblue", edgecolor="black", alpha=0.7)
        ax.set_title("Volume Distribution of Daily Exercises Per Month", fontsize=20, pad=30)
        ax.set_xlabel("Volume (kg)", fontsize=14, labelpad=30)
        ax.set_ylabel("Frequency", fontsize=14, labelpad=30)
        ax.grid(axis='y', linestyle="--", alpha=0.6)
        fig.tight_layout(pad=5.0)

        canvas = FigureCanvasTkAgg(fig, master=monthly_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        return monthly_chart_frame
