import customtkinter as ctk

def custom_entry_validation(event=None):
    # backspace key functions normally
    if event.keysym == "BackSpace":
        return
    
    # get cursor position
    i = entry_field.index("insert")
    char = event.char
    
    # validate only digits
    if not char.isdigit():
        # break ignores the key
        return "break"
    
    # current string values inputted into the entry field
    current = entry_field.get()
    digits_only = [c for c in current if c.isdigit()]

    # limit digits length to 8 (as per date format)
    # if 8 valid chars(i.e. digits) have been inputted into the entry field already, then ignore the incoming 
    
    # we have this here as a stopper, to let the program know not to proceed any further if there is already 8 valid digits entered in the entry field
    # because later down the line of code, we do the insertions, so stopping here prevent further character insertions - essentially stopping function early
    if len(digits_only) >= 8:
        return "break"
    
    # insert the dashes into the input at correct position
    # since dashes are visible in the input field, but are not apart of the digits_only list, this line of code
    # adjusts the insertion index position of the new char (that isn't a dash), 
    # by finding the number of dashes that are present and shifts the insertion index of the upcoming character (a digit) backward to align
    # with the digits only list.
    digits_only.insert(i - current[:i].count("-"), char)

    # create the patterned output
    formatted_output = ""
    for idx, c in enumerate(digits_only):
        if idx == 2 or idx == 4:
            formatted_output += "-"
        formatted_output += c

    # update the entry fields visible output with the patterned output
    entry_field.delete(0, ctk.END)
    entry_field.insert(0, formatted_output)

    # set cursor position (skip over the dashes)
    # dash_offset is a value to help re-align/adjust the position of the cursor
    if i == 2 or i == 5:
        dash_offset = 1
    else:
        dash_offset = 0
    # min function is used as a fail safe guard, to ensure that the index doesn't go out of bounds
    # i <-- latest/last char's index position + 1 <-- because we want to be infront of the last character + 
    # dash_offset <-- if there is a dash, this will let the program know that it needs to take a further step forward with the cursor
    # len(formatted) <-- is the comparison for the min function, because its the absolute last index possible for the cursor to legitimately be positioned
    entry_field.icursor(min(i + 1 + dash_offset, len(formatted_output)))

root = ctk.CTk()

entry_field = ctk.CTkEntry(root)
entry_field.pack()

entry_field.bind("<Key>", custom_entry_validation)


root.mainloop()