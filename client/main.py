import tkinter as tk
import customtkinter as ctk

from controller import Controller


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
            
        self.controller = Controller(self)
        self.init_tkinter_settings()

    
    def init_tkinter_settings(self) -> None:
        ctk.set_appearance_mode("dark")
        self.title('Client Login')
        self.geometry('1280x720')


def main() -> None:
    app: App = App()
    app.mainloop()


if __name__ == '__main__':
    main()

    