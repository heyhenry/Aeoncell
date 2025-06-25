import customtkinter as ctk

root = ctk.CTk()

def update_progress():
    progression_bar.set(float(current_progress.get())/total_progress)

current_progress = ctk.StringVar(value=300.20)
total_progress = 9999.99

progression_bar = ctk.CTkProgressBar(root, border_width=3, height=40, width=300)
progression_bar.set(float(current_progress.get())/total_progress)
progression_bar.pack(pady=(20, 40))
progress_entry = ctk.CTkEntry(root, textvariable=current_progress, font=("", 18))
progress_entry.pack(pady=(0, 10))
progress_update = ctk.CTkButton(root, text="Update Progress", font=("", 18), height=60, command=update_progress)
progress_update.pack()


root.mainloop()