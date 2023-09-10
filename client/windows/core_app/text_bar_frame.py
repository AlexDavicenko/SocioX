
import tkinter as tk
import customtkinter as ctk

from datetime import datetime
from typing import List, Dict
from controller_protocol import Controller


class TextBarFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, controller: Controller, username: str):
        super().__init__(master)
        
        self.controller = controller
        self.username = username
        self.message_box_text_variable = tk.StringVar()
        
        self.suggestion_frame = SuggestionFrame(self, controller)
        self.suggestion_frame.grid(column = 0, row = 0, columnspan = 2, sticky = 'ew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.message_entry_box = ctk.CTkEntry(self, textvariable = self.message_box_text_variable)
        self.message_entry_box.grid(column = 0, row = 1, padx = 10, pady = 10, sticky = 'nsew')
        self.message_entry_box.bind('<<Modified>>', self.on_message_entry_box_modify)


        self.send_button = ctk.CTkButton(self, text = "Send", command = self.send_button_clicked)
        self.send_button.grid(column = 1, row = 1, padx = (5,10), sticky = 'ew')
        
    def send_button_clicked(self, e = None):
        message_text = self.message_box_text_variable.get()
        if message_text:

            self.controller.add_outgoing_text_msg(message_text)
            self.controller.add_message_internal(message_text)
        self.message_box_text_variable.set("")
    
    def on_message_entry_box_modify(self, e = None):
        print(self.message_box_text_variable.get())
        words = self.controller.get_suggestions(self.message_box_text_variable.get())

        if len(words) == 3:
            self.suggestion_frame.suggestion_box_2.configure(text = words[2][0])
            self.suggestion_frame.suggestion_box_1.configure(text = words[1][0])
            self.suggestion_frame.suggestion_box_3.configure(text = words[0][0])
        elif len(words) == 2:
            self.suggestion_frame.suggestion_box_2.configure(text = words[1][0])
            self.suggestion_frame.suggestion_box_1.configure(text = words[0][0])
            self.suggestion_frame.suggestion_box_3.configure(text = '')
        elif len(words) == 1:
            self.suggestion_frame.suggestion_box_2.configure(text = words[0][0])
            self.suggestion_frame.suggestion_box_1.configure(text = '')
            self.suggestion_frame.suggestion_box_3.configure(text = '')

class SuggestionFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, controller):
        super().__init__(master, height=40, fg_color=['gray86', 'gray17'])

        self.suggestion_box_1 = ctk.CTkButton(self, text = 's1', fg_color='#454447')
        self.suggestion_box_2 = ctk.CTkButton(self, text = 's2', fg_color='#454447')
        self.suggestion_box_3 = ctk.CTkButton(self, text = 's3', fg_color='#454447')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.suggestion_box_1.grid(column = 0, row = 0, sticky = 'ew', padx = 10)
        self.suggestion_box_2.grid(column = 1, row = 0, sticky = 'ew', padx = (0,10))
        self.suggestion_box_3.grid(column = 2, row = 0, sticky = 'ew', padx = (0,10))