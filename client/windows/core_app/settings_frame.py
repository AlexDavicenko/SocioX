import tkinter as tk
import customtkinter as ctk

from controller_protocol import Controller

from windows.window_types import WindowTypes

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, controller: Controller):
        super().__init__(master)

        self.controller = controller
        self.add_channel_button = ctk.CTkButton(
            self,
            text= 'Add Channel',
            command = self.add_channel_button_clicked,
            width = 100, 
            height = 40, 
            fg_color = '#e21d27', 
            hover_color='#ce3b43'
        )
        
        self.settings_button = ctk.CTkButton(
            self,
            text = 'Settings',
            command = self.settings_button_clicked,
            width = 100,
            height = 40,
            fg_color = '#e21d27', 
            hover_color='#ce3b43'
        )


        self.add_channel_button.pack(pady = (5, 5), side = 'top', expand = True)
        self.settings_button.pack(pady = (0, 5), side = 'bottom', expand = True)

    
    def add_channel_button_clicked(self, e = None):
        self.controller.switch_frame(WindowTypes.AddChannelWindow)

    def settings_button_clicked(self, e = None):
        self.controller.switch_frame(WindowTypes.SettingWindow)
