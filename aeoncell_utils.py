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

def custom_setsreps_entry_validation(event, widget):
    if event.keysym == "BackSpace":
        return
    
    i = widget.index("insert")
    char = event.char

    if not char.isdigit():
        return "break"
    
    current = widget.get()
    digits_only = [c for c in current if c.isdigit()]

    if len(digits_only) >= 3:
        return "break"
    
    digits_only.insert(i, char)

    formatted_string = "".join(digits_only)

    widget.delete(0, ctk.END)
    widget.insert(0, formatted_string)

    widget.icursor(min(i + 1, len(formatted_string)))

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

def custom_entry_limit_chars(event, widget, limit):
    if event.keysym == "BackSpace":
        return 
    
    if len(widget.get()) >= limit:
        return "break"

# give an image a rounded frame and saved as its own file
def generate_round_frame_image(filepath):
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

    # get the full file path including the current name of the selected image without it's extension
    dot_pos = filepath.rfind(".")
    # concatenate and create a new filename in the same filepath with the same general naming convention with a unique marker (i.e. '_rounded')
    # also, using 'png' image extension as jpg, jpeg is incompatible
    new_filename = filepath[:dot_pos] + "_rounded.png"
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