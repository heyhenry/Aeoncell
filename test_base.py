import customtkinter as ctk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Testing Grounds")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nswe")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.pages = {}

        for P in (HomePage, SingleEntryPage, SessionEntryPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        self.show_page(HomePage)

    def show_page(self, current_page):
        page = self.pages[current_page]
        page.tkraise()

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="This is the Home Page", font=("", 32))
        single_entry_btn = ctk.CTkButton(self, text="Single Entry", font=("", 24), command=lambda: self.controller.show_page(SingleEntryPage))
        session_entry_btn = ctk.CTkButton(self, text="Session Entry", font=("", 24), command=lambda: self.controller.show_page(SessionEntryPage))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        title.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
        single_entry_btn.grid(row=2, column=1, pady=(0, 10), padx=10)
        session_entry_btn.grid(row=2, column=2, pady=(0, 10), padx=10)

class BaseEntryPage(ctk.CTkFrame):
    def __init__(self, parent, controller, entry_type):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.entry_type = entry_type
        self.type_var = ctk.StringVar(value=entry_type)
        self.create_widgets()

    def create_widgets(self):
        self.form_window = ctk.CTkFrame(self, fg_color="#FF8C69", corner_radius=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.form_window.grid(row=1, column=1)

        title = ctk.CTkLabel(self.form_window, text=f"Entry Page [{self.entry_type.capitalize()}]", font=("", 32))
        date_title = ctk.CTkLabel(self.form_window, text="Date*:", font=("", 24))
        self.date_entry = ctk.CTkEntry(self.form_window)
        label_title = ctk.CTkLabel(self.form_window, text=" (Optional):", font=("", 24))
        self.label_entry = ctk.CTkEntry(self.form_window)
        self.error_message = ctk.CTkLabel(self.form_window, text="", text_color="blue", font=("", 18))
        self.submit_btn = ctk.CTkButton(self.form_window, text="Submit", font=("", 24), command=self.process_entry)
        self.cancel_btn = ctk.CTkButton(self.form_window, text="Cancel", font=("", 24), command=self.confirm_cancellation)

        self.form_window.grid_columnconfigure(0, weight=1)
        self.form_window.grid_columnconfigure(3, weight=1)

        self.form_window.grid_rowconfigure(0, weight=1)
        self.form_window.grid_rowconfigure(7, weight=1)

        title.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
        date_title.grid(row=2, column=1, columnspan=2, pady=10, padx=10)
        self.date_entry.grid(row=3, column=1, columnspan=2, pady=10, padx=10)
        label_title.grid(row=4, column=1, columnspan=2, pady=10, padx=10)
        self.label_entry.grid(row=5, column=1, columnspan=2, pady=10, padx=10)
        self.submit_btn.grid(row=6, column=1, pady=10, padx=10)
        self.cancel_btn.grid(row=6, column=2, pady=10, padx=10)

        self.date_entry.bind("<Key>", lambda event: self.custom_date_entry_validation(event, self.date_entry))

    def custom_date_entry_validation(self, event, widget):
        # allow normal function of the backspace key
        if event.keysym == "BackSpace":
            return
        
        # get char input
        char = event.char
        # get cursor position 
        i = widget.index("insert")

        # ignore if not a digit
        if not char.isdigit():
            return "break"
        
        # get current full length user input in the entry field
        current = widget.get()
        digits_only = [c for c in current if c.isdigit()]

        # limit user full length input to 8 characters
        # by ignoring further inputs
        if len(digits_only) >= 8:
            return "break"
        
        # insert the current user's input (char) in the correct position in the digits_only list,
        # factoring and accounting for the dash 
        # 2 worlds: reality of the what the user sees in the entry field vs the reality of what goes inside the digits_only list (dashes are excluded here)
        digits_only.insert(i - current[:i].count("-"), char)

        # create formatted string aka the user's validated input (visible to the user)
        formatted_string = ""
        for idx, c in enumerate(digits_only):
            if idx == 2 or idx == 4:
                formatted_string += "-"
            formatted_string += c

        # update the entry field
        widget.delete(0, ctk.END)
        widget.insert(0, formatted_string)

        # set the cursor position to be post final char inserted last
        if i == 2 or i == 5:
            dash_offset = 1
        else:
            dash_offset = 0

        # min function implemented as a guard clause, to ensure that index position isn't out of bounds
        widget.icursor(min(i + 1 + dash_offset, len(formatted_string)))

        # prevent duplicate insertion in the entry field, as char is inserted and dealt with earlier
        return "break"

    def error_popup(self, message):
        self.error_message.configure(text=message)
        self.error_message.grid(row=6, column=1, pady=10, padx=10)
        self.submit_btn.grid(row=7, column=1)
        self.cancel_btn.grid(row=7, column=2)
        self.form_window.grid_rowconfigure(7, weight=0)
        self.form_window.grid_rowconfigure(8, weight=1)

        self.after(1000, self.error_message.grid_forget)
        self.after(1000, lambda: self.submit_btn.grid(row=6, column=1))
        self.after(1000, lambda: self.cancel_btn.grid(row=6, column=2))
        self.after(1000, lambda: self.form_window.grid_rowconfigure(7, weight=1))
        self.after(1000, lambda: self.form_window.grid_rowconfigure(8, weight=0))

    def process_entry(self):
        if self.validate_fields():
            data = self.get_entry_field_data()
            print(data)
            self.clear_entry_field_data()
            self.after_entry_submission()

    def after_entry_submission(self):
        pass

    def confirm_cancellation(self):

        def proceed_confirmation():
            self.clear_entry_field_data()
            confirmation_window.destroy()
            self.controller.show_page(HomePage)

        mid_entry = False
        data = self.get_entry_field_data()
        for key, val in data.items():
            if len(val) > 0:
                mid_entry = True

        if mid_entry:
            confirmation_window = ctk.CTkToplevel(self.form_window)
            confirmation_window.title("Unsaved Entry detected!")
            confirmation_window.attributes("-topmost", "true")
            message = ctk.CTkLabel(confirmation_window, text="Unsaved Entry Detected!\nAre you sure you want to leave the page without saving the entry?", font=("", 18))
            confirm_btn = ctk.CTkButton(confirmation_window, text="Confirm", font=("", 24), command=proceed_confirmation)
            cancel_btn = ctk.CTkButton(confirmation_window, text="Cancel", font=("", 24), command=confirmation_window.destroy)

            confirmation_window.grid_columnconfigure(0, weight=1)
            confirmation_window.grid_columnconfigure(3, weight=1)

            confirmation_window.grid_rowconfigure(0, weight=1)
            confirmation_window.grid_rowconfigure(3, weight=1)

            message.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
            confirm_btn.grid(row=2, column=1, pady=10, padx=10)
            cancel_btn.grid(row=2, column=2, pady=10, padx=10)
        else:
            proceed_confirmation()

    # checks if date is mid-filled
    def validate_fields(self):
        data = self.get_entry_field_data()
        for key, val in data.items():
            if key == "date" and len(val) > 0 and len(val) < 10:
                self.error_popup("Incomplete data in date.")
                return False
        return True

    # gets all data from entry fields
    def get_entry_field_data(self):
        return {
            "date": self.date_entry.get(),
            "label": self.label_entry.get()
        }
    
    # clears min required data fields
    def clear_entry_field_data(self):
        self.date_entry.delete(0, ctk.END)
        
class SingleEntryPage(BaseEntryPage):
    def __init__(self, parent, controller):
        BaseEntryPage.__init__(self, parent, controller, "single")

    def after_entry_submission(self):
        self.controller.show_page(HomePage)

    def clear_entry_field_data(self):
        self.label_entry.delete(0, ctk.END)
    
class SessionEntryPage(BaseEntryPage):
    def __init__(self, parent, controller):
        BaseEntryPage.__init__(self, parent, controller, "session")

if __name__ == "__main__":
    app = Windows()
    app.mainloop()
