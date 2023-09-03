import customtkinter as ctk
import tkinter as tk
import logging

from copy import copy
from typing import Dict, List

import sys
sys.path.append('../')
from communication_protocol.TCPMessages import *
sys.path.append('client/')

from windows.window import Window
from windows.window_types import WindowTypes
from windows.login import LoginWindow
from windows.signup import SignUpWindow
from windows.email_verification import EmailVerificationWindow
from windows.core_app_entry import CoreAppEntryPointWindow 
from windows.add_channel import AddChannelWindow

class Controller:

    def __init__(self, root: ctk.CTk) -> None:
        
        self.client_username: str = None
        self.logged_in: bool = False

        self.outgoing_msgs = []

        self.root_container = ctk.CTkFrame(root) 
        
        self._setup_frames()

    def _setup_frames(self) -> None:

        
        self.channel_frames: Dict[int, ctk.Frame] = {}

        self.frames: Dict[str, Window] = {} 
        
        #TODO: Solve with enums
        for FrameClass in (LoginWindow, SignUpWindow, EmailVerificationWindow, CoreAppEntryPointWindow, AddChannelWindow):

            frame = FrameClass(self.root_container, self)
  
            self.frames[FrameClass.__name__] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        self.switch_frame(WindowTypes.LoginWindow)

        self.root_container.pack(side = "top", fill = "both", expand = True)
    
        self.root_container.grid_rowconfigure(0, weight = 1)
        self.root_container.grid_columnconfigure(0, weight = 1)
        
    
    def switch_frame(self, frame_name: str) -> None:
        frame = self.frames[frame_name]
        frame.tkraise()
    
    def recieve_incoming_msg(self, msg: NewMessageNotif):
        #check channel id
        frame: CoreAppEntryPointWindow = self.frames[WindowTypes.CoreAppEntryPointWindow]
        frame.add_message(msg.channel_id, msg.sender_name, msg.time_sent, msg.content)

    def get_outgoing_msgs(self) -> List[TCPMessage]:
        if self.outgoing_msgs:

            msgs = copy(self.outgoing_msgs)
            self.outgoing_msgs = []
            return msgs

    def add_outgoing_text_msg(self, msg: str, channel_id: int) -> None:
        self.outgoing_msgs.append(
            TextMessage(channel_id, msg)
        )

    def channel_create_request(self, channel_name: str):
        print('channel_create_request')
        self.outgoing_msgs.append(
            ChannelCreateRequest(
            channel_name=channel_name
            )
        )   
    
    def add_channel(self, channel_id, channel_name):
        frame: CoreAppEntryPointWindow = self.frames[WindowTypes.CoreAppEntryPointWindow]
        frame.add_channel_icon_to_side_bar(channel_id, channel_name)
        self.switch_frame(WindowTypes.CoreAppEntryPointWindow)
    
    def switch_channel(self, channel_id):
        frame: CoreAppEntryPointWindow = self.frames[WindowTypes.CoreAppEntryPointWindow]
        frame.switch_channel_frame(channel_id)



    def channel_join_request(self, channel_id: int):
        self.outgoing_msgs.append(
            ChannelJoinRequest(
            channel_id=channel_id
            )
        )

    def attempt_login(self, name: str) -> None:
        self.client_username = name
        self.outgoing_msgs.append(
            LoginAttempt(
            ip = 0,
            username=name
            )
        )


    def login_approved(self): 
        
        self.logged_in = True
        self.switch_frame(WindowTypes.CoreAppEntryPointWindow)


    def close(self) -> None:
        pass 