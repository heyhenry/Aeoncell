import customtkinter as ctk
from tkinter import ttk as btk
from authmanager import AuthManager
import sqlite3
from datetime import date
from aeoncell_utils import *

ctk.set_appearance_mode("Light") # other options: "Dark", "System" (Default)
ctk.set_default_color_theme("green") # other options: "blue" (Default), "dark-blue"

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.auth = AuthManager()
        self.db_connection = sqlite3.connect("aeoncell_database.db")
        self.db_cursor = self.db_connection.cursor()
        self.frame_bg_colour = "#f8fbfd"

        self.today = date.today()
        self.today = self.today.strftime("%d-%m-%Y")

        self.title("Aeoncell")
        self.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nswe")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for P in (RegisterPage, LoginPage, DashboardPage, StatsPage, SingleEntryPage, SessionEntryPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        if self.auth.check_password_exists():
            self.show_page(LoginPage)
        else:
            self.show_page(RegisterPage)
        
        self.auto_create_daily_step_entry()
        self.protocol("WM_DELETE_WINDOW", self.auto_del_daily_step_entry)

    def show_page(self, selected_page):
        page = self.pages[selected_page]
        page.tkraise()

        if selected_page in (RegisterPage, LoginPage):
            self.set_initial_focus(page.password_entry)
        elif selected_page == DashboardPage:
            page.populate_logs_single()

    def set_initial_focus(self, widget_name):
        self.after(300, widget_name.focus_set)

    # checks to see if an entry for steps has been created today
    def auto_create_daily_step_entry(self):
        self.db_cursor.execute("SELECT exists (SELECT 1 FROM steps_tracker WHERE date = ?)", (self.today,))
        if not 1 in self.db_cursor.fetchone():
            self.db_cursor.execute("INSERT INTO steps_tracker (date) VALUES (?)", (self.today,))
            self.db_connection.commit()

    # only delete a step tracking entry if NULL (determines user made an accident, until total_steps gets a value)
    # and on app close
    def auto_del_daily_step_entry(self):
        self.db_cursor.execute("SELECT exists (SELECT 1 FROM steps_tracker WHERE date = ? AND total_steps IS NULL)", (self.today,))
        if 1 in self.db_cursor.fetchone():
            self.db_cursor.execute("DELETE FROM steps_tracker WHERE date = ?", (self.today,))
            self.db_connection.commit()
        self.destroy()

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
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller          
        style = btk.Style()
        style.configure("Treeview.Heading", font=(None, 12, "bold"))
        style.configure("Treeview", font=(None, 12), rowheight=30)
        style.map("Treeview", foreground=[('selected', 'black')], background=[('selected', 'white')])
        self.steps_taken_var = ctk.IntVar()
        self.steps_add_var = ctk.StringVar()
        self.steps_total_display = ctk.StringVar(value="0")
        self.exercise_count_var = ctk.StringVar()
        self.total_volume_var= ctk.StringVar()
        self.controller.db_cursor.execute("SELECT total_steps FROM steps_tracker WHERE date = ?", (self.controller.today,))
        total_steps = self.controller.db_cursor.fetchone()
        if total_steps:
            total_steps = int(total_steps[0])
            self.steps_taken_var.set(total_steps)
            total_steps = f"{total_steps:,}"
            self.steps_total_display.set(str(total_steps))
        self.create_widgets()

    def create_widgets(self):
        # frames + title
        page_title = ctk.CTkLabel(self, text="Fitness Dashboard", font=("", 32, "bold"))
        steps_section = ctk.CTkFrame(self, width=350, height=150, fg_color=self.controller.frame_bg_colour, corner_radius=10)
        stats_section = ctk.CTkFrame(self, width=350, height=150, fg_color=self.controller.frame_bg_colour, corner_radius=10)
        summary_section = ctk.CTkFrame(self, width=720, height=100, fg_color=self.controller.frame_bg_colour, corner_radius=10)
        self.log_section = ctk.CTkFrame(self, width=720, height=250, fg_color=self.controller.frame_bg_colour, corner_radius=10)

        # page layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        page_title.grid(row=1, column=0, columnspan=4, pady=(10, 10))
        steps_section.grid(row=2, column=1, padx=(10, 5))
        stats_section.grid(row=2, column=2, padx=(5, 10))
        summary_section.grid(row=3, column=0, columnspan=4, pady=10)
        self.log_section.grid(row=4, column=0, columnspan=4, pady=(0, 20))

        # steps section
        steps_title = ctk.CTkLabel(steps_section, text="Step Tracker", font=("", 24, "bold"))
        steps_count = ctk.CTkLabel(steps_section, textvariable=self.steps_total_display, font=("", 24))
        steps_add = ctk.CTkEntry(steps_section, textvariable=self.steps_add_var, font=("", 24))
        steps_update = ctk.CTkButton(steps_section, text="Add Steps", font=("", 24), command=self.update_steps)

        # steps section layout
        steps_section.grid_columnconfigure(0, weight=1)
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
        summary_section.grid_columnconfigure(3, weight=1)

        summary_section.grid_rowconfigure(0, weight=1)
        summary_section.grid_rowconfigure(3, weight=1)

        summary_section.grid_propagate(False)

        summary_title.grid(row=1, column=1, sticky="w", pady=10)
        exercise_count.grid(row=2, column=1, sticky="w", pady=(10, 20))
        total_volume.grid(row=2, column=2, pady=(10, 20))

        # log section
        log_title = ctk.CTkLabel(self.log_section, text="Recent Logs", font=("", 24, "bold"))
        self.expand_log = ctk.CTkCheckBox(self.log_section, text="Expand Logs", font=("", 24), command=self.toggle_logs)

        self.entries = btk.Treeview(self.log_section, columns=("exercise_name", "exercise_date", "exercise_type"), show="headings", height=1, selectmode="browse")
        self.entries.heading("exercise_name", text="Exercise Name", anchor="w")
        self.entries.heading("exercise_date", text="Date", anchor="w")
        self.entries.heading("exercise_type", text="Type", anchor="w")
        self.entries.column("exercise_name", width=200, minwidth=200, stretch=False)
        self.entries.column("exercise_date", width=200, minwidth=200, stretch=False)
        self.entries.column("exercise_type", width=200, minwidth=200, stretch=False)

        add_session = ctk.CTkButton(self.log_section, text="Add Session", font=("", 24), command=lambda: self.controller.show_page(SessionEntryPage))
        add_single = ctk.CTkButton(self.log_section, text="Add Single Exercise", font=("", 24), command=lambda: self.controller.show_page(SingleEntryPage))

        # log section layout
        self.log_section.grid_columnconfigure(0, weight=1)
        self.log_section.grid_columnconfigure(3, weight=1)

        self.log_section.grid_rowconfigure(0, weight=1)
        self.log_section.grid_rowconfigure(5, weight=1)
        
        self.log_section.grid_propagate(False)

        log_title.grid(row=1, column=1, stick="w", pady=(0, 10))
        self.expand_log.grid(row=2, column=1, columnspan=2, sticky="w", pady=(0, 10))
        self.entries.grid(row=3, column=1, columnspan=2, sticky="w")
        add_session.grid(row=4, column=1, pady=20)
        add_single.grid(row=4, column=2, pady=20)

    # updating the daily steps taken based on user input
    def update_steps(self):
        steps_taken = self.steps_taken_var.get()
        steps_add = int(self.steps_add_var.get())
        result = steps_taken + steps_add
        self.steps_taken_var.set(result)
        # no need to check if the entry already exists, as its been handled upon startup
        self.controller.db_cursor.execute("UPDATE steps_tracker SET total_steps = ? WHERE Date = ?", (result, self.controller.today))
        self.controller.db_connection.commit()
        result = f"{result:,}"
        self.steps_total_display.set(str(result))
        self.steps_add_var.set("")

    # expanded list of entries population up to 25
    def populate_logs_expanded(self):
        # clear existing entries data
        self.entries.delete(*self.entries.get_children())
        # get latest entries from database
        self.controller.db_cursor.execute("SELECT exercise_name, date, type FROM exercise_entries ORDER BY id DESC LIMIT 25")
        result = self.controller.db_cursor.fetchall()
        if result:
            for entry_info in result:
                # populate entries with latest data sourced from the database
                exercise_name = entry_info[0]
                exercise_date = entry_info[1]
                exercise_type = entry_info[2]
                self.entries.insert("", "end", values=(exercise_name, exercise_date, exercise_type))

    # single entry population (latest entry)
    def populate_logs_single(self):
        self.entries.delete(*self.entries.get_children())
        self.controller.db_cursor.execute("SELECT exercise_name, date, type FROM exercise_entries ORDER BY id DESC LIMIT 1")
        result = self.controller.db_cursor.fetchall()
        if result:
            for entry_info in result:
                exercise_name = entry_info[0]
                exercise_date = entry_info[1]
                exercise_type = entry_info[2]
                self.entries.insert("", "end", values=(exercise_name, exercise_date, exercise_type))

    # toggle between latest single entry view and multiple entries view (max. 25)
    def toggle_logs(self):
        if self.expand_log.get() == False:
            self.controller.geometry("800x600")
            self.log_section.configure(height=250)
            self.entries.configure(height=1)
            self.populate_logs_single()
        else:
            self.controller.geometry("800x700")
            self.log_section.configure(height=350)
            self.entries.configure(height=5)
            self.populate_logs_expanded()

