
import tkinter as tk
from tkinter import ttk
from controller.home_controller import homeController
from utils.styles import *
from utils.gnr_components import gnrComponents
from view.sells_ui import sales_screen
from view.storage_ui import storage_screen

# Classe principal para gerar uma janela
class home_screen(ttk.Frame):
    def __init__(self, parent, mController):
        super().__init__(parent)
        self.hController = homeController()
        self.mController = mController # Classe mainController
        Components = gnrComponents(self.mController)

        self.main_frame = Components.main_frame_create(self)
        self.main_frame_widgets()

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
            command= lambda: self.mController.show_screen(sales_screen)
        )
        self.sells_button.pack(pady=10)

        self.storage_button = ttk.Button(
            self.main_frame,
            text="Tela de Estoque",
            width=15,
            style='MainBt.TButton',
            padding=10,
            command=lambda: self.mController.show_screen(storage_screen)
        )
        self.storage_button.pack(pady=10)

        self.pagbank_login_button = ttk.Button(
            self.main_frame,
            text="Entrar na Pagbank",
            width=15,
            style='MainBt.TButton',
            padding=10,
            command=lambda: self.hController.open_pagbank_login()
        )
        self.pagbank_login_button.pack(pady=10)

        self.exit_button = ttk.Button(
            self.main_frame,
            text="Sair",
            width=15,
            style='Leave.MainBt.TButton',
            padding=10,
            command= self.mController.window.destroy
        )
        self.exit_button.pack(pady=10)





