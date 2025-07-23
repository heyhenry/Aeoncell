import customtkinter as ctk
from tkinter import ttk as btk
from PIL import Image
from datetime import date, timedelta, datetime
import random
import requests
from widgets import Navbar
from utils import *

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # temp
        self.icon = ctk.CTkImage(light_image=Image.open("img/big_flame.png"), dark_image=Image.open("img/big_flame.png"), size=(32, 32))
        self.badge = ctk.CTkImage(light_image=Image.open("img/achievements/original_icons/first_workout.png"), dark_image=Image.open("img/achievements/original_icons/first_workout.png"), size=(64, 64))
        self.mini_banner = ctk.CTkImage(light_image=Image.open("img/laid_dumbbell_man.png"), dark_image=Image.open("img/laid_dumbbell_man.png"), size=(100, 100))
        self.weather_forecast = ctk.CTkImage(light_image=Image.open("img/forecast_storm.png"), dark_image=Image.open("img/forecast_storm.png"), size=(64, 64))
        # multi-sectional use
        self.today = self.controller.today

        # intro section
        self.welcome_message = ctk.StringVar()
        today_full = date.today()
        today_full = today_full.strftime("%d %B %Y")
        self.today_full_display = ctk.StringVar(value=today_full)
        self.intro_icon = ctk.CTkImage(light_image=Image.open("img/intro_section/calendar.png"), dark_image=Image.open("img/intro_section/calendar.png"), size=(64, 64)) 
        self.motivation_icon = ctk.CTkImage(light_image=Image.open("img/intro_section/motivational_fist.png"), dark_image=Image.open("img/intro_section/motivational_fist.png"), size=(64, 64)) 
        self.motivational_message = ctk.StringVar()

        # image variables
        self.profile_image = ctk.CTkImage(light_image=Image.open("img/user_profile.png"), dark_image=Image.open("img/user_profile.png"), size=(192, 192))
        self.reset_icon = ctk.CTkImage(light_image=Image.open("img/dailies_section/reset.png"), dark_image=Image.open("img/dailies_section/reset.png"), size=(32, 32))
        self.sleep_icon = ctk.CTkImage(light_image=Image.open("img/dailies_section/sleeping.png"), dark_image=Image.open("img/dailies_section/sleeping.png"), size=(32, 32))
        self.hydration_icon = ctk.CTkImage(light_image=Image.open("img/dailies_section/hydration.png"), dark_image=Image.open("img/dailies_section/hydration.png"), size=(32, 32))
        self.walking_icon = ctk.CTkImage(light_image=Image.open("img/dailies_section/walking.png"), dark_image=Image.open("img/dailies_section/walking.png"), size=(32, 32))
        self.summary_icon = ctk.CTkImage(light_image=Image.open("img/summary.png"), dark_image=Image.open("img/summary.png"), size=(64, 64))
        self.fireball_icon = ctk.CTkImage(light_image=Image.open("img/fireball.png"), dark_image=Image.open("img/fireball.png"), size=(48, 48))
        self.weather_section_icon = ctk.CTkImage(light_image=Image.open("img/weather/general_weather.png"), dark_image=Image.open("img/weather/general_weather.png"), size=(64, 64))
        self.weather_icon = ctk.CTkImage(light_image=Image.open("img/weather/default_weather.png"), dark_image=Image.open("img/weather/default_weather.png"), size=(64, 64))
        self.session_entry_icon = ctk.CTkImage(light_image=Image.open("img/barbell.png"), dark_image=Image.open("img/barbell.png"), size=(64, 64))
        self.single_entry_icon = ctk.CTkImage(light_image=Image.open("img/dumbbell.png"), dark_image=Image.open("img/dumbbell.png"), size=(64, 64))

        # profile section related variables
        self.profile_first_name_var = ctk.StringVar()
        self.profile_last_name_var = ctk.StringVar()
        self.profile_age_var = ctk.StringVar()
        self.profile_height_var = ctk.StringVar()
        self.profile_current_weight_var = ctk.StringVar()
        self.profile_goal_weight_var = ctk.StringVar()
        self.profile_name_display = ctk.StringVar()

        self.monthly_weight_choice_display = ctk.StringVar()
        self.monthly_sleep_display = ctk.StringVar()
        self.monthly_sleep_goal_var = ctk.StringVar()
        self.monthly_sleep_current_var = ctk.StringVar()  
        self.monthly_walking_display = ctk.StringVar()
        self.monthly_walking_goal_var = ctk.StringVar()
        self.monthly_walking_current_var = ctk.StringVar()
        self.monthly_hydration_display = ctk.StringVar()
        self.monthly_hydration_goal_var = ctk.StringVar()
        self.monthly_hydration_current_var = ctk.StringVar()

        # daily section related variables
        self.steps_var = ctk.StringVar()
        self.steps_display = ctk.StringVar(value="0 steps")
        self.steps_current_progress = ctk.StringVar()
        self.steps_goal = ctk.StringVar()
        self.steps_progress_display = ctk.StringVar()

        self.hydration_var = ctk.StringVar()
        self.hydration_display = ctk.StringVar(value="0.0 ml")
        self.hydration_current_progress = ctk.StringVar()
        self.hydration_goal = ctk.StringVar()
        self.hydration_progress_display = ctk.StringVar()

        self.sleep_var = ctk.StringVar()
        self.sleep_display = ctk.StringVar(value="0.0 mins")
        self.sleep_current_progress = ctk.StringVar()
        self.sleep_goal = ctk.StringVar()
        self.sleep_progress_display = ctk.StringVar() 

        # quick stats
        self.exercise_total_var = ctk.StringVar(value=0)
        self.reps_total_var = ctk.StringVar(value=0)
        self.volume_total_var = ctk.StringVar(value=0)
        self.sets_total_var = ctk.StringVar(value=0)

        self.location_var = ctk.StringVar(value="Forecast Unavailable")
        self.last_updated_var = ctk.StringVar()
        self.temp_var = ctk.StringVar()
        self.weather_type_var = ctk.StringVar()

        # recent exercises section related variables
        style = btk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=28, borderwidth=2, font=("", 12))
        style.configure("Treeview.Heading", background="#d6c6f4", font=("", 14, "bold"))
        style.map('Treeview', background=[('selected', '#b799e3')])

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

        self.update_welcome_user()
        self.update_monthly_goal_progression_displays()
        self.daily_section_initialisation()
        self.update_exercise_summary()
        self.update_weather_forecast()

    def create_widgets(self):
        #region [Parent Frames]
        navbar = Navbar(self, self.controller)
        content = ctk.CTkScrollableFrame(self, corner_radius=0)
        
        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(7, weight=1)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)

        intro_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1300, height=100)
        profile_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1300, height=550)
        subtitle_section = ctk.CTkFrame(content, fg_color="transparent", width=1100, height=80)
        dailies_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1300, height=400)
        quick_stats_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1300, height=400)
        recent_exercises_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1300, height=800)

        intro_section.grid(row=1, column=1, pady=20)
        profile_section.grid(row=2, column=1, pady=(0, 20))
        subtitle_section.grid(row=3, column=1, pady=(0, 20))
        dailies_section.grid(row=4, column=1, pady=(0, 20))
        quick_stats_section.grid(row=5, column=1)
        recent_exercises_section.grid(row=6, column=1, pady=20)

        quick_stats_section.grid_propagate(False)

        profile_section.grid_rowconfigure(0, weight=1)
        profile_section.grid_rowconfigure(2, weight=1)
        profile_section.grid_columnconfigure(0, weight=1)
        profile_section.grid_columnconfigure(4, weight=1)

        subtitle_section.grid_rowconfigure(0, weight=1)
        subtitle_section.grid_columnconfigure(0, weight=1)

        dailies_section.grid_rowconfigure(0, weight=1)
        dailies_section.grid_rowconfigure(2, weight=1)
        dailies_section.grid_columnconfigure(0, weight=1)
        dailies_section.grid_columnconfigure(4, weight=1)

        quick_stats_section.grid_rowconfigure(0, weight=1)
        quick_stats_section.grid_rowconfigure(2, weight=1)
        quick_stats_section.grid_columnconfigure(0, weight=1)
        quick_stats_section.grid_columnconfigure(3, weight=1)

        recent_exercises_section.grid_rowconfigure(0, weight=1)
        recent_exercises_section.grid_rowconfigure(4, weight=1)
        recent_exercises_section.grid_columnconfigure(0, weight=1)
        recent_exercises_section.grid_columnconfigure(6, weight=1)
        #endregion

        #region [ Introduction Section ]
        hello_message = ctk.CTkLabel(intro_section, textvariable=self.welcome_message, width=750, anchor="w", font=("", 32))
        motivational_message_display = ctk.CTkLabel(intro_section, textvariable=self.motivational_message, width=750, anchor="w", font=("", 18, "italic"))
        current_date = ctk.CTkLabel(intro_section, textvariable=self.today_full_display, font=("", 24))
        date_icon = ctk.CTkLabel(intro_section, text="", image=self.intro_icon)
        motivation_icon = ctk.CTkLabel(intro_section, text="", image=self.motivation_icon)

        hello_message.grid(row=0, column=0, sticky="w", padx=(50, 0), pady=(20, 0))
        motivational_message_display.grid(row=1, column=0, sticky="w", padx=(50, 0))
        current_date.grid(row=0, rowspan=2, column=1, sticky="e", padx=(100, 0), pady=(20, 0))
        date_icon.grid(row=0, rowspan=2, column=2, sticky="e", padx=(20, 0), pady=(20, 0))
        motivation_icon.grid(row=0, rowspan=2, column=3, sticky="e", padx=(30, 0), pady=(20, 0))

        intro_section.grid_propagate(False)

        motivation_icon.bind("<Button-1>", self.random_motivational_quote)

        #endregion

        #region [ Profile Section ]

        # user info
        profile_info_section = ctk.CTkFrame(profile_section, fg_color="transparent")
        self.profile_image_display = ctk.CTkLabel(profile_info_section, text="", image=self.profile_image)
        profile_name = ctk.CTkLabel(profile_info_section, textvariable=self.profile_name_display, wraplength=300, font=("", 24))
        profile_height_title = ctk.CTkLabel(profile_info_section, text="Height (cm)", font=("", 14, "bold"))
        profile_height_frame = ctk.CTkFrame(profile_info_section, border_width=3, border_color="#B19CD9", corner_radius=15, width=150, height=50)
        profile_height_display = ctk.CTkLabel(profile_height_frame, textvariable=self.profile_height_var, font=("", 24))
        profile_current_weight_title = ctk.CTkLabel(profile_info_section, text="Current Weight (kg)", font=("", 14, "bold"))
        profile_current_weight_frame = ctk.CTkFrame(profile_info_section, border_width=3, border_color="#B19CD9", corner_radius=15, width=150, height=50)
        profile_current_weight_display = ctk.CTkLabel(profile_current_weight_frame, textvariable=self.profile_current_weight_var, font=("", 24))
        profile_age_title = ctk.CTkLabel(profile_info_section, text="Age (years)", font=("", 14, "bold"))
        profile_age_frame = ctk.CTkFrame(profile_info_section, border_width=3, border_color="#B19CD9", corner_radius=15, width=150, height=50)
        profile_age_display = ctk.CTkLabel(profile_age_frame, textvariable=self.profile_age_var, font=("", 24))
        profile_goal_weight_title = ctk.CTkLabel(profile_info_section, text="Goal Weight (kg)", font=("", 14, "bold"))
        profile_goal_weight_frame = ctk.CTkFrame(profile_info_section, border_width=3, border_color="#B19CD9", corner_radius=15, width=150, height=50)
        profile_goal_weight_display = ctk.CTkLabel(profile_goal_weight_frame, textvariable=self.profile_goal_weight_var, font=("", 24))
        
        # monthly progresssion insight
        profile_monthly_section = ctk.CTkFrame(profile_section, border_color="blue", fg_color="transparent")
        profile_monthly_title = ctk.CTkLabel(profile_monthly_section, text="Monthly Progress", font=("", 32))
        profile_monthly_weight_info = ctk.CTkLabel(profile_monthly_section, textvariable=self.monthly_weight_choice_display, font=("", 24))
        profile_sleep_title = ctk.CTkLabel(profile_monthly_section, text="Sleep", font=("", 18))
        profile_sleep_info = ctk.CTkLabel(profile_monthly_section, textvariable=self.monthly_sleep_display, font=("", 14))
        self.profile_sleep_progressbar = ctk.CTkProgressBar(profile_monthly_section, border_width=3, height=40, width=400, corner_radius=0)
        profile_hydration_title = ctk.CTkLabel(profile_monthly_section, text="Hydration", font=("", 18)) 
        profile_hydration_info = ctk.CTkLabel(profile_monthly_section, textvariable=self.monthly_hydration_display, font=("", 14))
        self.profile_hydration_progressbar = ctk.CTkProgressBar(profile_monthly_section, border_width=3, height=40, width=400, corner_radius=0)
        profile_walking_title = ctk.CTkLabel(profile_monthly_section, text="Walking", font=("", 18))
        profile_walking_info = ctk.CTkLabel(profile_monthly_section, textvariable=self.monthly_walking_display, font=("", 14))
        self.profile_walking_progressbar = ctk.CTkProgressBar(profile_monthly_section, border_width=3, height=40, width=400, corner_radius=0)
        
        # latest achievement showcase
        profile_achievements_section = ctk.CTkFrame(profile_section, fg_color="transparent")
        profile_achievements_title = ctk.CTkLabel(profile_achievements_section, text="Recent Achievements", font=("", 32))
        first_badge_name = ctk.CTkLabel(profile_achievements_section, text="Running Madman", font=("", 18))
        first_badge_spot = ctk.CTkLabel(profile_achievements_section, text="", image=self.badge)
        first_badge_date = ctk.CTkLabel(profile_achievements_section, text="Unlocked:\n16/06/2025", font=("", 12, "bold"))
        second_badge_name = ctk.CTkLabel(profile_achievements_section, text="First Workout", font=("", 18))
        second_badge_spot = ctk.CTkLabel(profile_achievements_section, text="", image=self.badge)
        second_badge_date = ctk.CTkLabel(profile_achievements_section, text="Unlocked:\n16/06/2025", font=("", 12, "bold"))
        third_badge_name = ctk.CTkLabel(profile_achievements_section, text="First Exercise", font=("", 18))
        third_badge_spot = ctk.CTkLabel(profile_achievements_section, text="", image=self.badge)
        third_badge_date = ctk.CTkLabel(profile_achievements_section, text="Unlocked:\n16/06/2025", font=("", 12, "bold"))
        fourth_badge_name = ctk.CTkLabel(profile_achievements_section, text="Ten Exercises", font=("", 18))
        fourth_badge_spot = ctk.CTkLabel(profile_achievements_section, text="", image=self.badge)
        fourth_badge_date = ctk.CTkLabel(profile_achievements_section, text="Unlocked:\n16/06/2025", font=("", 12, "bold"))

        # main frames inside profile section
        profile_info_section.grid(row=1, column=1, padx=(10, 60), pady=(0, 20))
        profile_monthly_section.grid(row=1, column=2, padx=(0, 50), pady=(0, 30))
        profile_achievements_section.grid(row=1, column=3, padx=(0, 40), pady=(0, 20))
        
        # profile info section
        self.profile_image_display.grid(row=0, column=0, columnspan=2, pady=(20, 0))
        profile_name.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        profile_height_title.grid(row=2, column=0, padx=(0, 10), pady=(20, 0))
        profile_height_frame.grid(row=3, column=0, padx=20, pady=(0, 20))
        profile_height_frame.grid_propagate(False)
        profile_height_frame.grid_rowconfigure(0, weight=1)
        profile_height_frame.grid_columnconfigure(0, weight=1)
        profile_height_display.grid(row=0, column=0, padx=10, pady=10)
        profile_current_weight_title.grid(row=2, column=1, padx=(0, 10),  pady=(20, 0))
        profile_current_weight_frame.grid(row=3, column=1, pady=(0, 20))
        profile_current_weight_frame.grid_propagate(False)
        profile_current_weight_frame.grid_rowconfigure(0, weight=1)
        profile_current_weight_frame.grid_columnconfigure(0, weight=1)
        profile_current_weight_display.grid(row=0, column=0, padx=10, pady=10)
        
        profile_age_title.grid(row=4, column=0, padx=(0, 10),  pady=(10, 0))
        profile_age_frame.grid(row=5, column=0, padx=20, pady=(0, 20))
        profile_age_frame.grid_propagate(False)
        profile_age_frame.grid_rowconfigure(0, weight=1)
        profile_age_frame.grid_columnconfigure(0, weight=1)
        profile_age_display.grid(row=0, column=0, padx=10, pady=10)
        profile_goal_weight_title.grid(row=4, column=1, padx=(0, 10), pady=(10, 0))
        profile_goal_weight_frame.grid(row=5, column=1, pady=(0, 20))
        profile_goal_weight_frame.grid_propagate(False)
        profile_goal_weight_frame.grid_rowconfigure(0, weight=1)
        profile_goal_weight_frame.grid_columnconfigure(0, weight=1)
        profile_goal_weight_display.grid(row=0, column=0, padx=10, pady=10)

        # profile monthly section
        profile_monthly_title.grid(row=0, column=0, columnspan=2, pady=20)
        profile_monthly_weight_info.grid(row=1, rowspan=2, column=0, pady=(10, 0), sticky="w")
        profile_sleep_title.grid(row=3, column=0, pady=(20, 0), sticky="w")
        profile_sleep_info.grid(row=3, column=1, pady=(20, 0), sticky="e")
        self.profile_sleep_progressbar.grid(row=4, column=0, columnspan=2)
        profile_hydration_title.grid(row=5, column=0, pady=(20, 0), sticky="w")
        profile_hydration_info.grid(row=5, column=1, pady=(20, 0), sticky="e")
        self.profile_hydration_progressbar.grid(row=6, column=0, columnspan=2)
        profile_walking_title.grid(row=7, column=0, pady=(20, 0), sticky="w")
        profile_walking_info.grid(row=7, column=1, pady=(20, 0), sticky="e")
        self.profile_walking_progressbar.grid(row=8, column=0, columnspan=2)

        # profile achievements section
        profile_achievements_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 60))
        first_badge_name.grid(row=1, column=0, padx=10)
        first_badge_spot.grid(row=2, column=0, padx=10)
        first_badge_date.grid(row=3, column=0, pady=(0, 40))
        second_badge_name.grid(row=1, column=1, padx=(0, 10))
        second_badge_spot.grid(row=2, column=1, padx=(0, 10))
        second_badge_date.grid(row=3, column=1, pady=(0, 40))
        third_badge_name.grid(row=4, column=0, padx=10)
        third_badge_spot.grid(row=5, column=0, padx=10)
        third_badge_date.grid(row=6, column=0, pady=(0, 20))
        fourth_badge_name.grid(row=4, column=1, padx=(0, 10))
        fourth_badge_spot.grid(row=5, column=1, padx=(0, 10))
        fourth_badge_date.grid(row=6, column=1, pady=(0, 20))

        profile_section.grid_propagate(False)
        # endregion

        #region [ Subtitle Section ]
        subtitle_display = ctk.CTkLabel(subtitle_section, text="Daily Tracking", font=("", 32))

        subtitle_display.grid(row=0, column=0, padx=(10, 0), sticky="sw")

        subtitle_section.grid_propagate(False)
        #endregion

        #region [ Dailies Section ] 
        sleep_section = ctk.CTkFrame(dailies_section, border_width=5, border_color="#B19CD9")
        hydration_section = ctk.CTkFrame(dailies_section, border_width=5, border_color="#B19CD9")
        walking_section = ctk.CTkFrame(dailies_section, border_width=5, border_color="#B19CD9")

        sleep_section.grid(row=1, column=1, padx=20)
        hydration_section.grid(row=1, column=2)
        walking_section.grid(row=1, column=3, padx=20)

        # sleep section
        total_hours_slept = ctk.CTkLabel(sleep_section, textvariable=self.sleep_display, font=("", 24))
        sleep_icon_reset_frame = ctk.CTkFrame(sleep_section, fg_color="transparent")
        self.sleep_icon_display = ctk.CTkLabel(sleep_icon_reset_frame, text="", image=self.sleep_icon)
        sleep_reset = ctk.CTkLabel(sleep_icon_reset_frame, text="", image=self.reset_icon)
        sleep_title = ctk.CTkLabel(sleep_section, text="Sleep", font=("", 14))
        sleep_goal_tally = ctk.CTkLabel(sleep_section, textvariable=self.sleep_progress_display, font=("", 14))
        self.sleep_progressbar = ctk.CTkProgressBar(sleep_section, border_width=3, height=40, width=300, corner_radius=0)
        sleep_hours_entry = ctk.CTkEntry(sleep_section, textvariable=self.sleep_var, width=140, height=60, font=("", 24))
        sleep_add_hours = ctk.CTkButton(sleep_section, width=140, height=60, text="Add Minutes", font=("", 18), command=self.process_sleep_entry)

        total_hours_slept.grid(row=0, column=0, padx=(40, 0), pady=(40, 0), sticky="sw")
        sleep_icon_reset_frame.grid(row=0, column=1, padx=(0, 40), pady=(40, 0), sticky="e")
        self.sleep_icon_display.grid(row=0, column=0, padx=(0, 20))
        sleep_reset.grid(row=0, column=1)
        sleep_title.grid(row=1, column=0, columnspan=2, padx=(40, 0), sticky="nw")
        sleep_goal_tally.grid(row=2, column=1, padx=(0, 40), sticky="se")
        self.sleep_progressbar.grid(row=3, column=0, padx=40, columnspan=2)
        sleep_hours_entry.grid(row=4, column=0, padx=(40, 0), pady=(20, 40))
        sleep_add_hours.grid(row=4, column=1, padx=(0, 40), pady=(20, 40))

        sleep_hours_entry.bind("<Key>", lambda event: custom_float_only_validation(event, sleep_hours_entry, 3))
        sleep_reset.bind("<Button-1>", lambda event: self.reset_daily(event, "sleep"))

        # hydration section
        total_ml_drunk = ctk.CTkLabel(hydration_section, textvariable=self.hydration_display, font=("", 24))
        hydration_icon_reset_frame = ctk.CTkFrame(hydration_section, fg_color="transparent")
        self.hydration_icon_display = ctk.CTkLabel(hydration_icon_reset_frame, text="", image=self.hydration_icon)
        hydration_reset = ctk.CTkLabel(hydration_icon_reset_frame, text="", image=self.reset_icon)
        hydration_title = ctk.CTkLabel(hydration_section, text="Hydration", font=("", 14))
        hydration_goal_tally = ctk.CTkLabel(hydration_section, textvariable=self.hydration_progress_display, font=("", 14))
        self.hydration_progressbar = ctk.CTkProgressBar(hydration_section, border_width=3, height=40, width=300, corner_radius=0)
        hydration_ml_entry = ctk.CTkEntry(hydration_section, textvariable=self.hydration_var, width=140, height=60, font=("", 24))
        hydration_add_ml = ctk.CTkButton(hydration_section, width=140, height=60, text="Add Mililitres", font=("", 18), command=self.process_hydration_entry)

        total_ml_drunk.grid(row=0, column=0, padx=(40, 0), pady=(40, 0), sticky="sw")
        hydration_icon_reset_frame.grid(row=0, column=1, padx=(0, 40), pady=(40, 0), sticky="e")
        self.hydration_icon_display.grid(row=0, column=0, padx=(0, 20))
        hydration_reset.grid(row=0, column=1)
        hydration_title.grid(row=1, column=0, columnspan=2, padx=(40, 0), sticky="nw")
        hydration_goal_tally.grid(row=2, column=1, padx=(0, 40), sticky="se")
        self.hydration_progressbar.grid(row=3, column=0, padx=40, columnspan=2)
        hydration_ml_entry.grid(row=4, column=0, padx=(40, 0), pady=(20, 40))
        hydration_add_ml.grid(row=4, column=1, padx=(0, 40), pady=(20, 40))

        hydration_ml_entry.bind("<Key>", lambda event: custom_float_only_validation(event, hydration_ml_entry, 4))
        hydration_reset.bind("<Button-1>", lambda event: self.reset_daily(event, "hydration"))

        # walking section
        total_steps_walked = ctk.CTkLabel(walking_section, textvariable=self.steps_display, font=("", 24))
        walking_icon_reset_frame = ctk.CTkFrame(walking_section, fg_color="transparent")
        self.walking_icon_display = ctk.CTkLabel(walking_icon_reset_frame, text="", image=self.walking_icon)
        walking_reset = ctk.CTkLabel(walking_icon_reset_frame, text="", image=self.reset_icon)
        walking_title = ctk.CTkLabel(walking_section, text="Walking", font=("", 14))
        walking_goal_tally = ctk.CTkLabel(walking_section, textvariable=self.steps_progress_display, font=("", 14))
        self.walking_progressbar = ctk.CTkProgressBar(walking_section, border_width=3, height=40, width=300, corner_radius=0)
        walking_steps_entry = ctk.CTkEntry(walking_section, textvariable=self.steps_var, width=140, height=60, font=("", 24))
        walking_add_steps = ctk.CTkButton(walking_section, width=140, height=60, text="Add Steps", font=("", 18), command=self.process_steps_entry)

        total_steps_walked.grid(row=0, column=0, padx=(40, 0), pady=(40, 0), sticky="sw")
        walking_icon_reset_frame.grid(row=0, column=1, padx=(0, 40), pady=(40, 0), sticky="e")
        self.walking_icon_display.grid(row=0, column=0, padx=(0, 20))
        walking_reset.grid(row=0, column=1)
        walking_title.grid(row=1, column=0, columnspan=2, padx=(40, 0), sticky="nw")
        walking_goal_tally.grid(row=2, column=1, padx=(0, 40), sticky="se")
        self.walking_progressbar.grid(row=3, column=0, padx=40, columnspan=2)
        walking_steps_entry.grid(row=4, column=0, padx=(40, 0), pady=(20, 40))
        walking_add_steps.grid(row=4, column=1, padx=(0, 40), pady=(20, 40))

        walking_steps_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, walking_steps_entry, 5))
        walking_reset.bind("<Button-1>", lambda event: self.reset_daily(event, "walking"))

        dailies_section.grid_propagate(False)

        #endregion

        #region [ Quick Stats Section ]

        exercise_summary = ctk.CTkFrame(quick_stats_section, border_width=5, border_color="#B19CD9")
        daily_forecast = ctk.CTkFrame(quick_stats_section, border_width=5, border_color="#B19CD9")

        exercise_summary.grid(row=1, column=1, padx=(0, 20))
        exercise_summary.grid_columnconfigure(0, minsize=40)
        exercise_summary.grid_columnconfigure(3, minsize=40)

        daily_forecast.grid(row=1, column=2)
        daily_forecast.grid_columnconfigure(0, minsize=40)
        daily_forecast.grid_columnconfigure(3, minsize=40)

        #region [Exercise Summary]
        # exercise summary [prefix: des_ short for dashboard exercise summary]
        des_title = ctk.CTkLabel(exercise_summary, text="Exercise Summary", font=("", 18)) # row0col0
        des_banner = ctk.CTkLabel(exercise_summary, text="", image=self.summary_icon) # row0col2-3
        
        des_subtitle_frame = ctk.CTkFrame(exercise_summary, fg_color="transparent") # row1col1-2
        des_today_icon_left = ctk.CTkLabel(des_subtitle_frame, text="", image=self.fireball_icon) # row0col0
        des_today_title = ctk.CTkLabel(des_subtitle_frame, text="Today", font=("", 32, "bold")) #row0col1
        des_today_icon_right = ctk.CTkLabel(des_subtitle_frame, text="", image=self.fireball_icon)
        
        des_total_exercises_frame = ctk.CTkFrame(exercise_summary, width=250, height=30, fg_color="transparent") #row2col1
        des_total_exercise_title = ctk.CTkLabel(des_total_exercises_frame, text="Total Exercises:", font=("", 24)) #row0col0
        des_total_exercise_sum = ctk.CTkLabel(des_total_exercises_frame, textvariable=self.exercise_total_var, font=("", 24, "bold")) #row0col1
        
        des_total_reps_frame = ctk.CTkFrame(exercise_summary, width=250, height=30, fg_color="transparent") #row2col2
        des_total_reps_title = ctk.CTkLabel(des_total_reps_frame, text="Total Reps:", font=("", 24)) #row0col0
        des_total_reps_sum = ctk.CTkLabel(des_total_reps_frame, textvariable=self.reps_total_var, font=("", 24, "bold")) #row0col1
        
        des_total_volume_frame = ctk.CTkFrame(exercise_summary, width=250, height=30, fg_color="transparent") #row3col1
        des_total_volume_title = ctk.CTkLabel(des_total_volume_frame, text="Total Volume:", font=("", 24)) #row0col0
        des_total_volume_sum = ctk.CTkLabel(des_total_volume_frame, textvariable=self.volume_total_var, font=("", 24, "bold")) #row0col1
        
        des_total_sets_frame = ctk.CTkFrame(exercise_summary, width=250, height=30, fg_color="transparent") #row3col2
        des_total_sets_title = ctk.CTkLabel(des_total_sets_frame, text="Total Sets:", font=("", 24)) #row0col0
        des_total_sets_sum = ctk.CTkLabel(des_total_sets_frame, textvariable=self.sets_total_var, font=("", 24, "bold")) #row0col1

        des_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=(40, 0), pady=20)
        des_banner.grid(row=0, column=2, columnspan=2, padx=(80, 0), pady=20)
        
        des_subtitle_frame.grid(row=1, column=1, columnspan=2, pady=(0, 40))
        des_today_icon_left.grid(row=0, column=0, padx=(0, 20))
        des_today_title.grid(row=0, column=1)
        des_today_icon_right.grid(row=0, column=2, padx=(20, 0))

        des_total_exercises_frame.grid(row=2, column=1, padx=(0, 40), pady=(0, 40), sticky="w")
        des_total_exercises_frame.grid_propagate(False)
        des_total_exercises_frame.grid_columnconfigure(1, weight=1)
        des_total_exercise_title.grid(row=0, column=0, sticky="w")
        des_total_exercise_sum.grid(row=0, column=1, sticky="e")

        des_total_reps_frame.grid(row=2, column=2, padx=(40, 0), pady=(0, 40), sticky="w")
        des_total_reps_frame.grid_propagate(False)
        des_total_reps_frame.grid_columnconfigure(1, weight=1)
        des_total_reps_title.grid(row=0, column=0, sticky="w")
        des_total_reps_sum.grid(row=0, column=1, sticky="e")

        des_total_volume_frame.grid(row=3, column=1, padx=(0, 40), pady=(0, 40), sticky="w")
        des_total_volume_frame.grid_propagate(False)
        des_total_volume_frame.grid_columnconfigure(1, weight=1)
        des_total_volume_title.grid(row=0, column=0, sticky="w")
        des_total_volume_sum.grid(row=0, column=1, sticky="e")

        des_total_sets_frame.grid(row=3, column=2, padx=(40, 0), pady=(0, 40), sticky="w")
        des_total_sets_frame.grid_propagate(False)
        des_total_sets_frame.grid_columnconfigure(1, weight=1)
        des_total_sets_title.grid(row=0, column=0, sticky="w")
        des_total_sets_sum.grid(row=0, column=1, sticky="e")
        #endregion

        #region [Weather Forecast]
        # weather forecast [prefix: ddf_ short for dashboard daily forecast]
        ddf_title = ctk.CTkLabel(daily_forecast, text="Daily Forecast", font=("", 18))
        ddf_weather_general_display = ctk.CTkLabel(daily_forecast, text="", image=self.weather_section_icon)

        ddf_location_display = ctk.CTkLabel(daily_forecast, textvariable=self.location_var, font=("", 32, "bold"))
        ddf_weather_display = ctk.CTkLabel(daily_forecast, text="", image=self.weather_icon)
        
        ddf_temp_weather_frame = ctk.CTkFrame(daily_forecast, fg_color="transparent", width=200, height=30)
        ddf_temp_display = ctk.CTkLabel(ddf_temp_weather_frame, textvariable=self.temp_var, font=("", 24))
        ddf_weather_type_display = ctk.CTkLabel(ddf_temp_weather_frame, textvariable=self.weather_type_var, font=("", 24))

        ddf_last_update_display = ctk.CTkLabel(daily_forecast, textvariable=self.last_updated_var, font=("", 18))
        
        ddf_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=(40, 0), pady=(30, 20))
        ddf_weather_general_display.grid(row=0, column=2, padx=(80, 0), pady=(30, 20))

        ddf_location_display.grid(row=1, column=1, padx=(0, 30), pady=(10, 20), sticky="w")
        ddf_weather_display.grid(row=1, column=2, pady=(10, 20))

        ddf_temp_weather_frame.grid(row=2, column=1, columnspan=2, sticky="w")
        ddf_temp_weather_frame.grid_propagate(False)
        ddf_temp_weather_frame.grid_columnconfigure(1, weight=1)
        ddf_temp_display.grid(row=0, column=0, padx=(0, 30), sticky="w")
        ddf_weather_type_display.grid(row=0, column=1, sticky="e")

        ddf_last_update_display.grid(row=3, column=1, columnspan=2, sticky="w", pady=(0, 65))
        #endregion 

        #endregion

        #region [ Recent Exercises Section ]
        redirect_session_entry_icon = ctk.CTkLabel(recent_exercises_section, text="", image=self.session_entry_icon)
        recent_exercises_title = ctk.CTkLabel(recent_exercises_section, text="Latest Exercise Entries", font=("", 32))
        redirect_single_entry_icon = ctk.CTkLabel(recent_exercises_section, text="", image=self.single_entry_icon)
        entries_frame = ctk.CTkFrame(recent_exercises_section, fg_color="transparent", border_width=0, width=1150, height=550)
        self.entries = btk.Treeview(entries_frame, columns=("exercise", "date", "time", "summary", "label"), show="headings", height=18, selectmode="browse")
        self.entries.heading("exercise", text="Exercise")
        self.entries.heading("date", text="Date")
        self.entries.heading("time", text="Time")
        self.entries.heading("summary", text="Sets x Reps @ Weight")
        self.entries.heading("label", text="Label")
        self.entries.column("exercise", width=330, minwidth=330, anchor="w", stretch=False)
        self.entries.column("date", width=100, minwidth=100, anchor="center", stretch=False)
        self.entries.column("time", width=100, minwidth=100, anchor="center", stretch=False)
        self.entries.column("summary", width=250, minwidth=250, anchor="center", stretch=False)
        self.entries.column("label", width=330, minwidth=330, anchor="w", stretch=False)
        # create tags for zebra design
        self.entries.tag_configure('oddrow', background='#f2f2f2')
        self.entries.tag_configure('evenrow', background='#ffffff')
        entries_buttons_frame = ctk.CTkFrame(recent_exercises_section, fg_color="transparent", border_width=0)
        add_session = ctk.CTkButton(entries_buttons_frame, text="Add a Session", width=140, height=60, font=("", 18), command=lambda: self.controller.show_page("SessionEntryPage"))
        add_single = ctk.CTkButton(entries_buttons_frame, text="Add an Exercise", width=140, height=60, font=("", 18), command=lambda: self.controller.show_page("SingleEntryPage"))

        redirect_session_entry_icon.grid(row=1, column=1, columnspan=2, pady=20)
        recent_exercises_title.grid(row=1, column=3, pady=20)
        redirect_single_entry_icon.grid(row=1, column=4, columnspan=2, pady=20)
        entries_frame.grid(row=2, column=1, columnspan=5, padx=10, pady=(0,10))
        entries_frame.grid_propagate(False)
        entries_frame.grid_rowconfigure(0, weight=1)
        entries_frame.grid_columnconfigure(0, weight=1)
        self.entries.grid(row=0, column=0)
        entries_buttons_frame.grid(row=3, column=1, columnspan=5, padx=10)
        add_session.grid(row=3, column=2, padx=(0, 40), pady=20)
        add_single.grid(row=3, column=4, padx=(40, 0), pady=20)

        recent_exercises_section.grid_propagate(False)

        redirect_session_entry_icon.bind("<Button-1>", lambda event: self.controller.show_page("SessionEntryPage"))
        redirect_single_entry_icon.bind("<Button-1>", lambda event: self.controller.show_page("SingleEntryPage"))
        #endregion

    # Reminder to adjust after finishing all widgets... 
    # coding ettiquette -> make sure all frames/configures are all placed in the same positioning/order throughout.
    # remember to implement binding for the actionable icons like -> reset icon

    def update_welcome_user(self):
        username = self.controller.username.get()
        self.welcome_message.set(f"Welcome Back, {username}")

    # deliver randomised yet inspiring quotes to the user
    def random_motivational_quote(self, event=None):
        motivational_quotes = [
            '"Sometimes, carrying on, just carrying on, is the superhuman achievement." - Albert C.',
            '"You can, you should, and if you are brave enough to start, you will." - Stephen K.',
            '"The only person who can stop you from reaching your goals is you." - Jackie J. K.',
            '"All progress takes place outside the comfort zone." - Michael J. B.',
            '"Stay Healthy and Keep Moving." - Anon M.',
            '"Take care of your body, It is the one place you have to live." - Jim R.',
            '"No matter how hard or impossible it is, never lose sight of your goal." - Monkey D. L.',
            '"I do not fear this new challenge, rather like a true warrior I will rise to meet it" - Vegeta IV.',
            '"Hard work. Because nothing is greater short-cut than hard work." - Coach K.'
        ]
        self.motivational_message.set(random.choice(motivational_quotes))

    def update_dashboard_profile_image(self):
        # reloads both the image widget and image attribute by re-reading the file with the new image
        self.profile_image = ctk.CTkImage(light_image=Image.open("img/user_profile.png"), dark_image=Image.open("img/user_profile.png"), size=(192, 192))
        self.profile_image_display.configure(image=self.profile_image)

    def retrieve_profile_details(self):
        profile_info = [
            self.profile_first_name_var,
            self.profile_last_name_var,
            self.profile_age_var,
            self.profile_height_var,
            self.profile_current_weight_var,
            self.profile_goal_weight_var
        ]
        retrieve_profile_data = """
        SELECT
            first_name,
            last_name,
            age,
            height,
            current_weight,
            goal_weight
        FROM profile_details
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(retrieve_profile_data)
        result = self.controller.db_cursor.fetchone()
        if result:
            for i in range(len(result)):
                profile_info[i].set(result[i])
            self.determine_name_display()
        
    # if there is a first name or full name (first & last) given, then display that over username
    def determine_name_display(self):
        first_name = self.profile_first_name_var.get()
        last_name = self.profile_last_name_var.get()

        if len(first_name) > 0 and len(last_name) > 0:
            self.profile_name_display.set(f"{first_name} {last_name}")
        elif len(first_name) > 0:
            self.profile_name_display.set(first_name)
        elif len(last_name) > 0:
            self.profile_name_display.set(last_name)
        else:
            self.profile_name_display.set(self.controller.username.get())
    
    # update monthly weight loss/gain goal 
    def update_monthly_goal_weight(self, goal_type, new_weight_value):
        self.monthly_weight_choice_display.set(f"Weight {goal_type} Goal: {new_weight_value} kg")

    # retrieve, sum and set total sleep value for current month
    def update_sum_monthly_sleep_minutes(self):
        total_sleep = 0.0
        current_month = self.controller.current_month
        current_year = self.controller.current_year
        self.controller.db_cursor.execute("SELECT sleep_mins FROM sleep_tracker WHERE date LIKE ?", (f'__-{current_month}-{current_year}',))
        results = self.controller.db_cursor.fetchall()
        if results:
            for i in results:
                total_sleep += i[0]
        self.monthly_sleep_current_var.set(total_sleep)

    def update_sum_monthly_walking_steps(self):
        total_steps = 0
        current_month = self.controller.current_month
        current_year = self.controller.current_year
        self.controller.db_cursor.execute("SELECT steps_taken FROM steps_tracker WHERE date LIKE ?", (f'__-{current_month}-{current_year}',))
        results = self.controller.db_cursor.fetchall()
        if results:
            for i in results:
                total_steps += i[0]
        self.monthly_walking_current_var.set(total_steps)

    def update_sum_monthly_hydration_consumption(self):
        total_consumption = 0.0
        current_month = self.controller.current_month
        current_year = self.controller.current_year
        self.controller.db_cursor.execute("SELECT consumption_ml FROM hydration_tracker WHERE date LIKE ?", (f'__-{current_month}-{current_year}',))
        results = self.controller.db_cursor.fetchall()
        if results:
            for i in results:
                total_consumption += i[0]
        self.monthly_hydration_current_var.set(total_consumption)

    # NOTE TO SELF!! NEED TO STILL IMPLEMENT FOR STEPS AND HYDRATION + ADD THIS AND MAYBE THE UPDATE_MONTHLY_PROGRESSBARS() TO PLACES LIKE SETTINGS AND DAILY TRACKERS FOR REAL TIME UPDATES.
    def update_monthly_goal_progression_displays(self):
        # for now just sleep
        monthly_sleep_goal = 0.0
        monthly_walking_goal = 0
        monthly_hydration_goal = 0.0

        self.controller.db_cursor.execute("SELECT monthly_sleep_goal, monthly_steps_goal, monthly_hydration_goal FROM profile_details WHERE rowid = 1")
        results = self.controller.db_cursor.fetchone()

        if results:
            monthly_sleep_goal, monthly_walking_goal, monthly_hydration_goal = results
        
        # get the latest set value for monthly goals (total goal value)
        self.monthly_sleep_goal_var.set(monthly_sleep_goal)
        self.monthly_walking_goal_var.set(monthly_walking_goal)
        self.monthly_hydration_goal_var.set(monthly_hydration_goal)

        # get latest calculated sum value for current progress on the monthly (current value tallied so far)
        self.update_sum_monthly_sleep_minutes()
        self.update_sum_monthly_walking_steps()
        self.update_sum_monthly_hydration_consumption()

        # update the monthly progress bar's tally info 
        self.monthly_sleep_display.set(f"{self.monthly_sleep_current_var.get()} / {self.monthly_sleep_goal_var.get()}")
        self.monthly_walking_display.set(f"{self.monthly_walking_current_var.get()} / {self.monthly_walking_goal_var.get()}")
        self.monthly_hydration_display.set(f"{self.monthly_hydration_current_var.get()} / {self.monthly_hydration_goal_var.get()}")

        # update the monthly progress bars
        self.update_monthly_sleep_progressbar()
        self.update_monthly_steps_progressbar()
        self.update_monthly_hydration_progressbar()

    def update_monthly_steps_progressbar(self):
        walking_current_progress = int(self.monthly_walking_current_var.get())
        walking_total_progress = int(self.monthly_walking_goal_var.get())

        try:
            self.profile_walking_progressbar.set(walking_current_progress/walking_total_progress)
        except ZeroDivisionError:
            self.profile_walking_progressbar.set(0)

    def update_monthly_sleep_progressbar(self):
        sleep_current_progress = float(self.monthly_sleep_current_var.get())
        sleep_total_progress = float(self.monthly_sleep_goal_var.get())

        try:
            self.profile_sleep_progressbar.set(sleep_current_progress/sleep_total_progress)
        except ZeroDivisionError:
            self.profile_sleep_progressbar.set(0)

    def update_monthly_hydration_progressbar(self):
        hydration_current_progress = float(self.monthly_hydration_current_var.get())
        hydration_total_progress = float(self.monthly_hydration_goal_var.get())

        try:
            self.profile_hydration_progressbar.set(hydration_current_progress/hydration_total_progress)
        except ZeroDivisionError:
            self.profile_hydration_progressbar.set(0)

    def daily_section_initialisation(self):
        print("daily sec init")
        # [ Walking ]
        # check if a steps entry exists for today
        self.controller.db_cursor.execute("SELECT steps_taken FROM steps_tracker WHERE date = ?", (self.today,))
        result = self.controller.db_cursor.fetchone()
        # if so, use it to set the initial display upon app startup
        if result:
            steps_taken = result[0]
        else:
            steps_taken = 0
        self.steps_display.set(f"{steps_taken:,} steps")
        self.steps_current_progress.set(steps_taken)
        
        # [ Hydration ]
        # check if an entry exists for today
        self.controller.db_cursor.execute("SELECT consumption_ml FROM hydration_tracker WHERE date = ?", (self.today,))
        result = self.controller.db_cursor.fetchone()
        # if so, use it to set the initial display upon app startup
        if result:
            liquids_consumed = result[0]
        else:   
            liquids_consumed = 0.0 
        self.hydration_display.set(f"{liquids_consumed} ml")
        self.hydration_current_progress.set(liquids_consumed)

        # [ Sleep ]
        # check if an entry exists for today
        self.controller.db_cursor.execute("SELECT sleep_mins FROM sleep_tracker WHERE date = ?", (self.today,))
        result = self.controller.db_cursor.fetchone()
        # if so, use it to set the initial display upon app startup
        if result:
            minutes_slept = result[0]
        else:
            minutes_slept = 0.0
        self.sleep_display.set(f"{minutes_slept} mins")
        self.sleep_current_progress.set(minutes_slept)

        self.update_daily_goal_progression_displays()

    def update_daily_goal_progression_displays(self):
        steps_goal = 0
        sleep_goal = 0.0
        hydration_goal = 0.0

        self.controller.db_cursor.execute("SELECT daily_steps_goal, daily_sleep_goal, daily_hydration_goal FROM profile_details WHERE rowid=1")
        result = self.controller.db_cursor.fetchone()

        # set temp variables with the data retrieved from the profile_details database
        if result:
            steps_goal, sleep_goal, hydration_goal = result

        # set the latest daily progression data only if changes 
        self.steps_progress_display.set(f"{self.steps_current_progress.get()} / {steps_goal}")
        self.sleep_progress_display.set(f"{self.sleep_current_progress.get()} / {sleep_goal}")
        self.hydration_progress_display.set(f"{self.hydration_current_progress.get()} / {hydration_goal}")

        self.steps_goal.set(steps_goal)
        self.sleep_goal.set(sleep_goal)
        self.hydration_goal.set(hydration_goal)

        self.update_steps_progressbar()
        self.update_sleep_progressbar()
        self.update_hydration_progressbar()

    def update_steps_progressbar(self):
        current_progress = int(self.steps_current_progress.get())
        total_progress = int(self.steps_goal.get())
        try:
            self.walking_progressbar.set(current_progress/total_progress)
        except ZeroDivisionError:
            if current_progress > total_progress:
                self.walking_progressbar.set(1)
            else:
                self.walking_progressbar.set(0)

    def update_hydration_progressbar(self):
        current_progress = float(self.hydration_current_progress.get())
        total_progress = float(self.hydration_goal.get())
        try:
            self.hydration_progressbar.set(current_progress/total_progress)
        except ZeroDivisionError:
            if current_progress > total_progress:
                self.hydration_progressbar.set(1)
            else:
                self.hydration_progressbar.set(0)

    def update_sleep_progressbar(self):
        current_progress = float(self.sleep_current_progress.get())
        total_progress = float(self.sleep_goal.get())
        try:
            self.sleep_progressbar.set(current_progress/total_progress)
        except ZeroDivisionError:
            if current_progress > total_progress:
                self.sleep_progressbar.set(1)
            else:
                self.sleep_progressbar.set(0)

    def process_steps_entry(self):
        input_value = self.steps_var.get()
        if len(input_value) == 0:
            return
        steps = int(input_value)
        # check if any steps were inputted
        if steps < 1:
            # do nothing on button click
            return 
        # check if an entry exists for today
        self.controller.db_cursor.execute("SELECT exists (SELECT 1 FROM steps_tracker WHERE date = ?)", (self.today,))
        if not 1 in self.controller.db_cursor.fetchone():
            # during processing an entry, check if conditions meet to unlock the 'first steps" achievement
            self.controller.pages["AchievementsPage"].check_first_steps()
            # if none exists, create a new entry with the initially given steps
            self.controller.db_cursor.execute("INSERT INTO steps_tracker (date, steps_taken) VALUES (?, ?)", (self.today, steps))
            self.controller.db_connection.commit()
            # format and update the total steps taken display
            self.steps_display.set(f"{steps:,} steps")
            # update daily & monthly steps progression
            self.steps_current_progress.set(steps)
            self.update_daily_goal_progression_displays()
            # clear the steps entry field
            self.steps_var.set("")
        # update the already existing entry
        else:
            # find out how many steps have been already taken (prior to this new input)
            self.controller.db_cursor.execute("SELECT steps_taken FROM steps_tracker WHERE date = ?", (self.today,))
            # int var by default from sqlite
            steps_taken = self.controller.db_cursor.fetchone()[0]
            # steps_taken + steps (current input)
            steps_taken += steps
            # check if the tally is valid (aka humanly possible)
            if steps_taken > 99999:
                self.controller.db_cursor.execute("UPDATE steps_tracker SET steps_taken = ? WHERE date = ?", (99999, self.today))
                self.controller.db_connection.commit()
                # set to max num if tally is equal to over 99999
                steps_taken = 99999
            # update the entry with the new total steps taken
            else:
                self.controller.db_cursor.execute("UPDATE steps_tracker SET steps_taken = ? WHERE date = ?", (steps_taken, self.today))
                self.controller.db_connection.commit()
            # format and update the total steps taken display
            self.steps_display.set(f"{steps_taken:,} steps")
            # update daily steps progression
            self.steps_current_progress.set(steps_taken)
            self.update_daily_goal_progression_displays()
            # clear the steps entry field
            self.steps_var.set("")
        # during processing an entry, check if conditions meet to unlock the 'step stacker I" achievement
        self.controller.pages["AchievementsPage"].check_step_stacker_I()
        # during processing an entry, check if conditions meet to unlock the 'step stacker II" achievement
        self.controller.pages["AchievementsPage"].check_step_stacker_II()
        self.update_monthly_goal_progression_displays()

    def process_hydration_entry(self):
        input_value = self.hydration_var.get()
        # check if user entered nothing
        if len(input_value) == 0:
            return
        # in ml, round to 2 decimal places
        liquids_consumed = float(input_value)
        if liquids_consumed < 0.00:
            return
        # check if there is an existing entry for today
        self.controller.db_cursor.execute("SELECT exists (SELECT 1 FROM hydration_tracker WHERE date = ?)", (self.today,))
        if not 1 in self.controller.db_cursor.fetchone():
            # during processing an entry, check if conditions meet to unlock the 'first drink" achievement
            self.controller.pages["AchievementsPage"].check_first_drink()
            # check if the given value is over 9999.99 ml, if so default to max value
            if liquids_consumed > 9999.99:
                liquids_consumed = 9999.99
            # ensure liquids_consumed variable is always set to 2 decimal points
            liquids_consumed = round(liquids_consumed, 2)
            # create a new hydration entry
            self.controller.db_cursor.execute("INSERT INTO hydration_tracker (date, consumption_ml) VALUES (?, ?)", (self.today, liquids_consumed))
            self.controller.db_connection.commit()
            # update the app's real time display
            self.hydration_display.set(f"{liquids_consumed} ml")
            # update daily hydration progression
            self.hydration_current_progress.set(liquids_consumed)
            self.update_daily_goal_progression_displays()
            self.hydration_var.set("")
        else:
            # find out how much liquids (ml) is currently stored (prior to this new input)
            self.controller.db_cursor.execute("SELECT consumption_ml FROM hydration_tracker WHERE date = ?", (self.today,))
            total_liquids_consumed = self.controller.db_cursor.fetchone()[0]
            total_liquids_consumed += liquids_consumed
            if total_liquids_consumed > 9999.99:
                total_liquids_consumed = 9999.99
                # ensure liquids_consumed variable is always set to 2 decimal points
                total_liquids_consumed = round(total_liquids_consumed, 2)
                self.controller.db_cursor.execute("UPDATE hydration_tracker SET consumption_ml = ? WHERE date = ?", (total_liquids_consumed, self.today))
                self.controller.db_connection.commit()
                self.hydration_display.set(f"{total_liquids_consumed} ml")
                # update daily hydration progression
                self.hydration_current_progress.set(total_liquids_consumed)
                self.update_daily_goal_progression_displays()
                self.hydration_var.set("")
            else:
                # ensure liquids_consumed variable is always set to 2 decimal points
                total_liquids_consumed = round(total_liquids_consumed, 2)
                self.controller.db_cursor.execute("UPDATE hydration_tracker SET consumption_ml = ? WHERE date = ?", (total_liquids_consumed, self.today))
                self.controller.db_connection.commit()
                self.hydration_display.set(f"{total_liquids_consumed} ml")
                # update daily hydration progression
                self.hydration_current_progress.set(total_liquids_consumed)
                self.update_daily_goal_progression_displays()
                self.hydration_var.set("")
        # during processing an entry, check if conditions meet to unlock the 'hydrated human I" achievement
        self.controller.pages["AchievementsPage"].check_hydrated_human_I()
        # during processing an entry, check if conditions meet to unlock the 'hydrated human II" achievement
        self.controller.pages["AchievementsPage"].check_hydrated_human_II()
        self.update_monthly_goal_progression_displays()

    def process_sleep_entry(self):
        input_value = self.sleep_var.get()
        if len(input_value) == 0:
            return
        minutes_slept = float(input_value)
        if minutes_slept < 0.00:
            return
        self.controller.db_cursor.execute("SELECT exists (SELECT 1 FROM sleep_tracker WHERE date = ?)", (self.today,))
        if not 1 in self.controller.db_cursor.fetchone():
            # during processing an entry, check if conditions meet to unlock the 'first sleep" achievement
            self.controller.pages["AchievementsPage"].check_first_sleep()
            # set max sleep limit (to discourage users who seek to get high scores that enter dangerous territory for their own health)
            # max sleep = 9 hours
            if minutes_slept > 540.00:
                minutes_slept = 540.00
            # ensure minutes_slept variable is always set to 2 decimal points
            minutes_slept = round(minutes_slept, 2)
            self.controller.db_cursor.execute("INSERT INTO sleep_tracker (date, sleep_mins) VALUES (?, ?)", (self.today, minutes_slept))
            self.controller.db_connection.commit()
            self.sleep_display.set(f"{minutes_slept} mins")
            # update daily sleep progression
            self.sleep_current_progress.set(minutes_slept)
            self.update_daily_goal_progression_displays()
            self.sleep_var.set("")
        else:
            self.controller.db_cursor.execute("SELECT sleep_mins FROM sleep_tracker WHERE date = ?", (self.today,))
            total_minutes_slept = self.controller.db_cursor.fetchone()[0]
            total_minutes_slept += minutes_slept
            if total_minutes_slept > 540.00:
                total_minutes_slept = 540.00
                # ensure minutes_slept variable is always set to 2 decimal points
                total_minutes_slept = round(total_minutes_slept, 2)
                self.controller.db_cursor.execute("UPDATE sleep_tracker SET sleep_mins = ? WHERE date = ?", (total_minutes_slept, self.today))
                self.controller.db_connection.commit()
                self.sleep_display.set(f"{total_minutes_slept} mins")
                # update daily sleep progression
                self.sleep_current_progress.set(total_minutes_slept)
                self.update_daily_goal_progression_displays()
                self.sleep_var.set("")
            else:
                # ensure minutes_slept variable is always set to 2 decimal points
                total_minutes_slept = round(total_minutes_slept, 2)
                self.controller.db_cursor.execute("UPDATE sleep_tracker SET sleep_mins = ? WHERE date = ?", (total_minutes_slept, self.today))
                self.controller.db_connection.commit()
                self.sleep_display.set(f"{total_minutes_slept} mins")
                # update daily sleep progression
                self.sleep_current_progress.set(total_minutes_slept)
                self.update_daily_goal_progression_displays()
                self.sleep_var.set("")
        # during processing an entry, check if conditions meet to unlock the 'sleep maxxed' achievement
        self.controller.pages["AchievementsPage"].check_sleep_maxxed()
        # during processing an entry, check if conditions meet to unlock the 'sleeping beauty I' acheivement
        self.controller.pages["AchievementsPage"].check_sleeping_beauty_I()
        # during processing an entry, check if conditions meet to unlock the 'sleeping beauty II' acheivement
        self.controller.pages["AchievementsPage"].check_sleeping_beauty_II()
        self.update_monthly_goal_progression_displays()

    def reset_daily(self, event, selected_daily):
        if selected_daily == "sleep":
            # check if the entry exists first
            self.controller.db_cursor.execute("SELECT exists (SELECT 1 FROM sleep_tracker WHERE date = ?)", (self.today,))
            # if the entry exists, delete entry from the database
            if 1 in self.controller.db_cursor.fetchone():
                self.controller.db_cursor.execute("DELETE FROM sleep_tracker WHERE date = ?", (self.today,))
                self.controller.db_connection.commit()
                # reset variables and update the counter display
                self.sleep_display.set("0.0 mins")
                self.sleep_current_progress.set(0.0)
                # update sleep progression display
                self.sleep_progress_display.set(f"{self.sleep_current_progress.get()} / {self.sleep_goal.get()}")
                self.update_sleep_progressbar()
        elif selected_daily == "hydration":
            self.controller.db_cursor.execute("SELECT exists (SELECT 1 FROM hydration_tracker WHERE date = ?)", (self.today,))
            if 1 in self.controller.db_cursor.fetchone():
                self.controller.db_cursor.execute("DELETE FROM hydration_tracker WHERE date = ?", (self.today,))
                self.controller.db_connection.commit()
                # reset variables and update the counter display
                self.hydration_display.set("0.0 ml")
                self.hydration_current_progress.set(0.0)
                # update hydration progression display
                self.hydration_progress_display.set(f"{self.hydration_current_progress.get()} / {self.hydration_goal.get()}")
                self.update_hydration_progressbar()
        elif selected_daily == "walking":
            self.controller.db_cursor.execute("SELECT exists (SELECT 1 FROM steps_tracker WHERE date = ?)", (self.today,))
            if 1 in self.controller.db_cursor.fetchone():
                self.controller.db_cursor.execute("DELETE FROM steps_tracker WHERE date = ?", (self.today,))
                self.controller.db_connection.commit()
                # reset variables and update the counter display
                self.steps_display.set("0 steps")
                self.steps_current_progress.set(0)
                # update steps progression display
                self.steps_progress_display.set(f"{self.steps_current_progress.get()} / {self.steps_goal.get()}")
                self.update_steps_progressbar()
        self.update_monthly_goal_progression_displays()

    def update_exercise_summary(self):
        # retrieve data for today's sets, reps and weight values
        self.controller.db_cursor.execute("SELECT sets_count, reps_count, weight_value FROM exercise_entries WHERE date = ?", (self.today,))
        results = self.controller.db_cursor.fetchall()
        # if entries exists, tally the data and display in the exercise summary section
        if results:
            # get count of total exercises
            self.exercise_total_var.set(len(results))
            sets_sum = 0
            reps_sum = 0
            volume_sum = 0
            # calculate the sets, reps and volume totals
            for i in results:
                sets_sum += i[0]
                reps_sum += i[0] * i[1]
                volume_sum += (i[0] * i[1]) * i[2]
            # update display widgets for respective sets, reps and volume totals
            self.sets_total_var.set(sets_sum)
            self.reps_total_var.set(reps_sum)
            self.volume_total_var.set(volume_sum)
            

    def update_weather_forecast(self):
        pass # temp during multiple startups to test other sections of the app..
        # wmo_list = self.controller.wmo_codes

        # # get user's approximate location
        # ip_response = requests.get("https://get.geojs.io/v1/ip/geo.json")
        # data = ip_response.json()
        # latitude = data["latitude"]
        # longitude = data["longitude"]

        # # try-except to ensure app still runs even if the weather request times out
        # try:
        #     # get weather forecast based on latitude x longitude
        #     weather_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code&timezone=auto")
        #     weather_data = weather_response.json()
        #     current_units = weather_data["current_units"]
        #     current_values = weather_data["current"]

        #     # format retrieved data
        #     location = weather_data["timezone"]
        #     last_updated_time = f"Last Updated: {current_values["time"][11:]}"
        #     temperature = f"{current_values["temperature_2m"]} {current_units["temperature_2m"]}"
        #     weather_code = current_values["weather_code"]

        #     # set display widgets with formatted string
        #     self.location_var.set(location)
        #     self.last_updated_var.set(last_updated_time)
        #     self.temp_var.set(temperature)
            
        #     # determine which weather icon to display based on wmo code reading
        #     for i in range(len(wmo_list)):
        #         if weather_code in wmo_list[i][0]:
        #             self.weather_icon.configure(light_image=Image.open(f"img/weather/{wmo_list[i][1]}.png"), dark_image=Image.open(f"img/weather/{wmo_list[i][1]}.png"), size=(64, 64))
        #             self.weather_type_var.set(wmo_list[i][1].capitalize())  
        # except requests.exceptions.Timeout:
        #     # do nothing and continue app startup
        #     pass

    def populate_entries_display(self):
        # update the entries list by first resetting existing data
        if self.entries.get_children():
            self.entries.delete(*self.entries.get_children())
        # retrieve latest data
        self.controller.db_cursor.execute("SELECT exercise_name, date, time, sets_count, reps_count, weight_value, exercise_label FROM exercise_entries ORDER BY id DESC LIMIT 25")
        result = self.controller.db_cursor.fetchall()
        if result:
            for i, (exercise, date, time, sets, reps, weight, label) in enumerate(result):
                # truncating values to a single string
                summary = f"{sets} x {reps} @ {weight}kg"
                # shortening exercise and label strings for readability and slight minimalism
                if len(exercise) > 20:
                    trimmed_exercise = exercise[:20] + "..."
                else:
                    trimmed_exercise = exercise
                if len(label) > 20:
                    trimmed_label = label[:20] + "..."   
                else:
                    trimmed_label = label
                revised_values = (trimmed_exercise, date, time, summary, trimmed_label)
                # allocating row colour based on row parity
                if i % 2 == 0:
                    tag = "evenrow"
                else:
                    tag = "oddrow"
                # populating the entries list with revised data collected from the exercise_entries database
                self.entries.insert("", "end", values=revised_values, tags=(tag,))