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

        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        
        self.information_frame = InformationFrame(self, controller)
        self.information_frame.grid(padx = 10, pady = 10, column = 0, row = 0, columnspan = 2, sticky = "nsew")
        
        self.friend_list_frame = FriendListFrame(self, controller)
        self.friend_list_frame.grid(padx = 10, pady = 10, column = 0, row = 1, columnspan = 2, sticky = "nsew")

        self.back_button = ctk.CTkButton(self, text = 'Back', command = self.back_button_pressed, width= 120, height = 40)
        self.back_button.grid(padx = 10, pady = 10, column = 1, row = 2) 

    def back_button_pressed(self, e = None):
        self.controller.switch_frame(WindowTypes.CoreAppEntryPointWindow)


class InformationFrame(ctk.CTkFrame): 
    def __init__(self, parent: SettingWindow, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])

        self.parent = parent    
        self.controller = controller
        #TODO: display user information
        self.username_label = ctk.CTkLabel(self, text="Username", font=('TkDefaultFont', 14, "bold"))
        self.name_label = ctk.CTkLabel(self, text="Name", font=('TkDefaultFont', 12))
        self.email_label = ctk.CTkLabel(self, text="Email", font=('TkDefaultFont', 12))



class FriendListFrame(tk.Frame): 
    def __init__(self, parent: SettingWindow, controller: Controller):
        super().__init__(parent,)# fg_color=['gray86', 'gray17']

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
    def __init__(self, parent: FriendListFrame, controller: Controller, username: str, firstname: str, lastname: str, decision: str):
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
            self.decision_button = ctk.CTkButton(self, text="Accept", command= lambda : self.controller.accept_friend_request(self.username), height = 20, width = 45)
            self.decision_button_alt = ctk.CTkButton(self, text="Reject", command= lambda : self.controller.reject_friend_request(self.username), height = 20, width = 45)

        elif decision == "Pending":
            self.decision_button = ctk.CTkButton(self, text="Pending", height = 20, width = 45, state = "off")
        elif decision == "Remove":
            self.decision_button = ctk.CTkButton(self, text="Remove", command= lambda : self.controller.remove_friend(self.username), height = 20, width = 45)

        if self.decision_button:
            self.decision_button.grid(column = 2, row = 0, rowspan = 2, sticky = 'e')
        if self.decision_button_alt:
            self.decision_button_alt.grid(column = 1, row = 0, rowspan = 2, sticky = 'e')
