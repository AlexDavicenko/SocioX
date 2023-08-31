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
 

        self.client = Client(self.controller, offline_mode =False)
        Thread(target=self.client.start, args=()).start()

        self.init_tkinter_settings()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self):
        self.client.close()
        self.destroy()


    def init_tkinter_settings(self) -> None:
        ctk.set_appearance_mode("dark")
        self.title('Client Login')
        self.geometry('1280x720')


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename='client.log',
    )
    app: App = App()    
    app.mainloop()


if __name__ == '__main__':
    main()

    