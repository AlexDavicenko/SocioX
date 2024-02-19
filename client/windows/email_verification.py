import tkinter as tk
import customtkinter as ctk

from controller_protocol import Controller
from windows.window import Window
from windows.widgets import PlaceHolderEntry
from windows.window_types import WindowTypes

class EmailVerificationWindow(Window):
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)
        self.controller = controller

        self.email = None

        self.instruction_label = ctk.CTkLabel(
            self, text = f'You will be emailed a verification code at {self.email}', font=('TkDefaultFont', 28))
        self.instruction_label.pack(pady = (120,30))

        self.code_entry_variable = tk.Variable()
        self.code_entry_box = PlaceHolderEntry(self, placeholder= "Enter code", width = 330, height = 45)
        self.code_entry_box.pack(pady = 10)

        self.verify_code_button = ctk.CTkButton(
            self, text= "Verify code", command = self.verify_code_button_pressed,  width = 120, height = 30)
        self.verify_code_button.pack(pady = 10)

        self.back_button = ctk.CTkButton(
            self, text = 'Back', command = self.back_button_pressed, width= 120, height = 40)
        self.back_button.pack(anchor = "se", side = "bottom", padx = 30, pady = 20)

    def set_email(self, email):
        self.email = email
        self.instruction_label.configure(text = f'You will be emailed a verification code at {self.email}')

    def back_button_pressed(self, e = None) -> None:
        self.controller.switch_frame(WindowTypes.LoginWindow)

    def verify_code_button_pressed(self):
        self.controller.verify_code(self.code_entry_box.get())










        