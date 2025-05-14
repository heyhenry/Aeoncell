import customtkinter as ctk
from PIL import Image, ImageOps, ImageDraw
import os

def round_yo_pics(filepath):
    # higher the file size, the better the image quality
    size = (256, 256)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    im = Image.open(filepath)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    dot_pos = filepath.rfind(".")
    new_filename = filepath[:dot_pos] + "_rounded.png"
    output.save(new_filename)

if not os.path.exists("img/user_profile_rounded.png"):
    round_yo_pics("img/user_profile.jpg")

root = ctk.CTk()
root.geometry("500x600")

title = ctk.CTkLabel(root, text="Display Profile Image", font=("", 32))
title.pack(pady=40)

profile_image = ctk.CTkImage(light_image=Image.open("img/user_profile_rounded.png"), dark_image=Image.open("img/user_profile_rounded.png"), size=(180,180))
profile_image_display = ctk.CTkLabel(root, text="", image=profile_image)
profile_image_display.pack()

root.mainloop()

# ** some thought process notes after the fact **
# to ensure images arent being rounded every startup, 
# use naming conventions to distinguish and also have a 
# structured process to ensure every new profile image goes 
# through the process of being rounded (the latter part, could make the former before the conjunction redundant)

