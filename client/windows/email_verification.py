

import tkinter as tk
import customtkinter as ctk

from controller_protocol import Controller
from windows.window import Window
from windows.widgets import PlaceHolderEntry

class EmailVerificationWindow(Window):
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text = 'You will be emailed a verification code at (TODO: email)')
        self.label.pack()

        self.verify_code_button = ctk.CTkButton(self, text= "Verify code", command = self.verify_code_button_clicked)
        self.verify_code_button.pack()


    def back_button_clicked(self) -> None:
        self.controller.switch_frame('LoginWindow')

    def verify_code_button_clicked(self):
        
        #If code correct:

        pass
        

        #else reenter code
