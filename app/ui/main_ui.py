from controller.main_controller import mainController
import tkinter as tk
from tkinter import ttk
from utils.styles import *
from ui.home_ui import home_screen
from ui.sells_ui import sales_screen

class Application:
    def __init__(self):
        self.controller = mainController()
        self.window = tk.Tk()
        self.style = ttk.Style()
        ui_styles.style_configure(self)
        self.window_create()
        self.controller.icon_define()

        # Ativa o modo escuro da barra de título (Windows 10 e 11)
        self.controller.enable_dark_mode()

        # Definindo o container onde ficarão as páginas
        self.container = ttk.Frame(self.window)
        self.controller.set_container(self.container)
        self.container.pack(fill="both", expand=True)

        # Mostra a Home screen
        self.controller.show_screen(home_screen)
        self.window.mainloop()

    def window_create(self):
        # Criando janela
        self.window.title("Sistema WYS - PDV")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.maxsize(width=1920, height=1080)
        self.window.minsize(width=800, height=600)

        self.controller.set_window(self.window)

