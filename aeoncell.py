import customtkinter as ctk
from tkinter import filedialog
from database_manager import DatabaseManager
import sqlite3
from datetime import date
from aeoncell_utils import *
from PIL import Image
import os
from CTkXYFrame import *
from tkinter import ttk as btk
import random

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("themes/custom_lavender.json")

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = DatabaseManager()
        self.db_connection = sqlite3.connect("aeoncell_database.db")
        self.db_cursor = self.db_connection.cursor()

        self.today = date.today()
        self.today = self.today.strftime("%d-%m-%Y")

        self.username = ctk.StringVar()
        self.user_profile_img = ctk.CTkImage(light_image=Image.open("img/user_profile.png"), dark_image=Image.open("img/user_profile.png"), size=(120,120))
        self.app_icon_img = ctk.CTkImage(light_image=Image.open("img/capsule_original_recround.png"), dark_image=Image.open("img/capsule_original_recround.png"), size=(64,64))

        self.title("Aeoncell")
        self.geometry("1440x900")
        self.minsize(1440, 900)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nswe")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # if user has successfully registered/exists
        # check this by seeing if a password has been stored (could also check for username, same end result)
        if self.db.check_password_exists():
            # set the global username variable with existing username found in the database
            self.set_username()
        

        # if a user has successfully registered, set the global username var's value with the username
        if self.db.check_password_exists():
            self.set_username()

        self.pages = {}
        for P in (RegisterPage, LoginPage, DashboardPage, DiscoverPage, SingleEntryPage, SessionEntryPage, StatsPage, AchievementsPage, SettingsPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        # center the app upon startup
        self.center_window(self, 1440, 900)

        self.show_page(DashboardPage)
        # determine initial page display based on user having a password (i.e. guaranteed account registration)
        # if self.db.check_password_exists():
        #     self.show_page(LoginPage)
        # else:
        #     self.show_page(RegisterPage)

    # display the selected page to the user
    def show_page(self, selected_page):
        page = self.pages[selected_page]

        # field focus config on startup for pages
        if selected_page == RegisterPage:
            self.set_initial_focus(page.username_entry)
        elif selected_page == LoginPage:
            self.set_initial_focus(page.password_entry)
        elif selected_page == DashboardPage:
            page.retrieve_profile_details()
            page.random_motivational_quote()
            page.populate_entries_display()
        elif selected_page in (SingleEntryPage, SessionEntryPage):
            page.reset_date()
        elif selected_page == SettingsPage:
            page.retrieve_current_info()

        page.tkraise()
        
        # loading logs for dashboard latest 25 entries display

    # set cursor focus to chosen field
    def set_initial_focus(self, widget_name):
        self.after(300, widget_name.focus_set)

    # retrieve and set username from value found in database
    def set_username(self):
        self.db_cursor.execute("SELECT username FROM authentication WHERE rowid=1")
        result = self.db_cursor.fetchone()
        self.username.set(result[0])

    def show_error_message(self, widget, message):
        widget.configure(text=message)
        widget.after(1000, lambda: widget.configure(text=""))

    def center_window(self, widget_frame, win_width, win_height):
        x = (self.winfo_screenwidth() // 2) - (win_width // 2)
        y = (self.winfo_screenheight() // 2) - (win_height // 2)
        return widget_frame.geometry(f"{win_width}x{win_height}+{x}+{y}")

class Navbar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.configure(fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0)

        # icon images
        self.dashboard_img = ctk.CTkImage(light_image=Image.open("img/dashboard_icon.png"), dark_image=Image.open("img/dashboard_icon.png"), size=(32, 32))
        self.discover_img = ctk.CTkImage(light_image=Image.open("img/discover_icon.png"), dark_image=Image.open("img/discover_icon.png"), size=(32, 32))
        self.entry_img = ctk.CTkImage(light_image=Image.open("img/entry_icon.png"), dark_image=Image.open("img/entry_icon.png"), size=(32, 32))
        self.stats_img = ctk.CTkImage(light_image=Image.open("img/stats_icon.png"), dark_image=Image.open("img/stats_icon.png"), size=(32, 32))
        self.achievements_img = ctk.CTkImage(light_image=Image.open("img/achievements_icon.png"), dark_image=Image.open("img/achievements_icon.png"), size=(32, 32))
        self.settings_img = ctk.CTkImage(light_image=Image.open("img/settings_icon.png"), dark_image=Image.open("img/settings_icon.png"), size=(32, 32))
        self.logout_img = ctk.CTkImage(light_image=Image.open("img/logout_icon.png"), dark_image=Image.open("img/logout_icon.png"), size=(32, 32))

        self.create_widgets()

    def create_widgets(self):
        app_name = ctk.CTkLabel(self, text="Aeoncell", font=("", 18))
        app_icon = ctk.CTkLabel(self, text="", image=self.controller.app_icon_img)
        self.dashboard_icon = ctk.CTkLabel(self, text="", image=self.dashboard_img)
        self.dashboard_title = ctk.CTkLabel(self, text="Dashboard", font=("", 11, "bold"))
        self.discover_icon = ctk.CTkLabel(self, text="", image=self.discover_img)
        self.discover_title = ctk.CTkLabel(self, text="Discover", font=("", 11, "bold"))
        self.entry_icon = ctk.CTkLabel(self, text="", image=self.entry_img)
        self.entry_title = ctk.CTkLabel(self, text="Entry", font=("", 11, "bold"))
        self.stats_icon = ctk.CTkLabel(self, text="", image=self.stats_img)
        self.stats_title = ctk.CTkLabel(self, text="Statistics", font=("", 11, "bold"))
        self.achievements_icon = ctk.CTkLabel(self, text="", image=self.achievements_img)
        self.achievements_title = ctk.CTkLabel(self, text="Achievements", font=("", 11, "bold"))
        self.settings_icon = ctk.CTkLabel(self, text="", image=self.settings_img)
        self.settings_title = ctk.CTkLabel(self, text="Settings", font=("", 11, "bold"))
        self.logout_icon = ctk.CTkLabel(self, text="", image=self.logout_img)
        self.logout_title = ctk.CTkLabel(self, text="Logout", font=("", 11, "bold"))

        app_name.grid(row=1, column=1, pady=20, padx=10)
        app_icon.grid(row=2, column=1, pady=(0, 50))
        self.dashboard_icon.grid(row=3, column=1, pady=(10, 0))
        self.dashboard_title.grid(row=4, column=1, pady=(0, 10))
        self.discover_icon.grid(row=5, column=1, pady=(10, 0))
        self.discover_title.grid(row=6, column=1, pady=(0, 10))
        self.entry_icon.grid(row=7, column=1, pady=(10, 0))
        self.entry_title.grid(row=8, column=1, pady=(0, 10))
        self.stats_icon.grid(row=9, column=1, pady=(10, 0))
        self.stats_title.grid(row=10, column=1, pady=(0, 10))
        self.achievements_icon.grid(row=11, column=1, pady=(10, 0))
        self.achievements_title.grid(row=12, column=1, pady=(0, 10))
        self.settings_icon.grid(row=13, column=1, pady=(10, 0))
        self.settings_title.grid(row=14, column=1, pady=(0, 20))
        self.logout_icon.grid(row=15, column=1, pady=(50, 0))
        self.logout_title.grid(row=16, column=1)

        self.dashboard_icon.bind("<Enter>", lambda event: self.display_selection(self.dashboard_icon, self.dashboard_title))
        self.dashboard_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.dashboard_icon, self.dashboard_title))
        self.dashboard_icon.bind("<Button-1>", lambda event: self.controller.show_page(DashboardPage))
        self.dashboard_title.bind("<Enter>", lambda event: self.display_selection(self.dashboard_icon, self.dashboard_title))
        self.dashboard_title.bind("<Leave>", lambda event: self.undisplay_selection(self.dashboard_icon, self.dashboard_title))
        self.dashboard_title.bind("<Button-1>", lambda event: self.controller.show_page(DashboardPage))
        self.discover_icon.bind("<Enter>", lambda event: self.display_selection(self.discover_icon, self.discover_title))
        self.discover_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.discover_icon, self.discover_title))
        self.discover_icon.bind("<Button-1>", lambda event: self.controller.show_page(DiscoverPage))
        self.discover_title.bind("<Enter>", lambda event: self.display_selection(self.discover_icon, self.discover_title))
        self.discover_title.bind("<Leave>", lambda event: self.undisplay_selection(self.discover_icon, self.discover_title))
        self.discover_title.bind("<Button-1>", lambda event: self.controller.show_page(DiscoverPage))
        self.entry_icon.bind("<Enter>", lambda event: self.display_selection(self.entry_icon, self.entry_title))
        self.entry_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.entry_icon, self.entry_title))
        self.entry_icon.bind("<Button-1>", lambda event: self.controller.show_page(SingleEntryPage))
        self.entry_title.bind("<Enter>", lambda event: self.display_selection(self.entry_icon, self.entry_title))
        self.entry_title.bind("<Leave>", lambda event: self.undisplay_selection(self.entry_icon, self.entry_title))
        self.entry_title.bind("<Button-1>", lambda event: self.controller.show_page(SingleEntryPage))
        self.stats_icon.bind("<Enter>", lambda event: self.display_selection(self.stats_icon, self.stats_title))
        self.stats_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.stats_icon, self.stats_title))
        self.stats_icon.bind("<Button-1>", lambda event: self.controller.show_page(StatsPage))
        self.stats_title.bind("<Enter>", lambda event: self.display_selection(self.stats_icon, self.stats_title))
        self.stats_title.bind("<Leave>", lambda event: self.undisplay_selection(self.stats_icon, self.stats_title))
        self.stats_title.bind("<Button-1>", lambda event: self.controller.show_page(StatsPage))
        self.achievements_icon.bind("<Enter>", lambda event: self.display_selection(self.achievements_icon, self.achievements_title))
        self.achievements_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.achievements_icon, self.achievements_title))
        self.achievements_icon.bind("<Button-1>", lambda event: self.controller.show_page(AchievementsPage))
        self.achievements_title.bind("<Enter>", lambda event: self.display_selection(self.achievements_icon, self.achievements_title))
        self.achievements_title.bind("<Leave>", lambda event: self.undisplay_selection(self.achievements_icon, self.achievements_title))
        self.achievements_title.bind("<Button-1>", lambda event: self.controller.show_page(AchievementsPage))
        self.settings_icon.bind("<Enter>", lambda event: self.display_selection(self.settings_icon, self.settings_title))
        self.settings_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.settings_icon, self.settings_title))
        self.settings_icon.bind("<Button-1>", lambda event: self.controller.show_page(SettingsPage))
        self.settings_title.bind("<Enter>", lambda event: self.display_selection(self.settings_icon, self.settings_title))
        self.settings_title.bind("<Leave>", lambda event: self.undisplay_selection(self.settings_icon, self.settings_title))
        self.settings_title.bind("<Button-1>", lambda event: self.controller.show_page(SettingsPage))
        self.logout_icon.bind("<Enter>", lambda event: self.display_selection(self.logout_icon, self.logout_title))
        self.logout_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.logout_icon, self.logout_title))
        self.logout_icon.bind("<Button-1>", lambda event: self.controller.show_page(LoginPage))
        self.logout_title.bind("<Enter>", lambda event: self.display_selection(self.logout_icon, self.logout_title))
        self.logout_title.bind("<Leave>", lambda event: self.undisplay_selection(self.logout_icon, self.logout_title))
        self.logout_title.bind("<Button-1>", lambda event: self.controller.show_page(LoginPage))

    def display_selection(self, widget_icon, widget_title, event=None):
        widget_icon.configure(cursor="hand2")
        widget_title.configure(font=("", 11, "bold", "underline"), cursor="hand2")

    def undisplay_selection(self, widget_icon, widget_title, event=None):
        widget_icon.configure(cursor="arrow")
        widget_title.configure(font=("", 11, "bold"), cursor="arrow")
    
    # implement at a later time when other pages/features are fleshed out
    # logout feature will have customised function to also deal with any erasure or resets to any pages upon logging out..

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.confirm_password_var = ctk.StringVar()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # register page's split frames (50/50)
        register_form_section = ctk.CTkFrame(self, corner_radius=0)
        cover_image_section = ctk.CTkFrame(self, corner_radius=0)

        register_form_section.grid(row=0, column=0, sticky="nswe")
        cover_image_section.grid(row=0, column=1, sticky="nswe")

        register_form_section.grid_rowconfigure(0, weight=1)
        register_form_section.grid_rowconfigure(2, weight=1)

        register_form_section.grid_columnconfigure(0, weight=1)
        register_form_section.grid_columnconfigure(2, weight=1)

        register_form_section.grid_propagate(False)

        cover_image_section.grid_rowconfigure(0, weight=1)
        cover_image_section.grid_columnconfigure(0, weight=1)

        cover_image_section.grid_propagate(False)

        # register form's frame
        register_form = ctk.CTkFrame(register_form_section, fg_color=("#F5F0FF", "#2A1A4A"), width=514, height=700, border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40)

        register_form.grid(row=1, column=1)

        register_form.grid_rowconfigure(0, weight=1)
        register_form.grid_rowconfigure(12, weight=1)

        register_form.grid_columnconfigure(0, weight=1)
        register_form.grid_columnconfigure(2, weight=1)

        register_form.grid_propagate(False)

        # internal widgets for the register form
        app_name = ctk.CTkLabel(register_form, text="Aeoncell", font=("", 18))
        form_name = ctk.CTkLabel(register_form, text="Register", font=("", 48))
        app_icon_main = ctk.CTkLabel(register_form, text="", image=self.controller.app_icon_img)
        username_title = ctk.CTkLabel(register_form, text="Username:", font=("", 24))
        self.username_entry = ctk.CTkEntry(register_form, textvariable=self.username_var, width=300, font=("", 24))
        password_title = ctk.CTkLabel(register_form, text="Create Password:", font=("", 24))
        self.password_entry = ctk.CTkEntry(register_form, textvariable=self.password_var, width=300, font=("", 24))
        confirm_password_title = ctk.CTkLabel(register_form, text="Confirm Password:", font=("", 24))
        self.confirm_password_entry = ctk.CTkEntry(register_form, textvariable=self.confirm_password_var, width=300, font=("", 24))
        self.error_message = ctk.CTkLabel(register_form, text="", font=("", 18))
        register_submit = ctk.CTkButton(register_form, height=50, text="Register", font=("", 24), command=self.process_registration)

        app_name.grid(row=1, column=1)
        form_name.grid(row=2, column=1, pady=(20, 0))
        app_icon_main.grid(row=3, column=1, pady=(20, 10))
        username_title.grid(row=4, column=1, pady=(30, 0), sticky="w")
        self.username_entry.grid(row=5, column=1, pady=(5, 0))
        password_title.grid(row=6, column=1, pady=(20, 0), sticky="w")
        self.password_entry.grid(row=7, column=1, pady=(5, 0))
        confirm_password_title.grid(row=8, column=1, pady=(20, 0), sticky="w")
        self.confirm_password_entry.grid(row=9, column=1, pady=(5, 0))
        self.error_message.grid(row=10, column=1, pady=(20, 0))
        register_submit.grid(row=11, column=1, pady=(10, 0))

        # cover image section
        register_cover_image = ctk.CTkImage(light_image=Image.open("img/cartoon_gym_background.png"), dark_image=Image.open("img/cartoon_gym_background.png"), size=((self.winfo_screenwidth()/2), (self.winfo_screenheight())))
        cover_image_display = ctk.CTkLabel(cover_image_section, text="", image=register_cover_image)
        cover_image_display.grid(row=0, column=0, sticky="nswe")

        # detect and process 'Enter' keybind interaction
        self.username_entry.bind("<Return>", self.process_registration)
        self.password_entry.bind("<Return>", self.process_registration)
        self.confirm_password_entry.bind("<Return>", self.process_registration)

    def process_registration(self, event=None):
        username = self.username_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        # validate username
        if len(username) < 4:
            self.controller.show_error_message(self.error_message, "Username must be at least 4 chars.")
            return 
        elif len(username) > 8:
            self.controller.show_error_message(self.error_message, "Username must be less than 8 chars.")
            return 
        elif username.isspace():
            self.controller.show_error_message(self.error_message, "Username cannot be whitespaces.")
            return 
        elif " " in username:
            self.controller.show_error_message(self.error_message, "Username cannot contain spaces.")
            return 

        # validate password
        if password != confirm_password:
            self.controller.show_error_message(self.error_message, "Passwords do not match.")
            return 
        elif password.isspace():
            self.controller.show_error_message(self.error_message, "Password cannot be whitespaces.")
            return 
        elif " " in password:
            self.controller.show_error_message(self.error_message, "Password cannot contain spaces.")
            return 
        elif len(password) < 8:
            self.controller.show_error_message(self.error_message, "Password must be at least 8 chars.")
            return 
    
        # if validation is successful run the following
        self.controller.db.create_username_and_password(username, password)
        # update the global username's value
        self.controller.set_username()
        # update the login page's welcome_message widget
        self.controller.pages[LoginPage].welcome_message.configure(text=f"Welcome back, {self.controller.username.get()}!")
        self.controller.show_page(LoginPage)

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.password_var = ctk.StringVar()

        self.masked_password_icon = ctk.CTkImage(light_image=Image.open("img/pw_masked.png"), dark_image=Image.open("img/pw_masked.png"), size=(32, 32))
        self.unmasked_password_icon = ctk.CTkImage(light_image=Image.open("img/pw_unmasked.png"), dark_image=Image.open("img/pw_unmasked.png"), size=(32, 32))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # login page's split frames (50/50)
        cover_image_section = ctk.CTkFrame(self, corner_radius=0)
        login_form_section = ctk.CTkFrame(self, corner_radius=0)

        cover_image_section.grid(row=0, column=0, sticky="nswe")
        login_form_section.grid(row=0, column=1, sticky="nswe")

        cover_image_section.grid_rowconfigure(0, weight=1)
        cover_image_section.grid_columnconfigure(0, weight=1)
        cover_image_section.grid_propagate(False)

        login_form_section.grid_rowconfigure(0, weight=1)
        login_form_section.grid_rowconfigure(2, weight=1)
        login_form_section.grid_columnconfigure(0, weight=1)
        login_form_section.grid_columnconfigure(2, weight=1)
        login_form_section.grid_propagate(False)

        # login form's frame
        login_form = ctk.CTkFrame(login_form_section, fg_color=("#F5F0FF", "#2A1A4A"), width=514, height=700, border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40)

        login_form.grid(row=1, column=1)
        login_form.grid_rowconfigure(0, weight=1)
        login_form.grid_rowconfigure(9, weight=1)
        login_form.grid_columnconfigure(0, weight=1)
        login_form.grid_columnconfigure(3, weight=1)
        login_form.grid_propagate(False)

        # internal widgets for the login form
        app_name = ctk.CTkLabel(login_form, text="Aeoncell", font=("", 18))
        form_name = ctk.CTkLabel(login_form, text="Login", font=("", 48))
        profile_image = ctk.CTkLabel(login_form, text="", image=self.controller.user_profile_img)
        self.welcome_message = ctk.CTkLabel(login_form, text=f"Welcome back, {self.controller.username.get()}!", font=("", 24))
        password_title = ctk.CTkLabel(login_form, text="Enter Password:", font=("", 24))
        self.password_entry = ctk.CTkEntry(login_form, show="*", textvariable=self.password_var, font=("", 24), width=300)
        self.toggle_password_mask_btn = ctk.CTkButton(login_form, text="", image=self.masked_password_icon, bg_color="transparent", fg_color="transparent", hover_color="#B19CD9", width=0, command=self.toggle_password_masking)
        self.error_message = ctk.CTkLabel(login_form, text="", font=("", 18))
        login_submit = ctk.CTkButton(login_form, text="Login", height=50, font=("", 24), command=self.process_login)

        app_name.grid(row=1, column=1, columnspan=2)
        form_name.grid(row=2, column=1, columnspan=2, pady=(10, 20))
        profile_image.grid(row=3, column=1, columnspan=2, pady=(0, 30))
        self.welcome_message.grid(row=4, column=1, columnspan=2, pady=(0, 40))
        password_title.grid(row=5, column=1, columnspan=2, sticky="w")
        self.password_entry.grid(row=6, column=1, pady=(0, 10))
        self.toggle_password_mask_btn.grid(row=6, column=2, pady=(0, 10), padx=(5, 0))
        self.error_message.grid(row=7, column=1, columnspan=2)
        login_submit.grid(row=8, column=1, columnspan=2, pady=(20, 40))

        # cover image section
        login_cover_image = ctk.CTkImage(light_image=Image.open("img/cartoon_gym_background.png"), dark_image=Image.open("img/cartoon_gym_background.png"), size=((self.winfo_screenwidth()/2), (self.winfo_screenheight())))
        cover_image_display = ctk.CTkLabel(cover_image_section, text="", image=login_cover_image)
        cover_image_display.grid(row=0, column=0, sticky="nswe")

        # detect and process 'Enter' keybind interaction
        self.password_entry.bind("<Return>", self.process_login)

    def process_login(self, event=None):
        password = self.password_var.get()
        if self.controller.db.verify_password(password):
            self.controller.show_page(DashboardPage)
        else:
            self.controller.show_error_message(self.error_message, "Incorrect Password.")

    # toggle password masking dependent on user's choice
    def toggle_password_masking(self):
        if self.password_entry.cget("show") == "*":
            self.toggle_password_mask_btn.configure(image=self.unmasked_password_icon)
            self.password_entry.configure(show="")
        else:
            self.toggle_password_mask_btn.configure(image=self.masked_password_icon)
            self.password_entry.configure(show="*")

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # temp
        self.icon = ctk.CTkImage(light_image=Image.open("img/big_flame.png"), dark_image=Image.open("img/big_flame.png"), size=(32, 32))
        self.badge = ctk.CTkImage(light_image=Image.open("img/achievements/first_workout_achievement.png"), dark_image=Image.open("img/achievements/first_workout_achievement.png"), size=(64, 64))
        self.mini_banner = ctk.CTkImage(light_image=Image.open("img/laid_dumbbell_man.png"), dark_image=Image.open("img/laid_dumbbell_man.png"), size=(100, 100))
        self.weather_forecast = ctk.CTkImage(light_image=Image.open("img/forecast_storm.png"), dark_image=Image.open("img/forecast_storm.png"), size=(64, 64))
        # multi-sectional use
        self.today = self.controller.today

        # intro section
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

        # recent exercises section related variables
        style = btk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=28, borderwidth=2, font=("", 12))
        style.configure("Treeview.Heading", background="#d6c6f4", font=("", 14, "bold"))
        style.map('Treeview', background=[('selected', '#b799e3')])

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.daily_section_initialisation()
        self.update_exercise_summary()
        self.create_widgets()

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
        hello_message = ctk.CTkLabel(intro_section, text=f"Hello, Henry", width=750, anchor="w", font=("", 32))
        motivational_message_display = ctk.CTkLabel(intro_section, textvariable=self.motivational_message, width=750, anchor="w", font=("", 18, "italic"))
        current_date = ctk.CTkLabel(intro_section, textvariable=self.today_full_display, font=("", 24))
        date_icon = ctk.CTkLabel(intro_section, text="", image=self.intro_icon)
        motivation_icon = ctk.CTkLabel(intro_section, text="", image=self.motivation_icon)

        hello_message.grid(row=0, column=0, sticky="w", padx=(50, 0), pady=(20, 0))
        motivational_message_display.grid(row=1, column=0, sticky="w", padx=(50, 0))
        current_date.grid(row=0, rowspan=2, column=1, sticky="e", padx=(100, 0), pady=(20, 0))
        date_icon.grid(row=0, rowspan=2, column=2, sticky="e", padx=(20, 0), pady=(20, 0))
        motivation_icon.grid(row=0, rowspan=2, column=3, sticky="e", padx=(60, 0), pady=(20, 0))

        intro_section.grid_propagate(False)

        motivation_icon.bind("<Button-1>", self.random_motivational_quote)

        #endregion

        #region [ Profile Section ]
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
        
        profile_monthly_section = ctk.CTkFrame(profile_section, border_color="blue", fg_color="transparent")
        profile_monthly_title = ctk.CTkLabel(profile_monthly_section, text="Monthly Progress", font=("", 32))
        profile_monthly_weight_title = ctk.CTkLabel(profile_monthly_section, text="Weight Loss", font=("", 18))
        profile_monthly_weight_info = ctk.CTkLabel(profile_monthly_section, text="2/5 kilos", font=("", 14))
        profile_monthly_weight_progressbar = ctk.CTkProgressBar(profile_monthly_section, border_width=3, height=40, width=400, corner_radius=0)
        profile_sleep_title = ctk.CTkLabel(profile_monthly_section, text="Sleep", font=("", 18))
        profile_sleep_info = ctk.CTkLabel(profile_monthly_section, text="110/300 hours", font=("", 14))
        profile_sleep_progressbar = ctk.CTkProgressBar(profile_monthly_section, border_width=3, height=40, width=400, corner_radius=0)
        profile_hydration_title = ctk.CTkLabel(profile_monthly_section, text="Hydration", font=("", 18)) 
        profile_hydration_info = ctk.CTkLabel(profile_monthly_section, text="80/250 litres", font=("", 14))
        profile_hydration_progressbar = ctk.CTkProgressBar(profile_monthly_section, border_width=3, height=40, width=400, corner_radius=0)
        profile_walking_title = ctk.CTkLabel(profile_monthly_section, text="Walking", font=("", 18))
        profile_walking_info = ctk.CTkLabel(profile_monthly_section, text="35,000/150,000 steps", font=("", 14))
        profile_walking_progressbar = ctk.CTkProgressBar(profile_monthly_section, border_width=3, height=40, width=400, corner_radius=0)
        
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
        profile_monthly_weight_title.grid(row=1, column=0, pady=(10, 0), sticky="w")
        profile_monthly_weight_info.grid(row=1, column=1, pady=(10, 0), sticky="e")
        profile_monthly_weight_progressbar.grid(row=2, column=0, columnspan=2)
        profile_sleep_title.grid(row=3, column=0, pady=(20, 0), sticky="w")
        profile_sleep_info.grid(row=3, column=1, pady=(20, 0), sticky="e")
        profile_sleep_progressbar.grid(row=4, column=0, columnspan=2)
        profile_hydration_title.grid(row=5, column=0, pady=(20, 0), sticky="w")
        profile_hydration_info.grid(row=5, column=1, pady=(20, 0), sticky="e")
        profile_hydration_progressbar.grid(row=6, column=0, columnspan=2)
        profile_walking_title.grid(row=7, column=0, pady=(20, 0), sticky="w")
        profile_walking_info.grid(row=7, column=1, pady=(20, 0), sticky="e")
        profile_walking_progressbar.grid(row=8, column=0, columnspan=2)

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
        self.update_sleep_progressbar()

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
        self.update_hydration_progressbar()

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
        self.update_steps_progressbar()

        dailies_section.grid_propagate(False)

        #endregion

        #region [ Quick Stats Section ]

        exercise_summary = ctk.CTkFrame(quick_stats_section, border_width=5, border_color="#B19CD9")
        daily_forecast = ctk.CTkFrame(quick_stats_section, border_width=5, border_color="#B19CD9")

        exercise_summary.grid(row=1, column=1, padx=(0, 20))
        exercise_summary.grid_columnconfigure(0, minsize=40)
        exercise_summary.grid_columnconfigure(3, minsize=40)

        daily_forecast.grid(row=1, column=2)

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
        add_session = ctk.CTkButton(entries_buttons_frame, text="Add a Session", width=140, height=60, font=("", 18), command=lambda: self.controller.show_page(SingleEntryPage))
        add_single = ctk.CTkButton(entries_buttons_frame, text="Add an Exercise", width=140, height=60, font=("", 18), command=lambda: self.controller.show_page(SessionEntryPage))

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

        redirect_session_entry_icon.bind("<Button-1>", lambda event: self.controller.show_page(SessionEntryPage))
        redirect_single_entry_icon.bind("<Button-1>", lambda event: self.controller.show_page(SingleEntryPage))
        #endregion

    # Reminder to adjust after finishing all widgets... 
    # coding ettiquette -> make sure all frames/configures are all placed in the same positioning/order throughout.
    # remember to implement binding for the actionable icons like -> reset icon

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

    def update_profile_image(self):
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

    def daily_section_initialisation(self):
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
        self.controller.db_cursor.execute("SELECT daily_steps_goal, daily_sleep_goal, daily_hydration_goal FROM profile_details WHERE rowid=1")
        steps_goal, sleep_goal, hydration_goal = self.controller.db_cursor.fetchone()

        # set goal variables for later use (for progress bar setting)
        self.steps_goal.set(steps_goal)
        self.sleep_goal.set(sleep_goal)
        self.hydration_goal.set(hydration_goal)

        # set the latest daily progression data
        self.steps_progress_display.set(f"{self.steps_current_progress.get()} / {steps_goal}")
        self.sleep_progress_display.set(f"{self.sleep_current_progress.get()} / {sleep_goal}")
        self.hydration_progress_display.set(f"{self.hydration_current_progress.get()} / {hydration_goal}")

    def update_steps_progressbar(self):
        current_progress = int(self.steps_current_progress.get())
        total_progress = int(self.steps_goal.get())
        self.walking_progressbar.set(current_progress/total_progress)

    def update_hydration_progressbar(self):
        current_progress = float(self.hydration_current_progress.get())
        total_progress = float(self.hydration_goal.get())
        self.hydration_progressbar.set(current_progress/total_progress)
    
    def update_sleep_progressbar(self):
        current_progress = float(self.sleep_current_progress.get())
        total_progress = float(self.sleep_goal.get())
        self.sleep_progressbar.set(current_progress/total_progress)

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
            # if none exists, create a new entry with the initially given steps
            self.controller.db_cursor.execute("INSERT INTO steps_tracker (date, steps_taken) VALUES (?, ?)", (self.today, steps))
            self.controller.db_connection.commit()
            # format and update the total steps taken display
            self.steps_display.set(f"{steps:,} steps")
            # update daily steps progression
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
        # update step's daily progress bar
        self.update_steps_progressbar()

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
        # update hydration's daily progress bar
        self.update_hydration_progressbar()

    def process_sleep_entry(self):
        input_value = self.sleep_var.get()
        if len(input_value) == 0:
            return
        minutes_slept = float(input_value)
        if minutes_slept < 0.00:
            return
        self.controller.db_cursor.execute("SELECT exists (SELECT 1 FROM sleep_tracker WHERE date = ?)", (self.today,))
        if not 1 in self.controller.db_cursor.fetchone():
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
        # update sleep's daily progress bar
        self.update_sleep_progressbar()

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

    def update_exercise_summary(self):
        # retrieve data for today's sets, reps and weight values
        self.controller.db_cursor.execute("SELECT sets_count, reps_count, weight_value FROM exercise_entries WHERE date = ?", (self.today,))
        result = self.controller.db_cursor.fetchall()
        # if entries exists, tally the data and display in the exercise summary section
        if result:
            self.exercise_total_var.set(len(result))
            sets_sum = 0
            reps_sum = 0
            weights_sum = 0
            for i in range(len(result)):
                sets_sum += result[i][0]
                reps_sum += result[i][1]
                weights_sum += result[i][2]
            self.sets_total_var.set(sets_sum)
            self.reps_total_var.set(reps_sum)
            self.volume_total_var.set(weights_sum)

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

class DiscoverPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        navbar = Navbar(self, self.controller)
        content = ctk.CTkFrame(self, fg_color="black", corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        dashboard_title = ctk.CTkLabel(content, text="This is the Discover Page!", text_color="green")
        dashboard_title.pack()

class BaseEntryPage(ctk.CTkFrame):
    def __init__(self, parent, controller, entry_type, btn_name):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.entry_type = entry_type
        self.btn_name = btn_name
        self.type_var = ctk.StringVar(value=self.entry_type)
        self.today = self.controller.today

        self.single_entry_icon = ctk.CTkImage(light_image=Image.open("img/dumbbell.png"), dark_image=Image.open("img/dumbbell.png"), size=(48, 48))
        self.session_entry_icon = ctk.CTkImage(light_image=Image.open("img/barbell.png"), dark_image=Image.open("img/barbell.png"), size=(48, 48))

        self.grid_rowconfigure(0, weight=1)
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        navbar = Navbar(self, self.controller)
        content = ctk.CTkFrame(self)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(2, weight=1)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)

        self.entry_form = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), width=814, height=700, border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40)

        self.entry_form.grid(row=1, column=1)

        self.entry_form.grid_columnconfigure(0, weight=1)
        self.entry_form.grid_columnconfigure(3, weight=1)

        self.entry_form.grid_rowconfigure(0, weight=1)
        self.entry_form.grid_rowconfigure(15, weight=1)

        self.entry_form.grid_propagate(False)

        self.toggle_entry_type_icon = ctk.CTkLabel(self.entry_form, text="", image=self.single_entry_icon)

        page_title = ctk.CTkLabel(self.entry_form, text=f"Create New Entry [{self.entry_type.capitalize()}]", font=("", 32, "bold"))

        type_title = ctk.CTkLabel(self.entry_form, text="Type*:", font=("", 24))
        self.type_entry = ctk.CTkEntry(self.entry_form, textvariable=self.type_var, width=300, font=("", 24), state="readonly")
        exercise_name_title = ctk.CTkLabel(self.entry_form, text="Exercise Name*:", font=("", 24))
        self.exercise_name_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 24))
        date_title = ctk.CTkLabel(self.entry_form, text="Date (dd-mm-yyy)*:", font=("", 24))
        self.date_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 24))
        time_title = ctk.CTkLabel(self.entry_form, text="Time (hh:mm)*:", font=("", 24))
        self.time_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 24))
        sets_title = ctk.CTkLabel(self.entry_form, text="Sets*:", font=("", 24))
        self.sets_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 24))
        reps_title = ctk.CTkLabel(self.entry_form, text="Reps*:", font=("", 24))
        self.reps_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 24))
        weight_title = ctk.CTkLabel(self.entry_form, text="Weight (kg)*:", font=("", 24))
        self.weight_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 24))
        label_title = ctk.CTkLabel(self.entry_form, text="Label:", font=("", 24))
        self.label_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 24))
        self.error_message = ctk.CTkLabel(self.entry_form, text="", text_color="red", font=("", 18))
        self.add_exercise_btn = ctk.CTkButton(self.entry_form, text="Add Exercise", height=48, font=("", 24), command=self.process_entry)
        self.redirect_btn = ctk.CTkButton(self.entry_form, text=f"{self.btn_name}", height=48, font=("", 24), command=self.process_confirmation)

        self.toggle_entry_type_icon.grid(row=1, column=2, sticky="e")

        page_title.grid(row=2, column=1, columnspan=2, pady=(20, 40), padx=20)

        type_title.grid(row=3, column=1, pady=(20, 0), padx=20, sticky="w")
        self.type_entry.grid(row=4, column=1, pady=(5, 0), padx=20)
        exercise_name_title.grid(row=3, column=2, pady=(20, 0), padx=20, sticky="w")
        self.exercise_name_entry.grid(row=4, column=2, pady=(5, 0), padx=20)
        date_title.grid(row=5, column=1, padx=20, pady=(20, 0), sticky="w")
        self.date_entry.grid(row=6, column=1, pady=(5, 0), padx=20)
        time_title.grid(row=5, column=2, pady=(20, 0), padx=20, sticky="w")
        self.time_entry.grid(row=6, column=2, pady=(5, 0), padx=20)
        sets_title.grid(row=7, column=1, pady=(20, 0), padx=20, sticky="w")
        self.sets_entry.grid(row=8, column=1, pady=(5, 0), padx=20)
        reps_title.grid(row=7, column=2, pady=(20, 0), padx=20, sticky="w")
        self.reps_entry.grid(row=8, column=2, pady=(5, 0), padx=20)
        weight_title.grid(row=9, column=1, pady=(20, 0), padx=20, sticky="w")
        self.weight_entry.grid(row=10, column=1, pady=(5, 10), padx=20)
        label_title.grid(row=9, column=2, pady=(20, 0), padx=20, sticky="w")
        self.label_entry.grid(row=10, column=2, pady=(5, 10), padx=20)
        self.error_message.grid(row=11, column=1, columnspan=2, pady=5, padx=20)
        self.add_exercise_btn.grid(row=12, column=1,pady=(10, 0), padx=20)
        self.redirect_btn.grid(row=12, column=2, pady=(10, 0), padx=20)

        self.exercise_name_entry.bind("<Key>", lambda event: custom_entry_limit_chars(event, self.exercise_name_entry, 30))
        self.date_entry.bind("<Key>", lambda event: custom_date_entry_validation(event, self.date_entry))
        self.time_entry.bind("<Key>", lambda event: custom_time_entry_validation(event, self.time_entry))
        self.label_entry.bind("<Key>", lambda event: custom_entry_limit_chars(event, self.label_entry, 100))
        self.sets_entry.bind("<Key>", lambda event: custom_digit_limit_entry_validation(event, self.sets_entry, 3))
        self.reps_entry.bind("<Key>", lambda event: custom_digit_limit_entry_validation(event, self.reps_entry, 3))
        self.weight_entry.bind("<Key>", lambda event: custom_digit_limit_entry_validation(event, self.weight_entry, 3))
        self.toggle_entry_type_icon.bind("<Button-1>", self.toggle_entry_type)

    def process_entry(self):
        if self.validate_entry_fields():
            data = self.get_entry_field_data()
            
            self.controller.db_cursor.execute("INSERT INTO exercise_entries (entry_type, exercise_label, date, time, exercise_name, sets_count, reps_count, weight_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data["type"], data["label"], data["date"], data["time"], data["exercise_name"], data["sets"], data["reps"], data["weight"]))
            self.controller.db_connection.commit()

            self.clear_entry_fields()
            # update the exercise summary section in the dashboard
            self.controller.pages[DashboardPage].update_exercise_summary()
            self.after_entry_submission()

    def process_confirmation(self):
        # confirm prompt to leave midway through filling form
        def proceed_confirmation():
            self.clear_entry_fields()
            # if prematurely exiting session entry page, ensure label is also cleared
            if self.entry_type == "session":
                self.label_entry.delete(0, ctk.END)
            confirmation_window.destroy()
            self.controller.show_page(DashboardPage)

        # check if the entry is validly filled or not
        incomplete_entry = False
        if not self.validate_entry_fields():
            incomplete_entry = True
        
        if incomplete_entry:
            confirmation_window = ctk.CTkToplevel(self.entry_form)
            confirmation_window.attributes("-topmost", "true")
            confirmation_window.title("Incomplete Entry Detected!")
            confirmation_window.geometry("600x150")
            message = ctk.CTkLabel(confirmation_window, text="Are you sure you want to leave the page without saving the entry?", font=("", 18))
            confirm_btn = ctk.CTkButton(confirmation_window, text="Confirm", font=("", 24), command=proceed_confirmation)
            cancel_btn = ctk.CTkButton(confirmation_window, text="Cancel", font=("", 24), command=confirmation_window.destroy)

            confirmation_window.grid_columnconfigure(0, weight=1)
            confirmation_window.grid_columnconfigure(3, weight=1)

            confirmation_window.grid_rowconfigure(0, weight=1)
            confirmation_window.grid_rowconfigure(3, weight=1)

            message.grid(row=1, column=1, columnspan=2, pady=(0, 10))
            confirm_btn.grid(row=2, column=1)
            cancel_btn.grid(row=2, column=2)

            self.controller.center_window(confirmation_window, 600, 150)
        else:
            # if entry is a session and valid, then process the entry accordingly before redirecting to dashboard
            if self.entry_type == "session":
                self.process_entry()
                self.label_entry.delete(0, ctk.END)
            # catch and clear user pressing the cancel button with a valid entry (filled)
            elif self.entry_type == "single":
                self.clear_entry_fields()
            self.controller.show_page(DashboardPage)

    def after_entry_submission(self):
        pass

    def get_entry_field_data(self):
        return {
            "type": self.type_entry.get(),
            "exercise_name": self.exercise_name_entry.get(),
            "date": self.date_entry.get(),
            "time": self.time_entry.get(),
            "label": self.label_entry.get(),
            "sets": self.sets_entry.get(),
            "reps": self.reps_entry.get(),
            "weight": self.weight_entry.get(),
        }
    
    def clear_entry_fields(self):
        for field in [
            self.exercise_name_entry,
            self.date_entry,
            self.time_entry,
            self.label_entry,
            self.sets_entry,
            self.reps_entry,
            self.weight_entry
        ]:
            field.delete(0, ctk.END)
    
    def validate_entry_fields(self):
        data = self.get_entry_field_data()
        for key, val in data.items():
            # if any fields aside from label is not filled
            if key not in ("label", "date") and len(val) < 1:
                self.controller.show_error_message(self.error_message, "All * fields need to be filled.")
                return False
            # if the date field has less than 10 characters/digits (ensures that there is a valid amount of digits inputted)
            if key == "date" and len(val) < 10:
                self.controller.show_error_message(self.error_message, "Date info incomplete. [dd-mm-yyyy]")
                return False
            # if the time field has less than 5 characters/digits (ensures that there is a valid amount of digits inputted)
            if key == "time" and len(val) < 5:
                self.controller.show_error_message(self.error_message, "Time info incomplete. [xx:xx]")
                return 
        # all fields have been filled (excl. label)
        return True

    # switch between the different types of entry pages via icon
    def toggle_entry_type(self, event=None):
        if self.entry_type == "single":
            self.clear_entry_fields()
            self.controller.show_page(SessionEntryPage)
        elif self.entry_type == "session":
            self.clear_entry_fields()
            self.label_entry.delete(0, ctk.END)
            self.controller.show_page(SingleEntryPage)

    # automatically insert today's date into the date entry field
    def reset_date(self):
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, self.today)

