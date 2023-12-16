import tkinter as tk
import customtkinter as ctk

from controller_protocol import Controller
from windows.window import Window
from windows.widgets import PlaceHolderEntry
from windows.window_types import WindowTypes

class SettingWindow(Window):
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)
        self.controller = controller
