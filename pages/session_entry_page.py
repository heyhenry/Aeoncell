import customtkinter as ctk
from pages import BaseEntryPage

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