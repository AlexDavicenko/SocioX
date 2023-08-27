import customtkinter as ctk
import tkinter as tk

from windows.login import LoginWindow
from windows.signup import SignUpWindow
from windows.window import Window
from windows.email_verification import EmailVerificationWindow
from typing import Dict

class Controller:

    def __init__(self, root: ctk.CTk) -> None:
        

        self.root_container = ctk.CTkFrame(root) 
        self.root_container.pack(side = "top", fill = "both", expand = True)
    
        self.root_container.grid_rowconfigure(0, weight = 1)
        self.root_container.grid_columnconfigure(0, weight = 1)

        self.setup_frames()

    def setup_frames(self) -> None:
        self.frames: Dict[str, Window] = {} 

        for FrameClass in (LoginWindow, SignUpWindow, EmailVerificationWindow):
  
            frame = FrameClass(self.root_container, self)
  
            self.frames[FrameClass.__name__] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.switch_frame('LoginWindow')
    
    def switch_frame(self, frame_name: str) -> None:
        frame = self.frames[frame_name]
        frame.tkraise()