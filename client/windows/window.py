import customtkinter as ctk

from abc import ABC, abstractclassmethod

class Window(ctk.CTkFrame, ABC):
    def __init__(self, parent: ctk.CTkFrame) -> None:
        super().__init__(parent)


    def window_bindings(self) -> None:
        pass