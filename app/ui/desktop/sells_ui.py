import os
import tkinter as tk
from tkinter import ttk
from app.utils.styles import *

class sales_screen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Classe Application

        upper_frame = controller.upper_frame_create(self)
        controller.upper_frame_widget(upper_frame)
        self.main_frame = controller.main_frame_create(self)
        self.main_frame_widget()

    def main_frame_widget(self):
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
            command= self.controller.go_back  # Fecha a janela
        )
        self.back_button.pack(pady=10)