class SingleEntryPage(BaseEntryPage):
    def __init__(self, parent, controller):
        BaseEntryPage.__init__(self, parent, controller, "single", "Cancel")
        
    # override the toggle icon's image
    def create_widgets(self):
        super().create_widgets()
        self.toggle_entry_type_icon.configure(image=self.single_entry_icon)

    # ensure user is redirect to the dashboard after completing an singular entry
    def after_entry_submission(self):
        self.controller.show_page(DashboardPage)

class SessionEntryPage(BaseEntryPage):
    def __init__(self, parent, controller):
        BaseEntryPage.__init__(self, parent, controller, "session", "Completed")

    # override the toggle icon's image
    def create_widgets(self):
        super().create_widgets()
        self.toggle_entry_type_icon.configure(image=self.session_entry_icon)

    def clear_entry_fields(self):
        for field in [
            self.exercise_name_entry,
            self.date_entry,
            self.time_entry,
            self.sets_entry,
            self.reps_entry,
            self.weight_entry
        ]:
            field.delete(0, ctk.END)

class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        navbar = Navbar(self, self.controller)
        content = ctk.CTkFrame(self, fg_color="black", corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        dashboard_title = ctk.CTkLabel(content, text="This is the Statistics Page!", text_color="green")
        dashboard_title.pack()

class AchievementsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        navbar = Navbar(self, self.controller)
        content = ctk.CTkFrame(self, fg_color="black", corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        dashboard_title = ctk.CTkLabel(content, text="This is the Achievements Page!", text_color="green")
        dashboard_title.pack()

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # profile related vars
        self.profile_username_var = ctk.StringVar()
        self.profile_first_name_var = ctk.StringVar()
        self.profile_last_name_var = ctk.StringVar()
        self.profile_age_var = ctk.StringVar()
        self.profile_height_var = ctk.StringVar()
        self.profile_current_weight_var = ctk.StringVar()
        self.profile_goal_weight_var = ctk.StringVar()

        # daily related vars
        self.daily_sleep_var = ctk.StringVar()
        self.daily_walking_var = ctk.StringVar()
        self.daily_hydration_var = ctk.StringVar()

        # retrieve existing data and set daily variables with them
        # only look to retrieve data if a database has been created (i.e. user has registered)
        if self.controller.db.check_password_exists():
            # we can use rowid as the primary key reference because there will only always be a single entry in this table
            self.controller.db_cursor.execute("SELECT daily_sleep_goal, daily_steps_goal, daily_hydration_goal FROM profile_details WHERE rowid=1")
            result = self.controller.db_cursor.fetchone()
            self.daily_sleep_var.set(result[0])
            self.daily_walking_var.set(result[1])
            self.daily_hydration_var.set(result[2])
        
        # monthly related vars
        self.monthly_weight_choice_var = ctk.StringVar()
        self.monthly_weight_var = ctk.StringVar()
        self.monthly_hydration_var = ctk.StringVar()
        self.monthly_sleep_var = ctk.StringVar()
        self.monthly_walking_var = ctk.StringVar()

        # temp for compartmentalising internally.. will fix later and only use 1 checker for all variable data retrievals.
        if self.controller.db.check_password_exists():
            self.controller.db_cursor.execute("SELECT monthly_weight_choice, monthly_weight_goal, monthly_sleep_goal, monthly_steps_goal, monthly_hydration_goal FROM profile_details WHERE rowid=1")
            result = self.controller.db_cursor.fetchone()
            self.monthly_weight_choice_var.set(result[0])
            self.monthly_weight_var.set(result[1])
            self.monthly_hydration_var.set(result[2])
            self.monthly_sleep_var.set(result[3])
            self.monthly_walking_var.set(result[4])

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
        content.grid_rowconfigure(6, weight=1)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)
        #endregion

        #region [Parent Frames]
        page_title = ctk.CTkLabel(content, text="Settings", font=("", 24))
        page_message = ctk.CTkLabel(content, text="Update your information here", font=("", 14))
        self.profile_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=900, height=650)
        self.daily_goals_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=900, height=430)
        self.monthly_goals_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=900, height=450)

        self.profile_section.grid_propagate(False)
        self.daily_goals_section.grid_propagate(False)
        self.monthly_goals_section.grid_propagate(False)
        
        page_title.grid(row=1, column=1, pady=(30, 0), sticky="w", padx=(0, 1000))
        page_message.grid(row=2, column=1, sticky="w", pady=(0, 50))
        self.profile_section.grid(row=3, column=1, pady=(0, 50))
        self.daily_goals_section.grid(row=4, column=1, pady=(0, 50))
        self.monthly_goals_section.grid(row=5, column=1, pady=(0, 50))
        #endregion

        #region [Profile Section]
        profile_title = ctk.CTkLabel(self.profile_section, text="Profile Details", font=("", 18))
        profile_image_title = ctk.CTkLabel(self.profile_section, text="Profile Image:", font=("", 18))
        profile_browse_image_select = ctk.CTkButton(self.profile_section, text="Browse Image", font=("", 18), command=self.browse_new_profile_image)
        self.profile_image_preview = ctk.CTkLabel(self.profile_section, text="")
        self.profile_image_message = ctk.CTkLabel(self.profile_section, text="", font=("", 14))
        profile_username_title = ctk.CTkLabel(self.profile_section, text="Username:", font=("", 18))
        self.profile_username_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_username_var)
        profile_first_name_title = ctk.CTkLabel(self.profile_section, text="First Name:", font=("", 18))
        self.profile_first_name_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_first_name_var)
        profile_last_name_title = ctk.CTkLabel(self.profile_section, text="Last Name:", font=("", 18))
        self.profile_last_name_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_last_name_var)
        profile_age_title = ctk.CTkLabel(self.profile_section, text="Age:", font=("", 18))
        self.profile_age_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_age_var)
        profile_height_title = ctk.CTkLabel(self.profile_section, text="Height (cm):", font=("", 18))
        self.profile_height_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_height_var)
        profile_current_weight_title = ctk.CTkLabel(self.profile_section, text="Current Weight (kg):", font=("", 18))
        self.profile_current_weight_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_current_weight_var)
        profile_goal_weight_title = ctk.CTkLabel(self.profile_section, text="Goal Weight (kg):", font=("", 18))
        self.profile_goal_weight_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_goal_weight_var)
        self.profile_action_message = ctk.CTkLabel(self.profile_section, text="", font=("", 18))
        profile_update_button = ctk.CTkButton(self.profile_section, height=60, width=200, text="Update Profile", font=("", 24), command=self.process_profile)

        profile_title.grid(row=0, column=0, sticky="w", padx=30, pady=30)
        profile_image_title.grid(row=1, column=0, padx=30, sticky="w")
        profile_browse_image_select.grid(row=2, column=0, padx=30, pady=10)
        self.profile_image_preview.grid(row=3, column=0, padx=30)
        self.profile_image_message.grid(row=4, column=0, padx=30)
        profile_username_title.grid(row=1, column=1, padx=30, sticky="w")
        self.profile_username_entry.grid(row=2, column=1, padx=30)
        profile_first_name_title.grid(row=5, column=0, padx=30, sticky="w")
        self.profile_first_name_entry.grid(row=6, column=0, padx=30)
        profile_last_name_title.grid(row=5, column=1, padx=30, sticky="w")
        self.profile_last_name_entry.grid(row=6, column=1, padx=30)
        profile_age_title.grid(row=7, column=0, padx=30, pady=(30, 0), sticky="w")
        self.profile_age_entry.grid(row=8, column=0, padx=30)
        profile_height_title.grid(row=7, column=1, padx=30, pady=(30, 0), sticky="w")
        self.profile_height_entry.grid(row=8, column=1, padx=30)
        profile_current_weight_title.grid(row=9, column=0, padx=30, pady=(30, 0), sticky="w")
        self.profile_current_weight_entry.grid(row=10, column=0, padx=30)
        profile_goal_weight_title.grid(row=9, column=1, padx=30, pady=(30, 0), sticky="w")
        self.profile_goal_weight_entry.grid(row=10, column=1, padx=30)
        self.profile_action_message.grid(row=11, column=0, columnspan=2, pady=20)
        profile_update_button.grid(row=12, column=0, columnspan=2)

        # profile related binds
        self.profile_username_entry.bind("<Key>", lambda event: custom_word_only_entry_validation(event, self.profile_username_entry, None))
        self.profile_first_name_entry.bind("<Key>", lambda event: custom_word_only_entry_validation(event, self.profile_first_name_entry, 13))
        self.profile_last_name_entry.bind("<Key>", lambda event: custom_word_only_entry_validation(event, self.profile_last_name_entry, 13))
        self.profile_age_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_age_entry, 3))
        self.profile_height_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_height_entry, 3))
        self.profile_current_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_current_weight_entry, 3))
        self.profile_goal_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_goal_weight_entry, 3))

        #endregion

        #region [Daily Section]
        daily_title = ctk.CTkLabel(self.daily_goals_section, text="Daily Goals", font=("", 18))
        daily_sleep_title = ctk.CTkLabel(self.daily_goals_section, text="Sleep (Minutes):", font=("", 24))
        self.daily_sleep_entry = ctk.CTkEntry(self.daily_goals_section, font=("", 24), width=350, textvariable=self.daily_sleep_var)
        daily_walking_title = ctk.CTkLabel(self.daily_goals_section, text="Walking (Steps):", font=("", 24))
        self.daily_walking_entry = ctk.CTkEntry(self.daily_goals_section, font=("", 24), width=350, textvariable=self.daily_walking_var)
        daily_hydration_title = ctk.CTkLabel(self.daily_goals_section, text="Hydration (Millilitres):", font=("", 24))
        self.daily_hydration_entry = ctk.CTkEntry(self.daily_goals_section, font=("", 24), width=350, textvariable=self.daily_hydration_var)
        self.daily_action_message = ctk.CTkLabel(self.daily_goals_section, text="", font=("", 18))
        daily_update_button = ctk.CTkButton(self.daily_goals_section, text="Update Goals", height=60, width=200, font=("", 24), command=self.process_daily_goals)

        daily_title.grid(row=0, column=0, sticky="w", padx=30, pady=30)
        daily_sleep_title.grid(row=1, column=0, padx=30, sticky="w")
        self.daily_sleep_entry.grid(row=2, column=0, padx=30, pady=(5, 0))
        daily_walking_title.grid(row=1, column=1, padx=30, sticky="w")
        self.daily_walking_entry.grid(row=2, column=1, padx=30, pady=(5, 0))
        daily_hydration_title.grid(row=3, column=0, padx=30, pady=(30, 0), sticky="w")
        self.daily_hydration_entry.grid(row=4, column=0, padx=30, pady=(5, 0))
        self.daily_action_message.grid(row=5, column=0, columnspan=2, pady=20)
        daily_update_button.grid(row=6, column=0, columnspan=2)

        # daily related binds
        self.daily_sleep_entry.bind("<Key>", lambda event: custom_float_only_validation(event, self.daily_sleep_entry, 3))
        self.daily_walking_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.daily_walking_entry, 5))
        self.daily_hydration_entry.bind("<Key>", lambda event: custom_float_only_validation(event, self.daily_hydration_entry, 4))

        #endregion

        #region [Monthly Section]
        monthly_title = ctk.CTkLabel(self.monthly_goals_section, text="Monthly Goals", font=("", 18))
        lose_weight_button = ctk.CTkButton(self.monthly_goals_section, text="Lose Weight", height=40, font=("", 18))
        gain_weight_button = ctk.CTkButton(self.monthly_goals_section, text="Gain Weight", height=40, font=("", 18))
        self.monthly_weight_entry = ctk.CTkEntry(self.monthly_goals_section, font=("", 24), width=350, textvariable=self.monthly_weight_var)
        monthly_hydration_title = ctk.CTkLabel(self.monthly_goals_section, text="Hydration (L):", font=("", 24))
        self.monthly_hydration_entry = ctk.CTkEntry(self.monthly_goals_section, font=("", 24), width=350, textvariable=self.monthly_hydration_var)
        monthly_sleep_title = ctk.CTkLabel(self.monthly_goals_section, text="Sleep (Hrs):", font=("", 24))
        self.monthly_sleep_entry = ctk.CTkEntry(self.monthly_goals_section, font=("", 24), width=350, textvariable=self.monthly_sleep_var)
        monthly_walking_title = ctk.CTkLabel(self.monthly_goals_section, text="Walking (Steps):", font=("", 24))
        self.monthly_walking_entry = ctk.CTkEntry(self.monthly_goals_section, font=("", 24), width=350, textvariable=self.monthly_walking_var)
        self.monthly_action_message = ctk.CTkLabel(self.monthly_goals_section, text="", font=("", 18))
        monthly_update_button = ctk.CTkButton(self.monthly_goals_section, text="Update Goals", height=60, width=200, font=("", 24), command=self.process_monthly_goals)

        monthly_title.grid(row=0, column=0, sticky="w", padx=30, pady=30)
        lose_weight_button.grid(row=1, column=0, padx=(30, 0), pady=(0, 10), sticky="nw")
        gain_weight_button.grid(row=1, column=1, pady=(0, 10), sticky="w")
        self.monthly_weight_entry.grid(row=2, column=0, columnspan=2, padx=30)
        monthly_hydration_title.grid(row=1, column=2, padx=30, pady=(0, 10), sticky="w")
        self.monthly_hydration_entry.grid(row=2, column=2, padx=30)
        monthly_sleep_title.grid(row=3, column=0, columnspan=2, padx=30, pady=(30, 0), sticky="w")
        self.monthly_sleep_entry.grid(row=4, column=0, columnspan=2, padx=30, pady=(5, 0))
        monthly_walking_title.grid(row=3, column=2, padx=30, pady=(30, 0), sticky="w")
        self.monthly_walking_entry.grid(row=4, column=2, padx=30, pady=(5, 0))
        self.monthly_action_message.grid(row=5, column=0, columnspan=3, pady=20)
        monthly_update_button.grid(row=6, column=0, columnspan=3)

        # monthly related binds
        self.monthly_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.monthly_weight_entry, 2))
        self.monthly_hydration_entry.bind("<Key>", lambda event: custom_float_only_validation(event, self.monthly_hydration_entry, 6))
        self.monthly_sleep_entry.bind("<Key>", lambda event: custom_float_only_validation(event, self.monthly_sleep_entry, 5))
        self.monthly_walking_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.monthly_walking_entry, 7))

        #endregion

    # allow user to search their local storage for a new profile image (.png only)
    def browse_new_profile_image(self):
        file_path = filedialog.askopenfilename(title="Select New Profile Image", filetypes=[('Image Files', '*.png')])
        if file_path:
            # generate temp rounded profile image
            generate_round_frame_image(file_path, "temp_profile_image")
            temp_profile_image = Image.open("img/temp_profile_image.png")
            # newly selected profile image storage
            new_profile_image = ctk.CTkImage(light_image=temp_profile_image, dark_image=temp_profile_image, size=(128, 128))
            # increase section box area size to accomodate new widgets
            self.profile_section.configure(height=760)
            # showcase the selected image
            self.profile_image_preview.configure(image=new_profile_image)
            # display informative message to user about their action
            self.profile_image_message.configure(text="Image Preview")

    # updates the profile set by user
    def process_profile(self):
        username = self.profile_username_var.get()
        first_name = self.profile_first_name_var.get()
        last_name = self.profile_last_name_var.get()
        age = self.profile_age_var.get()
        height = self.profile_height_var.get()
        current_weight = self.profile_current_weight_var.get()
        goal_weight = self.profile_goal_weight_var.get()
        update_profile_details_query = """
        UPDATE profile_details
        SET username = ?,
        first_name = ?,
        last_name = ?,
        age = ?,
        height = ?,
        current_weight = ?,
        goal_weight = ?
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(update_profile_details_query, (username, first_name, last_name, age, height, current_weight, goal_weight))
        self.controller.db_connection.commit()

        # update the user profile image IF there is a new image selected in the preview
        self.update_user_profile_img()

        self.show_action_message(self.profile_action_message)

    # updates the daily goals set by user
    def process_daily_goals(self):
        sleep = float(self.daily_sleep_var.get())
        steps = int(self.daily_walking_var.get())
        hydration = float(self.daily_hydration_var.get())
        
        # limiters in place to help discourage user from aiming for a dangerous lifestyle
        if sleep > 540.00:
            sleep = 540.00
        if steps > 99999:
            steps = 99999
        if hydration > 9999.99:
            hydration = 9999.99

        update_daily_goals_query = """
        UPDATE profile_details
        SET daily_sleep_goal = ?,
        daily_steps_goal = ?,
        daily_hydration_goal = ?
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(update_daily_goals_query, (sleep, steps, hydration))
        self.controller.db_connection.commit()
        self.show_action_message(self.daily_action_message)
        # reinitialise the daily trackers with the updated data
        self.controller.pages[DashboardPage].update_daily_goal_progression_displays()

    # updates the monthly goals set by user
    def process_monthly_goals(self):
        weight_choice = self.monthly_weight_choice_var.get()
        weight = int(self.monthly_weight_var.get())
        steps = int(self.monthly_walking_var.get())
        hydration = float(self.monthly_hydration_var.get())
        sleep = float(self.monthly_sleep_var.get())

        # 10kg weight loss/gain limit per month
        if weight > 10:
            weight = 10
        # 540.00 min per day x 31 days
        if sleep > 16740.00:
            sleep = 16740.00
        # 9999.99 ml per day x 31 days
        if hydration > 309999.99:
            hydration = 309999.99
        # 99999 steps per day x 31 days
        if steps > 3099999:
            steps = 3099999

        update_monthly_goals_query = """
        UPDATE profile_details
        SET monthly_weight_choice = ?, 
        monthly_weight_goal = ?,
        monthly_steps_goal = ?,
        monthly_hydration_goal = ?,
        monthly_sleep_goal = ?
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(update_monthly_goals_query, (weight_choice, weight, steps, hydration, sleep))
        self.controller.db_connection.commit()
        self.show_action_message(self.monthly_action_message)

    # display a temporary notification letting the user know of the successful action
    def show_action_message(self, section_widget):
        # list out the possible messages based on given widget
        section_messages = {
            self.profile_action_message: "Profile Successfully Updated.",
            self.daily_action_message: "Daily Goals Successfully Updated.",
            self.monthly_action_message: "Monthly Goals Successfully Updated."
        }
        # updated the widgets text
        section_widget.configure(text=section_messages[section_widget], text_color="#2E7D32")
        # reset to an empty string after a delayed time
        section_widget.after(800, lambda: section_widget.configure(text=""))
           
    # retrieve the current saved data related to each section (if there is any)
    # and populate entry with it
    def retrieve_current_info(self):
        # listed profile detail initialised variables in order of sql table
        entry_vars = [
            self.profile_username_var,
            self.profile_first_name_var,
            self.profile_last_name_var,
            self.profile_age_var,
            self.profile_height_var,
            self.profile_current_weight_var, 
            self.profile_goal_weight_var,
            self.daily_sleep_var,
            self.daily_walking_var,
            self.daily_hydration_var,
            self.monthly_weight_var,
            self.monthly_hydration_var,
            self.monthly_sleep_var,
            self.monthly_walking_var
        ]
        retrieve_current_data = """
        SELECT 
            username,
            first_name,
            last_name,
            age,
            height,
            current_weight,
            goal_weight,
            daily_sleep_goal,
            daily_steps_goal,
            daily_hydration_goal,
            monthly_weight_goal,
            monthly_hydration_goal,
            monthly_sleep_goal,
            monthly_steps_goal
        FROM profile_details 
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(retrieve_current_data)
        result = self.controller.db_cursor.fetchone()
        # only proceed with updating entry fields if there is stored data found
        if result:
            # loop through and set each variable with its saved data from the database
            for i in range(len(result)):
                entry_vars[i].set(result[i])

        self.reset_profile_preview()

    # update the user's profile image
    def update_user_profile_img(self):
        # updating user's profile image
        # check if a temp profile image exists aka user has selected a new image
        if os.path.isfile("img/temp_profile_image.png"):
            # log check
            print('temp profile image found!')
            # open the new profile image that's temporarily stored
            temp_image = Image.open("img/temp_profile_image.png")
            # update the user's profile image by overriding the user_profile.png by just renaming the new desire as 'user_profile.png'
            temp_image.save("img/user_profile.png")
            # remove the temporary image save -> 'temp_profile_image.png'
            os.remove("img/temp_profile_image.png")
        # updates the profile image on the dashboard in simultaneously
        self.controller.pages[DashboardPage].update_profile_image()

    # reset the profile image preview display
    def reset_profile_preview(self):
        self.profile_image_preview.configure(image=None)
        # check to see if a temp profile image has been saved
        if os.path.isfile("img/temp_profile_image.png"):
            # if so, delete the temp image
            os.remove("img/temp_profile_image.png")
        # only viable solution after testing ->
        # destroy the label widget and re-implement due to internal ctk cavas redraw issues with images
        self.profile_image_preview.destroy()
        self.profile_image_preview = ctk.CTkLabel(self.profile_section, text="")
        self.profile_image_preview.grid(row=3, column=0, padx=30)
        self.profile_image_message.configure(text="")
        self.profile_section.configure(height=650)

if __name__ == "__main__":
    app = Windows()
    app.mainloop()


