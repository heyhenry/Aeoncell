import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("themes/lavender.json")

root = ctk.CTk()
root.geometry("1280x800")
root.minsize(1280, 800)


bg_frame = ctk.CTkFrame(root)
bg_frame.pack(fill="both", expand=True)

bg_image = ctk.CTkImage(Image.open("img/cartoon_gym_background.png"), size=(root.winfo_screenwidth(), root.winfo_screenheight()))
bg_label = ctk.CTkLabel(bg_frame, image=bg_image, text="")
bg_label.pack(fill="both", expand=True, pady=0, padx=0)

form_win = ctk.CTkFrame(bg_frame, width=500, height=400, border_color="red", border_width=5)
form_win.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()