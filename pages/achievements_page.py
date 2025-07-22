import customtkinter as ctk
from PIL import Image
from widgets import Navbar
from datetime import datetime
from utils import achievement_map
from .images import achievement_images

class AchievementsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # ==================== [Variables] ====================
        #region Variables
        self.achievement_1_icon = achievement_images.loading_achievement_icon
        self.achievement_2_icon = achievement_images.loading_achievement_icon
        self.achievement_3_icon = achievement_images.loading_achievement_icon
        self.achievement_4_icon = achievement_images.loading_achievement_icon
        self.achievement_5_icon = achievement_images.loading_achievement_icon
        self.achievement_6_icon = achievement_images.loading_achievement_icon
        self.achievement_7_icon = achievement_images.loading_achievement_icon
        self.achievement_8_icon = achievement_images.loading_achievement_icon
        self.achievement_9_icon = achievement_images.loading_achievement_icon
        self.achievement_10_icon = achievement_images.loading_achievement_icon
        self.achievement_11_icon = achievement_images.loading_achievement_icon
        self.achievement_12_icon = achievement_images.loading_achievement_icon
        self.achievement_13_icon = achievement_images.loading_achievement_icon
        self.achievement_14_icon = achievement_images.loading_achievement_icon
        self.achievement_15_icon = achievement_images.loading_achievement_icon
        self.achievement_16_icon = achievement_images.loading_achievement_icon
        self.achievement_17_icon = achievement_images.loading_achievement_icon
        self.achievement_18_icon = achievement_images.loading_achievement_icon
        self.achievement_19_icon = achievement_images.loading_achievement_icon

        self.achievement_1_unlock_date = ctk.StringVar()
        self.achievement_2_unlock_date = ctk.StringVar()
        self.achievement_3_unlock_date = ctk.StringVar()
        self.achievement_4_unlock_date = ctk.StringVar()
        self.achievement_5_unlock_date = ctk.StringVar()
        self.achievement_6_unlock_date = ctk.StringVar()
        self.achievement_7_unlock_date = ctk.StringVar()
        self.achievement_8_unlock_date = ctk.StringVar()
        self.achievement_9_unlock_date = ctk.StringVar()
        self.achievement_10_unlock_date = ctk.StringVar()
        self.achievement_11_unlock_date = ctk.StringVar()
        self.achievement_12_unlock_date = ctk.StringVar()
        self.achievement_13_unlock_date = ctk.StringVar()
        self.achievement_14_unlock_date = ctk.StringVar()
        self.achievement_15_unlock_date = ctk.StringVar()
        self.achievement_16_unlock_date = ctk.StringVar()
        self.achievement_17_unlock_date = ctk.StringVar()
        self.achievement_18_unlock_date = ctk.StringVar()
        self.achievement_19_unlock_date = ctk.StringVar()

        self.achievement_icons = {
            1: self.achievement_1_icon,
            2: self.achievement_2_icon,
            3: self.achievement_3_icon,
            4: self.achievement_4_icon,
            5: self.achievement_5_icon,
            6: self.achievement_6_icon,
            7: self.achievement_7_icon,
            8: self.achievement_8_icon,
            9: self.achievement_9_icon,
            10: self.achievement_10_icon,
            11: self.achievement_11_icon,
            12: self.achievement_12_icon,
            13: self.achievement_13_icon,
            14: self.achievement_14_icon,
            15: self.achievement_15_icon,
            16: self.achievement_16_icon,
            17: self.achievement_17_icon,
            18: self.achievement_18_icon,
            19: self.achievement_19_icon,
        }

        #endregion

        self.create_widgets()

    def create_widgets(self):
        # ==================== [ROOT FRAMES] ====================
        #region RootFrames
        navbar = Navbar(self, self.controller)
        content = ctk.CTkScrollableFrame(self, corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(4, weight=1)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)
        #endregion

        # ==================== [PAGE FRAMES] ====================
        #region PageFrames
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

        # ==================== [ACHIEVEMENTS CONTENT] ====================
        #region AchievementsContent    
       
        #region AchievementOverviewSection
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

        achievements_left_sub_banner = ctk.CTkLabel(achievements_banner_subsection, text="", image=achievement_images.achievements_banner)
        achievements_triple_stars = ctk.CTkLabel(achievements_banner_subsection, text="", image=achievement_images.achievements_triple_stars)
        achievements_right_sub_banner = ctk.CTkLabel(achievements_banner_subsection, text="", image=achievement_images.achievements_banner)

        achievements_left_sub_banner.grid(row=0, column=0)
        achievements_triple_stars.grid(row=0, column=1, padx=20)
        achievements_right_sub_banner.grid(row=0, column=2)

        achievements_overview_progress_info = ctk.CTkLabel(achievements_overview_subsection, text="3 of 12 (40%) achievements earned:", font=("", 24))
        achievements_overview_progressbar = ctk.CTkProgressBar(achievements_overview_subsection, border_width=3, height=40, width=600, corner_radius=0)

        achievements_overview_progress_info.grid(row=0, column=0, pady=(0, 10))
        achievements_overview_progressbar.grid(row=1, column=0)                
        #endregion

        #region AchievementOneSection
        # First Day: Log into Aeoncell for the first time
        achievement_slot_1_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_1_section.grid_propagate(False)
        # achievement_slot_1_section.grid_rowconfigure(0, weight=1)
        # achievement_slot_1_section.grid_rowconfigure(2, weight=1)
        # achievement_slot_1_section.grid_columnconfigure(0, weight=1)
        # achievement_slot_1_section.grid_columnconfigure(4, weight=1)
        achievement_slot_1_section.grid_rowconfigure(0, weight=1)
        achievement_slot_1_section.grid_rowconfigure(2, weight=1)
        achievement_slot_1_section.grid_columnconfigure(3, weight=1)
        achievement_slot_1_section.grid(row=2, column=1, pady=(30, 0))

        achievement_slot_1_icon = ctk.CTkLabel(achievement_slot_1_section, text="", image=self.achievement_1_icon)
        achievement_slot_1_info_section = ctk.CTkFrame(achievement_slot_1_section, fg_color="transparent")
        achievement_slot_1_unlock_date = ctk.CTkLabel(achievement_slot_1_section, text="Unlocked 16 Jun 2025 @ 12:01 PM", font=("", 18))

        achievement_slot_1_icon.grid(row=1, column=1, padx=20)
        achievement_slot_1_info_section.grid(row=1, column=2)
        achievement_slot_1_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_1_name = ctk.CTkLabel(achievement_slot_1_info_section, text="First Day", font=("", 24, "bold"))
        achievement_1_desc = ctk.CTkLabel(achievement_slot_1_info_section, text="Log into Aeoncell for the first time.", font=("", 18))

        achievement_1_name.grid(row=0, column=0, sticky="w")
        achievement_1_desc.grid(row=1, column=0, sticky="w")
        #endregion

        #region AchievementTwoSection
        # First Drink: Log first hydration entry
        achievement_slot_2_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementThreeSection
        # First Sleep: Log first sleep entry
        achievement_slot_3_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementFourSection
        # First Steps: Log first steps entry
        achievement_slot_4_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementFiveSection
        # First Workout: Log first exercise entry
        achievement_slot_5_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementSixSection
        # New Profile: Change profile pic for the first time
        achievement_slot_6_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementSevenSection
        # Ten Exercises: Log 10 exercise entries
        achievement_slot_7_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementEightSection
        # Rep Warrior: Complete 1000 total reps
        achievement_slot_8_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementNineSection
        # Set It off: Complete 500 total sets
        achievement_slot_9_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementTenSection
        # Sleep Maxxed: Sleep over 9 hours in a single night
        achievement_slot_10_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementElevenSection
        # Heavy Lifter I: Lift a total of 1000kg
        achievement_slot_11_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementTwelveSection
        # Heavy Lifter II: Lift a total of 10,000kg
        achievement_slot_12_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementThirteenSection
        # Step Stacker I: Walk a total of 50,000 steps
        achievement_slot_13_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementFourteenSection
        # Step Stacker II: Walk a total of 250,000 steps
        achievement_slot_14_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementFifteenSection
        # Hydrated Human I: Drink a total of 10L
        achievement_slot_15_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementSixteenSection
        # Hydrated Human II: Drink a total of 100L 
        achievement_slot_16_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementSeventeenSection
        # Sleeping Beauty I: Sleep a total of 10hrs
        achievement_slot_17_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementEighteenSection
        # Sleeping Beauty II: Sleep a total of 100hrs
        achievement_slot_18_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

        #region AchievementNineteenSection
        # 1 Month Club: Log entries for 30 different days
        achievement_slot_19_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        #endregion

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

    def set_achievement_unlock_date(self, achievement_datetime_var):
        current_datetime = datetime.now().strftime("%d %b, %Y, %I:%M %p")
        achievement_datetime_var.set(f"Unlocked {current_datetime}")

    # def update_achievement_status(self, *args):
    #     for achievement_id in args:
    #         self.achievement_icons[achievement_id].

    # def update_achievement_status(self, achievement_id, achievement_icon_var, achievement_datetime_var):
    #     self.set_achievement_unlock_date()

    # def check_for_unlocked_achievements(self, *args):
    #     for achievement_id in args:
            