import os
import tkinter as tk
from tkinter import ttk
from app.utils.styles import *

class sales_screen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Classe Application

        controller.upper_frame_construct(self)
        self.main_frame = controller.main_frame_create(self)
        self.main_frame_widget()
        self.barcode_frame_create()
        self.barcode_frame_widget()

    def bind_resizeFont_event(self, widget, font, dividing):
        # Redimenciona o tamanho da fonte
        # Primeiro define a fonte de acordo com o tamanho atual da tela
        Fonts.resize_font(None, self, widget, font, dividing)

        # E caso a janela mude de tamanho, redimenciona de acordo com a altura
        self.bind(
            '<Configure>', 
            lambda e: Fonts.resize_font(
                e, 
                self, 
                widget, 
                font,
                dividing
            )
        )

    def barcode_frame_create(self):
        # Cria o frame do código de barras

        self.barcode_frame = ttk.Frame(self, padding=10, takefocus=1, style='BarcodeFrame.TFrame')
        self.barcode_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.15)

    def barcode_frame_widget(self):
        # Cria os widgets do Frame do código de barras

        self.barcode_entry = ttk.Entry(
            self.barcode_frame,
            background='white',
            foreground='black',
            style='BarcodeEntry.TEntry',
            font=Fonts.barcodeFont,
        )
        self.barcode_entry.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Redimenciona dinamicamente o tamanho da fonte do barcodeEntry
        self.bind_resizeFont_event(
            self.barcode_entry,
            Fonts.barcodeFont,
            35
        )

        self.barcode_label = ttk.Label(
            self.barcode_frame,
            background='white',
            foreground='gray',
            font=Fonts.infoTextFont,
            text="Entre com o código de barras aqui. Em seguida, tecle [ ENTER ]"
        )
        self.barcode_label.place(relx=0.01, rely=0.05)

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


