import customtkinter as ctk
from aeoncell_utils import *

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
        sets_title = ctk.CTkLabel(self.entry_form, text="Sets:", font=("", 18))
        self.sets_entry = ctk.CTkEntry(self.entry_form, font=("", 18))
        reps_title = ctk.CTkLabel(self.entry_form, text="Reps:", font=("", 18))
        self.reps_entry = ctk.CTkEntry(self.entry_form, font=("", 18))
        weight_title = ctk.CTkLabel(self.entry_form, text="Weight:", font=("", 18))
        self.weight_entry = ctk.CTkEntry(self.entry_form, font=("", 18))
        self.error_message = ctk.CTkLabel(self.entry_form, text_color="red", font=("", 14))
        self.add_exercise_btn = ctk.CTkButton(self.entry_form, text="Add Exercise", height=48, font=("", 18))
        self.redirect_btn = ctk.CTkButton(self.entry_form, text=f"{self.btn_name}", height=48, font=("", 18))

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

        # add binds
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
            proceed_confirmation()

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
    



    

