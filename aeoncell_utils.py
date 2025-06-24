import customtkinter as ctk
from PIL import Image, ImageOps, ImageDraw

def custom_date_entry_validation(event, widget):
    # allow normal function of the backspace key
    if event.keysym == "BackSpace":
        return
    
    # get char input
    char = event.char
    # get cursor position 
    i = widget.index("insert")

    # ignore if not a digit
    if not char.isdigit():
        return "break"
    
    # get current full length user input in the entry field
    current = widget.get()
    digits_only = [c for c in current if c.isdigit()]

    # limit user full length input to 8 characters
    # by ignoring further inputs
    if len(digits_only) >= 8:
        return "break"
    
    # insert the current user's input (char) in the correct position in the digits_only list,
    # factoring and accounting for the dash 
    # 2 worlds: reality of the what the user sees in the entry field vs the reality of what goes inside the digits_only list (dashes are excluded here)
    digits_only.insert(i - current[:i].count("-"), char)

    # create formatted string aka the user's validated input (visible to the user)
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

    # min function implemented as a guard clause, to ensure that index position isn't out of bounds
    widget.icursor(min(i + 1 + dash_offset, len(formatted_string)))

    # prevent duplicate insertion in the entry field, as char is inserted and dealt with earlier
    return "break"

def custom_time_entry_validation(event, widget):
    if event.keysym == "BackSpace":
        return
    
    i = widget.index("insert")
    char = event.char

    if not char.isdigit():
        return "break"
    
    current = widget.get()
    digits_only = [c for c in current if c.isdigit()]

    if len(digits_only) >= 4:
        return "break"
    
    digits_only.insert(i - current[:i].count(":"), char)

    formatted_string = ""
    for idx, c in enumerate(digits_only):
        if idx == 2:
            formatted_string += ":"
        formatted_string += c

    widget.delete(0, ctk.END)
    widget.insert(0, formatted_string)

    if i == 2:
        dash_offset = 1
    else:
        dash_offset = 0

    widget.icursor(min(i + 1 + dash_offset, len(formatted_string)))

    return "break"

def custom_digit_limit_entry_validation(event, widget, digit_limit):
    if event.keysym == "BackSpace":
        return
    
    i = widget.index("insert")
    char = event.char

    if not char.isdigit():
        return "break"
    
    current = widget.get()
    digits_only = [c for c in current if c.isdigit()]

    if len(digits_only) >= digit_limit:
        return "break"
    
    digits_only.insert(i, char)

    formatted_string = "".join(digits_only)

    widget.delete(0, ctk.END)
    widget.insert(0, formatted_string)

    widget.icursor(min(i + 1, len(formatted_string)))

    return "break"

def custom_entry_limit_chars(event, widget, limit):
    if event.keysym == "BackSpace":
        return 
    
    if len(widget.get()) >= limit:
        return "break"

def custom_word_only_entry_validation(event, widget, letter_limit):
    if event.keysym == "BackSpace":
        return
    
    if letter_limit is not None and len(widget.get()) >= letter_limit:
        return "break"

    char = event.char

    # if next input value is not a letter, then ignore
    if not char.isalpha():
        return "break"
    
def custom_digit_only_entry_validation(event, widget, digit_limit):
    if event.keysym == "BackSpace":
        return
    
    if digit_limit is not None and len(widget.get()) >= digit_limit:
        return "break"
    
    char = event.char

    if not char.isdigit():
        return "break"
    
# def custom_float_only_entry_validation(event, widget):
#     if event.keysym == "BackSpace":
#         return
    
#     char = event.char

#     # if the input is not a digit or ".", ignore
#     if not (char.isdigit() or char == "."):
#         return "break"

#     # if the user attempts to input a "." as the first char, ignore (ex. 12.2 <-- valid, ex. .2 <-- invalid)
#     if char == "." and widget.index("insert") == 0:
#         return "break"
    
#     # if there already is a ".", ignore any future "." 
#     if char == "." and "." in widget.get():
#         return "break"
    
#     # ignore incoming inputs if there is already 2 digits post the "." placement
#     if "." in widget.get():
#         # when the index of the "."
#         dot_index = widget.get().rfind(".")
#         # using the found index, find out the length of digits after the "."
#         if len(widget.get()[dot_index+1:]) == 2:
#             return "break"
        
