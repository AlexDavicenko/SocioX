import tkinter as tk
import customtkinter as ctk

from datetime import datetime
from typing import List, Dict

from controller_protocol import Controller
from windows.window_types import WindowTypes


class LeftSideFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller: Controller):
        super().__init__(master, width = 110, scrollbar_button_color = "#2B2B2B")
        self.controller = controller
        self.channel_buttons: Dict[id,ChannelButton] = {}        


    def add_channel_button_to_side_bar(self, channel_id: int, channel_name: str):
        btn = ChannelButton(self, self.controller, channel_id, channel_name)
        self.channel_buttons[channel_id] = btn
        btn.pack(pady = (0,5), side = 'top', expand = True)
    
    def remove_channel_button(self, channel_id: int): 
        btn = self.channel_buttons.pop(channel_id)
        btn.destroy()

class ChannelButton(ctk.CTkButton):
    def __init__(self, master, controller: Controller, channel_id: int, channel_name: str):
        super().__init__(master, text = channel_name, command=self.switch_channel_button_clicked, width = 100, height = 25)
        self.controller = controller
        self.channel_id = channel_id
        self.channel_name = channel_name

    def switch_channel_button_clicked(self, e = None):
        self.controller.switch_channel(self.channel_id)