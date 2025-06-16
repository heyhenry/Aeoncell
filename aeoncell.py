import customtkinter as ctk
from tkinter import filedialog
from database_manager import DatabaseManager
import sqlite3
from datetime import date
from aeoncell_utils import *
from PIL import Image
import os
from CTkXYFrame import *

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
        self.geometry("1280x800")
        self.minsize(1280, 800)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nswe")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # set the username's value if possible
        if self.db.check_password_exists():
            self.set_username()

        self.pages = {}
        for P in (RegisterPage, LoginPage, DashboardPage, DiscoverPage, SingleEntryPage, SessionEntryPage, StatsPage, AchievementsPage, SettingsPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        # center the app upon startup
        self.center_window(self, 1280, 800)

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
        elif selected_page == SettingsPage:
            page.retrieve_current_info()

        page.tkraise()
        
        # loading logs for dashboard latest 25 entries display

    # set cursor focus to chosen field
    def set_initial_focus(self, widget_name):
        self.after(300, widget_name.focus_set)

    # checks to see if an entry for the daily trackers have been created for today
    # if not, the daily trackers will be created
    def auto_create_daily_tracking_entries(self):
        self.db_cursor.execute("SELECT exists (SELECT 1 FROM steps_tracker WHERE date = ?)", (self.today,))
        if not 1 in self.db_cursor.fetchone():
            self.db_cursor.execute("INSERT INTO steps_tracker (date) VALUES (?)", (self.today,))
            self.db_cursor.execute("INSERT INTO hydration_tracker (date) VALUES (?)", (self.today,))
            self.db_cursor.execute("INSERT INTO sleep_tracker (date) VALUES (?)", (self.today,))
            
        self.db_connection.commit()

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
        self.profile_image = ctk.CTkImage(light_image=Image.open("img/user_profile.png"), dark_image=Image.open("img/user_profile.png"), size=(128, 128))

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        navbar = Navbar(self, self.controller)
        content = ctk.CTkScrollableFrame(self, corner_radius=0)
        
        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(7, weight=1)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)

        intro_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=100)
        profile_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=400)
        subtitle_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=200)
        dailies_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=200)
        quick_stats_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=200)
        recent_exercises_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=200)

        intro_section.grid_propagate(False)
        profile_section.grid_propagate(False)
        subtitle_section.grid_propagate(False)
        dailies_section.grid_propagate(False)
        quick_stats_section.grid_propagate(False)
        recent_exercises_section.grid_propagate(False)

        intro_section.grid(row=1, column=1, pady=20)
        profile_section.grid(row=2, column=1, pady=(0, 20))
        subtitle_section.grid(row=3, column=1, pady=(0, 20))
        dailies_section.grid(row=4, column=1, pady=(0, 20))
        quick_stats_section.grid(row=5, column=1)
        recent_exercises_section.grid(row=6, column=1, pady=20)

        profile_section.grid_rowconfigure(0, weight=1)
        profile_section.grid_rowconfigure(2, weight=1)
        profile_section.grid_columnconfigure(0, weight=1)
        profile_section.grid_columnconfigure(4, weight=1)

        # introduction section
        hello_message = ctk.CTkLabel(intro_section, text=f"Hello, Henry", font=("", 32))
        motivational_message = ctk.CTkLabel(intro_section, text="Keep Moving & Stay Healthy")
        current_date = ctk.CTkLabel(intro_section, text="12 October 2025", font=("", 18))
        date_icon = ctk.CTkLabel(intro_section, text="", image=self.icon)
        motivation_button = ctk.CTkButton(intro_section, text="", image=self.icon, width=0, height=0, fg_color="#F0E9FF", hover_color="#F0E9FF")

        hello_message.grid(row=0, column=0, sticky="w", padx=(50, 0), pady=(20, 0))
        motivational_message.grid(row=1, column=0, sticky="w", padx=(50, 0))
        current_date.grid(row=0, rowspan=2, column=1, sticky="e", padx=(550, 0), pady=(20, 0))
        date_icon.grid(row=0, rowspan=2, column=2, sticky="e", padx=(20, 0), pady=(20, 0))
        motivation_button.grid(row=0, rowspan=2, column=3, sticky="e", padx=(20, 0), pady=(20, 0))

        # profile section
        profile_info_section = ctk.CTkFrame(profile_section, border_color="green", border_width=1)
        profile_image = ctk.CTkLabel(profile_info_section, text="", image=self.profile_image)
        profile_name = ctk.CTkLabel(profile_info_section, text="Jojo Bizzaro", font=("", 24))
        profile_height_title = ctk.CTkLabel(profile_info_section, text="Height", font=("", 14, "bold"))
        profile_height_frame = ctk.CTkFrame(profile_info_section, border_width=1, border_color="black", corner_radius=15, width=100, height=50)
        profile_height_display = ctk.CTkLabel(profile_height_frame, text="177cm", font=("", 18))
        profile_weight_title = ctk.CTkLabel(profile_info_section, text="Weight", font=("", 14, "bold"))
        profile_weight_frame = ctk.CTkFrame(profile_info_section, border_width=1, border_color="black", corner_radius=15, width=100, height=50)
        profile_weight_display = ctk.CTkLabel(profile_weight_frame, text="93kg", font=("", 18))
        profile_age_title = ctk.CTkLabel(profile_info_section, text="Age", font=("", 14, "bold"))
        profile_age_frame = ctk.CTkFrame(profile_info_section, border_width=1, border_color="black", corner_radius=15, width=100, height=50)
        profile_age_display = ctk.CTkLabel(profile_age_frame, text="43yo", font=("", 18))
        profile_monthly_section = ctk.CTkFrame(profile_section, border_color="blue", border_width=1)
        profile_monthly_title = ctk.CTkLabel(profile_monthly_section, text="Monthly Progress", font=("", 24))
        profile_monthly_weight_title = ctk.CTkLabel(profile_monthly_section, text="Weight Loss", font=("", 18))
        profile_monthly_weight_info = ctk.CTkLabel(profile_monthly_section, text="2/5 kilos", font=("", 14))
        profile_monthly_weight_progressbar = ctk.CTkProgressBar(profile_monthly_section, height=30, width=350)
        profile_monthly_weight_progressbar.set(0.30)
        profile_sleep_title = ctk.CTkLabel(profile_monthly_section, text="Sleep", font=("", 18))
        profile_sleep_info = ctk.CTkLabel(profile_monthly_section, text="110/300 hours", font=("", 14))
        profile_sleep_progressbar = ctk.CTkProgressBar(profile_monthly_section, height=30, width=350)
        profile_sleep_progressbar.set(0.35)
        profile_hydration_title = ctk.CTkLabel(profile_monthly_section, text="Hydration", font=("", 18)) 
        profile_hydration_info = ctk.CTkLabel(profile_monthly_section, text="80/250 litres", font=("", 14))
        profile_hydration_progressbar = ctk.CTkProgressBar(profile_monthly_section, height=30, width=350)
        profile_hydration_progressbar.set(0.45)
        profile_walking_title = ctk.CTkLabel(profile_monthly_section, text="Walking", font=("", 18))
        profile_walking_info = ctk.CTkLabel(profile_monthly_section, text="35,000/150,000 steps", font=("", 14))
        profile_walking_progressbar = ctk.CTkProgressBar(profile_monthly_section, height=30, width=350)
        profile_walking_progressbar.set(0.70)
        profile_achievements_section = ctk.CTkFrame(profile_section, border_color="red", border_width=1)
        first_badge_spot = ctk.CTkButton(profile_achievements_section, text="BADGE 1", font=("", 24))
        second_badge_spot = ctk.CTkButton(profile_achievements_section, text="BADGE 2", font=("", 24))
        third_badge_spot = ctk.CTkButton(profile_achievements_section, text="BADGE 3", font=("", 24))  

        # main frames inside profile section
        profile_info_section.grid(row=1, column=1, padx=(10, 50))
        profile_monthly_section.grid(row=1, column=2)
        profile_achievements_section.grid(row=1, column=3, padx=(50, 10))
        
        # profile info section
        profile_image.grid(row=0, column=0, columnspan=3, pady=(20, 0))
        profile_name.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        profile_height_title.grid(row=2, column=0, padx=(0, 10), pady=(20, 0))
        profile_height_frame.grid(row=3, column=0, padx=20, pady=(0, 20))
        profile_height_frame.grid_propagate(False)
        profile_height_frame.grid_rowconfigure(0, weight=1)
        profile_height_frame.grid_columnconfigure(0, weight=1)
        profile_height_display.grid(row=0, column=0, padx=10, pady=10)
        profile_weight_title.grid(row=2, column=1, padx=(0, 10),  pady=(20, 0))
        profile_weight_frame.grid(row=3, column=1, pady=(0, 20))
        profile_weight_frame.grid_propagate(False)
        profile_weight_frame.grid_rowconfigure(0, weight=1)
        profile_weight_frame.grid_columnconfigure(0, weight=1)
        profile_weight_display.grid(row=0, column=0, padx=10, pady=10)
        profile_age_title.grid(row=2, column=2, padx=(0, 10),  pady=(20, 0))
        profile_age_frame.grid(row=3, column=2, padx=20, pady=(0, 20))
        profile_age_frame.grid_propagate(False)
        profile_age_frame.grid_rowconfigure(0, weight=1)
        profile_age_frame.grid_columnconfigure(0, weight=1)
        profile_age_display.grid(row=0, column=0, padx=10, pady=10)

        # profile monthly section
        profile_monthly_title.grid(row=0, column=0, columnspan=2, pady=(20, 0))
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

        self.single_entry_icon = ctk.CTkImage(light_image=Image.open("img/small_flame.png"), dark_image=Image.open("img/small_flame.png"), size=(48, 48))
        self.session_entry_icon = ctk.CTkImage(light_image=Image.open("img/big_flame.png"), dark_image=Image.open("img/big_flame.png"), size=(48, 48))

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

        incomplete_entry = False
        data = self.get_entry_field_data()
        for key, val in data.items():
            if key != "type" and len(val) == 0:
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
            if key != "label" and len(val) < 1:
                self.controller.show_error_message(self.error_message, "All * fields need to be filled.")
                return False
            elif key == "date" and len(val) < 10:
                self.controller.show_error_message(self.error_message, "Date info incomplete. [dd-mm-yyyy]")
                return False
            elif key == "time" and len(val) < 5:
                self.controller.show_error_message(self.error_message, "Time info incomplete. [xx:xx]")
                return False
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
        
        # monthly related vars
        self.monthly_weight_choice_var = ctk.StringVar()
        self.monthly_weight_var = ctk.StringVar()
        self.monthly_hydration_var = ctk.StringVar()
        self.monthly_sleep_var = ctk.StringVar()
        self.monthly_walking_var = ctk.StringVar()

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        navbar = Navbar(self, self.controller)
        content = ctk.CTkScrollableFrame(self, corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(6, weight=1)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)

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

        # profile section
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

        # daily section
        daily_title = ctk.CTkLabel(self.daily_goals_section, text="Daily Goals", font=("", 18))
        daily_sleep_title = ctk.CTkLabel(self.daily_goals_section, text="Sleep (Hrs):", font=("", 24))
        self.daily_sleep_entry = ctk.CTkEntry(self.daily_goals_section, font=("", 24), width=350, textvariable=self.daily_sleep_var)
        daily_walking_title = ctk.CTkLabel(self.daily_goals_section, text="Walking (Steps):", font=("", 24))
        self.daily_walking_entry = ctk.CTkEntry(self.daily_goals_section, font=("", 24), width=350, textvariable=self.daily_walking_var)
        daily_hydration_title = ctk.CTkLabel(self.daily_goals_section, text="Hydration (L):", font=("", 24))
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

        # monthly section
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

        # profile related binds
        self.profile_username_entry.bind("<Key>", lambda event: custom_word_only_entry_validation(event, self.profile_username_entry, None))
        self.profile_first_name_entry.bind("<Key>", lambda event: custom_word_only_entry_validation(event, self.profile_first_name_entry, None))
        self.profile_last_name_entry.bind("<Key>", lambda event: custom_word_only_entry_validation(event, self.profile_last_name_entry, None))
        self.profile_age_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_age_entry, 3))
        self.profile_height_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_height_entry, 3))
        self.profile_current_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_current_weight_entry, 3))
        self.profile_goal_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_goal_weight_entry, 3))

        # daily related binds
        self.daily_sleep_entry.bind("<Key>", lambda event: custom_float_only_entry_validation(event, self.daily_sleep_entry))
        self.daily_walking_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.daily_walking_entry, None))
        self.daily_hydration_entry.bind("<Key>", lambda event: custom_float_only_entry_validation(event, self.daily_hydration_entry))

        # monthly related binds
        self.monthly_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.monthly_weight_entry, 2))
        self.monthly_hydration_entry.bind("<Key>", lambda event: custom_float_only_entry_validation(event, self.monthly_hydration_entry))
        self.monthly_sleep_entry.bind("<Key>", lambda event: custom_float_only_entry_validation(event, self.monthly_sleep_entry))
        self.monthly_walking_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.monthly_walking_entry, None))

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
        sleep = self.daily_sleep_var.get()
        steps = self.daily_walking_var.get()
        hydration = self.daily_hydration_var.get()
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

    # updates the monthly goals set by user
    def process_monthly_goals(self):
        weight = self.monthly_weight_var.get()
        steps = self.monthly_walking_var.get()
        hydration = self.monthly_hydration_var.get()
        sleep = self.monthly_sleep_var.get()
        update_monthly_goals_query = """
        UPDATE profile_details
        SET monthly_weight_goal = ?,
        monthly_steps_goal = ?,
        monthly_hydration_goal = ?,
        monthly_sleep_goal = ?
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(update_monthly_goals_query, (weight, steps, hydration, sleep))
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
        SELECT * FROM profile_details WHERE rowid=1
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


