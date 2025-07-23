import customtkinter as ctk
from PIL import Image
from widgets import Navbar
from datetime import datetime
from utils import achievement_map
from .images import achievement_images
from .constants.achievement_constants import *

class AchievementsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # ==================== [Variables] ====================
        #region Variables
        
        # intialise all achievement icon variables with the loading achievement icon
        self.achievement_icons = {
            i : achievement_images.loading_achievement_icon
            for i in range(1, 20)
        }
        # initialise all achievement unlock date variables with an empty string var
        self.achievement_unlock_date = {
            i : ctk.StringVar()
            for i in range(1, 20)
        }

        self.achievement_icon_slots = {}
        #endregion

        self.set_achievement_icons_on_startup()
        self.set_unlock_dates_on_startup()
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
        achievement_slot_1_section.grid_rowconfigure(0, weight=1)
        achievement_slot_1_section.grid_rowconfigure(2, weight=1)
        achievement_slot_1_section.grid_columnconfigure(3, weight=1)
        achievement_slot_1_section.grid(row=2, column=1, pady=(30, 0))

        self.achievement_slot_1_icon = ctk.CTkLabel(achievement_slot_1_section, text="", image=self.achievement_icons[ACHIEVEMENT_FIRST_DAY])
        achievement_slot_1_info_section = ctk.CTkFrame(achievement_slot_1_section, fg_color="transparent")
        achievement_slot_1_unlock_date = ctk.CTkLabel(achievement_slot_1_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_FIRST_DAY], font=("", 18))

        self.achievement_slot_1_icon.grid(row=1, column=1, padx=20)
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
        
        achievement_slot_2_section.grid_propagate(False)
        achievement_slot_2_section.grid_rowconfigure(0, weight=1)
        achievement_slot_2_section.grid_rowconfigure(2, weight=1)
        achievement_slot_2_section.grid_columnconfigure(3, weight=1)
        achievement_slot_2_section.grid(row=3, column=1, pady=(30, 0))

        self.achievement_slot_2_icon = ctk.CTkLabel(achievement_slot_2_section, text="", image=self.achievement_icons[ACHIEVEMENT_FIRST_DRINK])
        achievement_slot_2_info_section = ctk.CTkFrame(achievement_slot_2_section, fg_color="transparent")
        achievement_slot_2_unlock_date = ctk.CTkLabel(achievement_slot_2_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_FIRST_DRINK], font=("", 18))

        self.achievement_slot_2_icon.grid(row=1, column=1, padx=20)
        achievement_slot_2_info_section.grid(row=1, column=2)
        achievement_slot_2_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_2_name = ctk.CTkLabel(achievement_slot_2_info_section, text="First Drink", font=("", 24, "bold"))
        achievement_2_desc = ctk.CTkLabel(achievement_slot_2_info_section, text="Log first hydration entry.", font=("", 18))

        achievement_2_name.grid(row=0, column=0, sticky="w")
        achievement_2_desc.grid(row=1, column=0, sticky="w")
        #endregion

        #region AchievementThreeSection
        # First Sleep: Log first sleep entry
        achievement_slot_3_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_3_section.grid_propagate(False)
        achievement_slot_3_section.grid_rowconfigure(0, weight=1)
        achievement_slot_3_section.grid_rowconfigure(2, weight=1)
        achievement_slot_3_section.grid_columnconfigure(3, weight=1)
        achievement_slot_3_section.grid(row=4, column=1, pady=(30, 0))

        self.achievement_slot_3_icon = ctk.CTkLabel(achievement_slot_3_section, text="", image=self.achievement_icons[ACHIEVEMENT_FIRST_SLEEP])
        achievement_slot_3_info_section = ctk.CTkFrame(achievement_slot_3_section, fg_color="transparent")
        achievement_slot_3_unlock_date = ctk.CTkLabel(achievement_slot_3_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_FIRST_SLEEP], font=("", 18))

        self.achievement_slot_3_icon.grid(row=1, column=1, padx=20)
        achievement_slot_3_info_section.grid(row=1, column=2)
        achievement_slot_3_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_3_name = ctk.CTkLabel(achievement_slot_3_info_section, text="First Sleep", font=("", 24, "bold"))
        achievement_3_desc = ctk.CTkLabel(achievement_slot_3_info_section, text="Log first sleep entry.", font=("", 18))

        achievement_3_name.grid(row=0, column=0, sticky="w")
        achievement_3_desc.grid(row=1, column=0, sticky="w")
        #endregion

        #region AchievementFourSection
        # First Steps: Log first steps entry
        achievement_slot_4_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_4_section.grid_propagate(False)
        achievement_slot_4_section.grid_rowconfigure(0, weight=1)
        achievement_slot_4_section.grid_rowconfigure(2, weight=1)
        achievement_slot_4_section.grid_columnconfigure(3, weight=1)
        achievement_slot_4_section.grid(row=5, column=1, pady=(30, 0))

        self.achievement_slot_4_icon = ctk.CTkLabel(achievement_slot_4_section, text="", image=self.achievement_icons[ACHIEVEMENT_FIRST_STEPS])
        achievement_slot_4_info_section = ctk.CTkFrame(achievement_slot_4_section, fg_color="transparent")
        achievement_slot_4_unlock_date = ctk.CTkLabel(achievement_slot_4_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_FIRST_STEPS], font=("", 18))

        self.achievement_slot_4_icon.grid(row=1, column=1, padx=20)
        achievement_slot_4_info_section.grid(row=1, column=2)
        achievement_slot_4_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_4_name = ctk.CTkLabel(achievement_slot_4_info_section, text="First Steps", font=("", 24, "bold"))
        achievement_4_desc = ctk.CTkLabel(achievement_slot_4_info_section, text="Log first steps entry.", font=("", 18))

        achievement_4_name.grid(row=0, column=0, sticky="w")
        achievement_4_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementFiveSection
        # First Workout: Log first exercise entry
        achievement_slot_5_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_5_section.grid_propagate(False)
        achievement_slot_5_section.grid_rowconfigure(0, weight=1)
        achievement_slot_5_section.grid_rowconfigure(2, weight=1)
        achievement_slot_5_section.grid_columnconfigure(3, weight=1)
        achievement_slot_5_section.grid(row=6, column=1, pady=(30, 0))

        self.achievement_slot_5_icon = ctk.CTkLabel(achievement_slot_5_section, text="", image=self.achievement_icons[ACHIEVEMENT_FIRST_WORKOUT])
        achievement_slot_5_info_section = ctk.CTkFrame(achievement_slot_5_section, fg_color="transparent")
        achievement_slot_5_unlock_date = ctk.CTkLabel(achievement_slot_5_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_FIRST_WORKOUT], font=("", 18))

        self.achievement_slot_5_icon.grid(row=1, column=1, padx=20)
        achievement_slot_5_info_section.grid(row=1, column=2)
        achievement_slot_5_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_5_name = ctk.CTkLabel(achievement_slot_5_info_section, text="First Workout", font=("", 24, "bold"))
        achievement_5_desc = ctk.CTkLabel(achievement_slot_5_info_section, text="Log first exercise entry.", font=("", 18))

        achievement_5_name.grid(row=0, column=0, sticky="w")
        achievement_5_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementSixSection
        # New Profile: Change profile pic for the first time
        achievement_slot_6_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)

        achievement_slot_6_section.grid_propagate(False)
        achievement_slot_6_section.grid_rowconfigure(0, weight=1)
        achievement_slot_6_section.grid_rowconfigure(2, weight=1)
        achievement_slot_6_section.grid_columnconfigure(3, weight=1)
        achievement_slot_6_section.grid(row=7, column=1, pady=(30, 0))

        self.achievement_slot_6_icon = ctk.CTkLabel(achievement_slot_6_section, text="", image=self.achievement_icons[ACHIEVEMENT_NEW_PROFILE])
        achievement_slot_6_info_section = ctk.CTkFrame(achievement_slot_6_section, fg_color="transparent")
        achievement_slot_6_unlock_date = ctk.CTkLabel(achievement_slot_6_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_NEW_PROFILE], font=("", 18))

        self.achievement_slot_6_icon.grid(row=1, column=1, padx=20)
        achievement_slot_6_info_section.grid(row=1, column=2)
        achievement_slot_6_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_6_name = ctk.CTkLabel(achievement_slot_6_info_section, text="New Profile", font=("", 24, "bold"))
        achievement_6_desc = ctk.CTkLabel(achievement_slot_6_info_section, text="Change profile pic for the first time.", font=("", 18))

        achievement_6_name.grid(row=0, column=0, sticky="w")
        achievement_6_desc.grid(row=1, column=0, sticky="w")        
        
        #endregion

        #region AchievementSevenSection
        # Ten Exercises: Log 10 exercise entries
        achievement_slot_7_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_7_section.grid_propagate(False)
        achievement_slot_7_section.grid_rowconfigure(0, weight=1)
        achievement_slot_7_section.grid_rowconfigure(2, weight=1)
        achievement_slot_7_section.grid_columnconfigure(3, weight=1)
        achievement_slot_7_section.grid(row=8, column=1, pady=(30, 0))

        self.achievement_slot_7_icon = ctk.CTkLabel(achievement_slot_7_section, text="", image=self.achievement_icons[ACHIEVEMENT_TEN_EXERCISES])
        achievement_slot_7_info_section = ctk.CTkFrame(achievement_slot_7_section, fg_color="transparent")
        achievement_slot_7_unlock_date = ctk.CTkLabel(achievement_slot_7_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_TEN_EXERCISES], font=("", 18))

        self.achievement_slot_7_icon.grid(row=1, column=1, padx=20)
        achievement_slot_7_info_section.grid(row=1, column=2)
        achievement_slot_7_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_7_name = ctk.CTkLabel(achievement_slot_7_info_section, text="Ten Exercises", font=("", 24, "bold"))
        achievement_7_desc = ctk.CTkLabel(achievement_slot_7_info_section, text="Log 10 exercise entries.", font=("", 18))

        achievement_7_name.grid(row=0, column=0, sticky="w")
        achievement_7_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementEightSection
        # Rep Warrior: Complete 1000 total reps
        achievement_slot_8_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_8_section.grid_propagate(False)
        achievement_slot_8_section.grid_rowconfigure(0, weight=1)
        achievement_slot_8_section.grid_rowconfigure(2, weight=1)
        achievement_slot_8_section.grid_columnconfigure(3, weight=1)
        achievement_slot_8_section.grid(row=9, column=1, pady=(30, 0))

        self.achievement_slot_8_icon = ctk.CTkLabel(achievement_slot_8_section, text="", image=self.achievement_icons[ACHIEVEMENT_REP_WARRIOR])
        achievement_slot_8_info_section = ctk.CTkFrame(achievement_slot_8_section, fg_color="transparent")
        achievement_slot_8_unlock_date = ctk.CTkLabel(achievement_slot_8_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_REP_WARRIOR], font=("", 18))

        self.achievement_slot_8_icon.grid(row=1, column=1, padx=20)
        achievement_slot_8_info_section.grid(row=1, column=2)
        achievement_slot_8_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_8_name = ctk.CTkLabel(achievement_slot_8_info_section, text="Rep Warrior", font=("", 24, "bold"))
        achievement_8_desc = ctk.CTkLabel(achievement_slot_8_info_section, text="Complete 1000 total reps.", font=("", 18))

        achievement_8_name.grid(row=0, column=0, sticky="w")
        achievement_8_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementNineSection
        # Set It off: Complete 500 total sets
        achievement_slot_9_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_9_section.grid_propagate(False)
        achievement_slot_9_section.grid_rowconfigure(0, weight=1)
        achievement_slot_9_section.grid_rowconfigure(2, weight=1)
        achievement_slot_9_section.grid_columnconfigure(3, weight=1)
        achievement_slot_9_section.grid(row=10, column=1, pady=(30, 0))

        self.achievement_slot_9_icon = ctk.CTkLabel(achievement_slot_9_section, text="", image=self.achievement_icons[ACHIEVEMENT_SET_IT_OFF])
        achievement_slot_9_info_section = ctk.CTkFrame(achievement_slot_9_section, fg_color="transparent")
        achievement_slot_9_unlock_date = ctk.CTkLabel(achievement_slot_9_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_SET_IT_OFF], font=("", 18))

        self.achievement_slot_9_icon.grid(row=1, column=1, padx=20)
        achievement_slot_9_info_section.grid(row=1, column=2)
        achievement_slot_9_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_9_name = ctk.CTkLabel(achievement_slot_9_info_section, text="Set It Off", font=("", 24, "bold"))
        achievement_9_desc = ctk.CTkLabel(achievement_slot_9_info_section, text="Complete 500 total sets.", font=("", 18))

        achievement_9_name.grid(row=0, column=0, sticky="w")
        achievement_9_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementTenSection
        # Sleep Maxxed: Sleep over 9 hours in a single night
        achievement_slot_10_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_10_section.grid_propagate(False)
        achievement_slot_10_section.grid_rowconfigure(0, weight=1)
        achievement_slot_10_section.grid_rowconfigure(2, weight=1)
        achievement_slot_10_section.grid_columnconfigure(3, weight=1)
        achievement_slot_10_section.grid(row=11, column=1, pady=(30, 0))

        self.achievement_slot_10_icon = ctk.CTkLabel(achievement_slot_10_section, text="", image=self.achievement_icons[ACHIEVEMENT_SLEEP_MAXXED])
        achievement_slot_10_info_section = ctk.CTkFrame(achievement_slot_10_section, fg_color="transparent")
        achievement_slot_10_unlock_date = ctk.CTkLabel(achievement_slot_10_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_SLEEP_MAXXED], font=("", 18))

        self.achievement_slot_10_icon.grid(row=1, column=1, padx=20)
        achievement_slot_10_info_section.grid(row=1, column=2)
        achievement_slot_10_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_10_name = ctk.CTkLabel(achievement_slot_10_info_section, text="Sleep Maxxed", font=("", 24, "bold"))
        achievement_10_desc = ctk.CTkLabel(achievement_slot_10_info_section, text="Sleep over 9 hours in a single night.", font=("", 18))

        achievement_10_name.grid(row=0, column=0, sticky="w")
        achievement_10_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementElevenSection
        # Heavy Lifter I: Lift a total of 1000kg
        achievement_slot_11_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_11_section.grid_propagate(False)
        achievement_slot_11_section.grid_rowconfigure(0, weight=1)
        achievement_slot_11_section.grid_rowconfigure(2, weight=1)
        achievement_slot_11_section.grid_columnconfigure(3, weight=1)
        achievement_slot_11_section.grid(row=12, column=1, pady=(30, 0))

        self.achievement_slot_11_icon = ctk.CTkLabel(achievement_slot_11_section, text="", image=self.achievement_icons[ACHIEVEMENT_HEAVY_LIFTER_I])
        achievement_slot_11_info_section = ctk.CTkFrame(achievement_slot_11_section, fg_color="transparent")
        achievement_slot_11_unlock_date = ctk.CTkLabel(achievement_slot_11_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_HEAVY_LIFTER_I], font=("", 18))

        self.achievement_slot_11_icon.grid(row=1, column=1, padx=20)
        achievement_slot_11_info_section.grid(row=1, column=2)
        achievement_slot_11_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_11_name = ctk.CTkLabel(achievement_slot_11_info_section, text="Heavy Lifter I", font=("", 24, "bold"))
        achievement_11_desc = ctk.CTkLabel(achievement_slot_11_info_section, text="Lift a total of 1000kg.", font=("", 18))

        achievement_11_name.grid(row=0, column=0, sticky="w")
        achievement_11_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementTwelveSection
        # Heavy Lifter II: Lift a total of 10,000kg
        achievement_slot_12_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_12_section.grid_propagate(False)
        achievement_slot_12_section.grid_rowconfigure(0, weight=1)
        achievement_slot_12_section.grid_rowconfigure(2, weight=1)
        achievement_slot_12_section.grid_columnconfigure(3, weight=1)
        achievement_slot_12_section.grid(row=13, column=1, pady=(30, 0))

        self.achievement_slot_12_icon = ctk.CTkLabel(achievement_slot_12_section, text="", image=self.achievement_icons[ACHIEVEMENT_HEAVY_LIFTER_II])
        achievement_slot_12_info_section = ctk.CTkFrame(achievement_slot_12_section, fg_color="transparent")
        achievement_slot_12_unlock_date = ctk.CTkLabel(achievement_slot_12_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_HEAVY_LIFTER_II], font=("", 18))

        self.achievement_slot_12_icon.grid(row=1, column=1, padx=20)
        achievement_slot_12_info_section.grid(row=1, column=2)
        achievement_slot_12_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_12_name = ctk.CTkLabel(achievement_slot_12_info_section, text="Heavy Lifter II", font=("", 24, "bold"))
        achievement_12_desc = ctk.CTkLabel(achievement_slot_12_info_section, text="Lift a total of 10,000kg", font=("", 18))

        achievement_12_name.grid(row=0, column=0, sticky="w")
        achievement_12_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementThirteenSection
        # Step Stacker I: Walk a total of 50,000 steps
        achievement_slot_13_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_13_section.grid_propagate(False)
        achievement_slot_13_section.grid_rowconfigure(0, weight=1)
        achievement_slot_13_section.grid_rowconfigure(2, weight=1)
        achievement_slot_13_section.grid_columnconfigure(3, weight=1)
        achievement_slot_13_section.grid(row=14, column=1, pady=(30, 0))

        self.achievement_slot_13_icon = ctk.CTkLabel(achievement_slot_13_section, text="", image=self.achievement_icons[ACHIEVEMENT_STEP_STACKER_I])
        achievement_slot_13_info_section = ctk.CTkFrame(achievement_slot_13_section, fg_color="transparent")
        achievement_slot_13_unlock_date = ctk.CTkLabel(achievement_slot_13_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_STEP_STACKER_I], font=("", 18))

        self.achievement_slot_13_icon.grid(row=1, column=1, padx=20)
        achievement_slot_13_info_section.grid(row=1, column=2)
        achievement_slot_13_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_13_name = ctk.CTkLabel(achievement_slot_13_info_section, text="Step Stacker I", font=("", 24, "bold"))
        achievement_13_desc = ctk.CTkLabel(achievement_slot_13_info_section, text="Walk a total of 50,000 steps.", font=("", 18))

        achievement_13_name.grid(row=0, column=0, sticky="w")
        achievement_13_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementFourteenSection
        # Step Stacker II: Walk a total of 250,000 steps
        achievement_slot_14_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_14_section.grid_propagate(False)
        achievement_slot_14_section.grid_rowconfigure(0, weight=1)
        achievement_slot_14_section.grid_rowconfigure(2, weight=1)
        achievement_slot_14_section.grid_columnconfigure(3, weight=1)
        achievement_slot_14_section.grid(row=15, column=1, pady=(30, 0))

        self.achievement_slot_14_icon = ctk.CTkLabel(achievement_slot_14_section, text="", image=self.achievement_icons[ACHIEVEMENT_STEP_STACKER_II])
        achievement_slot_14_info_section = ctk.CTkFrame(achievement_slot_14_section, fg_color="transparent")
        achievement_slot_14_unlock_date = ctk.CTkLabel(achievement_slot_14_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_STEP_STACKER_II], font=("", 18))

        self.achievement_slot_14_icon.grid(row=1, column=1, padx=20)
        achievement_slot_14_info_section.grid(row=1, column=2)
        achievement_slot_14_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_14_name = ctk.CTkLabel(achievement_slot_14_info_section, text="Step Stacker II", font=("", 24, "bold"))
        achievement_14_desc = ctk.CTkLabel(achievement_slot_14_info_section, text="Walk a total of 250,000 steps.", font=("", 18))

        achievement_14_name.grid(row=0, column=0, sticky="w")
        achievement_14_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementFifteenSection
        # Hydrated Human I: Drink a total of 10L
        achievement_slot_15_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_15_section.grid_propagate(False)
        achievement_slot_15_section.grid_rowconfigure(0, weight=1)
        achievement_slot_15_section.grid_rowconfigure(2, weight=1)
        achievement_slot_15_section.grid_columnconfigure(3, weight=1)
        achievement_slot_15_section.grid(row=16, column=1, pady=(30, 0))

        self.achievement_slot_15_icon = ctk.CTkLabel(achievement_slot_15_section, text="", image=self.achievement_icons[ACHIEVEMENT_HYDRATED_HUMAN_I])
        achievement_slot_15_info_section = ctk.CTkFrame(achievement_slot_15_section, fg_color="transparent")
        achievement_slot_15_unlock_date = ctk.CTkLabel(achievement_slot_15_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_HYDRATED_HUMAN_I], font=("", 18))

        self.achievement_slot_15_icon.grid(row=1, column=1, padx=20)
        achievement_slot_15_info_section.grid(row=1, column=2)
        achievement_slot_15_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_15_name = ctk.CTkLabel(achievement_slot_15_info_section, text="Hydrated Human I", font=("", 24, "bold"))
        achievement_15_desc = ctk.CTkLabel(achievement_slot_15_info_section, text="Drink a total of 10L.", font=("", 18))

        achievement_15_name.grid(row=0, column=0, sticky="w")
        achievement_15_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementSixteenSection
        # Hydrated Human II: Drink a total of 100L 
        achievement_slot_16_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_16_section.grid_propagate(False)
        achievement_slot_16_section.grid_rowconfigure(0, weight=1)
        achievement_slot_16_section.grid_rowconfigure(2, weight=1)
        achievement_slot_16_section.grid_columnconfigure(3, weight=1)
        achievement_slot_16_section.grid(row=17, column=1, pady=(30, 0))

        self.achievement_slot_16_icon = ctk.CTkLabel(achievement_slot_16_section, text="", image=self.achievement_icons[ACHIEVEMENT_HYDRATED_HUMAN_II])
        achievement_slot_16_info_section = ctk.CTkFrame(achievement_slot_16_section, fg_color="transparent")
        achievement_slot_16_unlock_date = ctk.CTkLabel(achievement_slot_16_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_HYDRATED_HUMAN_II], font=("", 18))

        self.achievement_slot_16_icon.grid(row=1, column=1, padx=20)
        achievement_slot_16_info_section.grid(row=1, column=2)
        achievement_slot_16_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_16_name = ctk.CTkLabel(achievement_slot_16_info_section, text="Hydrated Human II", font=("", 24, "bold"))
        achievement_16_desc = ctk.CTkLabel(achievement_slot_16_info_section, text="Drink a total of 100L.", font=("", 18))

        achievement_16_name.grid(row=0, column=0, sticky="w")
        achievement_16_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementSeventeenSection
        # Sleeping Beauty I: Sleep a total of 10hrs
        achievement_slot_17_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_17_section.grid_propagate(False)
        achievement_slot_17_section.grid_rowconfigure(0, weight=1)
        achievement_slot_17_section.grid_rowconfigure(2, weight=1)
        achievement_slot_17_section.grid_columnconfigure(3, weight=1)
        achievement_slot_17_section.grid(row=18, column=1, pady=(30, 0))

        self.achievement_slot_17_icon = ctk.CTkLabel(achievement_slot_17_section, text="", image=self.achievement_icons[ACHIEVEMENT_SLEEPING_BEAUTY_I])
        achievement_slot_17_info_section = ctk.CTkFrame(achievement_slot_17_section, fg_color="transparent")
        achievement_slot_17_unlock_date = ctk.CTkLabel(achievement_slot_17_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_SLEEPING_BEAUTY_I], font=("", 18))

        self.achievement_slot_17_icon.grid(row=1, column=1, padx=20)
        achievement_slot_17_info_section.grid(row=1, column=2)
        achievement_slot_17_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_17_name = ctk.CTkLabel(achievement_slot_17_info_section, text="Sleeping Beauty I", font=("", 24, "bold"))
        achievement_17_desc = ctk.CTkLabel(achievement_slot_17_info_section, text="Sleep a total of 10hrs.", font=("", 18))

        achievement_17_name.grid(row=0, column=0, sticky="w")
        achievement_17_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementEighteenSection
        # Sleeping Beauty II: Sleep a total of 100hrs
        achievement_slot_18_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_18_section.grid_propagate(False)
        achievement_slot_18_section.grid_rowconfigure(0, weight=1)
        achievement_slot_18_section.grid_rowconfigure(2, weight=1)
        achievement_slot_18_section.grid_columnconfigure(3, weight=1)
        achievement_slot_18_section.grid(row=19, column=1, pady=(30, 0))

        self.achievement_slot_18_icon = ctk.CTkLabel(achievement_slot_18_section, text="", image=self.achievement_icons[ACHIEVEMENT_SLEEPING_BEAUTY_II])
        achievement_slot_18_info_section = ctk.CTkFrame(achievement_slot_18_section, fg_color="transparent")
        achievement_slot_18_unlock_date = ctk.CTkLabel(achievement_slot_18_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_SLEEPING_BEAUTY_II], font=("", 18))

        self.achievement_slot_18_icon.grid(row=1, column=1, padx=20)
        achievement_slot_18_info_section.grid(row=1, column=2)
        achievement_slot_18_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_18_name = ctk.CTkLabel(achievement_slot_18_info_section, text="Sleeping Beauty II", font=("", 24, "bold"))
        achievement_18_desc = ctk.CTkLabel(achievement_slot_18_info_section, text="Sleep a total of 100hrs.", font=("", 18))

        achievement_18_name.grid(row=0, column=0, sticky="w")
        achievement_18_desc.grid(row=1, column=0, sticky="w")        
        #endregion

        #region AchievementNineteenSection
        # 1 Month Club: Log entries for 30 different days
        achievement_slot_19_section = ctk.CTkFrame(achievements_section, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=3, corner_radius=0, width=1100, height=120)
        
        achievement_slot_19_section.grid_propagate(False)
        achievement_slot_19_section.grid_rowconfigure(0, weight=1)
        achievement_slot_19_section.grid_rowconfigure(2, weight=1)
        achievement_slot_19_section.grid_columnconfigure(3, weight=1)
        achievement_slot_19_section.grid(row=20, column=1, pady=(30, 0))

        self.achievement_slot_19_icon = ctk.CTkLabel(achievement_slot_19_section, text="", image=self.achievement_icons[ACHIEVEMENT_1_MONTH_CLUB])
        achievement_slot_19_info_section = ctk.CTkFrame(achievement_slot_19_section, fg_color="transparent")
        achievement_slot_19_unlock_date = ctk.CTkLabel(achievement_slot_19_section, textvariable=self.achievement_unlock_date[ACHIEVEMENT_1_MONTH_CLUB], font=("", 18))

        self.achievement_slot_19_icon.grid(row=1, column=1, padx=20)
        achievement_slot_19_info_section.grid(row=1, column=2)
        achievement_slot_19_unlock_date.grid(row=1, column=3, padx=(0, 20), sticky="e")

        achievement_19_name = ctk.CTkLabel(achievement_slot_19_info_section, text="1 Month Club", font=("", 24, "bold"))
        achievement_19_desc = ctk.CTkLabel(achievement_slot_19_info_section, text="Log entries for 30 different days.", font=("", 18))

        achievement_19_name.grid(row=0, column=0, sticky="w")
        achievement_19_desc.grid(row=1, column=0, sticky="w")        
        #endregion   

        # update self.achievement_icon_slots dict
        self.achievement_icon_slots.update({
            i : getattr(self, f"achievement_slot_{i}_icon")
            for i in range(1, 20)
        })

        #endregion

    def set_unlock_dates_on_startup(self):
        self.controller.db_cursor.execute("SELECT achievement_id, achievement_unlock_date FROM achievements_details")
        results = self.controller.db_cursor.fetchall()
        for i in results:
            self.achievement_unlock_date[i[0]].set(i[1])

    def set_achievement_icons_on_startup(self):
        self.controller.db_cursor.execute("SELECT achievement_id, achievement_status FROM achievements_details")
        results = self.controller.db_cursor.fetchall()
        for i in results:
            if i[1] == "locked":
                self.achievement_icons[i[0]] = achievement_images.locked_achievements[i[0]]
            else:
                self.achievement_icons[i[0]] = achievement_images.unlocked_achievements[i[0]]

    def update_achievement_unlock_date_and_icon(self, achievement_id):
        print("An Achievement has been Unlocked!")
        current_datetime = datetime.now().strftime("%d %b, %Y, %I:%M %p")
        formatted_unlocked_date = f"Unlocked {current_datetime}"
        self.controller.db_cursor.execute("UPDATE achievements_details SET achievement_unlock_date = ? WHERE achievement_id = ?", (formatted_unlocked_date, achievement_id))
        self.achievement_unlock_date[achievement_id].set(formatted_unlocked_date)
        self.achievement_icons[achievement_id] = achievement_images.unlocked_achievements[achievement_id]
        self.achievement_icon_slots[achievement_id].configure(image=self.achievement_icons[achievement_id])

    def is_achievement_locked(self, achievement_id):
        self.controller.db_cursor.execute("SELECT achievement_status FROM achievements_details WHERE achievement_id = ?", (achievement_id,))
        result = self.controller.db_cursor.fetchone()
        if result:
            if result[0] == "locked":
                return True
        return False

    def check_first_day(self):
        if self.is_achievement_locked(ACHIEVEMENT_FIRST_DAY):
            self.update_achievement_unlock_date_and_icon(ACHIEVEMENT_FIRST_DAY)
            self.controller.db_cursor.execute("UPDATE achievements_details SET achievement_status = ? WHERE achievement_id = ?", ("unlocked", ACHIEVEMENT_FIRST_DAY))
            self.controller.db_connection.commit()

    def check_first_drink(self):
        # check to see if the achievement has already been unlocked
        if self.is_achievement_locked(ACHIEVEMENT_FIRST_DRINK):
            # check to see if acheivement conditions have been met
            # unlock condition: the table has to be empty of entries before current entry is being processed
            self.controller.db_cursor.execute("SELECT 1 FROM hydration_tracker LIMIT 1")
            has_entries = self.controller.db_cursor.fetchone()
            if not has_entries:
                self.update_achievement_unlock_date_and_icon(ACHIEVEMENT_FIRST_DRINK)
                self.controller.db_cursor.execute("UPDATE achievements_details SET achievement_status = ? WHERE achievement_id = ?", ("unlocked", ACHIEVEMENT_FIRST_DRINK))
                self.controller.db_connection.commit()

    def check_first_sleep(self):
        if self.is_achievement_locked(ACHIEVEMENT_FIRST_SLEEP):
            self.controller.db_cursor.execute("SELECT 1 FROM sleep_tracker LIMIT 1")
            has_entries = self.controller.db_cursor.fetchone()
            if not has_entries:
                self.update_achievement_unlock_date_and_icon(ACHIEVEMENT_FIRST_SLEEP)
                self.controller.db_cursor.execute("UPDATE achievements_details SET achievement_status = ? WHERE achievement_id = ?", ("unlocked", ACHIEVEMENT_FIRST_SLEEP))

    def check_first_steps(self):
        if self.is_achievement_locked(ACHIEVEMENT_FIRST_STEPS):
            self.controller.db_cursor.execute("SELECT 1 FROM steps_tracker LIMIT 1")
            has_entries = self.controller.db_cursor.fetchone()
            if not has_entries:
                self.update_achievement_unlock_date_and_icon(ACHIEVEMENT_FIRST_STEPS)
                self.controller.db_cursor.execute("UPDATE achievements_details SET achievement_status = ? WHERE achievement_id = ?", ("unlocked", ACHIEVEMENT_FIRST_STEPS))

    def check_first_workout(self):
        if self.is_achievement_locked(ACHIEVEMENT_FIRST_WORKOUT):
            self.controller.db_cursor.execute("SELECT 1 FROM exercise_entries LIMIT 1")
            has_entries = self.controller.db_cursor.fetchone()
            if not has_entries:
                self.update_achievement_unlock_date_and_icon(ACHIEVEMENT_FIRST_WORKOUT)
                self.controller.db_cursor.execute("UPDATE achievements_details SET achievement_status = ? WHERE achievement_id = ?", ("unlocked", ACHIEVEMENT_FIRST_WORKOUT))

    def check_new_profile(self):
        if self.is_achievement_locked(ACHIEVEMENT_NEW_PROFILE):
            self.update_achievement_unlock_date_and_icon(ACHIEVEMENT_NEW_PROFILE)
            self.controller.db_cursor.execute("UPDATE achievements_details SET achievement_status = ? WHERE achievement_id = ?", ("unlocked", ACHIEVEMENT_NEW_PROFILE))
            self.controller.db_connection.commit()

    # def update_achievement_status(self, *args):
    #     for achievement_id in args:
    #         self.achievement_icons[achievement_id].

    # def update_achievement_status(self, achievement_id, achievement_icon_var, achievement_datetime_var):
    #     self.set_achievement_unlock_date()

    # def check_for_unlocked_achievements(self, *args):
    #     for achievement_id in args:


            