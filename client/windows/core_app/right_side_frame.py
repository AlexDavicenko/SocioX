import customtkinter as ctk

from typing import List, Dict, Tuple
from controller_protocol import Controller
from windows.window_types import WindowTypes


class RightSideFrame(ctk.CTkFrame):
    def __init__(self, master, controller: Controller):
        super().__init__(master, width = 110)
        self.controller = controller

        self.search_other_buttons = ctk.CTkButton(self, text='Search', command = self.search_button_pressed)
        self.search_other_buttons.pack(side = 'top', fill = 'x', padx = 10, pady = 10)

        self.user_list_frame = UserListFrame(self, controller)
        self.user_list_frame.pack(expand = True, fill = 'both')
        
    def search_button_pressed(self, e = None):
        self.controller.switch_frame(WindowTypes.SearchWindow)

class UserListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller: Controller):
        super().__init__(master, width = 100, scrollbar_button_color = "#2B2B2B", fg_color=['gray86', 'gray17'])
        self.controller = controller

        self.username_labels: List[ctk.CTkLabel] = []
        
        
        self.title_label = ctk.CTkLabel(self, text = "Users", font=('TkDefaultFont', 14, "bold"))
        self.title_label.pack()


    
    def set_users(self, users: List[Tuple[str,str,str]]):
        
        #Clear all current Username Labels
        for user_label in self.username_labels:
            user_label.pack_forget()
        self.username_labels = []
        
        #Set new Username Labels
        for username, _, _ in users:
            user_label = ctk.CTkLabel(self, text=username)
            self.username_labels.append(user_label)
            user_label.pack()
