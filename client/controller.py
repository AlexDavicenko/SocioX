import customtkinter as ctk
import tkinter as tk
from copy import copy
from typing import Dict

import sys
sys.path.append('../')
from communication_protocol.messagesTCP import *
sys.path.append('client/')

from windows.window import Window
from windows.login import LoginWindow
from windows.signup import SignUpWindow
from windows.email_verification import EmailVerificationWindow
from windows.core_app_entry import CoreAppEntryPointWindow 

class Controller:

    def __init__(self, root: ctk.CTk) -> None:
        
        self.outgoing_msgs = []

        self.root_container = ctk.CTkFrame(root) 
        self.root_container.pack(side = "top", fill = "both", expand = True)
    
        self.root_container.grid_rowconfigure(0, weight = 1)
        self.root_container.grid_columnconfigure(0, weight = 1)

        self._setup_frames()

    def _setup_frames(self) -> None:
        self.frames: Dict[str, Window] = {} 

        #TODO: Solve with enums
        for FrameClass in (LoginWindow, SignUpWindow, EmailVerificationWindow, CoreAppEntryPointWindow):
  
            frame = FrameClass(self.root_container, self)
  
            self.frames[FrameClass.__name__] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.switch_frame('LoginWindow')
    
    def switch_frame(self, frame_name: str) -> None:
        frame = self.frames[frame_name]
        frame.tkraise()

    def recieve_incoming_msg(self, msg: NewMessageNotif):
        print(msg)
        print(msg.__dict__)
        self.frames['CoreAppEntryPointWindow'].message_box_frame.add_message(msg.text, msg.text, msg.text)


    def get_outgoing_msgs(self) -> str:
        if self.outgoing_msgs:

            msgs = copy(self.outgoing_msgs)
            self.outgoing_msgs = []
            return msgs

    def add_outgoing_msg(self, msg) -> None:
        self.outgoing_msgs.append(
            TextMessage(0, 0, msg)
            )

    def close(self) -> None:


        pass 