def custom_float_only_entry_limited_validation(event, widget, digit_limit):
    if event.keysym == "BackSpace":
        return
    
    if digit_limit is not None and len(widget.get()) >= digit_limit:
        return "break"

    char = event.char

    # if the input is not a digit or ".", ignore
    if not (char.isdigit() or char == "."):
        return "break"

    # if the user attempts to input a "." as the first char, ignore (ex. 12.2 <-- valid, ex. .2 <-- invalid)
    if char == "." and widget.index("insert") == 0:
        return "break"
    
    # if there already is a ".", ignore any future "." 
    if char == "." and "." in widget.get():
        return "break"
    
    # ignore incoming inputs if there is already 2 digits post the "." placement
    if "." in widget.get():
        # when the index of the "."
        dot_index = widget.get().rfind(".")
        # using the found index, find out the length of digits after the "."
        if len(widget.get()[dot_index+1:]) == 2:
            return "break"

def custom_hydration_validation(event, widget):
    if event.keysym == "BackSpace":
        return 
    
    char = event.char
    i = widget.index("insert")

    if not char.isdigit():
        return "break"
    
    current = widget.get()
    digits_only = [c for c in current if c.isdigit()]

    if len(digits_only) >= 6:
        return "break"
    
    digits_only.insert(i - current[:i].count("."), char)

    formatted_string = ""
    for idx, c in enumerate(digits_only):
        if idx == 4:
            formatted_string += "."
        formatted_string += c
    
    widget.delete(0, ctk.END)
    widget.insert(0, formatted_string)

    if i == 4:
        decimal_point_offset = 1
    else:
        decimal_point_offset = 0

    widget.icursor(min(i + 1 + decimal_point_offset, len(formatted_string)))

    return "break"

def custom_sleep_validation(event, widget):
    if event.keysym == "BackSpace":
        return 
    
    char = event.char
    i = widget.index("insert")

    if not char.isdigit():
        return "break"
    
    current = widget.get()
    digits_only = [c for c in current if c.isdigit()]

    if len(digits_only) >= 5:
        return "break"
    
    digits_only.insert(i - current[:i].count("."), char)

    formatted_string = ""
    for idx, c in enumerate(digits_only):
        if idx == 3:
            formatted_string += "."
        formatted_string += c
    
    widget.delete(0, ctk.END)
    widget.insert(0, formatted_string)

    if i == 4:
        decimal_point_offset = 1
    else:
        decimal_point_offset = 0

    widget.icursor(min(i + 1 + decimal_point_offset, len(formatted_string)))

    return "break"

def custom_float_only_validation(event, widget, digits_before_point):
    # add 2 digits to account for two decimal points
    digits = digits_before_point + 2
    point_index = digits_before_point

    if event.keysym == "BackSpace":
        return 
    
    char = event.char
    i = widget.index("insert")

    if not char.isdigit():
        return "break"
    
    current = widget.get()
    digits_only = [c for c in current if c.isdigit()]

    if len(digits_only) >= digits:
        return "break"
    
    digits_only.insert(i - current[:i].count("."), char)

    formatted_string = ""
    for idx, c in enumerate(digits_only):
        if idx == point_index:
            formatted_string += "."
        formatted_string += c
    
    widget.delete(0, ctk.END)
    widget.insert(0, formatted_string)

    if i == digits_before_point:
        decimal_point_offset = 1
    else:
        decimal_point_offset = 0

    widget.icursor(min(i + 1 + decimal_point_offset, len(formatted_string)))

    return "break"







# give an image a rounded frame and saved as its own file
def generate_round_frame_image(filepath, new_filename):
    # create the mask shape
    size = (256, 256)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # choose an image to be altered
    selected_image = Image.open(filepath)

    # round the selected image
    round_image = ImageOps.fit(selected_image, mask.size, centering=(0.5, 0.5))
    # prioritise the shape over image
    round_image.putalpha(mask)

    # concatenate and create a new filename in the same filepath with the same general naming convention with a unique marker (i.e. '_rounded')
    # also, using 'png' image extension as jpg, jpeg is incompatible
    new_filename = "img/" + new_filename + ".png"
    # save new rounded image 
    round_image.save(new_filename)

def generate_round_rectangle_image(filepath):
    original_image = Image.open(filepath)

    mask = Image.new('L', original_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        [(0,0), original_image.size],
        radius=40,
        fill=255
    )

    round_image = original_image.copy()
    round_image.putalpha(mask)

    new_filename = filepath[:filepath.rfind(".")] + "_recround.png"
    round_image.save(new_filename)
    print("successfully created image.")

# generate_round_rectangle_image("img/capsule_original.png")