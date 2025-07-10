import customtkinter as ctk

_original_init = ctk.CTkScrollableFrame.__init__
def patched_init(self, *args, **kwargs):
    _original_init(self, *args, **kwargs)
    self._scrollbar.configure(width=100)
ctk.CTkScrollableFrame.__init__ = patched_init

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
        