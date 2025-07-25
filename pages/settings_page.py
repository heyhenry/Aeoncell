import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os
from widgets import Navbar
from utils import *

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # profile related vars
        self.profile_username_var = ctk.StringVar()
        self.profile_password_var = ctk.StringVar()
        self.profile_first_name_var = ctk.StringVar()
        self.profile_last_name_var = ctk.StringVar()
        self.profile_age_var = ctk.StringVar()
        self.profile_height_var = ctk.StringVar()
        self.profile_current_weight_var = ctk.StringVar()
        self.profile_goal_weight_var = ctk.StringVar()

        # daily related vars
        self.daily_sleep_var = ctk.StringVar()
        self.daily_walking_var = ctk.StringVar()
        self.daily_hydration_var = ctk.StringVar()

        # retrieve existing data and set daily variables with them
        # only look to retrieve data if a database has been created (i.e. user has registered)
        if self.controller.db.check_account_exists():
            # we can use rowid as the primary key reference because there will only always be a single entry in this table
            self.controller.db_cursor.execute("SELECT daily_sleep_goal, daily_steps_goal, daily_hydration_goal FROM profile_details WHERE rowid=1")
            result = self.controller.db_cursor.fetchone()
            self.daily_sleep_var.set(result[0])
            self.daily_walking_var.set(result[1])
            self.daily_hydration_var.set(result[2])
        
        # monthly related vars
        self.monthly_weight_choice_var = ctk.StringVar(value="lose")
        self.monthly_weight_var = ctk.StringVar()
        self.monthly_hydration_var = ctk.StringVar()
        self.monthly_sleep_var = ctk.StringVar()
        self.monthly_walking_var = ctk.StringVar()

        # temp for compartmentalising internally.. will fix later and only use 1 checker for all variable data retrievals.
        if self.controller.db.check_account_exists():
            self.controller.db_cursor.execute("SELECT monthly_weight_choice, monthly_weight_goal, monthly_sleep_goal, monthly_steps_goal, monthly_hydration_goal FROM profile_details WHERE rowid=1")
            result = self.controller.db_cursor.fetchone()
            self.monthly_weight_choice_var.set(result[0])
            self.monthly_weight_var.set(result[1])
            self.monthly_hydration_var.set(result[2])
            self.monthly_sleep_var.set(result[3])
            self.monthly_walking_var.set(result[4])

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        #region [Main Frames]
        navbar = Navbar(self, self.controller)
        content = ctk.CTkScrollableFrame(self, corner_radius=0)

        navbar.grid(row=0, column=0, sticky="nswe")
        content.grid(row=0, column=1, sticky="nswe")

        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(6, weight=1)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(2, weight=1)
        #endregion

        #region [Parent Frames]
        page_title = ctk.CTkLabel(content, text="Settings", font=("", 24))
        page_message = ctk.CTkLabel(content, text="Update your information here", font=("", 14))
        self.profile_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=900, height=750)
        self.daily_goals_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=900, height=430)
        self.monthly_goals_section = ctk.CTkFrame(content, fg_color=("#F5F0FF", "#2A1A4A"), border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40, width=900, height=450)

        self.profile_section.grid_propagate(False)
        self.daily_goals_section.grid_propagate(False)
        self.monthly_goals_section.grid_propagate(False)
        
        page_title.grid(row=1, column=1, padx=(0, 1000), pady=(30, 0), sticky="w")
        page_message.grid(row=2, column=1, sticky="w", pady=(0, 50))
        self.profile_section.grid(row=3, column=1, pady=(0, 50))
        self.daily_goals_section.grid(row=4, column=1, pady=(0, 50))
        self.monthly_goals_section.grid(row=5, column=1, pady=(0, 50))
        #endregion

        #region [Profile Section]
        profile_title = ctk.CTkLabel(self.profile_section, text="Profile Details", font=("", 18))
        profile_image_title = ctk.CTkLabel(self.profile_section, text="Profile Image:", font=("", 18))
        profile_browse_image_select = ctk.CTkButton(self.profile_section, text="Browse Image", font=("", 18), command=self.browse_new_profile_image)
        self.profile_image_preview = ctk.CTkLabel(self.profile_section, text="")
        self.profile_image_message = ctk.CTkLabel(self.profile_section, text="", font=("", 14))
        profile_username_title = ctk.CTkLabel(self.profile_section, text="Username:", font=("", 18))
        self.profile_username_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_username_var)
        profile_password_title = ctk.CTkLabel(self.profile_section, text="Password:", font=("", 18))
        self.profile_password_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_password_var)
        profile_first_name_title = ctk.CTkLabel(self.profile_section, text="First Name:", font=("", 18))
        self.profile_first_name_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_first_name_var)
        profile_last_name_title = ctk.CTkLabel(self.profile_section, text="Last Name:", font=("", 18))
        self.profile_last_name_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_last_name_var)
        profile_age_title = ctk.CTkLabel(self.profile_section, text="Age:", font=("", 18))
        self.profile_age_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_age_var)
        profile_height_title = ctk.CTkLabel(self.profile_section, text="Height (cm):", font=("", 18))
        self.profile_height_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_height_var)
        profile_current_weight_title = ctk.CTkLabel(self.profile_section, text="Current Weight (kg):", font=("", 18))
        self.profile_current_weight_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_current_weight_var)
        profile_goal_weight_title = ctk.CTkLabel(self.profile_section, text="Goal Weight (kg):", font=("", 18))
        self.profile_goal_weight_entry = ctk.CTkEntry(self.profile_section, font=("", 24), width=350, textvariable=self.profile_goal_weight_var)
        self.profile_action_message = ctk.CTkLabel(self.profile_section, text="", font=("", 18))
        profile_update_button = ctk.CTkButton(self.profile_section, height=60, width=200, text="Update Profile", font=("", 24), command=self.process_profile)

        profile_title.grid(row=0, column=0, sticky="w", padx=30, pady=30)
        profile_image_title.grid(row=1, column=0, padx=30, sticky="w")
        profile_browse_image_select.grid(row=2, column=0, padx=30, pady=10)
        self.profile_image_preview.grid(row=3, rowspan=3, column=0, padx=30)
        self.profile_image_message.grid(row=6, column=0, padx=30)
        profile_username_title.grid(row=1, column=1, padx=30, sticky="w")
        self.profile_username_entry.grid(row=2, column=1, padx=30)
        profile_password_title.grid(row=5, column=1, padx=30, pady=(30, 0), sticky="w")
        self.profile_password_entry.grid(row=6, column=1, padx=30)
        profile_first_name_title.grid(row=7, column=0, padx=30, pady=(30, 0), sticky="w")
        self.profile_first_name_entry.grid(row=8, column=0, padx=30)
        profile_last_name_title.grid(row=7, column=1, padx=30, pady=(30, 0), sticky="w")
        self.profile_last_name_entry.grid(row=8, column=1, padx=30)
        profile_age_title.grid(row=9, column=0, padx=30, pady=(30, 0), sticky="w")
        self.profile_age_entry.grid(row=10, column=0, padx=30)
        profile_height_title.grid(row=9, column=1, padx=30, pady=(30, 0), sticky="w")
        self.profile_height_entry.grid(row=10, column=1, padx=30)
        profile_current_weight_title.grid(row=11, column=0, padx=30, pady=(30, 0), sticky="w")
        self.profile_current_weight_entry.grid(row=12, column=0, padx=30)
        profile_goal_weight_title.grid(row=11, column=1, padx=30, pady=(30, 0), sticky="w")
        self.profile_goal_weight_entry.grid(row=12, column=1, padx=30)
        self.profile_action_message.grid(row=13, column=0, columnspan=2, pady=20)
        profile_update_button.grid(row=14, column=0, columnspan=2)

        # profile related binds
        self.profile_username_entry.bind("<Key>", lambda event: custom_entry_limit_chars(event, self.profile_username_entry, 13))
        self.profile_first_name_entry.bind("<Key>", lambda event: custom_word_only_entry_validation(event, self.profile_first_name_entry, 13))
        self.profile_last_name_entry.bind("<Key>", lambda event: custom_word_only_entry_validation(event, self.profile_last_name_entry, 13))
        self.profile_age_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_age_entry, 3))
        self.profile_height_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_height_entry, 3))
        self.profile_current_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_current_weight_entry, 3))
        self.profile_goal_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.profile_goal_weight_entry, 3))

        #endregion

        #region [Daily Section]
        daily_title = ctk.CTkLabel(self.daily_goals_section, text="Daily Goals", font=("", 18))
        daily_sleep_title = ctk.CTkLabel(self.daily_goals_section, text="Sleep (Minutes):", font=("", 24))
        self.daily_sleep_entry = ctk.CTkEntry(self.daily_goals_section, font=("", 24), width=350, textvariable=self.daily_sleep_var)
        daily_walking_title = ctk.CTkLabel(self.daily_goals_section, text="Walking (Steps):", font=("", 24))
        self.daily_walking_entry = ctk.CTkEntry(self.daily_goals_section, font=("", 24), width=350, textvariable=self.daily_walking_var)
        daily_hydration_title = ctk.CTkLabel(self.daily_goals_section, text="Hydration (Millilitres):", font=("", 24))
        self.daily_hydration_entry = ctk.CTkEntry(self.daily_goals_section, font=("", 24), width=350, textvariable=self.daily_hydration_var)
        self.daily_action_message = ctk.CTkLabel(self.daily_goals_section, text="", font=("", 18))
        daily_update_button = ctk.CTkButton(self.daily_goals_section, text="Update Goals", height=60, width=200, font=("", 24), command=self.process_daily_goals)

        daily_title.grid(row=0, column=0, sticky="w", padx=30, pady=30)
        daily_sleep_title.grid(row=1, column=0, padx=30, sticky="w")
        self.daily_sleep_entry.grid(row=2, column=0, padx=30, pady=(5, 0))
        daily_walking_title.grid(row=1, column=1, padx=30, sticky="w")
        self.daily_walking_entry.grid(row=2, column=1, padx=30, pady=(5, 0))
        daily_hydration_title.grid(row=3, column=0, padx=30, pady=(30, 0), sticky="w")
        self.daily_hydration_entry.grid(row=4, column=0, padx=30, pady=(5, 0))
        self.daily_action_message.grid(row=5, column=0, columnspan=2, pady=20)
        daily_update_button.grid(row=6, column=0, columnspan=2)

        # daily related binds
        self.daily_sleep_entry.bind("<Key>", lambda event: custom_float_only_validation(event, self.daily_sleep_entry, 3))
        self.daily_walking_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.daily_walking_entry, 5))
        self.daily_hydration_entry.bind("<Key>", lambda event: custom_float_only_validation(event, self.daily_hydration_entry, 4))

        #endregion

        #region [Monthly Section]
        monthly_title = ctk.CTkLabel(self.monthly_goals_section, text="Monthly Goals", font=("", 18))
        self.lose_weight_button = ctk.CTkButton(self.monthly_goals_section, text="Lose Weight", height=40, font=("", 18), command=lambda: self.select_weight_choice("lose"))
        self.gain_weight_button = ctk.CTkButton(self.monthly_goals_section, text="Gain Weight", height=40, font=("", 18), command=lambda: self.select_weight_choice("gain"))
        self.monthly_weight_entry = ctk.CTkEntry(self.monthly_goals_section, font=("", 24), width=350, textvariable=self.monthly_weight_var)
        monthly_hydration_title = ctk.CTkLabel(self.monthly_goals_section, text="Hydration (L):", font=("", 24))
        self.monthly_hydration_entry = ctk.CTkEntry(self.monthly_goals_section, font=("", 24), width=350, textvariable=self.monthly_hydration_var)
        monthly_sleep_title = ctk.CTkLabel(self.monthly_goals_section, text="Sleep (Hrs):", font=("", 24))
        self.monthly_sleep_entry = ctk.CTkEntry(self.monthly_goals_section, font=("", 24), width=350, textvariable=self.monthly_sleep_var)
        monthly_walking_title = ctk.CTkLabel(self.monthly_goals_section, text="Walking (Steps):", font=("", 24))
        self.monthly_walking_entry = ctk.CTkEntry(self.monthly_goals_section, font=("", 24), width=350, textvariable=self.monthly_walking_var)
        self.monthly_action_message = ctk.CTkLabel(self.monthly_goals_section, text="", font=("", 18))
        monthly_update_button = ctk.CTkButton(self.monthly_goals_section, text="Update Goals", height=60, width=200, font=("", 24), command=self.process_monthly_goals)

        monthly_title.grid(row=0, column=0, sticky="w", padx=30, pady=30)
        self.lose_weight_button.grid(row=1, column=0, padx=(30, 0), pady=(0, 10), sticky="nw")
        self.gain_weight_button.grid(row=1, column=1, pady=(0, 10), sticky="w")
        self.monthly_weight_entry.grid(row=2, column=0, columnspan=2, padx=30)
        monthly_hydration_title.grid(row=1, column=2, padx=30, pady=(0, 10), sticky="w")
        self.monthly_hydration_entry.grid(row=2, column=2, padx=30)
        monthly_sleep_title.grid(row=3, column=0, columnspan=2, padx=30, pady=(30, 0), sticky="w")
        self.monthly_sleep_entry.grid(row=4, column=0, columnspan=2, padx=30, pady=(5, 0))
        monthly_walking_title.grid(row=3, column=2, padx=30, pady=(30, 0), sticky="w")
        self.monthly_walking_entry.grid(row=4, column=2, padx=30, pady=(5, 0))
        self.monthly_action_message.grid(row=5, column=0, columnspan=3, pady=20)
        monthly_update_button.grid(row=6, column=0, columnspan=3)

        # determine pre-selection for weight choice button based on saved data
        weight = self.monthly_weight_var.get()
        if self.monthly_weight_choice_var.get() == "lose":
            self.gain_weight_button.configure(fg_color="red")
            self.lose_weight_button.configure(fg_color="green")
            # reflect the current setting in the dashboard page
            self.controller.pages["DashboardPage"].update_monthly_goal_weight("Loss", weight)
        else:
            self.lose_weight_button.configure(fg_color="red")
            self.gain_weight_button.configure(fg_color="green")
            # reflect the current setting in the dashboard page
            self.controller.pages["DashboardPage"].update_monthly_goal_weight("Gain", weight)

        # monthly related binds
        self.monthly_weight_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.monthly_weight_entry, 2))
        self.monthly_hydration_entry.bind("<Key>", lambda event: custom_float_only_validation(event, self.monthly_hydration_entry, 6))
        self.monthly_sleep_entry.bind("<Key>", lambda event: custom_float_only_validation(event, self.monthly_sleep_entry, 5))
        self.monthly_walking_entry.bind("<Key>", lambda event: custom_digit_only_entry_validation(event, self.monthly_walking_entry, 7))

        #endregion

    # allow user to search their local storage for a new profile image (.png only)
    def browse_new_profile_image(self):
        file_path = filedialog.askopenfilename(title="Select New Profile Image", filetypes=[('Image Files', '*.png')])
        if file_path:
            # generate temp rounded profile image
            generate_round_frame_image(file_path, "temp_profile_image")
            temp_profile_image = Image.open("img/temp_profile_image.png")
            # newly selected profile image storage
            new_profile_image = ctk.CTkImage(light_image=temp_profile_image, dark_image=temp_profile_image, size=(128, 128))
            # increase section box area size to accomodate new widgets
            self.profile_section.configure(height=860)
            # showcase the selected image
            self.profile_image_preview.configure(image=new_profile_image)
            # display informative message to user about their action
            self.profile_image_message.configure(text="Image Preview", font=("", 18))

    # updates the profile set by user
    def process_profile(self):
        username = self.profile_username_var.get()
        password = self.profile_password_var.get()
        first_name = self.profile_first_name_var.get()
        last_name = self.profile_last_name_var.get()
        age = self.profile_age_var.get()
        height = self.profile_height_var.get()
        current_weight = self.profile_current_weight_var.get()
        goal_weight = self.profile_goal_weight_var.get()

        # checks and validates the username and password fields (potentially others in the future but probably not required due to custom entry validation)
        # will not proceed with the processing of profile details if validation fails
        if self.validate_profile_entry_fields():
            return

        update_profile_details_query = """
        UPDATE profile_details
        SET username = ?,
        password = ?,
        first_name = ?,
        last_name = ?,
        age = ?,
        height = ?,
        current_weight = ?,
        goal_weight = ?
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(update_profile_details_query, (username, password, first_name, last_name, age, height, current_weight, goal_weight))
        self.controller.db_connection.commit()

        # check if new password was given, only then update the password in the database (as it requires rehashing)
        if not self.controller.db.verify_password(password):
            print("new password detected! password change occurred.")
            self.controller.db.update_password(password)
        # update the login's username value
        self.controller.db_cursor.execute("UPDATE authentication SET username = ?", (username,))
        self.controller.db_connection.commit()

        # update username global variable
        self.controller.update_username()

        # update the user profile image if there is a new image selected in the preview
        self.update_user_profile_img()

        # update dashboard welcome message
        self.controller.pages["DashboardPage"].update_welcome_user()

        # update login message
        self.controller.pages["LoginPage"].update_login_message()

        self.show_success_message(self.profile_action_message)

    # updates the daily goals set by user
    def process_daily_goals(self):
        # initialise variables with user's given entry values, if invalid value to type conversion, then use defaulted value.
        sleep = self.controller.validate_conversion_value(self.daily_sleep_var.get(), float, 0.0)
        steps = self.controller.validate_conversion_value(self.daily_walking_var.get(), int, 0)
        hydration = self.controller.validate_conversion_value(self.daily_hydration_var.get(), float, 0.0)
        
        # limiters in place to help discourage user from aiming for a dangerous lifestyle
        if sleep > 540.00:
            sleep = 540.00
        if steps > 99999:
            steps = 99999
        if hydration > 9999.99:
            hydration = 9999.99

        update_daily_goals_query = """
        UPDATE profile_details
        SET daily_sleep_goal = ?,
        daily_steps_goal = ?,
        daily_hydration_goal = ?
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(update_daily_goals_query, (sleep, steps, hydration))
        self.controller.db_connection.commit()
        # reinitialise the daily trackers with the updated data
        self.controller.pages["DashboardPage"].update_daily_goal_progression_displays()
        self.show_success_message(self.daily_action_message)

    def select_weight_choice(self, selection):
        if selection == "lose":
            self.gain_weight_button.configure(fg_color="red")
            self.lose_weight_button.configure(fg_color="green")
            self.monthly_weight_choice_var.set("lose")
        elif selection == "gain":
            self.lose_weight_button.configure(fg_color="red")
            self.gain_weight_button.configure(fg_color="green")
            self.monthly_weight_choice_var.set("gain")

    # updates the monthly goals set by user
    def process_monthly_goals(self):
        weight_choice = self.monthly_weight_choice_var.get()
        weight = self.controller.validate_conversion_value(self.monthly_weight_var.get(), int, 0)
        steps = self.controller.validate_conversion_value(self.monthly_walking_var.get(), int, 0)
        hydration = self.controller.validate_conversion_value(self.monthly_hydration_var.get(), float, 0.0)
        sleep = self.controller.validate_conversion_value(self.monthly_sleep_var.get(), float, 0.0)

        # 10kg weight loss/gain limit per month
        if weight > 10:
            weight = 10
        # 540.00 min per day x 31 days
        if sleep > 16740.00:
            sleep = 16740.00
        # 9999.99 ml per day x 31 days
        if hydration > 309999.99:
            hydration = 309999.99
        # 99999 steps per day x 31 days
        if steps > 3099999:
            steps = 3099999

        update_monthly_goals_query = """
        UPDATE profile_details
        SET monthly_weight_choice = ?, 
        monthly_weight_goal = ?,
        monthly_steps_goal = ?,
        monthly_hydration_goal = ?,
        monthly_sleep_goal = ?
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(update_monthly_goals_query, (weight_choice, weight, steps, hydration, sleep))
        self.controller.db_connection.commit()
        # Update the dashboard's profile section for weight choice in real-time
        if weight_choice == "lose":
            self.controller.pages["DashboardPage"].update_monthly_goal_weight("Loss", weight)
        elif weight_choice == "gain":
            self.controller.pages["DashboardPage"].update_monthly_goal_weight("Gain", weight)
        self.controller.pages["DashboardPage"].update_monthly_goal_progression_displays()
        self.show_success_message(self.monthly_action_message)

    # display a temporary notification letting the user know of the successful action
    def show_success_message(self, section_widget):
        # list out the possible messages based on given widget
        section_messages = {
            self.profile_action_message: "Profile Successfully Updated.",
            self.daily_action_message: "Daily Goals Successfully Updated.",
            self.monthly_action_message: "Monthly Goals Successfully Updated."
        }
        # updated the widgets text
        section_widget.configure(text=section_messages[section_widget], text_color="#2E7D32")
        # reset to an empty string after a delayed time
        section_widget.after(1000, lambda: section_widget.configure(text=""))
           
    def validate_profile_entry_fields(self):
        username = self.profile_username_var.get()
        password = self.profile_password_var.get()

        # validate username
        if len(username) < 4:
            self.controller.show_error_message(self.profile_action_message, "Username must be at least 4 chars.")
            return True
        elif username.isspace():
            self.controller.show_error_message(self.profile_action_message, "Username cannot be whitespaces.")
            return True
        elif " " in username:
            self.controller.show_error_message(self.profile_action_message, "Username cannot contain spaces.")
            return True

        # validate password
        if len(password) < 8:
            self.controller.show_error_message(self.profile_action_message, "Password must be at least 8 chars.")
            return True
        elif password.isspace():
            self.controller.show_error_message(self.profile_action_message, "Password cannot be whitespaces.")
            return True
        elif " " in password:
            self.controller.show_error_message(self.profile_action_message, "Password cannot contain spaces.")
            return True
        
        return False
 
    # retrieve the current saved data related to each section (if there is any)
    # and populate entry with it
    def retrieve_current_info(self):
        # listed profile detail initialised variables in order of sql table
        entry_vars = [
            self.profile_username_var,
            self.profile_password_var,
            self.profile_first_name_var,
            self.profile_last_name_var,
            self.profile_age_var,
            self.profile_height_var,
            self.profile_current_weight_var, 
            self.profile_goal_weight_var,
            self.daily_sleep_var,
            self.daily_walking_var,
            self.daily_hydration_var,
            self.monthly_weight_choice_var,
            self.monthly_weight_var,
            self.monthly_hydration_var,
            self.monthly_sleep_var,
            self.monthly_walking_var
        ]
        retrieve_current_data = """
        SELECT 
            username,
            password,
            first_name,
            last_name,
            age,
            height,
            current_weight,
            goal_weight,
            daily_sleep_goal,
            daily_steps_goal,
            daily_hydration_goal,
            monthly_weight_choice,
            monthly_weight_goal,
            monthly_hydration_goal,
            monthly_sleep_goal,
            monthly_steps_goal
        FROM profile_details 
        WHERE rowid=1
        """
        self.controller.db_cursor.execute(retrieve_current_data)
        result = self.controller.db_cursor.fetchone()
        # only proceed with updating entry fields if there is stored data found
        if result:
            # loop through and set each variable with its saved data from the database except for monthly_weight_choice
            for i in range(len(result)):
                if i != 11:
                    entry_vars[i].set(result[i])

        # ensure the weight choice button is correctly selected
        self.select_weight_choice(result[11])

        self.reset_profile_preview()

    # update the user's profile image
    def update_user_profile_img(self):
        # during updating user's profile image, check if conditions meet to unlock the 'new profile" achievement
        self.controller.pages["AchievementsPage"].check_new_profile()
        # updating user's profile image
        # check if a temp profile image exists aka user has selected a new image
        if os.path.isfile("img/temp_profile_image.png"):
            # open the new profile image that's temporarily stored
            temp_image = Image.open("img/temp_profile_image.png")
            # update the user's profile image by overriding the user_profile.png by just renaming the new desire as 'user_profile.png'
            temp_image.save("img/user_profile.png")
            # remove the temporary image save -> 'temp_profile_image.png'
            os.remove("img/temp_profile_image.png")
        # updates the profile image on the dashboard and login simultaneously
        self.controller.pages["DashboardPage"].update_dashboard_profile_image()
        self.controller.pages["LoginPage"].update_login_profile_image()

    # reset the profile image preview display
    def reset_profile_preview(self):
        self.profile_image_preview.configure(image=None)
        # check to see if a temp profile image has been saved
        if os.path.isfile("img/temp_profile_image.png"):
            # if so, delete the temp image
            os.remove("img/temp_profile_image.png")
        # only viable solution after testing ->
        # destroy the label widget and re-implement due to internal ctk cavas redraw issues with images
        self.profile_image_preview.destroy()
        self.profile_image_preview = ctk.CTkLabel(self.profile_section, text="")
        self.profile_image_preview.grid(row=3, column=0, padx=30)
        self.profile_image_message.configure(text="")
        self.profile_section.configure(height=750)