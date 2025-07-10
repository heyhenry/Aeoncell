import customtkinter as ctk

# creating and using an altered version of the CTkScrollableFrame class
def reinitialise_scrollableframe_widget():
    # get an instance of the original __init__ method of the CTkScrollableFrame class
    _original_init = ctk.CTkScrollableFrame.__init__
    # try-except in place as a failsafe in the case of future changes to the CTkScrollableFrame class
    try:
        # function to update attribute found in the CTkScrollableFrame class
        def patched_init(self, *args, **kwargs):
            # initialise the class
            _original_init(self, *args, **kwargs)
            # update with custom width for the scrollbar attribute
            self._scrollbar.configure(width=100)
        # make the CTkScrollableFrame use the altered __init__ method
        ctk.CTkScrollableFrame.__init__ = patched_init
    # if the try fails, opt for the defaulted version of CTkScrollableFrame class
    except Exception:
        return

reinitialise_scrollableframe_widget()

root = ctk.CTk()

var_a = ctk.StringVar()
var_display = ctk.StringVar()

def is_valid_type(val, conversion_type, defaulted_value):
    try:
        # if the conversion can work... itll return the converted value.. 
        return conversion_type(val)
    except (ValueError, TypeError):
        # if the conversion fails, it will return .. a defaulted value in the case of a invalid conversion..
        return defaulted_value
    
def update_label():
    temp = var_a.get()
    var_display.set(temp)

main = ctk.CTkScrollableFrame(root, width=800, height=500)
label = ctk.CTkLabel(main, textvariable=var_display)
entry = ctk.CTkEntry(main, textvariable=var_a)
submission = ctk.CTkButton(main, text="submit", command=update_label)

main.grid(row=0, column=0)
main.grid_rowconfigure(0, weight=1)
main.grid_rowconfigure(1, weight=1)
main.grid_rowconfigure(2, weight=1)
main.grid_columnconfigure(0, weight=1)

label.grid(row=0, column=0)
entry.grid(row=1, column=0)
submission.grid(row=2, column=0)

root.mainloop()
        