import customtkinter as ctk
from tkinter import ttk as btk
from database_manager import DatabaseManager
import sqlite3
from datetime import date
from aeoncell_utils import *
from PIL import Image, ImageTk, ImageOps, ImageDraw

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
        self.user_profile_img = ctk.CTkImage(light_image=Image.open("img/user_profile_rounded.png"), dark_image=Image.open("img/user_profile_rounded.png"), size=(120,120))
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

        self.show_page(DashboardPage)
        # if self.db.check_password_exists():
        #     self.show_page(LoginPage)
        # else:
        #     self.show_page(RegisterPage)

    # display the selected page to the user
    def show_page(self, selected_page):
        page = self.pages[selected_page]
        page.tkraise()

        # field focus config on startup for pages
        if selected_page == RegisterPage:
            self.set_initial_focus(page.username_entry)
        elif selected_page == LoginPage:
            self.set_initial_focus(page.password_entry)

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

        self.dashboard_icon.bind("<Enter>", lambda event: self.display_underline(self.dashboard_icon, self.dashboard_title))
        self.dashboard_icon.bind("<Leave>", lambda event: self.undisplay_underline(self.dashboard_icon, self.dashboard_title))
        self.dashboard_icon.bind("<Button-1>", lambda event: self.controller.show_page(DashboardPage))
        self.dashboard_title.bind("<Enter>", lambda event: self.display_underline(self.dashboard_icon, self.dashboard_title))
        self.dashboard_title.bind("<Leave>", lambda event: self.undisplay_underline(self.dashboard_icon, self.dashboard_title))
        self.dashboard_title.bind("<Button-1>", lambda event: self.controller.show_page(DashboardPage))
        self.discover_icon.bind("<Enter>", lambda event: self.display_underline(self.discover_icon, self.discover_title))
        self.discover_icon.bind("<Leave>", lambda event: self.undisplay_underline(self.discover_icon, self.discover_title))
        self.discover_icon.bind("<Button-1>", lambda event: self.controller.show_page(DiscoverPage))
        self.discover_title.bind("<Enter>", lambda event: self.display_underline(self.discover_icon, self.discover_title))
        self.discover_title.bind("<Leave>", lambda event: self.undisplay_underline(self.discover_icon, self.discover_title))
        self.discover_title.bind("<Button-1>", lambda event: self.controller.show_page(DiscoverPage))
        self.entry_icon.bind("<Enter>", lambda event: self.display_underline(self.entry_icon, self.entry_title))
        self.entry_icon.bind("<Leave>", lambda event: self.undisplay_underline(self.entry_icon, self.entry_title))
        self.entry_icon.bind("<Button-1>", lambda event: self.controller.show_page(SingleEntryPage))
        self.entry_title.bind("<Enter>", lambda event: self.display_underline(self.entry_icon, self.entry_title))
        self.entry_title.bind("<Leave>", lambda event: self.undisplay_underline(self.entry_icon, self.entry_title))
        self.entry_title.bind("<Button-1>", lambda event: self.controller.show_page(SingleEntryPage))
        self.stats_icon.bind("<Enter>", lambda event: self.display_underline(self.stats_icon, self.stats_title))
        self.stats_icon.bind("<Leave>", lambda event: self.undisplay_underline(self.stats_icon, self.stats_title))
        self.stats_icon.bind("<Button-1>", lambda event: self.controller.show_page(StatsPage))
        self.stats_title.bind("<Enter>", lambda event: self.display_underline(self.stats_icon, self.stats_title))
        self.stats_title.bind("<Leave>", lambda event: self.undisplay_underline(self.stats_icon, self.stats_title))
        self.stats_title.bind("<Button-1>", lambda event: self.controller.show_page(StatsPage))
        self.achievements_icon.bind("<Enter>", lambda event: self.display_underline(self.achievements_icon, self.achievements_title))
        self.achievements_icon.bind("<Leave>", lambda event: self.undisplay_underline(self.achievements_icon, self.achievements_title))
        self.achievements_icon.bind("<Button-1>", lambda event: self.controller.show_page(AchievementsPage))
        self.achievements_title.bind("<Enter>", lambda event: self.display_underline(self.achievements_icon, self.achievements_title))
        self.achievements_title.bind("<Leave>", lambda event: self.undisplay_underline(self.achievements_icon, self.achievements_title))
        self.achievements_title.bind("<Button-1>", lambda event: self.controller.show_page(AchievementsPage))
        self.settings_icon.bind("<Enter>", lambda event: self.display_underline(self.settings_icon, self.settings_title))
        self.settings_icon.bind("<Leave>", lambda event: self.undisplay_underline(self.settings_icon, self.settings_title))
        self.settings_icon.bind("<Button-1>", lambda event: self.controller.show_page(SettingsPage))
        self.settings_title.bind("<Enter>", lambda event: self.display_underline(self.settings_icon, self.settings_title))
        self.settings_title.bind("<Leave>", lambda event: self.undisplay_underline(self.settings_icon, self.settings_title))
        self.settings_title.bind("<Button-1>", lambda event: self.controller.show_page(SettingsPage))
        self.logout_icon.bind("<Enter>", lambda event: self.display_underline(self.logout_icon, self.logout_title))
        self.logout_icon.bind("<Leave>", lambda event: self.undisplay_underline(self.logout_icon, self.logout_title))
        self.logout_icon.bind("<Button-1>", lambda event: self.controller.show_page(LoginPage))
        self.logout_title.bind("<Enter>", lambda event: self.display_underline(self.logout_icon, self.logout_title))
        self.logout_title.bind("<Leave>", lambda event: self.undisplay_underline(self.logout_icon, self.logout_title))
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
        self.password_entry = ctk.CTkEntry(login_form, textvariable=self.password_var, font=("", 24), width=300)
        toggle_password_mask = ctk.CTkButton(login_form, text="", image=self.masked_password_icon, bg_color="transparent", fg_color="transparent", hover_color="#B19CD9", width=0)
        self.error_message = ctk.CTkLabel(login_form, text="", font=("", 18))
        login_submit = ctk.CTkButton(login_form, text="Login", height=50, font=("", 24), command=self.process_login)

        app_name.grid(row=1, column=1, columnspan=2)
        form_name.grid(row=2, column=1, columnspan=2, pady=(10, 20))
        profile_image.grid(row=3, column=1, columnspan=2, pady=(0, 30))
        self.welcome_message.grid(row=4, column=1, columnspan=2, pady=(0, 40))
        password_title.grid(row=5, column=1, columnspan=2, sticky="w")
        self.password_entry.grid(row=6, column=1, pady=(0, 10))
        toggle_password_mask.grid(row=6, column=2, pady=(0, 10), padx=(5, 0))
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

class DashboardPage(ctk.CTkFrame):
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

        dashboard_title = ctk.CTkLabel(content, text="This is the Dashboard Page!", text_color="green")
        dashboard_title.pack()

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

class SingleEntryPage(ctk.CTkFrame):
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

        dashboard_title = ctk.CTkLabel(content, text="This is the Single Entry Page!", text_color="green")
        dashboard_title.pack()

class SessionEntryPage(ctk.CTkFrame):
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

        dashboard_title = ctk.CTkLabel(content, text="This is the Session Entry Page!", text_color="green")
        dashboard_title.pack()

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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        navbar = Navbar(self, self.controller)
        content = ctk.CTkFrame(self, fg_color="black", corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        dashboard_title = ctk.CTkLabel(content, text="This is the Settings Page!", text_color="green")
        dashboard_title.pack()

if __name__ == "__main__":
    app = Windows()
    app.mainloop()


