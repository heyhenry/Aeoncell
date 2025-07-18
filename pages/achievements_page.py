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

        self.achievements_triple_stars = ctk.CTkImage(light_image=Image.open("img/achievements/triple_stars.png"), dark_image=Image.open("img/achievements/triple_stars.png"), size=(128, 96))
        self.achievements_banner = ctk.CTkImage(light_image=Image.open("img/achievements/achievement_banner.png"), dark_image=Image.open("img/achievements/achievement_banner.png"), size=(96, 96))

        self.create_widgets()

    def create_widgets(self):
        #region [Main Frames]
        navbar = Navbar(self, self.controller)
        content = ctk.CTkScrollableFrame(self, corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(4, weight=1)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)

        #endregion

        #region [Parent Frames]
        page_title = ctk.CTkLabel(content, text="Achievements", font=("", 24))
        page_message = ctk.CTkLabel(content, text="View your achievements here", font=("", 14))
        achievements_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=1200, height=3200)

        achievements_section.grid_propagate(False)
        achievements_section.grid_rowconfigure(0, weight=1)
        achievements_section.grid_rowconfigure(21, weight=1)
        achievements_section.grid_columnconfigure(0, weight=1)
        achievements_section.grid_columnconfigure(2, weight=1)

        page_title.grid(row=1, column=1, pady=(30, 0), sticky="w", padx=(0, 1000))
        page_message.grid(row=2, column=1, pady=(0, 50), sticky="w")
        achievements_section.grid(row=3, column=1, pady=(0, 50))
        #endregion

        #region [Achievement Frames]
        achievements_overview_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=0, width=1100, height=160)
        
        achievements_overview_section.grid_propagate(False)
        achievements_overview_section.grid_rowconfigure(0, weight=1)
        achievements_overview_section.grid_rowconfigure(2, weight=1)
        achievements_overview_section.grid_columnconfigure(0, weight=1)
        achievements_overview_section.grid_columnconfigure(3, weight=1)
        achievements_overview_section.grid(row=1, column=1, pady=(30, 20))
        
        achievements_banner_subsection = ctk.CTkFrame(achievements_overview_section, fg_color="transparent")
        achievements_overview_subsection = ctk.CTkFrame(achievements_overview_section, fg_color="transparent")

        achievements_banner_subsection.grid(row=1, column=1, padx=(0, 60))
        achievements_overview_subsection.grid(row=1, column=2)

        achievements_left_sub_banner = ctk.CTkLabel(achievements_banner_subsection, text="", image=self.achievements_banner)
        achievements_triple_stars = ctk.CTkLabel(achievements_banner_subsection, text="", image=self.achievements_triple_stars)
        achievements_right_sub_banner = ctk.CTkLabel(achievements_banner_subsection, text="", image=self.achievements_banner)

        achievements_left_sub_banner.grid(row=0, column=0)
        achievements_triple_stars.grid(row=0, column=1, padx=20)
        achievements_right_sub_banner.grid(row=0, column=2)

        achievements_overview_progress_info = ctk.CTkLabel(achievements_overview_subsection, text="3 of 12 (40%) achievements earned:", font=("", 24))
        achievements_overview_progressbar = ctk.CTkProgressBar(achievements_overview_subsection, border_width=3, height=40, width=600, corner_radius=0)

        achievements_overview_progress_info.grid(row=0, column=0, pady=(0, 10))
        achievements_overview_progressbar.grid(row=1, column=0)                

        # First Day: Log into Aeoncell for the first time
        achievement_slot_1_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # First Drink: Log first hydration entry
        achievement_slot_2_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # First Sleep: Log first sleep entry
        achievement_slot_3_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # First Steps: Log first steps entry
        achievement_slot_4_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # First Workout: Log first exercise entry
        achievement_slot_5_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # New Profile: Change profile pic for the first time
        achievement_slot_6_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Ten Exercises: Log 10 exercise entries
        achievement_slot_7_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Rep Warrior: Complete 1000 total reps
        achievement_slot_8_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Set It off: Complete 500 total sets
        achievement_slot_9_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Sleep Maxxed: Sleep over 9 hours in a single night
        achievement_slot_10_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Heavy Lifter I: Lift a total of 1000kg
        achievement_slot_11_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Heavy Lifter II: Lift a total of 10,000kg
        achievement_slot_12_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Step Stacker I: Walk a total of 50,000 steps
        achievement_slot_13_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Step Stacker II: Walk a total of 250,000 steps
        achievement_slot_14_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        # Hydrated Human I: Drink a total of 10L
        achievement_slot_15_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)

        # Hydrated Human II: Drink a total of 100L 
        achievement_slot_16_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)

        # Sleeping Beauty I: Sleep a total of 10hrs
        achievement_slot_17_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)

        # Sleeping Beauty II: Sleep a total of 100hrs
        achievement_slot_18_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)

        # 1 Month Club: Log entries for 30 different days
        achievement_slot_19_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)

        achievement_slot_1_section.grid(row=2, column=1, pady=(30, 0))
        achievement_slot_2_section.grid(row=3, column=1, pady=(30, 0))
        achievement_slot_3_section.grid(row=4, column=1, pady=(30, 0))
        achievement_slot_4_section.grid(row=5, column=1, pady=(30, 0))
        achievement_slot_5_section.grid(row=6, column=1, pady=(30, 0))
        achievement_slot_6_section.grid(row=7, column=1, pady=(30, 0))
        achievement_slot_7_section.grid(row=8, column=1, pady=(30, 0))
        achievement_slot_8_section.grid(row=9, column=1, pady=(30, 0))
        achievement_slot_9_section.grid(row=10, column=1, pady=(30, 0))
        achievement_slot_10_section.grid(row=11, column=1, pady=(30, 0))
        achievement_slot_11_section.grid(row=12, column=1, pady=(30, 0))
        achievement_slot_12_section.grid(row=13, column=1, pady=(30, 0))
        achievement_slot_13_section.grid(row=14, column=1, pady=(30, 0))
        achievement_slot_14_section.grid(row=15, column=1, pady=(30, 0))
        achievement_slot_15_section.grid(row=16, column=1, pady=(30, 0))
        achievement_slot_16_section.grid(row=17, column=1, pady=(30, 0))
        achievement_slot_17_section.grid(row=18, column=1, pady=(30, 0))
        achievement_slot_18_section.grid(row=19, column=1, pady=(30, 0))
        achievement_slot_19_section.grid(row=20, column=1, pady=(30, 0))

        #endregion
