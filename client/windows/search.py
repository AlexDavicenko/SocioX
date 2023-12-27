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

        self.grid_rowconfigure(0,weight=5)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=5)
        self.grid_columnconfigure(2,weight=1)



        self.central_search_frame = CentralSearchFrame(self, controller)
        self.central_search_frame.grid(column = 0, row = 0, sticky = 'nsew', columnspan = 3)

        self.back_button = ctk.CTkButton(self, text = 'Back', command = self.back_button_pressed, width= 120, height = 40)
        self.back_button.grid(padx = 10, pady = 10, column = 2, row = 1) 

        self.get_suggestions_button = ctk.CTkButton(self, text = 'Generate Suggestions', command = self.get_suggestions_button_pressed, width= 120, height = 40)
        self.get_suggestions_button.grid(padx = 10, pady = 10, column = 0, row = 1)


    def back_button_pressed(self, e = None):
        self.controller.switch_frame(WindowTypes.CoreAppEntryPointWindow)


    def get_suggestions_button_pressed(self, e = None): 
        pass

class CentralSearchFrame(ctk.CTkFrame):
    def __init__(self, parent: SearchWindow, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17']) 
        self.controller = controller



        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)


        self.user_search_bar = PlaceHolderEntry(self, placeholder="Start typing a username...", width = 300, height = 40)
        self.user_search_bar.grid(padx = 10, pady = (10,0), column = 0, row = 0, sticky = "e")

        self.search_button = ctk.CTkButton(self, text = 'Search', command = self.search_button_pressed, width= 120, height = 40)
        self.search_button.grid(padx = 10, pady = (10,0), column = 1, row = 0,  sticky = "w")

        self.results_frame = ResultsFrame(self, controller)
        self.results_frame.grid(padx = 10, column = 0, row = 1, columnspan = 2, sticky = "nsew") 



    def search_button_pressed(self, e = None):
        self.controller.search_request(self.user_search_bar.get())


class ResultsFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent: CentralSearchFrame, controller: Controller):
        super().__init__(parent, fg_color=['gray86', 'gray17'])
        self.controller = controller
        self.results_list: List[UserResultFrame] = []


    #List[{Username, Firstname, AccountAge}]
    def set_results(self, result_data: List):
        
        for result in self.results_list:
            result.pack_forget()
        self.results_list = []
        for result in result_data:
            user_result_frame = UserResultFrame(self, self.controller, result["Username"], result["Firstname"], result['Lastname'], result["AccountAge"])
            self.results_list.append(user_result_frame)
            user_result_frame.pack(expand = True, side = "top", fill = 'x', padx = (0,25))





class UserResultFrame(ctk.CTkFrame):
    def __init__(self, parent: ResultsFrame, controller: Controller, username, firstname, lastname, account_age):
        super().__init__(parent)

        self.controller = controller
        self.firstname = firstname
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.account_age = account_age
    

        self.username_label = ctk.CTkLabel(self, text=username, font=('TkDefaultFont', 14, "bold"))
        self.name_label = ctk.CTkLabel(self, text=firstname+" "+lastname, font=('TkDefaultFont', 12))
        self.account_age_label = ctk.CTkLabel(self, text=account_age, font=('TkDefaultFont', 12))
        self.add_friend_button = ctk.CTkButton(self, text="Add", command=self.add_friend, height = 20, width = 45)
        if username in self.controller.friends:
            self.add_friend_button.config(state ="disabled")


        self.grid_columnconfigure(2,weight=1)

        self.username_label.grid(padx = 10, pady = 5, column = 1, row = 0,sticky = "ns")
        self.add_friend_button.grid(padx = 10, column = 0, row = 0, sticky = "w")
        self.account_age_label.grid(padx = 0, pady = 5, column = 3, row = 0,sticky = 'e')
        self.name_label.grid(padx = 10, pady = 10, column = 0, row = 1, columnspan = 2, sticky = "w")

    def add_friend(self):
        self.controller.send_friend_request(self.username, self.firstname, self.lastname)
