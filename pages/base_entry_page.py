import customtkinter as ctk
from PIL import Image
from widgets import Navbar
from utils import *

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
            # during processing an entry, check if conditions meet to unlock the 'first workout" achievement
            self.controller.pages["AchievementsPage"].check_first_workout()
            data = self.get_entry_field_data()
            
            self.controller.db_cursor.execute("INSERT INTO exercise_entries (entry_type, exercise_label, date, time, exercise_name, sets_count, reps_count, weight_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data["type"], data["label"], data["date"], data["time"], data["exercise_name"], data["sets"], data["reps"], data["weight"]))
            self.controller.db_connection.commit()

            self.clear_entry_fields()
            self.reset_date()
            # update the exercise summary section in the dashboard
            self.controller.pages["DashboardPage"].update_exercise_summary()
            self.after_entry_submission()

    def process_confirmation(self):
        # confirm prompt to leave midway through filling form
        def proceed_confirmation():
            self.clear_entry_fields()
            # if prematurely exiting session entry page, ensure label is also cleared
            if self.entry_type == "session":
                self.label_entry.delete(0, ctk.END)
            confirmation_window.destroy()
            self.controller.show_page("DashboardPage")

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
            self.controller.show_page("DashboardPage")

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
            self.controller.show_page("SessionEntryPage")
        elif self.entry_type == "session":
            self.clear_entry_fields()
            self.label_entry.delete(0, ctk.END)
            self.controller.show_page("SingleEntryPage")

    # automatically insert today's date into the date entry field
    def reset_date(self):
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, self.today)