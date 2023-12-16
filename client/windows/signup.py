import tkinter as tk
import customtkinter as ctk

from controller_protocol import Controller
from windows.window import Window
from windows.widgets import PlaceHolderEntry
from windows.window_types import WindowTypes

class SignUpWindow(Window):
    
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)


        self.controller = controller
    
        self.top_entry_frame = TopEntryFrame(self, self.controller)
        self.day_entry_frame = DateEntryFrame(self, self.controller)
        self.signup_frame = SignUpFrame(self, self.controller)
        self.bottom_frame = BottomFrame(self, self.controller)

        self.top_entry_frame.pack(expand = True, fill = 'y')
        self.day_entry_frame.pack(expand = True, fill = 'y')
        self.signup_frame.pack(expand = True, fill = 'y')
        self.bottom_frame.pack(expand = True)
        
        





class TopEntryFrame(ctk.CTkFrame): 
    def __init__(self, master: SignUpWindow, controller: Controller):
        super().__init__(master, fg_color=['gray86', 'gray17'])

        self.master = master
        self.controller = controller

        self.password_shown = False

        
        
        self.firstname_entry_box = PlaceHolderEntry(self, "First name", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.lastname_entry_box = PlaceHolderEntry(self, "Last name", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.username_entry_box = PlaceHolderEntry(self, "Username", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.email_entry_box = PlaceHolderEntry(self, "Email", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.password_entry_box = PlaceHolderEntry(self, "Enter password", show = "*", font=('TkDefaultFont', 16), width = 330, height = 45)
        
        self.show_password_button = ctk.CTkButton(self, text = "Show", command=self.show_password_button_clicked, width = 70, height = 30)
    
        self.firstname_entry_box.pack()
        self.lastname_entry_box.pack()
        self.username_entry_box.pack()
        self.email_entry_box.pack()
        self.password_entry_box.pack()

        self.show_password_button.pack()


    def show_password_button_clicked(self) -> None:
        pass

class DateEntryFrame(ctk.CTkFrame):
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
    def __init__(self, master: SignUpWindow, controller: Controller):
        super().__init__(master, fg_color=['gray86', 'gray17'])

        self.master = master
        self.controller = controller
    

        self.month = ctk.CTkOptionMenu(self, values = self.MONTHS)
        self.month.set('January')
        
        self.day_entry_box = PlaceHolderEntry(self, "Day", font=('TkDefaultFont', 16), width = 50, height = 30)
        self.year_entry_box = PlaceHolderEntry(self, "Year", font=('TkDefaultFont', 16), width = 50, height = 30)

        self.year_entry_box.pack(side="right")
        self.month.pack(side="right")
        self.day_entry_box.pack(side="right")
        
    

class SignUpFrame(ctk.CTkFrame): 
    def __init__(self, master: SignUpWindow, controller: Controller):
        super().__init__(master, fg_color=['gray86', 'gray17'])

        self.master = master
        self.controller = controller
        
        self.tos_var = ctk.StringVar(value=False)
        self.tos_checkbox = ctk.CTkCheckBox(self, text="I agree with the terms of service", variable=self.tos_var, onvalue=True, offvalue=False)
        self.signup_button = ctk.CTkButton(self, text= "Sign up", command = self.signup_button_clicked)


        self.tos_checkbox.pack(side="right")
        self.signup_button.pack(side="left")


    def signup_button_clicked(self) -> None:
        self.controller.switch_frame(WindowTypes.EmailVerificationWindow)


class BottomFrame(ctk.CTkFrame): 
    def __init__(self, master: SignUpWindow, controller: Controller):
        super().__init__(master, fg_color=['gray86', 'gray17'])

        self.master = master
        self.controller = controller
        self.login_button = ctk.CTkButton(self, text = "Back", command=self.back_button_clicked)
        self.login_button.pack(side="right")

    
    def back_button_clicked(self) -> None:
        self.controller.switch_frame(WindowTypes.LoginWindow)
