from customtkinter import *

class Screen:
    def __init__(self):
        self.screen = CTk()
        self.theme()
        self.size()
        self.text = ("Arial", 20)

    def theme(self):
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")

    def size(self):
        self.screen.geometry("800x600")
        self.screen.resizable(False, False)

    def run(self):
        self.screen.mainloop()