

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
        self.central_frame.pack(expand = True, fill = 'both', padx = 200)


class CentralFrame(ctk.CTkFrame):
    def __init__(self, master: AddChannelWindow, controller: Controller):
        super().__init__(master, fg_color=['gray86', 'gray17'])
        self.controller = controller

        self.join_channel_frame = JoinChannelFrame(self, controller)
        self.join_channel_frame.grid(column = 0, row = 0, sticky = '', pady = (100,40), columnspan = 2)

        self.create_channel_frame = CreateChannelFrame(self, controller)
        self.create_channel_frame.grid(column = 0, row = 1, sticky = 'n', pady = (20,20), columnspan = 2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.back_button = ctk.CTkButton(self, text = 'Back', command = self.back_button_pressed, width= 120, height = 40)
        self.back_button.grid(column = 1, row = 2, padx = 15, pady = 15)

    def back_button_pressed(self, e = None):
        self.controller.switch_frame(WindowTypes.CoreAppEntryPointWindow)
        self.create_channel_frame.channel_name_entry_box.clear()
        self.join_channel_frame.channel_id_entry_box.clear()
    
class JoinChannelFrame(ctk.CTkFrame):
    def __init__(self, master: CentralFrame, controller: Controller):
        super().__init__(master, fg_color=['gray86', 'gray17'])
        self.controller = controller

        self.join_channel_label = ctk.CTkLabel(self, text = 'Enter a channel ID to join a channel', font=('TkDefaultFont', 16))
        self.join_channel_label.grid(row = 0, column = 0, sticky = 'nw', pady = (0, 35))


        self.channel_id_entry_box = PlaceHolderEntry(self, "Channel ID", width = 450, height = 50, font=('TkDefaultFont', 16))
        self.channel_id_entry_box.grid(row = 1, column = 0)

        self.channel_id_submit_button = ctk.CTkButton(self, text='Join', command = self.channel_id_submit_button_clicked, width = 120, height = 50, font=('TkDefaultFont', 16))
        self.channel_id_submit_button.grid(row = 1, column = 1, padx = (50,20))

    def channel_id_submit_button_clicked(self, e = None):
        try:
            channel_id = int(self.channel_id_entry_box.get())
            self.controller.channel_join_request(channel_id)
        except ValueError:
            #handle bad channel_id
            pass

class CreateChannelFrame(ctk.CTkFrame): 
    def __init__(self, master, controller: Controller):
        super().__init__(master, fg_color=['gray86', 'gray17'])

        self.controller = controller
        self.join_channel_label = ctk.CTkLabel(self, text = 'Create your own channel', font=('TkDefaultFont', 16))
        self.join_channel_label.grid(row = 0, column = 0, sticky = 'nw', pady = (0,35))

        self.channel_name_entry_box = PlaceHolderEntry(self, "Channel Name", width = 450, height = 50, font=('TkDefaultFont', 16))
        self.channel_name_entry_box.grid(row = 1, column = 0)

        self.channel_create_button = ctk.CTkButton(self, text='Create',  command = self.channel_name_submit_button_clicked, width = 120, height = 50, font=('TkDefaultFont', 16))
        self.channel_create_button.grid(row = 1, column = 1, padx = (50,20))

    def channel_name_submit_button_clicked(self, e = None):
        self.controller.channel_create_request(self.channel_name_entry_box.get())


