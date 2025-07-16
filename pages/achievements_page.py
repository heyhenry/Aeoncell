from __future__ import annotations
import customtkinter as ctk
from PIL import Image
from widgets import Navbar

class AchievementsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        navbar = Navbar(self, self.controller)
        content = ctk.CTkFrame(self, fg_color="black", corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        dashboard_title = ctk.CTkLabel(content, text="This is the Achievements Page!", text_color="green")
        dashboard_title.pack()