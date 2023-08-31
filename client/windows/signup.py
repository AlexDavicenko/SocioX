import tkinter as tk
import customtkinter as ctk

from controller_protocol import Controller
from windows.window import Window
from windows.widgets import PlaceHolderEntry
from windows.window_types import WindowTypes

class SignUpWindow(Window):
    password_shown = False
    MONTHS = [
            "January",
            "Febuary",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "Decemeber",
        ]    

    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)

        self.controller = controller

        self.login_botton = ctk.CTkButton(self, text = "Back", command=self.back_button_clicked)
        self.login_botton.pack()

        self.firstname_entry_box = PlaceHolderEntry(self, "First name", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.lastname_entry_box = PlaceHolderEntry(self, "Last name", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.username_entry_box = PlaceHolderEntry(self, "Username", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.email_entry_box = PlaceHolderEntry(self, "Email", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.password_entry_box = PlaceHolderEntry(self, "Enter password", show = "*", font=('TkDefaultFont', 16), width = 330, height = 45)

        
        self.month = ctk.CTkOptionMenu(self, values = self.MONTHS)
        self.month.set('January')
        
        self.day_entry_box = PlaceHolderEntry(self, "Month", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.year_entry_box = PlaceHolderEntry(self, "Year", font=('TkDefaultFont', 16), width = 330, height = 45)


        self.tos_var = ctk.StringVar(value=False)
        self.tos_checkbox = ctk.CTkCheckBox(self, text="I agree with the terms of service", variable=self.tos_var, onvalue=True, offvalue=False)
        self.signup_button = ctk.CTkButton(self, text= "Sign up", command = self.signup_button_clicked)


        self.firstname_entry_box.pack()
        self.lastname_entry_box.pack()
        self.username_entry_box.pack()
        self.email_entry_box.pack()
        self.password_entry_box.pack()
        self.month.pack()
        self.day_entry_box.pack()
        self.year_entry_box.pack()
        self.tos_checkbox.pack()
        self.signup_button.pack()
        
    
    def back_button_clicked(self) -> None:
        self.controller.switch_frame(WindowTypes.LoginWindow)

        
    def signup_button_clicked(self) -> None:
        self.controller.switch_frame(WindowTypes.EmailVerificationWindow)