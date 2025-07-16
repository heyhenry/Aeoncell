import customtkinter as ctk
from tkinter import filedialog
from database_manager import DatabaseManager
import sqlite3
from datetime import date, timedelta, datetime
import calendar
from utils.aeoncell_utils import *
from PIL import Image
import os
from CTkXYFrame import *
from tkinter import ttk as btk
import random
import requests

from pages import RegisterPage
from pages import LoginPage
from pages import DashboardPage
from pages import SingleEntryPage
from pages import SessionEntryPage
from pages import AchievementsPage
from pages import StatsPage
from pages import DiscoverPage
from pages import SettingsPage

#region initialisation logic pre-startup

# creating and using an altered version of the CTkScrollableFrame class
def reinitialise_scrollableframe_widget():
    # get an instance of the original __init__ method of the CTkScrollableFrame class
    _original_init = ctk.CTkScrollableFrame.__init__
    # try-except in place as a failsafe in the case of future changes to the CTkScrollableFrame class
    try:
        # function to update attribute found in the CTkScrollableFrame class
        def patched_init(self, *args, **kwargs):
            # initialise the class
            _original_init(self, *args, **kwargs)
            # update with custom width for the scrollbar attribute
            self._scrollbar.configure(width=30)
        # make the CTkScrollableFrame use the altered __init__ method
        ctk.CTkScrollableFrame.__init__ = patched_init
    # if the try fails, opt for the defaulted version of CTkScrollableFrame class
    except Exception:
        return

# alter the CTkSrollableFrame widget base class
reinitialise_scrollableframe_widget()

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("themes/custom_lavender.json")

#endregion

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # flag to use as reference determinant of whether to set default profile pic
        db_exists = True

        if not os.path.exists("aeoncell_database.db"):
            db_exists = False

        self.db = DatabaseManager()
        self.db_connection = sqlite3.connect("aeoncell_database.db")
        self.db_cursor = self.db_connection.cursor()

        self.today = date.today()
        self.today = self.today.strftime("%d-%m-%Y")

        self.current_month = datetime.now().month
        if self.current_month < 10:
            self.current_month = f"0{self.current_month}"
        self.current_year = datetime.now().year

        # weather reference codes (used by open-meteo)
        self.wmo_codes = [
            ((0,), "clear"),
            ((1,2,3), "cloudy"),
            ((45, 48), "fog"),
            ((51, 53, 55, 56, 57), "drizzle"),
            ((61, 63, 65, 66, 67, 80, 81, 82), "rain"),
            ((71, 73, 75, 77, 85, 86), "snow"),
            ((95, 96, 99), "thunderstorm")
        ]

        self.username = ctk.StringVar()
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
            self.update_username()

        self.pages = {}
        for P in (RegisterPage, LoginPage, DashboardPage, DiscoverPage, SingleEntryPage, SessionEntryPage, StatsPage, AchievementsPage, SettingsPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        # center the app upon startup
        self.center_window(self, 1440, 900)

        # auto set default page on startup and any time db is deleted and re-added on new startup
        if not db_exists:
            print(db_exists)
            print("auto-defaulting-profile-pic")
            self.set_default_profile_image()

        # self.show_page(DashboardPage)
        # determine initial page display based on user having a password (i.e. guaranteed account registration)
        if self.db.check_password_exists():
            self.show_page(LoginPage)
        else:
            self.show_page(RegisterPage)

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
    def update_username(self):
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

    # auto set default profile image on creation of new db (usually only once for users, but in the case they delete the db file..)
    def set_default_profile_image(self):
        generate_round_frame_image("img/user_profile_asset.jpg", "user_profile")
        self.pages[LoginPage].update_login_profile_image()
        self.pages[DashboardPage].update_dashboard_profile_image()

    # check and use a defaulted value if found value is invalid
    def validate_conversion_value(self, value, conversion_type, defaulted_value):
        try:
            return conversion_type(value)
        except (ValueError, TypeError):
            return defaulted_value

if __name__ == "__main__":
    app = Windows()
    app.mainloop()


