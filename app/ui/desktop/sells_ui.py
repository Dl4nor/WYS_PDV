import os
import tkinter as tk
from tkinter import ttk
from app.utils.styles import *

class SalesScreen():
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Tela de Vendas")
        self.window.geometry("600x400")
        self.window.resizable(False, False)

        # Criar um frame principal
        self.main_frame = ttk.Frame(self.window, padding=20, style='MainFrame.TFrame')
        self.main_frame.pack(fill="both", expand=True)

        # Criar título
        self.title = ttk.Label(
            self.main_frame,
            text="Tela de Vendas",
            font=Fonts.mainTitleFont,
            padding=10,
            background=Colors.violetBackground
        )
        self.title.pack(pady=10)

        # Adicionar um botão de voltar
        self.back_button = ttk.Button(
            self.main_frame,
            text="Voltar",
            width=15,
            style='Leave.MainBt.TButton',
            command=self.window.destroy  # Fecha a janela
        )
        self.back_button.pack(pady=10)
