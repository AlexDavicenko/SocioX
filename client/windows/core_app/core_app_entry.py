import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from typing import List, Dict


from controller_protocol import Controller
from ..window import Window
from ..window_types import *

from windows.core_app.channel_frame import ChannelFrame
from windows.core_app.left_side_frame import LeftSideFrame
from windows.core_app.right_side_frame import RightSideFrame
from windows.core_app.settings_frame import SettingsFrame
from windows.core_app.text_bar_frame import TextBarFrame



class CoreAppEntryPointWindow(Window):
    def __init__(self, parent: ctk.CTkFrame, controller: Controller):
        super().__init__(parent)

        self.controller = controller

        self.username = self.controller.username



        self.left_side_frame = LeftSideFrame(self, controller)
        self.left_side_frame.grid(row=0, column=0, padx=5, pady=1, sticky="ns")#rowspan = 2
        self.grid_rowconfigure(0, weight=1)
        
        self.channel_frame = ChannelFrame(self, controller)
        self.channel_frame.grid(row=0, column=1, padx=5, pady=1, sticky="nesw")
        self.grid_columnconfigure(1, weight=1)


        self.message_box_text_variable = tk.StringVar()
        self.text_bar_frame = TextBarFrame(self, controller, self.message_box_text_variable)
        self.text_bar_frame.grid(row=1,column=1, padx=5, pady=5, sticky="nesw")


        self.right_side_frame = RightSideFrame(self, controller)
        self.right_side_frame.grid(column = 2, row =0, rowspan = 2,sticky ='ns')

        self.settings_frame = SettingsFrame(self, controller)
        self.settings_frame.grid(column = 0, row =1, rowspan = 2,sticky ='nsew', padx = 10, pady = 10)


    def window_bindings(self): #Polymorphism
        self.controller.add_binding('<Return>', self.text_bar_frame.send_button_clicked)
  


    def add_channel(self, channel_id, channel_name):
        self.left_side_frame.add_channel_button_to_side_bar(channel_id, channel_name)
        self.channel_frame.add_channel(channel_id, channel_name)
    


    