class BaseEntryPage(ctk.CTkFrame):
    def __init__(self, parent, controller, entry_type, btn_name):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.entry_type = entry_type
        self.btn_name = btn_name
        self.type_var = ctk.StringVar(value=self.entry_type)
        self.create_widgets()

    def create_widgets(self):
        self.entry_form = ctk.CTkFrame(self, fg_color=self.controller.frame_bg_colour, corner_radius=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.entry_form.grid(row=1, column=1)

        page_title = ctk.CTkLabel(self.entry_form, text=f"Create New Entry [{self.entry_type}]", font=("", 24, "bold"))

        type_title = ctk.CTkLabel(self.entry_form, text="Type*:", font=("", 18))
        self.type_entry = ctk.CTkEntry(self.entry_form, textvariable=self.type_var, width=300, font=("", 18), state="readonly")
        exercise_name_title = ctk.CTkLabel(self.entry_form, text="Exercise Name*:", font=("", 18))
        self.exercise_name_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 18))
        date_title = ctk.CTkLabel(self.entry_form, text="Date*:", font=("", 18))
        self.date_entry = ctk.CTkEntry(self.entry_form, font=("", 18))
        time_title = ctk.CTkLabel(self.entry_form, text="Time*:", font=("", 18))
        self.time_entry = ctk.CTkEntry(self.entry_form, font=("", 18))
        label_title = ctk.CTkLabel(self.entry_form, text="Label:", width=300, font=("", 18))
        self.label_entry = ctk.CTkEntry(self.entry_form, width=300, font=("", 18))
        sets_title = ctk.CTkLabel(self.entry_form, text="Sets*:", font=("", 18))
        self.sets_entry = ctk.CTkEntry(self.entry_form, font=("", 18))
        reps_title = ctk.CTkLabel(self.entry_form, text="Reps*:", font=("", 18))
        self.reps_entry = ctk.CTkEntry(self.entry_form, font=("", 18))
        weight_title = ctk.CTkLabel(self.entry_form, text="Weight*:", font=("", 18))
        self.weight_entry = ctk.CTkEntry(self.entry_form, font=("", 18))
        self.error_message = ctk.CTkLabel(self.entry_form, text_color="red", font=("", 14))
        self.add_exercise_btn = ctk.CTkButton(self.entry_form, text="Add Exercise", height=48, font=("", 18), command=self.process_entry)
        self.redirect_btn = ctk.CTkButton(self.entry_form, text=f"{self.btn_name}", height=48, font=("", 18), command=self.process_confirmation)

        self.entry_form.grid_columnconfigure(0, weight=1)
        self.entry_form.grid_columnconfigure(3, weight=1)

        self.entry_form.grid_rowconfigure(0, weight=1)
        self.entry_form.grid_rowconfigure(15, weight=1)

        page_title.grid(row=1, column=1, columnspan=2, sticky="w")

        type_title.grid(row=2, column=1, columnspan=2, sticky="w")
        self.type_entry.grid(row=3, column=1, columnspan=2, sticky="w")
        exercise_name_title.grid(row=4, column=1, columnspan=2, sticky="w")
        self.exercise_name_entry.grid(row=5, column=1, columnspan=2, sticky="w")
        date_title.grid(row=6, column=1, sticky="w")
        self.date_entry.grid(row=7, column=1, sticky="w")
        time_title.grid(row=6, column=2, sticky="w")
        self.time_entry.grid(row=7, column=2, sticky="w")
        label_title.grid(row=8, column=1, columnspan=2, sticky="w")
        self.label_entry.grid(row=9, column=1, columnspan=2, sticky="w")
        sets_title.grid(row=10, column=1, sticky="w")
        self.sets_entry.grid(row=11, column=1, sticky="w")
        reps_title.grid(row=10, column=2, sticky="w")
        self.reps_entry.grid(row=11, column=2, sticky="w")
        weight_title.grid(row=12, column=1, columnspan=2, sticky="w")
        self.weight_entry.grid(row=13, column=1, columnspan=2, sticky="w")
        self.add_exercise_btn.grid(row=14, column=1, sticky="w")
        self.redirect_btn.grid(row=14, column=2, sticky="w")

        self.exercise_name_entry.bind("<Key>", lambda event: custom_entry_limit_chars(event, self.exercise_name_entry, 30))
        self.date_entry.bind("<Key>", lambda event: custom_date_entry_validation(event, self.date_entry))
        self.time_entry.bind("<Key>", lambda event: custom_time_entry_validation(event, self.time_entry))
        self.label_entry.bind("<Key>", lambda event: custom_entry_limit_chars(event, self.label_entry, 100))
        self.sets_entry.bind("<Key>", lambda event: custom_setsreps_entry_validation(event, self.sets_entry))
        self.reps_entry.bind("<Key>", lambda event: custom_setsreps_entry_validation(event, self.reps_entry))
        self.weight_entry.bind("<Key>", lambda event: custom_entry_limit_chars(event, self.weight_entry, 20))

    def process_entry(self):
        if self.validate_entry_fields():
            data = self.get_entry_field_data()
            
            self.controller.db_cursor.execute("INSERT INTO exercise_entries (type, label, date, time, exercise_name, sets, reps, weight) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data["type"], data["label"], data["date"], data["time"], data["exercise_name"], data["sets"], data["reps"], data["weight"]))
            self.controller.db_connection.commit()

            self.clear_entry_fields()

        self.after_entry_submission()

    def process_confirmation(self):

        def proceed_confirmation():
            self.clear_entry_fields()
            confirmation_window.destroy()
            self.controller.show_page(DashboardPage)

        incomplete_entry = False
        data = self.get_entry_field_data()
        for key, val in data.items():
            if key != "type" and len(val) > 0:
                incomplete_entry = True
        
        if incomplete_entry:
            confirmation_window = ctk.CTkToplevel(self.entry_form)
            confirmation_window.attributes("-topmost", "true")
            confirmation_window.title("Incomplete Entry Detected!")
            message = ctk.CTkLabel(confirmation_window, text="Are you sure you want to leave the page without saving the entry?", font=("", 18))
            confirm_btn = ctk.CTkButton(confirmation_window, text="Confirm", font=("", 24), command=proceed_confirmation)
            cancel_btn = ctk.CTkButton(confirmation_window, text="Cancel", font=("", 24), command=confirmation_window.destroy)

            confirmation_window.grid_columnconfigure(0, weight=1)
            confirmation_window.grid_columnconfigure(3, weight=1)

            confirmation_window.grid_rowconfigure(0, weight=1)
            confirmation_window.grid_rowconfigure(3, weight=1)

            message.grid(row=1, column=1, columnspan=2)
            confirm_btn.grid(row=2, column=1)
            cancel_btn.grid(row=2, column=2)
        else:
            self.controller.show_page(DashboardPage)

    def after_entry_submission(self):
        pass

    # flashes an error message in the form
    def error_display(self, message):

        # component of the error_display function - changes widget settings back to normal after timed period
        def error_display_revert():
            self.error_message.configure(text="") # not really needed. more for extra protecc | might remove later after tests
            self.error_message.grid_forget()
            self.add_exercise_btn.grid(row=14, column=1)
            self.redirect_btn.grid(row=14, column=2)
            self.entry_form.grid_rowconfigure(15, weight=1)
            self.entry_form.grid_rowconfigure(16, weight=0)

        # display error message and reconfig widgets
        self.error_message.configure(text=message)
        self.error_message.grid(row=14, column=1, columnspan=2, sticky="n")
        self.add_exercise_btn.grid(row=15, column=1)
        self.redirect_btn.grid(row=15, column=2)
        self.entry_form.grid_rowconfigure(15, weight=0)
        self.entry_form.grid_rowconfigure(16, weight=1)

        # revert error message and widgets back to original state/configuration
        self.after(1000, error_display_revert)

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
                self.error_display("All * fields need to be filled.")
                return False
            elif key == "date" and len(val) < 10:
                self.error_display("Date info incomplete. [dd-mm-yyyy]")
                return False
            elif key == "time" and len(val) < 5:
                self.error_display("Time info incomplete. [xx:xx]")
                return False
        return True

class SingleEntryPage(BaseEntryPage):
    def __init__(self, parent, controller):
        BaseEntryPage.__init__(self, parent, controller, "single", "Cancel")

class SessionEntryPage(BaseEntryPage):
    def __init__(self, parent, controller):
        BaseEntryPage.__init__(self, parent, controller, "session", "Completed")

class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text="Stats Page")
        btn = ctk.CTkButton(self, text="Go to Entry", command=lambda: self.controller.show_page(SingleEntryPage))

        lbl.pack()
        btn.pack()

if __name__ == "__main__":
    app = Windows()
    app.mainloop()
