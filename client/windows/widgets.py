#https://blog.teclado.com/tkinter-placeholder-entry-field/

import customtkinter as ctk
import tkinter as tk

#add centered option with string formatting like in the blad guys video
class PlaceHolderEntry(ctk.CTkEntry):
    def __init__(self, master: ctk.CTkFrame, placeholder: str, show: str = "", *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        self.insert("0", placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        self.placeholder = placeholder
        self.show_char = show
        
        
    def _clear_placeholder(self, e: tk.Event = None) -> None:

        if self.get() == self.placeholder:
            self.configure(show = self.show_char)
            self.delete(0, tk.END)


    def _add_placeholder(self, e: tk.Event = None) -> None:
        if not self.get():
            self.configure(show = "")
            self.insert(0, self.placeholder)

    def clear(self, e: tk.Event = None) -> None:
        self.delete(0, tk.END)
        self.insert(0, self.placeholder)