import tkinter as tk
import customtkinter as ctk
from client import Client
from threading import Thread
from datetime import datetime


class App(ctk.CTk):
    def __init__(self, name):
        super().__init__()

        self.init_window()
        self.name = name
        self.messageBoxText = tk.StringVar()
        self.messages_to_send = []

        self.channel_frame = ChannelBoxFrame(self)
        self.channel_frame.grid(row=0, column=0, padx=5, pady=1, sticky="ns")#rowspan = 2
        self.grid_rowconfigure(0, weight=1)
        

        self.message_box_frame = MessageBoxFrame(self)
        self.message_box_frame.grid(row=0, column=1, padx=5, pady=1, sticky="nesw")
        self.grid_columnconfigure(1, weight=1)

        self.text_bar_frame = TextBarFrame(self)
        self.text_bar_frame.grid(row=1,column=1, padx=10, pady=10, sticky="nesw")

        self.bind('<Return>', self.send_button_clicked)
        
    def send_button_clicked(self, e = None):
        text = self.messageBoxText.get()
        if text:
            self.messages_to_send.append(text)

            self.message_box_frame.add_message(
                name,
                datetime.now().strftime('%H:%M:%S'),
                text
                )
        self.messageBoxText.set("")


    def init_window(self):
        ctk.set_appearance_mode("dark")
        self.title('Client Interface')
        self.geometry('1280x720')

class TextBarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.message_box = ctk.CTkEntry(self, textvariable = master.messageBoxText)
        self.message_box.pack(fill="both",expand=True, padx = 10, pady = 10,side=tk.LEFT)
        
        self.send_button = ctk.CTkButton(self, text = "Send", command = master.send_button_clicked)
        self.send_button.pack(side=tk.RIGHT)


class ChannelBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width = 120, scrollbar_button_color = "#2B2B2B")
        self.channels = []
        

    def add_channel(self, msg):
        #impl chanels
        pass


class MessageBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        
        head = ctk.CTkLabel(self, text = master.name)
        head.pack(side= tk.TOP, expand = True, fill = tk.X)

        self.messages = []
        
        
    def add_message(self, username, time, text):
        message_frame = MessageFrame(self, username, time, text)
        message_frame.pack(expand = True, fill = ctk.X, pady = (10,10))

        self.messages.append(message_frame)

class MessageFrame(ctk.CTkFrame):
    def __init__(self, master, username, time, text):
        super().__init__(master, border_color= "gray", border_width= 1)
        
        self.USERNAME_FONT = ctk.CTkFont('Helvetica', 16, 'bold')
        self.MESSAGE_FONT = ctk.CTkFont('Helvetica', 12)


        self.username = username
        self.time = time
        self.text = text

        self.context_frame = ctk.CTkFrame(self, corner_radius = 1)

        self.context_frame.pack(expand = True, fill = ctk.X)
        self.text_frame = ctk.CTkFrame(self, corner_radius = 1)
        self.text_frame.pack(expand = True, fill = ctk.X)


        self.usernameLabel = ctk.CTkLabel(self.context_frame, text=username, font = self.USERNAME_FONT)
        self.usernameLabel.pack(side= tk.LEFT,  anchor="nw", ipadx = 10)


        self.timeLabel = ctk.CTkLabel(self.context_frame, text=time)
        self.timeLabel.pack(side= tk.RIGHT, anchor = "ne", ipadx = 10)


        self.textLabel = ctk.CTkLabel(self.text_frame, text=text, justify="left", font = self.MESSAGE_FONT,anchor="w")
        self.textLabel.pack(side= tk.LEFT, fill = tk.X, padx = 10, pady = (0,5), anchor = "w", expand = True)
        self.textLabel.bind('<Configure>', lambda e: self.textLabel.configure(wraplength=self.textLabel.winfo_width()))


if __name__ == "__main__":
    
    name = input("Name?")
    #name = "Alex "
    app = App(name)
    client = Client(app, name)

    Thread(target=client.start, args=()).start()
    app.mainloop()
