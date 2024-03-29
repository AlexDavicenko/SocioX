import tkinter as tk
import customtkinter as ctk

from datetime import datetime
from typing import List, Dict, Tuple
from controller_protocol import Controller

class ChannelFrame(ctk.CTkFrame):
    def __init__(self, master, controller: Controller):
        super().__init__(master, fg_color=['gray86', 'gray17'])

        self.controller = controller
        #ChannelId: ChannelFrame
        self.channel_frames: Dict[int, MessagesFrame] = {}


        self.leave_button = ctk.CTkButton(self, text='Leave', command = controller.leave_channel)
        self.leave_button.grid(row = 0, column = 1, sticky= 'ew', padx = 10, pady =10)


        self.header_label = ctk.CTkLabel(self, text = "", font=('TkDefaultFont', 14))
        self.header_label.grid(row = 0, column = 0, sticky= 'ew')

        self.message_frame_container = ctk.CTkFrame(self)

        self.current_channel_frame: MessagesFrame = None
        self.message_frame_container.grid(row=1, column=0, padx=5, pady=1, sticky="nesw", columnspan = 2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def add_channel(self, channel_id: int, channel_name: str):
        channel_frame = MessagesFrame(self.message_frame_container, self.controller, channel_name, channel_id)
        self.channel_frames[channel_id] = channel_frame

    def add_message(self, channel_id: int, username: str, time_sent: datetime, content: str):
        self.channel_frames[channel_id].add_message(username, time_sent, content)

    
    def add_user(self, channel_id: int, username: str, firstname: str, lastname: str):
        self.channel_frames[channel_id].add_user(username, firstname, lastname)

    

    def switch_channel(self, channel_id: int):
        channel_frame = self.channel_frames[channel_id]
        
        if self.current_channel_frame:
            self.current_channel_frame.unpack()
            self.current_channel_frame.pack_forget()
        self.current_channel_frame = channel_frame

        self.header_label.configure(
            text =
f"Your Name: { self.controller.username} {' '*20} Channel name: {channel_frame.channel_name} {' '*20} Channel ID: {channel_id}")
        channel_frame.pack_all()
        channel_frame.pack(expand = True, fill = 'both')
        channel_frame.tkraise()
        channel_frame.scroll_to_bottom()


class MessagesFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, controller: Controller, channel_name, channel_id):
        super().__init__(master, fg_color=['gray86', 'gray17']) 
        self.controller = controller
        self.channel_id = channel_id
        self.channel_name = channel_name

        self.users: List[Tuple[str, str, str]] = []
        self.messages: List[MessageFrame] = []
    
    def unpack(self):
        for message in self.messages:
            message.pack_forget()

    def pack_all(self):
        for message in self.messages:
            message.pack(expand = True, fill = ctk.X, pady = (10,10))

        
    def add_message(self, username: str, time_sent: datetime, content: str):
        firstname = None    
        lastname = None
        for user in self.users:
            if user[0] == username:
                firstname = user[1]
                lastname = user[2]

        message_frame = MessageFrame(
            self, self.controller, username, firstname, lastname, time_sent.strftime('%H:%M:%S'), content)
        if self.channel_id == self.controller.current_channel_id:
            message_frame.pack(expand = True, fill = ctk.X, pady = (10,10))
        self.messages.append(message_frame)
        self.scroll_to_bottom()

    def add_user(self, username: str, firstname: str, lastname: str):
        self.users.append((username, firstname, lastname))

    def scroll_to_bottom(self):
        self.update()
        self._parent_canvas.yview_moveto(1.0)



class MessageFrame(ctk.CTkFrame):
    def __init__(
            self, 
            master, 
            controller: Controller, 
            username: str, firstname: str, lastname: str, time: str, content: str):
        super().__init__(master, border_color = "gray", border_width= 1)

        self.USERNAME_FONT = ctk.CTkFont('Helvetica', 16, 'bold')
        self.MESSAGE_FONT = ctk.CTkFont('Helvetica', 12)
        self.PLUS_FONT = ctk.CTkFont('Helvetica', 15)

        self.controller = controller
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
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

        #The user is still in the channel and the data was sent abt their first and last name
        if self.firstname != None and self.lastname != None:
            #If the message sender is not the user and not a friend of the user
            if self.username != self.controller.username and self.username not in self.controller.friends:
                self.friend_request_user_button = ctk.CTkButton(
                    self.context_frame,
                    text="+", 
                    width=20, 
                    height=20, 
                    font = self.PLUS_FONT, 
                    command= lambda : self.controller.send_friend_request(self.username, self.firstname, self.lastname))
                self.friend_request_user_button.pack(side = tk.LEFT, anchor = "w", padx = 25)

        

        self.textLabel = ctk.CTkLabel(self.text_frame, text=content, justify="left", font = self.MESSAGE_FONT,anchor="w")
        self.textLabel.pack(side= tk.LEFT, fill = tk.X, padx = 10, pady = (0,5), anchor = "w", expand = True)

        #Dynamically allocates the width of the text label warplength based on its width using an event
        self.textLabel.bind('<Configure>', lambda e: self.textLabel.configure(wraplength=self.textLabel.winfo_width()))

