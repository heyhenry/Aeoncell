import customtkinter as ctk
from authmanager import AuthManager

ctk.set_appearance_mode("Light") # other options: "Dark", "System" (Default)
ctk.set_default_color_theme("green") # other options: "blue" (Default), "dark-blue"

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.auth = AuthManager()

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

    def show_page(self, selected_page):
        self.pages[selected_page].tkraise()

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

    def process_password(self):
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

    def process_password(self):
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
        self.create_widgets()

    def create_widgets(self):
        page_title = ctk.CTkLabel(self, text="Fitness Dashboard", font=("",32))
        steps_section = ctk.CTkFrame(self, width=350, height=150)
        stats_section = ctk.CTkFrame(self, width=350, height=150)
        summary_section = ctk.CTkFrame(self, width=720, height=100)
        log_section = ctk.CTkFrame(self, width=720, height=250)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        page_title.grid(row=1, column=0, columnspan=4, pady=(10, 10))
        steps_section.grid(row=2, column=1, padx=10)
        stats_section.grid(row=2, column=2, padx=10)
        summary_section.grid(row=3, column=0, columnspan=4, pady=10)
        log_section.grid(row=4, column=0, columnspan=4, pady=(0, 20))

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
