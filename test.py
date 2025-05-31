# credit: https://www.w3resource.com/python-exercises/tkinter/python-tkinter-dialogs-and-file-handling-exercise-8.php

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    file_path = filedialog.askopenfilename(title='Open Image File', filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
    if file_path:
        display_image(file_path)
def display_image(file_path):
    print(file_path)
    image = ctk.CTkImage(light_image=Image.open(file_path), dark_image=Image.open(file_path))
    image_display.configure(image=image)
    status_label.configure(text=f'Image loaded: {file_path}')

root = ctk.CTk()
root.title('Simple Image Viewer')

text_widget = ctk.CTkTextbox(root, wrap=ctk.WORD, height=15, width=35)
open_button = ctk.CTkButton(root, text='Open Image', command=open_image)
open_button.pack(pady=20, padx=10)
image_display = ctk.CTkLabel(root, text="", image=None)
image_display.pack(padx=20, pady=20)
status_label = ctk.CTkLabel(root, text='', padx=20, pady=10)
status_label.pack()

root.mainloop()