

import customtkinter as ctk
import tkinter as tk

from .widgets import PlaceHolderEntry
from .window import Window
from controller_protocol import Controller
from .window_types import WindowTypes


class AddChannelWindow(Window):
    def __init__(self, parent: ctk.CTkFrame, controller: Controller) -> None:
        super().__init__(parent)
        self.controller = controller 
        
        self.central_frame = CentralFrame(self, controller)
        self.central_frame.pack()

class CentralFrame(ctk.CTkFrame):
    def __init__(self, master: AddChannelWindow, controller: Controller):
        super().__init__(master)
        self.controller = controller

        self.join_channel_frame = JoinChannelFrame(self, controller)
        self.join_channel_frame.pack()

        self.create_channel_frame = CreateChannelFrame(self, controller)
        self.create_channel_frame.pack()
    
class JoinChannelFrame(ctk.CTkFrame):
    def __init__(self, master: CentralFrame, controller: Controller):
        super().__init__(master)
        self.controller = controller

        self.join_channel_label = ctk.CTkLabel(self, text = 'Enter a channel ID to join a channel')
        self.join_channel_label.pack()


        self.channel_id_entry_box = PlaceHolderEntry(self, "Channel ID")
        self.channel_id_entry_box.pack()

        self.channel_id_submit_button = ctk.CTkButton(self, text='Join', command = self.channel_id_submit_button_clicked)
        self.channel_id_submit_button.pack()


    def channel_id_submit_button_clicked(self, e = None):
        self.controller.channel_join_request(self.channel_id_entry_box.get())


class CreateChannelFrame(ctk.CTkFrame):
    def __init__(self, master, controller: Controller):
        super().__init__(master)

        self.controller = controller
        self.join_channel_label = ctk.CTkLabel(self, text = 'Create your own channel')
        self.join_channel_label.pack()


        self.channel_id_variable = tk.StringVar()
        self.channel_id_entry_box = PlaceHolderEntry(self, "Channel Name", textvariable = self.channel_id_variable)
        self.channel_id_entry_box.pack()

        self.channel_create_button = ctk.CTkButton(self, text='Create',  command = self.channel_id_submit_button_clicked)
        self.channel_create_button.pack()

    def channel_id_submit_button_clicked(self, e = None):
        self.controller.channel_create_request(self.channel_id_entry_box.get())

