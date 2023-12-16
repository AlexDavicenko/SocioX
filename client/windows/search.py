import tkinter as tk
import customtkinter as ctk

from typing import List

from controller_protocol import Controller
from windows.window import Window
from windows.widgets import PlaceHolderEntry
from windows.window_types import WindowTypes

class SearchWindow(Window):
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)
        self.controller = controller



class CentralSearchFrame(ctk.CTkFrame):
    def __init__(self, parent: SearchWindow, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        self.controller = controller


        self.user_search_bar = PlaceHolderEntry(self, placeholder="Start typing a username...")
        self.user_search_bar.pack(expand = True, fill = 'y')

        self.search_button = ctk.CTkButton(self, )

        self.results_frame = ResultsFrame(self, controller)
        self.results_frame.pack(expand = True, fill = 'both')

    def search_button_pressed(self, e = None):
        #TODO
        pass


class ResultsFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent: CentralSearchFrame, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        self.controller = controller
        self.results_list: List[UserResultFrame] = []


    #List[(UserID, Username, AccountAge)]
    def set_results(self, result_data: List):
        
        for result in self.results_list:
            result.pack_forget()
        self.results_list = []
        for user_id, username, account_age in zip(result_data):
            user_result_frame = UserResultFrame(self, self.controller, user_id, username, account_age)
            self.results_list.append(user_result_frame)
            user_result_frame.pack(expand = True, fill = "x")




class UserResultFrame(ctk.CTkFrame):
    def __init__(self, parent: ResultsFrame, controller: Controller, user_id, username, account_age):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        self.controller = controller
        self.user_id = user_id
        self.username = username
        self.account_age = account_age


class BottomButtonFrame(ctk.CTkFrame):
    def __init__(self, parent: SearchWindow, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        self.controller = controller

        self.back_button = ctk.CTkButton(self, text = 'Back', command = self.back_button_pressed, width= 120, height = 40)
        self.back_button.pack(expand = True, fill = 'both', )
    def back_button_pressed(self, e = None):
        pass