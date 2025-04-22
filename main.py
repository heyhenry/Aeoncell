import customtkinter as ctk
from authmanager import AuthManager
import sqlite3
from datetime import date

ctk.set_appearance_mode("Light") # other options: "Dark", "System" (Default)
ctk.set_default_color_theme("green") # other options: "blue" (Default), "dark-blue"

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.auth = AuthManager()
        self.db_connection = sqlite3.connect("aeoncell_database.db")
        self.db_cursor = self.db_connection.cursor()
        self.frame_bg_colour = "#f8fbfd"

        self.title("Aeoncell")
        self.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nswe")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for P in (RegisterPage, LoginPage, DashboardPage, StatsPage, EntryPage, UpdateEntryPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        if self.auth.check_password_exists():
            self.show_page(LoginPage)
        else:
            self.show_page(RegisterPage)
        
        self.auto_create_daily_step_entry()

    def show_page(self, selected_page):
        page = self.pages[selected_page]

        if selected_page in (RegisterPage, LoginPage):
            self.set_initial_focus(page.password_entry)
        
        page.tkraise()

    def set_initial_focus(self, widget_name):
        self.after(100, widget_name.focus)

    def auto_create_daily_step_entry(self):
        today = date.today()
        today = today.strftime("%d-%m-%Y")
        self.db_cursor.execute("SELECT exists (SELECT 1 FROM steps_tracker WHERE date = ?) AS row_exists", (today,))
        if not 1 in self.db_cursor.fetchone():
            self.db_cursor.execute("INSERT INTO steps_tracker (date) VALUES (?)", (today,))
            self.db_connection.commit()

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.password_var = ctk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        page_title = ctk.CTkLabel(self, text="Register for Aeoncell", font=("", 48))
        password = ctk.CTkLabel(self, text="Create Password:", font=("", 24))
        self.password_entry = ctk.CTkEntry(self, textvariable=self.password_var, width=240, font=("", 24))
        self.error_message = ctk.CTkLabel(self, text="", text_color="red", font=("", 18))
        submit = ctk.CTkButton(self, text="Register", command=self.process_password, font=("", 24))

        # horizontal centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # vertical centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # place widgets in the center column (col=1), and rows 1–5
        page_title.grid(row=1, column=1, pady=10)
        password.grid(row=2, column=1)
        self.password_entry.grid(row=3, column=1)
        self.error_message.grid(row=4, column=1)
        submit.grid(row=5, column=1)

        self.password_entry.bind("<Return>", self.process_password)

    def process_password(self, event=None):
        # validate password
        password = self.password_var.get()
        if len(password) < 8:
            self.display_error("Password too short. 8 characters minium.")
        elif password.isspace():
            self.display_error("Whitespaces aren't allowed.")
        else:
            self.controller.auth.create_password(password)
            self.controller.show_page(LoginPage)

    def display_error(self, error_msg):
        self.error_message.configure(text=error_msg)
        self.error_message.after(1000, lambda: self.error_message.configure(text=""))
        self.error_message.after(1000, lambda: self.password_var.set(""))

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.password_var = ctk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        page_title = ctk.CTkLabel(self, text="Login to Aeoncell", font=("", 48))
        password = ctk.CTkLabel(self, text="Enter Password:", font=("", 24))
        self.password_entry = ctk.CTkEntry(self, textvariable=self.password_var, width=240, font=("", 24))
        self.error_message = ctk.CTkLabel(self, text="", text_color="red", font=("", 18))
        submit = ctk.CTkButton(self, text="Login", command=self.process_password, font=("", 24))

        # horizontal centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # vertical centering
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # place widgets in the center column (col=1), and rows 1–5
        page_title.grid(row=1, column=1, pady=10)
        password.grid(row=2, column=1)
        self.password_entry.grid(row=3, column=1)
        self.error_message.grid(row=4, column=1)
        submit.grid(row=5, column=1)

        self.password_entry.bind("<Return>", self.process_password)

    def process_password(self, event=None):
        # validate password
        password = self.password_var.get()
        if self.controller.auth.verify_password(password):
            self.controller.show_page(DashboardPage)
        else:
            self.display_error("Incorrect Password.")

    def display_error(self, error_msg):
        self.error_message.configure(text=error_msg)
        self.error_message.after(1000, lambda: self.error_message.configure(text=""))
        self.error_message.after(1000, lambda: self.password_var.set(""))

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        self.steps_taken_var = ctk.IntVar()
        self.steps_add_var = ctk.StringVar()
        self.steps_total_display = ctk.StringVar(value="0")
        self.exercise_count_var = ctk.StringVar()
        self.total_volume_var= ctk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # frames + title
        page_title = ctk.CTkLabel(self, text="Fitness Dashboard", font=("", 32, "bold"))
        steps_section = ctk.CTkFrame(self, width=350, height=150, fg_color=self.controller.frame_bg_colour, corner_radius=10)
        stats_section = ctk.CTkFrame(self, width=350, height=150, fg_color=self.controller.frame_bg_colour, corner_radius=10)
        summary_section = ctk.CTkFrame(self, width=720, height=100, fg_color=self.controller.frame_bg_colour, corner_radius=10)
        log_section = ctk.CTkFrame(self, width=720, height=250, fg_color=self.controller.frame_bg_colour, corner_radius=10)

        # page layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        page_title.grid(row=1, column=0, columnspan=4, pady=(10, 10))
        steps_section.grid(row=2, column=1, padx=(10, 5))
        stats_section.grid(row=2, column=2, padx=(5, 10))
        summary_section.grid(row=3, column=0, columnspan=4, pady=10)
        log_section.grid(row=4, column=0, columnspan=4, pady=(0, 20))

        # steps section
        steps_title = ctk.CTkLabel(steps_section, text="Step Tracker", font=("", 24, "bold"))
        steps_count = ctk.CTkLabel(steps_section, textvariable=self.steps_total_display, font=("", 24))
        steps_add = ctk.CTkEntry(steps_section, textvariable=self.steps_add_var, font=("", 24))
        steps_update = ctk.CTkButton(steps_section, text="Add Steps", font=("", 24), command=self.update_steps)

        # steps section layout
        steps_section.grid_columnconfigure(0, weight=1)
        steps_section.grid_columnconfigure(1, weight=0)
        steps_section.grid_columnconfigure(2, weight=0)
        steps_section.grid_columnconfigure(3, weight=1)

        steps_section.grid_rowconfigure(0, weight=1)
        steps_section.grid_rowconfigure(4, weight=1)

        steps_section.grid_propagate(False)

        steps_title.grid(row=1, column=0, columnspan=4, pady=10)
        steps_count.grid(row=2, column=1, columnspan=2)
        steps_add.grid(row=3, column=1, pady=10, padx=(0, 5))
        steps_update.grid(row=3, column=2, pady=10, padx=(5, 0))

        # stats section
        stats_title = ctk.CTkLabel(stats_section, text="Stats Overview", font=("", 24, "bold"))
        stats_button = ctk.CTkButton(stats_section, text="View Stats", font=("", 24), command=lambda: self.controller.show_page(StatsPage))

        # stats section layout
        stats_section.grid_columnconfigure(0, weight=1)
        stats_section.grid_columnconfigure(1, weight=0)
        stats_section.grid_columnconfigure(2, weight=1)

        stats_section.grid_rowconfigure(0, weight=1)
        stats_section.grid_rowconfigure(3, weight=1)

        stats_section.grid_propagate(False)

        stats_title.grid(row=1, column=1, pady=10)
        stats_button.grid(row=2, column=1, pady=10)

        # summary section 
        summary_title = ctk.CTkLabel(summary_section, text="Today's Summary", font=("", 24, "bold"))
        exercise_count = ctk.CTkLabel(summary_section, text="Exercises: 6", font=("", 24))
        total_volume = ctk.CTkLabel(summary_section, text="Total Volume: 8.250kg", font=("", 24))        

        # summary section layout
        summary_section.grid_columnconfigure(0, weight=1)
        summary_section.grid_columnconfigure(1, weight=0)
        summary_section.grid_columnconfigure(2, weight=0)
        summary_section.grid_columnconfigure(3, weight=1)

        summary_section.grid_rowconfigure(0, weight=1)
        summary_section.grid_rowconfigure(3, weight=1)

        summary_section.grid_propagate(False)

        summary_title.grid(row=1, column=1, sticky="w", pady=10)
        exercise_count.grid(row=2, column=1, sticky="w", pady=(10, 20))
        total_volume.grid(row=2, column=2, pady=(10, 20))

        # log section
        log_title = ctk.CTkLabel(log_section, text="Recent Logs", font=("", 24, "bold"))
        log_button = ctk.CTkButton(log_section, text="- 2024-04-21 - Chest Day", font=("", 24))
        log_info = ctk.CTkLabel(log_section, text="- Bench Press: 3x8 @ 80kg\n- Incline DB Press: 3x10 @ 25kg\n- Flyes: 3x12 @ 12kg", font=("", 24))
        add_session = ctk.CTkButton(log_section, text="Add Session", font=("", 24))
        add_single_exercise = ctk.CTkButton(log_section, text="Add Single Exercise", font=("", 24))

        # log section layout
        log_section.grid_columnconfigure(0, weight=1)
        log_section.grid_columnconfigure(1, weight=0)
        log_section.grid_columnconfigure(2, weight=1)
        log_section.grid_columnconfigure(3, weight=1)

        log_section.grid_rowconfigure(0, weight=1)
        log_section.grid_rowconfigure(5, weight=1)
        
        log_section.grid_propagate(False)

        log_title.grid(row=1, column=1, stick="w", pady=10)
        log_button.grid(row=2, column=1, columnspan=2, sticky="w", pady=(0, 10))
        log_info.grid(row=3, column=1, columnspan=2, sticky="w")
        add_session.grid(row=4, column=1)
        add_single_exercise.grid(row=4, column=2, pady=10)

    def update_steps(self):
        steps_taken = self.steps_taken_var.get()
        steps_add = int(self.steps_add_var.get())
        result = steps_taken + steps_add
        self.steps_taken_var.set(result)
        result = f"{result:,}"
        self.steps_total_display.set(str(result))
        self.steps_add_var.set("")
        # self.controller.db_cursor.execute("UPDATE ")

class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text="Stats Page")
        btn = ctk.CTkButton(self, text="Go to Entry", command=lambda: self.controller.show_page(EntryPage))

        lbl.pack()
        btn.pack()

class EntryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text="Entry Page")
        btn = ctk.CTkButton(self, text="Go to UpdateEntry", command=lambda: self.controller.show_page(UpdateEntryPage))

        lbl.pack()
        btn.pack()

class UpdateEntryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text="UpdateEntry Page")
        btn = ctk.CTkButton(self, text="Go to Register", command=lambda: self.controller.show_page(RegisterPage))

        lbl.pack()
        btn.pack()

if __name__ == "__main__":
    app = Windows()
    app.mainloop()
