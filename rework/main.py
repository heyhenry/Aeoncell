import customtkinter as ctk

# ctk.set_default_color_theme("rework/aeoncell.json")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Aeoncell - NEW")
        self.geometry("1280x800")
        self.minsize(1280, 720)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nswe")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for P in (DashboardPage, SomethingPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nswe")

        self.show_page(DashboardPage)

    def show_page(self, selected_page):
        page = self.pages[selected_page]
        page.tkraise()

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def create_widgets(self):
        
        page_title = ctk.CTkLabel(self, text="Aeoncell | Dashboard", font=("", 32))
        nav_bar = ctk.CTkFrame(self, width=1000, height=70, border_color="red", border_width=1)
        steps_section = ctk.CTkFrame(self, width=490, height=140, border_color="green", border_width=1)
        hydration_section = ctk.CTkFrame(self, width=490, height=140, border_color="green", border_width=1)
        overview_section = ctk.CTkFrame(self, width=1000, height=150, border_color="black", border_width=1)
        history_section = ctk.CTkFrame(self, width=1000, height=300, border_color="brown", border_width=1)

        page_title.grid(row=1, column=1, columnspan=2, pady=(0, 10))
        nav_bar.grid(row=2, column=1, columnspan=2, pady=(0, 10))
        steps_section.grid(row=3, column=1, pady=(0, 10), padx=(0, 10))
        hydration_section.grid(row=3, column=2, pady=(0, 10), padx=(10, 0))
        overview_section.grid(row=4, column=1, columnspan=2, pady=(0, 10))
        history_section.grid(row=5, column=1, columnspan=2, pady=(0, 10))

class SomethingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        lbl = ctk.CTkLabel(self, text="Something..")
        lbl.pack()


if __name__ == "__main__":
    app = Windows()
    app.mainloop()



