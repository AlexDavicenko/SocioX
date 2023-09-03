import tkinter as tk
import customtkinter as ctk
from datetime import datetime

from controller_protocol import Controller
from .window import Window
from .window_types import *
from typing import List, Dict

class CoreAppEntryPointWindow(Window):
    def __init__(self, parent: ctk.CTkFrame, controller: Controller):
        super().__init__(parent)

        self.controller = controller

        self.name = self.controller.client_username

        #remove and fix later
        self.messageBoxText = tk.StringVar()


        self.side_channel_frame = SideChannelFrame(self, controller)
        self.side_channel_frame.grid(row=0, column=0, padx=5, pady=1, sticky="ns")#rowspan = 2
        self.grid_rowconfigure(0, weight=1)
        
        #ChannelId: ChannelFrame
        self.channel_frames: Dict[int, ChannelFrame] = {}
        self.current_channel_id: int = None


        self.current_channel_frame: ChannelFrame = None
        self.channel_frame_container = ctk.CTkFrame(self) 
        self.channel_frame_container.grid(row=0, column=1, padx=5, pady=1, sticky="nesw")
        self.grid_columnconfigure(1, weight=1)


        self.text_bar_frame = TextBarFrame(self)
        self.text_bar_frame.grid(row=1,column=1, padx=10, pady=10, sticky="nesw")

        self.bind('<Return>', self.send_button_clicked)
    
    

    def send_button_clicked(self, e = None):
        message_text = self.messageBoxText.get()
        if message_text:

            self.controller.add_outgoing_text_msg(message_text, self.current_channel_id)
        self.messageBoxText.set("")

    def add_channel_icon_to_side_bar(self, channel_id, channel_name):
        
        self.side_channel_frame.add_channel_button_to_side_bar(channel_id, channel_name)

        channel_frame = ChannelFrame(self.channel_frame_container, channel_name)
        self.channel_frames[channel_id] = channel_frame
        #channel_frame.grid(row=0, column=1, padx=5, pady=1, sticky="nesw")

    def add_message(self, channel_id: int, username: str, time_sent: datetime, content: str):
        self.channel_frames[channel_id].add_message(username, time_sent, content)


    def switch_channel_frame(self, channel_id: int):
        channel_frame = self.channel_frames[channel_id]
        print('frame switch attempt')
        self.current_channel_id = channel_id
        if self.current_channel_frame:
            self.current_channel_frame.pack_forget()
        channel_frame.pack(expand = True, fill = 'both')
        self.current_channel_frame = channel_frame
        channel_frame.tkraise()
        #                frame.grid(row = 0, column = 0, sticky ="nsew")

        
class TextBarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.message_entry_box = ctk.CTkEntry(self, textvariable = master.messageBoxText)
        self.message_entry_box.pack(fill="both",expand=True, padx = 10, pady = 10,side=tk.LEFT)
        
        self.send_button = ctk.CTkButton(self, text = "Send", command = master.send_button_clicked)
        self.send_button.pack(side=tk.RIGHT, padx = 5)


class SideChannelFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller: Controller):
        super().__init__(master, width = 110, scrollbar_button_color = "#2B2B2B")
        self.controller = controller
        self.channel_buttons: Dict[id,ChannelButton] = {}        

        self.add_channel_button = ctk.CTkButton(self, text= 'Add Channel', command = self.add_channel_button_clicked, width = 100, height = 25)
        self.add_channel_button.pack(pady = (5, 5))

    def add_channel_button_clicked(self, e = None):
        self.controller.switch_frame(WindowTypes.AddChannelWindow)

    def add_channel_button_to_side_bar(self, channel_id: int, channel_name: str):
        btn = ChannelButton(self, self.controller, channel_id, channel_name)
        self.channel_buttons[channel_id] = btn
        btn.pack(pady = (0,5))
    

class ChannelButton(ctk.CTkButton):
    def __init__(self, master, controller: Controller, channel_id: int, channel_name: str):
        super().__init__(master, text = channel_name, command=self.switch_channel_button_clicked, width = 100, height = 25)
        self.controller = controller
        self.channel_id = channel_id
        self.channel_name = channel_name

    def switch_channel_button_clicked(self, e = None):
        print("Switch button clicked")
        self.controller.switch_channel(self.channel_id)

class ChannelFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, channel_name):
        super().__init__(master, fg_color=['gray86', 'gray17'])
        
        head = ctk.CTkLabel(self, text = channel_name)
        head.pack(side= tk.TOP, expand = True, fill = tk.X)

        self.messages: List[MessageFrame] = []
        
        
    def add_message(self, username, time, content):
        message_frame = MessageFrame(self, username, time, content)
        message_frame.pack(expand = True, fill = ctk.X, pady = (10,10))

        self.messages.append(message_frame)

class MessageFrame(ctk.CTkFrame):
    def __init__(self, master, username, time, content):
        super().__init__(master, border_color= "gray", border_width= 1)
        
        self.USERNAME_FONT = ctk.CTkFont('Helvetica', 16, 'bold')
        self.MESSAGE_FONT = ctk.CTkFont('Helvetica', 12)


        self.username = username
        self.time = time
        self.content = content

        self.context_frame = ctk.CTkFrame(self, corner_radius = 1)

        self.context_frame.pack(expand = True, fill = ctk.X)
        self.text_frame = ctk.CTkFrame(self, corner_radius = 1)
        self.text_frame.pack(expand = True, fill = ctk.X)


        self.usernameLabel = ctk.CTkLabel(self.context_frame, text=username, font = self.USERNAME_FONT)
        self.usernameLabel.pack(side= tk.LEFT,  anchor="nw", ipadx = 10)


        self.timeLabel = ctk.CTkLabel(self.context_frame, text=time)
        self.timeLabel.pack(side= tk.RIGHT, anchor = "ne", ipadx = 10)


        self.textLabel = ctk.CTkLabel(self.text_frame, text=content, justify="left", font = self.MESSAGE_FONT,anchor="w")
        self.textLabel.pack(side= tk.LEFT, fill = tk.X, padx = 10, pady = (0,5), anchor = "w", expand = True)
        self.textLabel.bind('<Configure>', lambda e: self.textLabel.configure(wraplength=self.textLabel.winfo_width()))

