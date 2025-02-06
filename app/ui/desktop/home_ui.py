import os
import tkinter as tk
from tkinter import ttk
from app.utils.styles import *
from app.ui.desktop.sells_ui import SalesScreen

# Classe principal para gerar uma janela
class Home_screen():
    def __init__(self, window):
        self.window = window
        self.main_frame_create()
        self.main_frame_widgets()

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
            command=lambda: SalesScreen(self.window)
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
            style='Leave.MainBt.TButton',
            padding=10,
            command=self.window.destroy
        )
        self.exit_button.pack(pady=10)





