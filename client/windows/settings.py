import tkinter as tk
import customtkinter as ctk

from controller_protocol import Controller
from windows.window import Window
from windows.widgets import PlaceHolderEntry
from windows.window_types import WindowTypes

from typing import List

class SettingWindow(Window):
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent, fg_color= ['gray86', 'gray17'])
        self.controller = controller

        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(3,weight=10)
        self.grid_columnconfigure(0,weight=1)
        
        self.information_title_label = ctk.CTkLabel(self, text = 'Your information', font=('TkDefaultFont', 24))
        self.information_title_label.grid(padx = 10, pady = 10, column = 0, row =1, sticky = "w")

        self.information_frame = InformationFrame(self, controller)
        self.information_frame.grid(padx = 10, pady = 10, column = 0, row = 1, columnspan = 2, sticky = "nwe")
        
        self.manage_friends_label = ctk.CTkLabel(self, text = 'Manage Friends', font=('TkDefaultFont', 24))
        self.manage_friends_label.grid(padx = 10, pady = 10, column = 0, row = 2, sticky = "w")

        self.friend_list_frame = FriendListFrame(self, controller)
        self.friend_list_frame.grid(padx = 10, pady = 10, column = 0, row = 3, columnspan = 2, sticky = "nsew")

        self.back_button = ctk.CTkButton(
            self, text = 'Back', command = self.back_button_pressed, width= 120, height = 40)
        self.back_button.grid(padx = 10, pady = 10, column = 1, row = 4) 

    def back_button_pressed(self, e = None):
        self.controller.switch_frame(WindowTypes.CoreAppEntryPointWindow)


class InformationFrame(ctk.CTkFrame): 
    def __init__(self, parent: SettingWindow, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])

        self.parent = parent    
        self.controller = controller

    def create_labels(self, username: str, firstname: str, lastname: str, email: str, dob: str, account_age: str):
        self.username_label = ctk.CTkLabel(self, text="Username: " + username, font=('TkDefaultFont', 12))
        self.firstname_label = ctk.CTkLabel(self, text="Firstname: " + firstname, font=('TkDefaultFont', 12))
        self.lastname_label = ctk.CTkLabel(self, text="Lastname: " + lastname, font=('TkDefaultFont', 12))
        self.email_label = ctk.CTkLabel(self, text="Email: " + email, font=('TkDefaultFont', 12))
        self.dob_label = ctk.CTkLabel(self, text="Date of birth: " + dob, font=('TkDefaultFont', 12))
        self.account_age_label = ctk.CTkLabel(self, text=account_age, font=('TkDefaultFont', 12))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.username_label.grid(column = 0, row = 0, sticky = 'w', padx = 10)
        self.firstname_label.grid(column = 0, row = 1, sticky = 'w', padx = 10)
        self.lastname_label.grid(column = 0, row = 2, sticky = 'w', padx = 10)
        self.email_label.grid(column = 1, row = 0, sticky = 'n', padx = 10)
        self.dob_label.grid(column = 2, row = 0, sticky = 'e', padx = 10)
        self.account_age_label.grid(column = 2, row = 1, sticky = 'e', padx = 10)

class FriendListFrame(ctk.CTkScrollableFrame): 
    def __init__(self, parent: SettingWindow, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])

        self.parent = parent    
        self.controller = controller

        self.decision_frames: List[FriendDecisionFrame] = []

    
    def add_decision_frame(self, username, firstname, lastname, decision):
        decision_frame = FriendDecisionFrame(self, self.controller, username, firstname, lastname, decision)
        self.decision_frames.append(decision_frame)
        decision_frame.pack(padx = 10, pady = 10, side = 'top', fill = 'x', expand = True)

    def remove_decision_frame(self, username: str):
        for decision_frame in self.decision_frames:
            if decision_frame.username == username:
                decision_frame.pack_forget()
                self.decision_frames.remove(decision_frame)

    def update_decision_frame(self, username: str, decision: str):
        for decision_frame in self.decision_frames:
            if decision_frame.username == username:
                decision_frame.update(decision)

class FriendDecisionFrame(ctk.CTkFrame): 
    def __init__(self, 
                parent: FriendListFrame, 
                controller: Controller, 
                username: str, firstname: str, lastname: str, decision: str):
        super().__init__(parent, fg_color=['gray86', 'gray17'])

        self.parent = parent    
        self.controller = controller
         
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.decision = decision

        self.username_label = ctk.CTkLabel(self, text=username, font=('TkDefaultFont', 14, "bold"))
        self.name_label = ctk.CTkLabel(self, text=firstname+" "+lastname, font=('TkDefaultFont', 12))

        self.username_label.grid(column = 0, row = 0, sticky = 'w')
        self.name_label.grid(column = 0, row = 1, sticky = 'w')
        self.columnconfigure(1, weight=1)

        self.render_decision_buttons(decision)

    def update(self, decision: str):
        if self.decision_button_alt:
            self.decision_button_alt.grid_forget()

        if self.decision_button:
            self.decision_button.grid_forget()
        self.render_decision_buttons(decision)
        
    def render_decision_buttons(self, decision: str):
        self.decision_button: ctk.CTkButton = None
        self.decision_button_alt: ctk.CTkButton = None

        if decision == "Accept":
            self.decision_button = ctk.CTkButton(self, 
                text="Accept", 
                command= lambda : self.controller.accept_friend_request(self.username), 
                height = 35, 
                width = 80,
                fg_color = '#03a551', 
                hover_color='#06a503'
                )
            self.decision_button_alt = ctk.CTkButton(self,
                text="Reject",
                command= lambda : self.controller.reject_friend_request(self.username),
                height = 35,
                width = 80, 
                fg_color = '#e21d27', 
                hover_color='#ce3b43'
                )

        elif decision == "Pending":
            self.decision_button = ctk.CTkButton(
                self, text="Pending", height = 35, width = 80, state = "off")
            
        elif decision == "Remove":
            self.decision_button = ctk.CTkButton(self, 
                text="Remove", 
                fg_color = '#e21d27', 
                hover_color='#ce3b43', 
                command= lambda : self.controller.remove_friend(self.username), 
                height = 35, 
                width = 80
                )

        if self.decision_button:
            self.decision_button.grid(column = 3, row = 0, rowspan = 2, sticky = 'e')
        if self.decision_button_alt:
            self.decision_button_alt.grid(column = 2, row = 0, rowspan = 2, sticky = 'e', padx = (0,10))
