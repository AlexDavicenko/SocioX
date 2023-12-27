
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

        self.send_button = ctk.CTkButton(self, text = "Send", command = self.send_button_clicked, state="off")
        self.send_button.grid(column = 1, row = 1, padx = (5,10), sticky = 'ew')
        self.on_message_entry_box_modify()

    def window_bindings(self) -> None:
        self.message_entry_box.bind('<<Modified>>', self.on_message_entry_box_modify)
        self.controller.add_binding('<F1>', lambda e : self.on_suggestion_press(e=None, suggestionNo=1))
        self.controller.add_binding('<F2>', lambda e : self.on_suggestion_press(e=None, suggestionNo=2))
        self.controller.add_binding('<F3>', lambda e : self.on_suggestion_press(e=None, suggestionNo=3))


    def send_button_clicked(self, e = None):
        message_text = self.message_box_text_variable.get()
        if message_text:
            self.controller.add_message(message_text)

        self.message_box_text_variable.set("")

    def on_suggestion_press(self, e = None, suggestionNo: int = 2):
        #print('Suggestion press')
        match suggestionNo:
            case 1:
                suggestion = self.suggestion_frame.suggestion_box_1._text
            case 2: 
                suggestion = self.suggestion_frame.suggestion_box_2._text
            case 3:
                suggestion = self.suggestion_frame.suggestion_box_3._text
                
        text = self.message_box_text_variable.get().split(' ')
        
        self.message_entry_box.delete(0, tk.END)
        self.message_entry_box.insert(0,' '.join(text[:-1]) + " " + suggestion + " ")
        self.message_entry_box.icursor(tk.END)

    def on_message_entry_box_modify(self, e = None):
        words = self.controller.get_suggestions(self.message_box_text_variable.get().split(' ')[-1])

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
    def __init__(self, master: ctk.CTkFrame, controller: Controller):
        super().__init__(master, height=40, fg_color=['gray86', 'gray17'])

        self.suggestion_box_1 = ctk.CTkButton(self, text = '', fg_color='#454447', command= lambda : controller.on_suggestion_press(suggestionNo=1))
        self.suggestion_box_2 = ctk.CTkButton(self, text = '', fg_color='#454447', command= lambda : controller.on_suggestion_press(suggestionNo=2))
        self.suggestion_box_3 = ctk.CTkButton(self, text = '', fg_color='#454447', command= lambda : controller.on_suggestion_press(suggestionNo=3))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.suggestion_box_1.grid(column = 0, row = 0, sticky = 'ew', padx = 10)
        self.suggestion_box_2.grid(column = 1, row = 0, sticky = 'ew', padx = (0,10))
        self.suggestion_box_3.grid(column = 2, row = 0, sticky = 'ew', padx = (0,10))
    
