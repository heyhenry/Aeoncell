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

        self.left_slider_arrow_icon = ctk.CTkImage(light_image=Image.open("img/left_slider_arrow.png"), dark_image=Image.open("img/left_slider_arrow.png"), size=(64, 64))
        self.right_slider_arrow_icon = ctk.CTkImage(light_image=Image.open("img/right_slider_arrow.png"), dark_image=Image.open("img/right_slider_arrow.png"), size=(64, 64))
        self.graph_name = ctk.StringVar()

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

        # false indicates the chart is not currently the one being displayed
        self.chart_frames = [
            ("daily_steps_per_week", True, self.create_per_week_daily_tracker_bar_chart, {
                "parent_frame": self.display_chart_frame,
                "entry_type": "Steps",
                "dates": self.steps_current_week_data[0],
                "values": self.steps_current_week_data[1],
                "daily_goal": self.steps_daily_goal_value  
                }),
            ("daily_hydration_per_week", False, self.create_per_week_daily_tracker_bar_chart, {
                "parent_frame": self.display_chart_frame,
                "entry_type": "Hydration",
                "dates": self.hydration_current_week_data[0],
                "values": self.hydration_current_week_data[1],
                "daily_goal": self.hydration_daily_goal_value  
                }),
            ("daily_sleep_per_week", False, self.create_per_week_daily_tracker_bar_chart, {
                "parent_frame": self.display_chart_frame,
                "entry_type": "Sleep",
                "dates": self.sleep_current_week_data[0],
                "values": self.sleep_current_week_data[1],
                "daily_goal": self.sleep_daily_goal_value  
                }),
            ("daily_steps_per_month", False, self.create_per_month_daily_tracker_line_chart, {
                "parent_frame": self.display_chart_frame,
                "entry_type": "Steps",
                "dates": self.monthly_steps_dates,
                "values": self.monthly_steps_values,
                "daily_goal": self.monthly_steps_daily_goal_value
            }),
            ("daily_hydration_per_month", False, self.create_per_month_daily_tracker_line_chart, {
                "parent_frame": self.display_chart_frame,
                "entry_type": "Hydration",
                "dates": self.monthly_hydration_dates,
                "values": self.monthly_hydration_values,
                "daily_goal": self.monthly_hydration_daily_goal_value
            }),
            ("daily_sleep_per_month", False, self.create_per_month_daily_tracker_line_chart, {
                "parent_frame": self.display_chart_frame,
                "entry_type": "Sleep",
                "dates": self.monthly_sleep_dates,
                "values": self.monthly_sleep_values,
                "daily_goal": self.monthly_sleep_daily_goal_value
            }),
            ("daily_exercise_volume_per_month", False, self.create_per_month_daily_exercise_weight_volume_bar_chart, {
                "parent_frame": self.display_chart_frame,
                "dates": self.monthly_exercise_daily_volume_dates,
                "values": self.monthly_exercise_daily_volume_values 
            })
        ]

        self.initial_chart_displayed()

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
        statistics_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=1250, height=1400)

        statistics_section.grid_propagate(False)
        statistics_section.grid_rowconfigure(0, weight=1)
        statistics_section.grid_rowconfigure(2, weight=1)
        statistics_section.grid_columnconfigure(0, weight=1)
        statistics_section.grid_columnconfigure(4, weight=1)

        page_title.grid(row=1, column=1, pady=(30, 0), sticky="w", padx=(0, 1000))
        page_message.grid(row=2, column=1, pady=(0, 50), sticky="w")
        statistics_section.grid(row=3, column=1, pady=(0, 50))
        #endregion

        # ==================== [STATISTICS CONTENT] ====================
        #region [Chart Display]
        self.display_chart_frame = ctk.CTkFrame(statistics_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        left_slider_arrow_display = ctk.CTkLabel(statistics_section, text="", image=self.left_slider_arrow_icon)
        right_slider_arrow_display = ctk.CTkLabel(statistics_section, text="", image=self.right_slider_arrow_icon)
        
        self.display_chart_frame.grid(row=1, column=2, pady=10)
        left_slider_arrow_display.grid(row=1, column=1, padx=(10, 20))
        right_slider_arrow_display.grid(row=1, column=3, padx=(20, 10))

        # chart_content_display = 
        # weekly_steps_graph = self.create_per_week_daily_tracker_bar_chart(daily_steps_per_week_section, "Steps", self.steps_current_week_data[0], self.steps_current_week_data[1], self.steps_daily_goal_value)
        # weekly_steps_graph.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")
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

    # redundant ? may use for other use case
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

    def update_chart_frame_content(self, chart_func, chart_params):
        self.chart_display_content = chart_func(**chart_params)
        self.chart_display_content.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

    def initial_chart_displayed(self):
        # check the list to see which chart to display upon startup
        for chart_name, is_active, chart_func, func_params in self.chart_frames:
            if is_active:
                self.update_chart_frame_content(chart_func, func_params)
                # in case - shouldnt need it, so may just remove it in final copy
                break
        
    def switch_chart_display(self):
        pass
        # check which chart is currently displayed

        # update the dictionary on the new chart displayed

        # generate and display the new chart


