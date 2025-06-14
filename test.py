import customtkinter as ctk

def configure_scroll_region():
    # Update both the scrollregion AND force a canvas update
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.update_idletasks()  # This forces immediate update
    
    # Additional check to ensure scrollbars appear correctly
    if content.winfo_height() > canvas.winfo_height():
        v_scroll.grid()  # Ensure vertical scrollbar is visible
    if content.winfo_width() > canvas.winfo_width():
        h_scroll.grid()  # Ensure horizontal scrollbar is visible

root = ctk.CTk()
root.geometry("1200x1000")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# Main container
container = ctk.CTkFrame(root)
container.grid(row=1, column=1, sticky="nsew")
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Canvas setup
canvas = ctk.CTkCanvas(container, bg="gray14", highlightthickness=0)
canvas.grid(row=0, column=0, sticky="nsew")

# Scrollbars
v_scroll = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
h_scroll = ctk.CTkScrollbar(container, orientation="horizontal", command=canvas.xview)
v_scroll.grid(row=0, column=1, sticky="ns")
h_scroll.grid(row=1, column=0, sticky="ew")

# Connect scrollbars
canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

# Content frame
content = ctk.CTkFrame(canvas, width=1500, height=1200, border_width=3, border_color="red")
content.grid_propagate(False)
canvas.create_window((0, 0), window=content, anchor="nw")

# Add content
for i in range(30):
    ctk.CTkButton(content, text=f"Row {i}").grid(row=i, column=0, padx=5, pady=5)
for i in range(15):
    ctk.CTkButton(content, text=f"Col {i}").grid(row=0, column=i+1, padx=5, pady=5)

# Initial configuration
content.update_idletasks()  # Ensure widgets are rendered
configure_scroll_region()  # Force proper scrollbar initialization

# Mouse wheel bindings
def on_mousewheel(event):
    if event.state & 0x0001:  # Shift key
        canvas.xview_scroll(-1*(event.delta//120), "units")
    else:
        canvas.yview_scroll(-1*(event.delta//120), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)
canvas.bind_all("<Shift-MouseWheel>", on_mousewheel)

root.mainloop()