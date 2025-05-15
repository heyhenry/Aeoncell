import customtkinter as ctk
from tkinter import ttk as btk
from database_manager import DatabaseManager
import sqlite3
from datetime import date
from aeoncell_utils import *
from PIL import Image, ImageTk, ImageOps, ImageDraw

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = DatabaseManager()
        self.db_connection = sqlite3.connect("aeoncell_database.db")
        self.db_cursor = self.db_connection.cursor()

        self.today = date.today()
        self.today = self.today.strftime("%d-%m-%Y")

        self.user_profile_img = ctk.CTkImage(light_image=Image.open("img/user_profile_rounded.png"), dark_image=Image.open("img/user_profile_rounded.png"), size=(180,180))

        self.title("Aeoncell")
        self.geometry("1280x800")
        self.minsize(1280, 800)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nswe")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for P in (RegisterPage, LoginPage, DashboardPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        self.show_page(RegisterPage)

    # display the selected page to the user
    def show_page(self, selected_page):
        page = self.pages[selected_page]
        page.tkraise()

        # field focus config on startup for pages
        
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

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.password_var = ctk.StringVar()
        self.confirm_password_var = ctk.StringVar()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        register_form_section = ctk.CTkFrame(self, fg_color="red", corner_radius=0)
        cover_image_section = ctk.CTkFrame(self, fg_color="blue", corner_radius=0)

        register_form_section.grid(row=0, column=0, sticky="nswe")
        cover_image_section.grid(row=0, column=1, sticky="nswe")

        

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.password_var = ctk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        profile_image = ctk.CTkLabel(self, text="", image=self.controller.user_profile_img)
        profile_image.pack(pady=40)

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

if __name__ == "__main__":
    app = Windows()
    app.mainloop()


