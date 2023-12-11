import customtkinter as ctk

from typing import List, Dict
from controller_protocol import Controller


class RightSideFrame(ctk.CTkFrame):
    def __init__(self, master, controller: Controller):
        super().__init__(master, width = 110    )
        self.controller = controller

        self.search_other_buttons = ctk.CTkButton(self, text='Search')
        self.search_other_buttons.pack(side = 'top', fill = 'x', padx = 10, pady = 10)

        self.user_list_frame = UserListFrame(self, controller)
        self.user_list_frame.pack(expand = True, fill = 'both')
        


class UserListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller: Controller):
        super().__init__(master, width = 100, scrollbar_button_color = "#2B2B2B", fg_color=['gray86', 'gray17'])
        self.controller = controller

        self.username_labels: List[ctk.CTkLabel] = []
        
        
        self.title_label = ctk.CTkLabel(self, text = "Users")
        self.title_label.pack()


    
    def set_users(self, users: List[str]):
        
        #Clear all current Username Labels
        for user_label in self.username_labels:
            user_label.pack_forget()
        self.username_labels = []
        
        #Set new Username Labels
        for user in users:
            user_label = ctk.CTkLabel(self, text=user)
            self.username_labels.append(user_label)
            user_label.pack()
