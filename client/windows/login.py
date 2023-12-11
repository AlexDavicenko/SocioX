import tkinter as tk
import customtkinter as ctk
import webbrowser as wb
from client import Client
from threading import Thread
from datetime import datetime
from windows.widgets import PlaceHolderEntry
from windows.window import Window
from controller_protocol import Controller
from windows.window_types import WindowTypes

#https://github.com/mydraft-cc/ui


class LoginWindow(Window):
    password_shown = False
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)

        self.controller = controller


        self.upper_frame = UpperFrame(self)
        self.options_frame = OptionsFrame(self)

        self.upper_frame.pack(expand = True, fill = 'both', anchor = "n")
        self.options_frame.pack(fill = 'x', anchor = "s")


    def window_bindings(self): #Polymorphism
        self.controller.add_binding('<Return>', self.login_button_clicked)

    def login_button_clicked(self, e = None) -> None:
        self.controller.attempt_login(self.upper_frame.input_boxes_frame.username_entry_box.get())


        #Show that pass is being verified


    

    def show_password_button_clicked(self) -> None:

        password_box = self.upper_frame.input_boxes_frame.password_input_frame.password_entry_box
        show_button = self.upper_frame.input_boxes_frame.password_input_frame.show_password_button
        
        self.password_shown = not self.password_shown
        if self.password_shown:
            if password_box.get() != password_box.placeholder:
                password_box.configure(show = "")
                show_button.configure(text = "Hide")
        else:
            if password_box.get() != password_box.placeholder:
                password_box.configure(show = "*")
                show_button.configure(text = "Show")


    def password_entry_box_focus_out(self, e: tk.EventType) -> None:
        password_box = self.upper_frame.input_boxes_frame.password_input_frame.password_entry_box
        show_button = self.upper_frame.input_boxes_frame.password_input_frame.show_password_button

        if password_box.get() != password_box.placeholder:
            self.password_shown = False
            password_box.configure(show = "*")
            show_button.configure(text = "Show")
            


    def signup_button_clicked(self) -> None:
        self.controller.switch_frame('SignUpWindow')
        

    def forgot_password_button_clicked(self) -> None:
        pass

    
    def github_button_clicked(self) -> None:
        wb.open("https://github.com/AlexDavicenko/ChatApp")
    
    


class UpperFrame(ctk.CTkFrame):
    def __init__(self, master: LoginWindow):
        super().__init__(master, fg_color=['gray86', 'gray17'])
        self.welcome_label = ctk.CTkLabel(self, text="Login to SocioX", font=('TkDefaultFont', 40))
        self.welcome_label.grid(padx = 10, pady = 10, column = 0, row = 0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=3)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=5)

        self.input_boxes_frame = InputBoxesFrame(self, master)
        self.input_boxes_frame.grid(padx = 10, pady = 10, column = 0, row = 1)
        frame = ctk.CTkFrame(self, fg_color=['gray86', 'gray17'])

        self.login_button = ctk.CTkButton(frame, text = "Login", width = 330, font=('TkDefaultFont', 24), height = 50, command = master.login_button_clicked)
        self.login_button.pack(anchor='n', side = 'top')

        frame.grid(sticky= 'ns', column = 0, row = 2)

class InputBoxesFrame(ctk.CTkFrame):
    def __init__(self, parent: UpperFrame, master: LoginWindow):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        
        #self.configure()

        self.username_entry_box = PlaceHolderEntry(self, "Enter username", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.username_entry_box.pack(padx = 10, pady = 10)

        self.password_input_frame = PasswordInputFrame(self, master)
        self.password_input_frame.pack(padx = 10, pady = 10)



class PasswordInputFrame(ctk.CTkFrame):
    def __init__(self, parent: InputBoxesFrame, master: LoginWindow):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        
        self.password_entry_box = PlaceHolderEntry(self, "Enter password", show = "*", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.show_password_button = ctk.CTkButton(self, text = "Show", command=master.show_password_button_clicked, width = 70, height = 30)
        self.forgot_password_button = ctk.CTkButton(self, text = "Forgot Password", command=master.forgot_password_button_clicked, width = 130, height = 30)
        
        self.password_entry_box.grid(padx = 10, pady = 0, column = 0, row = 0, columnspan= 2)
        self.show_password_button.grid(padx = 10, sticky = 'w', pady = 10, column = 0, row = 1)
        self.forgot_password_button.grid(sticky = 'e',  padx = 10, pady = 10, column = 1, row = 1)
        #self.grid_columnconfigure(1, weight=3)
        #self.grid_columnconfigure(0, weight=1)


        self.password_entry_box.bind("<FocusOut>", master.password_entry_box_focus_out)
    


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master: LoginWindow):
        super().__init__(master, fg_color=['gray86', 'gray17'])
        
        self.signup_button = ctk.CTkButton(self, text = "Sign Up", command=master.signup_button_clicked)
        self.github_link_button = ctk.CTkButton(self, text = "Github", command=master.github_button_clicked)
        #github link button

        self.signup_button.pack(side='right', padx = 15, pady = 15)
        self.github_link_button.pack(side='right', padx = 15, pady = 15)
        

        #self.signup_button.grid(column = 1, row = 0, sticky = 'e', padx = 15, pady = 15)
        #self.forgot_password_button.grid(column = 0, row = 0, sticky = 'e', padx = 15, pady = 15)

