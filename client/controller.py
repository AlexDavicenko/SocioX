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
from windows.core_app.core_app_entry import CoreAppEntryPointWindow 
from windows.add_channel import AddChannelWindow
from suggestions.suggestion_API import WordSuggestionAPI

class Controller:

    def __init__(self, root: ctk.CTk) -> None:
        
        self.root = root
        self.username: str = None
        self.logged_in: bool = False 
        self.current_channel_id: int = None
        self.ip = 0

        self.suggestion_API = WordSuggestionAPI()
        
        self.outgoing_msgs = []

        self.root_container = ctk.CTkFrame(root) 
        
        self._setup_frames()

    def add_binding(self, key: str, func: callable):
        self.root.bind(key, func)

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
        self.core_app: CoreAppEntryPointWindow = self.frames[WindowTypes.CoreAppEntryPointWindow]

    
    def switch_frame(self, frame_name: str) -> None:
        frame = self.frames[frame_name]
        frame.window_bindings()
        frame.tkraise()
    
    def recieve_incoming_msg(self, msg: NewMessageNotif):
        #check channel id
        self.core_app.channel_frame.add_message(msg.channel_id, msg.sender_name, msg.time_sent, msg.content)

    def get_outgoing_msgs(self) -> List[TCPMessage]:
        if self.outgoing_msgs:

            msgs = copy(self.outgoing_msgs)
            self.outgoing_msgs = []
            return msgs

    def add_outgoing_text_msg(self, content: str) -> None:
        self.outgoing_msgs.append(
            TextMessage(self.current_channel_id, content)
        )

    def add_message_internal(self, content):
        self.core_app.channel_frame.add_message(self.current_channel_id, self.username, datetime.now(), content)

    def channel_create_request(self, channel_name: str):
        self.outgoing_msgs.append(
            ChannelCreateRequest(
            channel_name=channel_name
            )
        )
    
    def add_channel(self, channel_id: int, channel_name: str):
        self.core_app.add_channel(channel_id, channel_name)
        self.core_app.channel_frame.add_user(channel_id, self.username)
        self.switch_frame(WindowTypes.CoreAppEntryPointWindow)

    
    def switch_channel(self, channel_id):
        self.core_app.channel_frame.switch_channel(channel_id)
        self.core_app.right_side_frame.user_list_frame.set_users(self.core_app.channel_frame.current_channel_frame.users)

    def user_join_channel_update(self, channel_id: int, username: str) -> None:
        #rerender if in focus
        self.core_app.channel_frame.add_user(channel_id, username)
        self.core_app.right_side_frame.user_list_frame.set_users(self.core_app.channel_frame.current_channel_frame.users)


    def channel_join_request(self, channel_id: int):
        if channel_id not in self.core_app.channel_frame.channel_frames:
            self.outgoing_msgs.append(
                ChannelJoinRequest(
                channel_id=channel_id
                )
            )
        else:
            print("Channel already added")
            # TODO: Tell core app that the channel has already been joined
            pass

    def create_channel(self, channel_id: int, channel_name: str):
        self.add_channel(channel_id, channel_name)


    def join_channel(self, channel_id: int, channel_name: str):
        self.add_channel(channel_id, channel_name)


    def attempt_login(self, name: str) -> None:
        self.username = name
        self.core_app.username = name
        self.outgoing_msgs.append(
            LoginAttempt(
            ip = 0,
            username=name
            )
        )

    def login_approved(self, user_id: int): 
               
        self.logged_in = True
        self.switch_frame(WindowTypes.CoreAppEntryPointWindow)

    def get_suggestions(self, prefix: str) -> List[str]:
        return self.suggestion_API.get_suggestion(prefix)

    def on_suggestion_press(self, suggestionNo):
        self.core_app.text_bar_frame.on_suggestion_press(suggestionNo=suggestionNo)

    def close(self) -> None:
        pass 