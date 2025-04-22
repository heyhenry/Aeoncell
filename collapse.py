import customtkinter as ctk

root = ctk.CTk()

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

root.title("Collapse Me!")
root.geometry("800x600")

def toggle_frame():
    if latest_exercise_checkbox.get() == False:
        exercise_frame.grid(row=3, column=1)
    else:
        exercise_frame.grid_forget()

title = ctk.CTkLabel(root, text="Recent Log", font=("", 32))
latest_exercise_checkbox = ctk.CTkCheckBox(root, text="Poop", font=("", 32), command=toggle_frame)
exercise_frame = ctk.CTkScrollableFrame(root, width=300, height=200)
lst = []
for i in range(10):
    lst.append(ctk.CTkLabel(exercise_frame, text=f"Index: {i} something new"))
    lst[i].grid(row=i, column=0)

title.grid(row=1, column=1, padx=10, pady=10)
latest_exercise_checkbox.grid(row=2, column=1)
exercise_frame.grid(row=3, column=1)

root.mainloop()