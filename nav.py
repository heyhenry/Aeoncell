import customtkinter as ctk

root = ctk.CTk()
root.geometry("1280x800")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)

navbar = ctk.CTkFrame(root, width=80, border_color="red")
navbar.grid(row=0, column=0, sticky="nswe")

content = ctk.CTkFrame(root, fg_color="black")
content.grid(row=0, column=1, sticky="nswe")

root.mainloop()