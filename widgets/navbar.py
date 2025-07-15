import customtkinter as ctk
from PIL import Image
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.single_entry_page import SingleEntryPage
from pages.achievements_page import AchievementsPage
from pages.stats_page import StatsPage
from pages.discover_page import DiscoverPage
from pages.settings_page import SettingsPage

class Navbar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.configure(fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0)

        # icon images
        self.dashboard_img = ctk.CTkImage(light_image=Image.open("img/dashboard_icon.png"), dark_image=Image.open("img/dashboard_icon.png"), size=(32, 32))
        self.discover_img = ctk.CTkImage(light_image=Image.open("img/discover_icon.png"), dark_image=Image.open("img/discover_icon.png"), size=(32, 32))
        self.entry_img = ctk.CTkImage(light_image=Image.open("img/entry_icon.png"), dark_image=Image.open("img/entry_icon.png"), size=(32, 32))
        self.stats_img = ctk.CTkImage(light_image=Image.open("img/stats_icon.png"), dark_image=Image.open("img/stats_icon.png"), size=(32, 32))
        self.achievements_img = ctk.CTkImage(light_image=Image.open("img/achievements_icon.png"), dark_image=Image.open("img/achievements_icon.png"), size=(32, 32))
        self.settings_img = ctk.CTkImage(light_image=Image.open("img/settings_icon.png"), dark_image=Image.open("img/settings_icon.png"), size=(32, 32))
        self.logout_img = ctk.CTkImage(light_image=Image.open("img/logout_icon.png"), dark_image=Image.open("img/logout_icon.png"), size=(32, 32))

        self.create_widgets()

    def create_widgets(self):
        app_name = ctk.CTkLabel(self, text="Aeoncell", font=("", 18))
        app_icon = ctk.CTkLabel(self, text="", image=self.controller.app_icon_img)
        self.dashboard_icon = ctk.CTkLabel(self, text="", image=self.dashboard_img)
        self.dashboard_title = ctk.CTkLabel(self, text="Dashboard", font=("", 11, "bold"))
        self.discover_icon = ctk.CTkLabel(self, text="", image=self.discover_img)
        self.discover_title = ctk.CTkLabel(self, text="Discover", font=("", 11, "bold"))
        self.entry_icon = ctk.CTkLabel(self, text="", image=self.entry_img)
        self.entry_title = ctk.CTkLabel(self, text="Entry", font=("", 11, "bold"))
        self.stats_icon = ctk.CTkLabel(self, text="", image=self.stats_img)
        self.stats_title = ctk.CTkLabel(self, text="Statistics", font=("", 11, "bold"))
        self.achievements_icon = ctk.CTkLabel(self, text="", image=self.achievements_img)
        self.achievements_title = ctk.CTkLabel(self, text="Achievements", font=("", 11, "bold"))
        self.settings_icon = ctk.CTkLabel(self, text="", image=self.settings_img)
        self.settings_title = ctk.CTkLabel(self, text="Settings", font=("", 11, "bold"))
        self.logout_icon = ctk.CTkLabel(self, text="", image=self.logout_img)
        self.logout_title = ctk.CTkLabel(self, text="Logout", font=("", 11, "bold"))

        app_name.grid(row=1, column=1, pady=20, padx=10)
        app_icon.grid(row=2, column=1, pady=(0, 50))
        self.dashboard_icon.grid(row=3, column=1, pady=(10, 0))
        self.dashboard_title.grid(row=4, column=1, pady=(0, 10))
        self.discover_icon.grid(row=5, column=1, pady=(10, 0))
        self.discover_title.grid(row=6, column=1, pady=(0, 10))
        self.entry_icon.grid(row=7, column=1, pady=(10, 0))
        self.entry_title.grid(row=8, column=1, pady=(0, 10))
        self.stats_icon.grid(row=9, column=1, pady=(10, 0))
        self.stats_title.grid(row=10, column=1, pady=(0, 10))
        self.achievements_icon.grid(row=11, column=1, pady=(10, 0))
        self.achievements_title.grid(row=12, column=1, pady=(0, 10))
        self.settings_icon.grid(row=13, column=1, pady=(10, 0))
        self.settings_title.grid(row=14, column=1, pady=(0, 20))
        self.logout_icon.grid(row=15, column=1, pady=(50, 0))
        self.logout_title.grid(row=16, column=1)

        self.dashboard_icon.bind("<Enter>", lambda event: self.display_selection(self.dashboard_icon, self.dashboard_title))
        self.dashboard_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.dashboard_icon, self.dashboard_title))
        self.dashboard_icon.bind("<Button-1>", lambda event: self.controller.show_page(DashboardPage))
        self.dashboard_title.bind("<Enter>", lambda event: self.display_selection(self.dashboard_icon, self.dashboard_title))
        self.dashboard_title.bind("<Leave>", lambda event: self.undisplay_selection(self.dashboard_icon, self.dashboard_title))
        self.dashboard_title.bind("<Button-1>", lambda event: self.controller.show_page(DashboardPage))
        self.discover_icon.bind("<Enter>", lambda event: self.display_selection(self.discover_icon, self.discover_title))
        self.discover_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.discover_icon, self.discover_title))
        self.discover_icon.bind("<Button-1>", lambda event: self.controller.show_page(DiscoverPage))
        self.discover_title.bind("<Enter>", lambda event: self.display_selection(self.discover_icon, self.discover_title))
        self.discover_title.bind("<Leave>", lambda event: self.undisplay_selection(self.discover_icon, self.discover_title))
        self.discover_title.bind("<Button-1>", lambda event: self.controller.show_page(DiscoverPage))
        self.entry_icon.bind("<Enter>", lambda event: self.display_selection(self.entry_icon, self.entry_title))
        self.entry_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.entry_icon, self.entry_title))
        self.entry_icon.bind("<Button-1>", lambda event: self.controller.show_page(SingleEntryPage))
        self.entry_title.bind("<Enter>", lambda event: self.display_selection(self.entry_icon, self.entry_title))
        self.entry_title.bind("<Leave>", lambda event: self.undisplay_selection(self.entry_icon, self.entry_title))
        self.entry_title.bind("<Button-1>", lambda event: self.controller.show_page(SingleEntryPage))
        self.stats_icon.bind("<Enter>", lambda event: self.display_selection(self.stats_icon, self.stats_title))
        self.stats_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.stats_icon, self.stats_title))
        self.stats_icon.bind("<Button-1>", lambda event: self.controller.show_page(StatsPage))
        self.stats_title.bind("<Enter>", lambda event: self.display_selection(self.stats_icon, self.stats_title))
        self.stats_title.bind("<Leave>", lambda event: self.undisplay_selection(self.stats_icon, self.stats_title))
        self.stats_title.bind("<Button-1>", lambda event: self.controller.show_page(StatsPage))
        self.achievements_icon.bind("<Enter>", lambda event: self.display_selection(self.achievements_icon, self.achievements_title))
        self.achievements_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.achievements_icon, self.achievements_title))
        self.achievements_icon.bind("<Button-1>", lambda event: self.controller.show_page(AchievementsPage))
        self.achievements_title.bind("<Enter>", lambda event: self.display_selection(self.achievements_icon, self.achievements_title))
        self.achievements_title.bind("<Leave>", lambda event: self.undisplay_selection(self.achievements_icon, self.achievements_title))
        self.achievements_title.bind("<Button-1>", lambda event: self.controller.show_page(AchievementsPage))
        self.settings_icon.bind("<Enter>", lambda event: self.display_selection(self.settings_icon, self.settings_title))
        self.settings_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.settings_icon, self.settings_title))
        self.settings_icon.bind("<Button-1>", lambda event: self.controller.show_page(SettingsPage))
        self.settings_title.bind("<Enter>", lambda event: self.display_selection(self.settings_icon, self.settings_title))
        self.settings_title.bind("<Leave>", lambda event: self.undisplay_selection(self.settings_icon, self.settings_title))
        self.settings_title.bind("<Button-1>", lambda event: self.controller.show_page(SettingsPage))
        self.logout_icon.bind("<Enter>", lambda event: self.display_selection(self.logout_icon, self.logout_title))
        self.logout_icon.bind("<Leave>", lambda event: self.undisplay_selection(self.logout_icon, self.logout_title))
        self.logout_icon.bind("<Button-1>", lambda event: self.controller.show_page(LoginPage))
        self.logout_title.bind("<Enter>", lambda event: self.display_selection(self.logout_icon, self.logout_title))
        self.logout_title.bind("<Leave>", lambda event: self.undisplay_selection(self.logout_icon, self.logout_title))
        self.logout_title.bind("<Button-1>", lambda event: self.controller.show_page(LoginPage))

    def display_selection(self, widget_icon, widget_title, event=None):
        widget_icon.configure(cursor="hand2")
        widget_title.configure(font=("", 11, "bold", "underline"), cursor="hand2")

    def undisplay_selection(self, widget_icon, widget_title, event=None):
        widget_icon.configure(cursor="arrow")
        widget_title.configure(font=("", 11, "bold"), cursor="arrow")