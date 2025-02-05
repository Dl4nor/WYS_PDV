import os
import tkinter as tk
from tkinter import ttk
from app.utils.styles import *

# Classe principal para gerar uma janela
class Initiate():
    def __init__(self):
        self.window = tk.Tk()
        self.style = ttk.Style()
        self.style_configure()
        self.window_create()
        self.icon_define()
        self.main_frame_create()
        self.main_frame_widgets()
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

    def main_frame_create(self):
        # Criar frame principal

        self.main_frame = ttk.Frame(self.window, padding=20, style='MainFrame.TFrame')
        self.main_frame.pack(fill="both", expand=True)

    def main_frame_widgets(self):
        # Criar título do frame principal
        self.title = ttk.Label(
            self.main_frame,
            text="Bem-vindo ao Wys",
            font=Fonts.mainTitleFont,
            padding=10,
            background=Colors.violetBackground
        )
        self.title.pack(pady=10)

        # Adiciona botão
        self.sells_button = ttk.Button(
            self.main_frame,
            text="Tela de Vendas",
            width=15,
            style='MainBt.TButton',
            padding=10,
            command=lambda: print("Tela de vendas aberta!")
        )
        self.sells_button.pack(pady=10)

        self.storage_button = ttk.Button(
            self.main_frame,
            text="Tela de Estoque",
            width=15,
            style='MainBt.TButton',
            padding=10,
            command=lambda: print("Tela de estoque aberta!")
        )
        self.storage_button.pack(pady=10)

        self.exit_button = ttk.Button(
            self.main_frame,
            text="Sair",
            width=15,
            style='MainBt.TButton',
            padding=10,
            command=self.window.destroy
        )
        self.exit_button.pack(pady=10)





