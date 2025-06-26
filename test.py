import customtkinter as ctk

root = ctk.CTk()

def update_progress():
    add_progress = float(add_progress_var.get())
    current_progress = float(current_progress_var.get()) + add_progress
    total_progress = float(total_progress_var.get())
    progression_bar.set(current_progress/total_progress)
    current_progress_var.set(current_progress)
    add_progress_var.set("")

add_progress_var = ctk.StringVar()
# w/e its starting with
current_progress_var = ctk.StringVar(value=0)
total_progress_var = ctk.StringVar(value=23123)

print(float(current_progress_var.get())/float(total_progress_var.get()))

progression_bar = ctk.CTkProgressBar(root, border_width=3, height=40, width=300, corner_radius=0)
# progression_bar.set(float(current_progress_var.get())/float(total_progress_var.get()))
progression_bar.set(0.0)
progression_bar.pack(pady=(20, 40))
progress_entry = ctk.CTkEntry(root, textvariable=add_progress_var, font=("", 18))
progress_entry.pack(pady=(0, 10))
progress_update = ctk.CTkButton(root, text="Update Progress", font=("", 18), height=60, command=update_progress)
progress_update.pack()

root.mainloop()