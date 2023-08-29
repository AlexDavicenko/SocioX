import tkinter as tk
import customtkinter as ctk

from controller import Controller
from client import Client
from threading import Thread

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
            
        self.controller = Controller(self)

        name = input("Name?")

        self.client = Client(self.controller, name, offline_mode = False)
        Thread(target=self.client.start, args=()).start()

        self.init_tkinter_settings()
        #self.protocol('WM_DELETE_WINDOW', self.on_close)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close = True


    def init_tkinter_settings(self) -> None:
        ctk.set_appearance_mode("dark")
        self.title('Client Login')
        self.geometry('1280x720')


def main() -> None:

    app: App = App()    
    app.mainloop()


if __name__ == '__main__':
    main()

    