import customtkinter as ctk

class Windows(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.wm_title = ('Aeoncell')

        container = ctk.CTkFrame(self, height=400, width=600)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for P in (RegisterPage, LoginPage, DashboardPage, StatsPage, EntryPage, UpdateEntryPage):
            page = P(container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky='nswe')

        self.show_page(RegisterPage)

    def show_page(self, selected_page):
        page = self.pages[selected_page]
        page.tkraise()

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text='Register Page')
        btn = ctk.CTkButton(self, text='Go to Login', command=lambda: self.controller.show_page(LoginPage))

        lbl.pack()
        btn.pack()
        
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text='Login Page')
        btn = ctk.CTkButton(self, text='Go to Dashboard', command=lambda: self.controller.show_page(DashboardPage))

        lbl.pack()
        btn.pack()

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text='Dashboard Page')
        btn = ctk.CTkButton(self, text='Go to Stats', command=lambda: self.controller.show_page(StatsPage))

        lbl.pack()
        btn.pack()

class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text='Stats Page')
        btn = ctk.CTkButton(self, text='Go to Entry', command=lambda: self.controller.show_page(EntryPage))

        lbl.pack()
        btn.pack()

class EntryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text='Entry Page')
        btn = ctk.CTkButton(self, text='Go to UpdateEntry', command=lambda: self.controller.show_page(UpdateEntryPage))

        lbl.pack()
        btn.pack()

class UpdateEntryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        lbl = ctk.CTkLabel(self, text='UpdateEntry Page')
        btn = ctk.CTkButton(self, text='Go to Register', command=lambda: self.controller.show_page(RegisterPage))

        lbl.pack()
        btn.pack()

if __name__ == '__main__':
    app = Windows()
    app.mainloop()
