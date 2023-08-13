import tkinter as tk
import customtkinter as ctk
from client import Client
from threading import Thread
from datetime import datetime
from placeHolderEntry import PlaceHolderEntry

#https://github.com/mydraft-cc/ui


class LoginWindow(ctk.CTk):
    password_shown = False
    def __init__(self):
        super().__init__()


        self.init_window()

        self.upper_frame = UpperFrame(self)
        self.options_frame = OptionsFrame(self)

        self.upper_frame.pack(expand = True, fill = 'both', anchor = "n")
        self.options_frame.pack(fill = 'x', anchor = "s")
        
        

    def login_button_clicked(self, e = None):
        pass

    def show_password_button_clicked(self, e = None):

        password_box = self.upper_frame.input_boxes_frame.password_input_frame.password_entry_box
        show_button = self.upper_frame.input_boxes_frame.password_input_frame.show_password_button
        
        self.password_shown = not self.password_shown
        if self.password_shown:
            password_box.configure(show = "")
            show_button.configure(text = "Hide")
        else:
            if password_box.get() != password_box.placeholder:
                password_box.configure(show = "*")
                show_button.configure(text = "Show")


    def password_entry_box_focus_out(self, e = None):

        password_box = self.upper_frame.input_boxes_frame.password_input_frame.password_entry_box
        show_button = self.upper_frame.input_boxes_frame.password_input_frame.show_password_button

        if password_box.get() != password_box.placeholder:
            self.password_shown = False
            password_box.configure(show = "*")
            show_button.configure(text = "Show")
            


    def signup_button_clicked(self, e = None):
        pass
    def forgot_password_button_clicked(self, e = None):
        pass
    def github_button_clicked(self, e = None):
        pass
    
    def init_window(self):
        ctk.set_appearance_mode("dark")
        self.title('Client Login')
        self.geometry('1280x720')


class UpperFrame(ctk.CTkFrame):
    def __init__(self, master: LoginWindow):
        super().__init__(master)
        self.welcome_label = ctk.CTkLabel(self, text="Welcome", font=('TkDefaultFont', 40))
        self.welcome_label.pack(side = 'top', padx =10, pady=15)


        self.input_boxes_frame = InputBoxesFrame(self, master)
        self.input_boxes_frame.pack(anchor = 'center', pady = 40, fill= 'y', expand = True)


        self.login_button = ctk.CTkButton(self, text = "Login", width = 330, font=('TkDefaultFont', 24), height = 50, command = master.login_button_clicked)
        self.login_button.pack(anchor = "s", side = "bottom",padx = 20, pady = 60)


class InputBoxesFrame(ctk.CTkFrame):
    def __init__(self, parent: UpperFrame, master: LoginWindow):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        
        #self.configure()

        self.username_entry_box = PlaceHolderEntry(self, "Enter username", font=('TkDefaultFont', 16), width = 330, height = 45)
        self.username_entry_box.pack(padx = 10, pady = 35)

        self.password_input_frame = PasswordInputFrame(self, master)
        self.password_input_frame.pack()



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
        super().__init__(master)
        
        self.signup_button = ctk.CTkButton(self, text = "Sign Up", command=master.signup_button_clicked)
        self.github_link_button = ctk.CTkButton(self, text = "Github", command=master.github_button_clicked)
        #github link button

        self.signup_button.pack(side='right', padx = 15, pady = 15)
        self.github_link_button.pack(side='right', padx = 15, pady = 15)
        

        #self.signup_button.grid(column = 1, row = 0, sticky = 'e', padx = 15, pady = 15)
        #self.forgot_password_button.grid(column = 0, row = 0, sticky = 'e', padx = 15, pady = 15)


if __name__ == "__main__":
    
    app = LoginWindow()
    #client = Client(app)

    #Thread(target=client.start, args=()).start()
    app.mainloop()
