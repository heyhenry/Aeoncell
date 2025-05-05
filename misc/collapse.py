import customtkinter as ctk
import sqlite3

conn = sqlite3.connect("aeoncell_database.db")
cursor = conn.cursor()

root = ctk.CTk()

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

root.title("Collapse Me!")
root.geometry("800x600")
lst = []
def toggle_frame():
    if latest_exercise_checkbox.get() == False:
        for i in lst:
            i.grid_forget()
        lst.clear()
        cursor.execute("SELECT exercise_name, date, type FROM exercise_entries ORDER BY id DESC LIMIT 1")
        entry = cursor.fetchone()
        latest_entry.configure(exercise_frame, text=f"{entry[0]} | {entry[1]} | {entry[2]}", font=("", 24))
        latest_entry.grid(row=0, column=0, sticky="w")
    else:
        latest_entry.grid_forget()
        cursor.execute("SELECT exercise_name, date, type FROM exercise_entries ORDER BY id DESC")
        for i, entry in enumerate(cursor.fetchall()):  
            lst.append(ctk.CTkLabel(exercise_frame, text=f"{entry[0]} | {entry[1]} | {entry[2]}", font=("", 24)))
            lst[i].grid(row=i, column=0, sticky="w")

title = ctk.CTkLabel(root, text="Recent Log", font=("", 32))
latest_exercise_checkbox = ctk.CTkCheckBox(root, text="Expand Log", font=("", 32), command=toggle_frame)
exercise_frame = ctk.CTkScrollableFrame(root, width=500, height=200)
latest_entry = ctk.CTkLabel(exercise_frame)
cursor.execute("SELECT exercise_name, date, type FROM exercise_entries ORDER BY id DESC LIMIT 1")
entry = cursor.fetchone()
latest_entry.configure(exercise_frame, text=f"{entry[0]} | {entry[1]} | {entry[2]}", font=("", 24))
latest_entry.grid(row=0, column=0, sticky="w")


title.grid(row=1, column=1, padx=10, pady=10)
latest_exercise_checkbox.grid(row=2, column=1)
exercise_frame.grid(row=3, column=1)

root.mainloop()