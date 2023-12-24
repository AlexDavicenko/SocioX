import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from controller_protocol import Controller
from windows.window import Window
from windows.widgets import PlaceHolderEntry
from windows.window_types import WindowTypes

class SignUpWindow(Window):
    
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)
        self.controller = controller
    
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
    

        self.detail_entry_frame = DetailEntryFrame(self, self.controller)
        self.detail_entry_frame.grid(column = 0, row = 0, sticky = 'nsew') 
        self.bottom_frame = BottomFrame(self, controller)
        self.bottom_frame.grid(column = 0, row = 1, sticky = 'we')


class DetailEntryFrame(ctk.CTkFrame): 
    def __init__(self, parent: SignUpWindow, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        self.controller = controller

        self.signup_label = ctk.CTkLabel(self, text="SocioX Signup", font=('TkDefaultFont', 28))
        self.top_entry_frame = TopEntryFrame(self, self.controller)
        self.date_entry_frame = DateEntryFrame(self, self.controller)
        self.signup_frame = SignUpFrame(self, self.controller)

        self.grid_rowconfigure(3,weight=1)
        self.grid_columnconfigure(0,weight=1)


        self.signup_label.grid(column = 0, row = 0, pady = 30)
        self.top_entry_frame.grid(column = 0, row = 1, pady = (0,15))
        self.date_entry_frame.grid(column = 0, row = 2)
        self.signup_frame.grid(column = 0, row = 3)


class TopEntryFrame(ctk.CTkFrame): 
    def __init__(self, parent: DetailEntryFrame, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])

        self.parent = parent
        self.controller = controller

        self.password_shown = False

        
        self.username_entry_box = PlaceHolderEntry(self, "Username", font=('TkDefaultFont', 16), width = 330, height = 45)   
        self.firstname_entry_box = PlaceHolderEntry(self, "First name", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.lastname_entry_box = PlaceHolderEntry(self, "Last name", font=('TkDefaultFont', 16), width = 330, height = 45)
        
        self.email_entry_box = PlaceHolderEntry(self, "Email", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.password_entry_box = PlaceHolderEntry(self, "Enter password", show = "*", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.password_repeat_entry_box = PlaceHolderEntry(self, "Repeat password", show = "*", font=('TkDefaultFont', 16), width = 330, height = 45)
        

        self.username_entry_box.pack(pady= (0,5))
        self.firstname_entry_box.pack(pady= (0,5))
        self.lastname_entry_box.pack(pady= (0,20))
        self.email_entry_box.pack(pady= (0,5))
        self.password_entry_box.pack(pady= (0,5))
        self.password_repeat_entry_box.pack()


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
    def __init__(self, parent: DetailEntryFrame, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])

        self.parent = parent
        self.controller = controller
    

        self.month_option_menu = ctk.CTkOptionMenu(self, values = self.MONTHS)
        self.month_option_menu.set('January')
        
        self.day_entry_box = PlaceHolderEntry(self, "Day", font=('TkDefaultFont', 16), width = 80, height = 30)
        self.year_entry_box = PlaceHolderEntry(self, "Year", font=('TkDefaultFont', 16), width = 80, height = 30)

        self.day_entry_box.pack(side="left", padx = (0,10))
        self.month_option_menu.pack(side="left", padx = (0,10))
        self.year_entry_box.pack(side="left")
    

class SignUpFrame(ctk.CTkFrame): 
    def __init__(self, parent: DetailEntryFrame, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])

        self.parent = parent
        self.controller = controller
        
        self.tos_var = ctk.StringVar(value=False)
        self.tos_checkbox = ctk.CTkCheckBox(self, text="I agree with the terms of service", variable=self.tos_var, onvalue=True, offvalue=False)
        self.signup_button = ctk.CTkButton(self, text= "Sign up", command = self.signup_button_clicked)

        self.tos_checkbox.pack(side="left", padx = (0,10))
        self.signup_button.pack(side="right")


    def signup_button_clicked(self) -> None:
        pass_entry1 = self.parent.top_entry_frame.password_entry_box.get()
        pass_entry2 = self.parent.top_entry_frame.password_repeat_entry_box.get()
        
        print(pass_entry1, pass_entry2)
        if pass_entry1 == "":
            CTkMessagebox(title = "Invalid password", message= "Please enter a password", icon="cancel")
            return
        if pass_entry1 != pass_entry2:
            CTkMessagebox(title = "Invalid password", message= "Passwords do not match", icon="cancel")
            return
        if not self.parent.signup_frame.tos_checkbox.get():
            CTkMessagebox(title = "Terms of service", message= "Please agree to the terms of service", icon="cancel")
            return
        
        self.controller.signup_request()
        self.controller.switch_frame(WindowTypes.EmailVerificationWindow)



class BottomFrame(ctk.CTkFrame): 
    def __init__(self, parent: SignUpWindow, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])

        self.parent = parent    
        self.controller = controller
        self.back_button = ctk.CTkButton(self, text = "Back", command=self.back_button_clicked, width= 120, height = 40)
        self.back_button.pack(side = "right", padx = 10, pady = 10)

    
    def back_button_clicked(self) -> None:
        self.controller.switch_frame(WindowTypes.LoginWindow)