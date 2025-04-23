import customtkinter as ctk

def custom_date_entry_validation(event, widget):
    
    # allow normal function of the backspace key
    if event.keysym == "BackSpace":
        return
    
    # get char inputs
    char = event.char
    
    # get cursor position
    i = widget.index("insert")

    # ignore if not a digit
    if not char.isdigit():
        return "break"
    
    # get current full length user input in the entry field
    current = widget.get()
    digits_only = [c for c in current if c.isdigit()]

    # limit to 8 chars aka ignore any further 'valid digits'
    if len(digits_only) >= 8:
        return "break"
    
    # insert digits in correct spot in the digits_only list, 
    # factoring in dashes which wont be inserted into the list, 
    # but is visibly present in the user input and will be maintained as such
    digits_only.insert(i - current[:i].count("-"), char)

    # create formatted string
    formatted_string = ""
    for idx, c in enumerate(digits_only):
        if idx == 2 or idx == 4:
            formatted_string += "-"
        formatted_string += c

    # update the entry field
    widget.delete(0, ctk.END)
    widget.insert(0, formatted_string)

    # set the cursor position to be post final char inserted last
    if i == 2 or i == 5:
        dash_offset = 1
    else:
        dash_offset = 0

    widget.icursor(min(i + 1 + dash_offset, len(formatted_string)))

    return "break"



def print_details():
    exercise_name_var.set(exercise_entry.get())
    date_var.set(date_entry.get())
    print(f"Exercise Name: {exercise_name_var.get()}\nDate Exercised: {date_var.get()}")

root = ctk.CTk()
root.geometry("800+300")

exercise_name_var = ctk.StringVar()
date_var = ctk.StringVar()

exercise_name_title = ctk.CTkLabel(root, text="Exercise Name:")
exercise_entry = ctk.CTkEntry(root)
root.after(100, exercise_entry.focus_set)

date_title = ctk.CTkLabel(root, text="Date:")
date_entry = ctk.CTkEntry(root)

submission = ctk.CTkButton(root, text="Print Details", command=print_details)

exercise_name_title.grid(row=0, column=0, pady=(30, 10), padx=20)
exercise_entry.grid(row=1, column=0, pady=10, padx=20)
date_title.grid(row=2, column=0, pady=10, padx=20)
date_entry.grid(row=3, column=0, pady=10, padx=20)
submission.grid(row=4, column=0, pady=(10, 30), padx=20)

date_entry.bind("<Key>", lambda event: custom_date_entry_validation(event, date_entry))


root.mainloop()