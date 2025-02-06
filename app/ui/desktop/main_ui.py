import os
import tkinter as tk
from tkinter import ttk
from app.utils.styles import *
from app.ui.desktop.home_ui import Home_screen
from app.ui.desktop.sells_ui import SalesScreen


class Aplication:
    def __init__(self):
        self.window = tk.Tk()
        self.style = ttk.Style()
        self.style_configure()
        self.window_create()
        self.icon_define()
        self.home = Home_screen(self.window)
        self.window.mainloop()
        
    def style_configure(self):
        # Definindo o tema de toda aplicação
        self.style.theme_use('alt')

        # Definindo o estilo dos MainFrame
        self.style.configure(
            'MainFrame.TFrame', 
            background=Colors.violetBackground
        )

        # Definindo o estilo do MainBt
        self.style.configure(
            'MainBt.TButton', 
            background='#C77DFF', 
            foreground='black', 
            focuscolor='',
            font=Fonts.mainButtonFont
        )
        self.style.map(
            'MainBt.TButton',
            background=[('active', Colors.violetBackground)],
            foreground=[('active', 'black')]             
        )
        self.style.map(
            'Leave.MainBt.TButton',
            background=[('active', "#c05299")]
        )

    def window_create(self):
        # Criando janela
        self.window.title("Sistema WYS - PDV")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.maxsize(width=1920, height=1080)
        self.window.minsize(width=800, height=600)

    def icon_define(self):
        # Caminho absoluto para o ícone
        script_dir = os.path.dirname(__file__)  # Diretório onde o script está
        icon_path = os.path.join(script_dir, "..", "..", "assets", "icons", "wys_t_icon.ico")
        icon_path = os.path.abspath(icon_path)  # Converte para caminho absoluto

        # Definir icone
        self.window.iconbitmap(icon_path)
