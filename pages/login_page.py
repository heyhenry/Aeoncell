import customtkinter as ctk
from PIL import Image

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()

        self.user_profile_image = ctk.CTkImage(light_image=Image.open("img/user_profile.png"), dark_image=Image.open("img/user_profile.png"), size=(120,120))
        self.masked_password_icon = ctk.CTkImage(light_image=Image.open("img/pw_masked.png"), dark_image=Image.open("img/pw_masked.png"), size=(32, 32))
        self.unmasked_password_icon = ctk.CTkImage(light_image=Image.open("img/pw_unmasked.png"), dark_image=Image.open("img/pw_unmasked.png"), size=(32, 32))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.update_login_message()

        self.create_widgets()

    def create_widgets(self):
        # login page's split frames (50/50)
        cover_image_section = ctk.CTkFrame(self, corner_radius=0)
        login_form_section = ctk.CTkFrame(self, corner_radius=0)

        cover_image_section.grid(row=0, column=0, sticky="nswe")
        login_form_section.grid(row=0, column=1, sticky="nswe")

        cover_image_section.grid_rowconfigure(0, weight=1)
        cover_image_section.grid_columnconfigure(0, weight=1)
        cover_image_section.grid_propagate(False)

        login_form_section.grid_rowconfigure(0, weight=1)
        login_form_section.grid_rowconfigure(2, weight=1)
        login_form_section.grid_columnconfigure(0, weight=1)
        login_form_section.grid_columnconfigure(2, weight=1)
        login_form_section.grid_propagate(False)

        # login form's frame
        login_form = ctk.CTkFrame(login_form_section, fg_color=("#F5F0FF", "#2A1A4A"), width=514, height=700, border_color=("#B19CD9", "#9370DB"), border_width=5, corner_radius=40)

        login_form.grid(row=1, column=1)
        login_form.grid_rowconfigure(0, weight=1)
        login_form.grid_rowconfigure(9, weight=1)
        login_form.grid_columnconfigure(0, weight=1)
        login_form.grid_columnconfigure(3, weight=1)
        login_form.grid_propagate(False)

        # internal widgets for the login form
        app_name = ctk.CTkLabel(login_form, text="Aeoncell", font=("", 18))
        form_name = ctk.CTkLabel(login_form, text="Login", font=("", 48))
        self.profile_image = ctk.CTkLabel(login_form, text="", image=self.user_profile_image)
        self.welcome_message = ctk.CTkLabel(login_form, textvariable=self.username_var, font=("", 24))
        password_title = ctk.CTkLabel(login_form, text="Enter Password:", font=("", 24))
        self.password_entry = ctk.CTkEntry(login_form, show="*", textvariable=self.password_var, font=("", 24), width=300)
        self.toggle_password_mask_btn = ctk.CTkButton(login_form, text="", image=self.masked_password_icon, bg_color="transparent", fg_color="transparent", hover_color="#B19CD9", width=0, command=self.toggle_password_masking)
        self.error_message = ctk.CTkLabel(login_form, text="", font=("", 18))
        login_submit = ctk.CTkButton(login_form, text="Login", height=50, font=("", 24), command=self.process_login)

        app_name.grid(row=1, column=1, columnspan=2)
        form_name.grid(row=2, column=1, columnspan=2, pady=(10, 20))
        self.profile_image.grid(row=3, column=1, columnspan=2, pady=(0, 30))
        self.welcome_message.grid(row=4, column=1, columnspan=2, pady=(0, 40))
        password_title.grid(row=5, column=1, columnspan=2, sticky="w")
        self.password_entry.grid(row=6, column=1, pady=(0, 10))
        self.toggle_password_mask_btn.grid(row=6, column=2, pady=(0, 10), padx=(5, 0))
        self.error_message.grid(row=7, column=1, columnspan=2)
        login_submit.grid(row=8, column=1, columnspan=2, pady=(20, 40))

        # cover image section
        login_cover_image = ctk.CTkImage(light_image=Image.open("img/cartoon_gym_background.png"), dark_image=Image.open("img/cartoon_gym_background.png"), size=((self.winfo_screenwidth()/2), (self.winfo_screenheight())))
        cover_image_display = ctk.CTkLabel(cover_image_section, text="", image=login_cover_image)
        cover_image_display.grid(row=0, column=0, sticky="nswe")

        # detect and process 'Enter' keybind interaction
        self.password_entry.bind("<Return>", self.process_login)

    def update_login_message(self):
        username = self.controller.username.get()
        self.username_var.set(f"Logged in as: \n[{username}]")

    def update_login_profile_image(self):
        self.user_profile_image = ctk.CTkImage(light_image=Image.open("img/user_profile.png"), dark_image=Image.open("img/user_profile.png"), size=(120,120))
        self.profile_image.configure(image=self.user_profile_image)

    def process_login(self, event=None):
        password = self.password_var.get()
        if self.controller.db.verify_password(password):
            # during login, check if conditions meet to unlock the 'first day' achievement
            self.controller.pages["AchievementsPage"].check_first_day()
            self.controller.show_page("DashboardPage")
            # clear the password entry field
            self.password_var.set("")
        else:
            self.controller.show_error_message(self.error_message, "Incorrect Password.")

    # toggle password masking dependent on user's choice
    def toggle_password_masking(self):
        if self.password_entry.cget("show") == "*":
            self.toggle_password_mask_btn.configure(image=self.unmasked_password_icon)
            self.password_entry.configure(show="")
        else:
            self.toggle_password_mask_btn.configure(image=self.masked_password_icon)
            self.password_entry.configure(show="*")