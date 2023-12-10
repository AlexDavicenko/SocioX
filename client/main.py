import logging
import tkinter as tk
import customtkinter as ctk

from threading import Thread
from controller import Controller
from client import Client

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        self.controller = Controller(self)
        
        try:
            self.client = Client(self.controller, offline_mode =False)
            Thread(target=self.client.start, args=()).start()
        except ConnectionRefusedError:
            print("Server is currently offline. Try again later!")
            exit(0)

        self.init_tkinter_settings()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self):
        self.destroy()
        self.client.close()


    def init_tkinter_settings(self) -> None:
        ctk.set_appearance_mode("dark")
        self.title('Client Login')
        self.geometry('1280x720')


def main() -> None:
    app: App = App()    
    app.mainloop()


if __name__ == '__main__':
    main()

    