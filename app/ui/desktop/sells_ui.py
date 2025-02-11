import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
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
        self.quantity_frame_create()
        self.quantity_frame_widgets()
        #
        self.sellList_frame_create()
        #

        self.resize_controller()



    def resize_controller(self):
        # Redimenciona dinamicamente o tamanho da fonte dos entrys de quantity_frame
        self.bind_resizeFont_event(
            [self.quantity_entry, self.uniPrice_entry, self.subtotal_entry],
            Fonts.quantityFont,
            20
        )

        # Redimenciona dinamicamente o tamanho da fonte do barcodeEntry
        self.bind_resizeFont_event(
            [self.barcode_entry],
            Fonts.barcodeFont,
            30
        )

        self.bind_resizeFont_event(
            [self.title],
            Fonts.screenTitleFont,
            15
        )

    def sellList_frame_create(self):
        # Cria o frame de informações da atual venda

        self.sellList_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.sellList_frame.place(rely=0.305, relx=0.37, relheight=0.6, relwidth=0.53)    

    def quantity_frame_create(self):
        # Cria o frame de quantidade do produto vendido

        self.quantity_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.quantity_frame.place(rely=0.305, relx=0.1, relheight=0.6, relwidth=0.25)

    def quantity_frame_widgets(self):
        # Cria os widgets do Frame de quantidade

        # Cria o entry de quantidade do produto
        self.quantity_entry = ctk.CTkEntry(
            self.quantity_frame,
            corner_radius=20,
            bg_color=Colors.violetButton,
            text_color='black',
            fg_color='white',
#            style='BarcodeEntry.TEntry',
            justify='right',
            font=Fonts.quantityFont,
        )
        self.quantity_entry.place(rely=0.05, relx=0.04, relheight=0.15, relwidth=0.92)

        self.quantity_label = ttk.Label(
            self.quantity_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Quantidade:"
        )
        self.quantity_label.place(rely=0.003, relx=0.04)

        # Cria o entry de preço unitário
        self.uniPrice_entry = ctk.CTkEntry(
            self.quantity_frame,
            corner_radius=20,
            fg_color='white',
            text_color='gray',
            bg_color=Colors.violetButton,
#           style='BarcodeEntry.TEntry',
            justify='right',
            state='normal',
            font=Fonts.quantityFont,
        )
        self.uniPrice_entry.insert(0, "R$ 0,00")
        self.uniPrice_entry.configure(state='readonly')
        self.uniPrice_entry.place(rely=0.30, relx=0.04, relheight=0.15, relwidth=0.92)

        self.uniPrice_label = ttk.Label(
            self.quantity_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Preço unitário:"
        )
        self.uniPrice_label.place(rely=0.253, relx=0.04)

        # Cria o entry de subtotal
        self.subtotal_entry = ctk.CTkEntry(
            self.quantity_frame,
            corner_radius=20,
            fg_color='white',
            bg_color=Colors.violetButton,
            text_color='gray',
#            style='BarcodeEntry.TEntry',
            justify='right',
            state='normal',
            font=Fonts.quantityFont,
        )
        self.subtotal_entry.insert(0, "R$ 0,00")
        self.subtotal_entry.configure(state='readonly')
        self.subtotal_entry.place(rely=0.55, relx=0.04, relheight=0.15, relwidth=0.92)

        self.subtotal_label = ttk.Label(
            self.quantity_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="SUBTOTAL:"
        )
        self.subtotal_label.place(rely=0.503, relx=0.04)

    def barcode_frame_create(self):
        # Cria o frame do código de barras

        self.barcode_frame = ttk.Frame(self, padding=10, takefocus=1, style='BarcodeFrame.TFrame')
        self.barcode_frame.place(relx=0.1, rely=0.145, relwidth=0.8, relheight=0.15)

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

        self.barcode_label = ttk.Label(
            self.barcode_frame,
            background='white',
            foreground='gray',
            font=Fonts.infoTextFont,
            text="Entre com o código de barras aqui. Em seguida, tecle [ ENTER ]"
        )
        self.barcode_label.place(relx=0.01, rely=0.022)

    def main_frame_widget(self):
        # Criar título
        self.title = ttk.Label(
            self.main_frame,
            text="Tela de Vendas",
            font=Fonts.screenTitleFont,
            justify='center',
            background=Colors.violetBackground
        )
        self.title.pack(side='top', anchor='n')

    def bind_resizeFont_event(self, widgets, font, dividing):
        # Redimenciona o tamanho da fonte com evento <Mudar tamnho da janela>
        # Primeiro, define a fonte de acordo com o tamanho atual da tela
        for w in widgets:
            Fonts.resize_font(None, self, w, font, dividing)

        # E caso a janela mude de tamanho, redimenciona de acordo com a altura
        for w in widgets:
            w.bind(
                '<Configure>', 
                lambda e, widget=w: Fonts.resize_font(
                    e,
                    self,
                    widget, 
                    font,
                    dividing
                )
            )



