import customtkinter as ctk
from tkinter import Canvas

class CTkBidirectionalFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Extract width/height first since we need them for canvas
        width = kwargs.pop('width', 300)
        height = kwargs.pop('height', 300)
        
        super().__init__(master, **kwargs)
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create Canvas
        self._canvas = Canvas(
            self,
            width=width,
            height=height,
            highlightthickness=0,
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        )
        self._canvas.grid(row=0, column=0, sticky="nsew")
        
        # Create Scrollbars
        self._v_scroll = ctk.CTkScrollbar(self, orientation="vertical", command=self._canvas.yview)
        self._h_scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=self._canvas.xview)
        self._v_scroll.grid(row=0, column=1, sticky="ns")
        self._h_scroll.grid(row=1, column=0, sticky="ew")
        
        # Configure Canvas
        self._canvas.configure(
            yscrollcommand=self._v_scroll.set,
            xscrollcommand=self._h_scroll.set
        )
        
        # Create container frame
        self._scrollable_frame = ctk.CTkFrame(self._canvas)
        self._canvas.create_window((0, 0), window=self._scrollable_frame, anchor="nw")
        
        # Forward all child additions to the scrollable frame
        self._children = self._scrollable_frame.children
        
        # Bind events
        self._scrollable_frame.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind_all("<MouseWheel>", self._vertical_scroll)
        self._canvas.bind_all("<Shift-MouseWheel>", self._horizontal_scroll)
    
    def _vertical_scroll(self, event):
        self._canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _horizontal_scroll(self, event):
        self._canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    # Make it behave like a normal frame
    def __getattr__(self, name):
        """Forward any unknown attribute calls to the inner frame"""
        return getattr(self._scrollable_frame, name)