import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

root = ctk.CTk()

temp_file_path = ""
new_image = None

def browse_image():
    global temp_file_path, new_image
    file_path = filedialog.askopenfilename(title="Save a new image.", filetypes=[('Image Files', '*.png')])
    if file_path:
        new_image = ctk.CTkImage(light_image=Image.open(file_path), dark_image=Image.open(file_path), size=(128,128))
        image_showcase.configure(image=new_image)
        temp_file_path = file_path

def save_image():
    if temp_file_path:
        print(temp_file_path)
        save_image = Image.open(temp_file_path)
        save_image = save_image.save("img/test_image.png")
        notif_message.configure(text="Image has been saved.", text_color="green")
        notif_message.after(500, lambda: notif_message.configure(text="", text_color="white"))

def clear_image():
    global temp_file_path, new_image
    if temp_file_path:
        new_image = None
        image_showcase.configure(image=None)
        image_showcase.pack_forget()
        image_showcase.pack()
        notif_message.configure(text="Image has been cleared.", text_color="blue")
        notif_message.after(500, lambda: notif_message.configure(text="", text_color="white"))
        temp_file_path = ""

root.geometry("400x300")

show_save_img = ctk.CTkButton(root, text="show and save image.", command=browse_image)
show_save_img.pack(pady=20)

image_showcase = ctk.CTkLabel(root, text="")
image_showcase.pack()

clear_image_btn = ctk.CTkButton(root, text="Clear Image", command=clear_image)
clear_image_btn.pack(side=ctk.LEFT, padx=(40, 20))

save_image_btn = ctk.CTkButton(root, text="Save Image", command=save_image)
save_image_btn.pack(side=ctk.LEFT)

notif_message = ctk.CTkLabel(root, text="")

root.mainloop()