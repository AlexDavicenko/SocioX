import customtkinter as ctk
from abc import ABC

class Window(ctk.CTkFrame, ABC):
    def __init__(self, parent: ctk.CTkFrame, fg_color=None) -> None:
        super().__init__(parent, fg_color=fg_color)

    def window_bindings(self) -> None: ...

