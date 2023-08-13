#https://blog.teclado.com/tkinter-placeholder-entry-field/

import customtkinter as ctk
from tkinter import ttk

class PlaceHolderEntry(ctk.CTkEntry):
    def __init__(self, master, placeholder, show = "", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.insert("0", placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        self.placeholder = placeholder
        self.show_char = show
        
        
    def _clear_placeholder(self, e):
        if self.get() == self.placeholder:
            self.configure(show = self.show_char)
            self.delete("0", "end")


    def _add_placeholder(self, e):
        if not self.get():
            self.configure(show = "")
            self.insert("0", self.placeholder)

