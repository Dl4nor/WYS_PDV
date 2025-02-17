import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from app.utils.styles import *
from app.models.db_storage import DBProducts

class sales_screen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Classe Application
        self.bdP = DBProducts()

        controller.upper_frame_construct(self)
        self.main_frame = controller.main_frame_create(self)
        self.main_frame_widget()
        self.barcode_frame_create()
        self.barcode_frame_widget()
        self.quantity_frame_create()
        self.quantity_frame_widgets()
        self.sellList_frame_create()
        self.sellList_frame_widget()
        #
        self.resize_controller()

    def main_frame_widget(self):
        # Criar título
        self.title = ttk.Label(
            self.main_frame,
            text="Wys >> Vendas",
            font=Fonts.screenTitleFont,
            justify='center',
            background=Colors.violetBackground
        )
        self.title.pack(side='top', anchor='n')

    def barcode_frame_create(self):
        # Cria o frame do código de barras

        self.barcode_frame = ttk.Frame(self, padding=10, takefocus=1, style='BarcodeFrame.TFrame')
        self.barcode_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.15)

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

        self.barcode_entry.bind("<Return>", self.barcode_entry_bind_enter)

    def quantity_entry_bind_enter(self, event=None):
        items = self.sellList_treeview.get_children()

        if items:
            last_item_id = items[-1]
            values = self.sellList_treeview.item(last_item_id, "values")

            if values:
                values_list = list(values)

                new_qnt = self.quantity_entry.get().strip()
                new_subtotal = self.subtotal_entry.get().strip()

                values_list[2] = new_qnt
                values_list[4] = new_subtotal

                self.sellList_treeview.item(last_item_id, values=tuple(values_list))
                self.total_calculate()

    def quantity_entry_bind_KeyRelease(self, event=None):
        # Ação ao atualizar o preço
        price = float(self.uniPrice_entry.get().replace("R$", "").replace(",", ".").strip())
        quantity_text = self.quantity_entry.get().strip()

        if not quantity_text:
            quantity = 0
        else:
            quantity = int(self.quantity_entry.get().strip())

        new_subtotal = price*quantity
        new_subtotal_text = f"R$ {new_subtotal:.2f}".replace(".", ",")

        self.rewrite_entry(self.subtotal_entry, new_subtotal_text, True)

    def quantity_frame_create(self):
        # Cria o frame de quantidade do produto vendido

        self.quantity_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.quantity_frame.place(rely=0.31, relx=0.1, relheight=0.6, relwidth=0.25)

    def quantity_frame_widgets(self):
        # Cria os widgets do Frame de quantidade

        # Cria o entry de quantidade do produto
        self.quantity_entry = ctk.CTkEntry(
            self.quantity_frame,
            corner_radius=20,
            bg_color=Colors.violetButton,
            text_color='black',
            fg_color='white',
            justify='right',
            font=Fonts.quantityFont,
        )
        self.quantity_entry.place(rely=0.05, relx=0.04, relheight=0.15, relwidth=0.92)
        self.quantity_entry.bind("<Return>", self.quantity_entry_bind_enter)
        self.quantity_entry.bind("<KeyRelease>", self.quantity_entry_bind_KeyRelease)

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

    def sellList_frame_create(self):
        # Cria o frame de informações da atual venda

        self.sellList_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.sellList_frame.place(rely=0.31, relx=0.37, relheight=0.6, relwidth=0.53) 

    def rewrite_entry(self, entry, text, isReadonly=False):
        if isReadonly:
            entry.configure(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, text)
            entry.configure(state='readonly')
        else:
            entry.delete(0, tk.END)
            entry.insert(0, text)

    def get_item_by_barcode(self, barcode):
        # Recupera os itens pelo código de barras e adiciona no treeview
        product = self.bdP.get_product_by_barcode(barcode)

        if product:
            barcode = product["barcode"]
            product_name = product["product_name"]
            quantity = 1
            price = product["price"]
            price_text = f"R$ {price:.2f}".replace(".", ",")
            subtotal = quantity * price
            subtotal_text = f"R$ {subtotal:.2f}".replace(".", ",")
            
            self.sellList_treeview.insert("", tk.END, values=(
                    barcode, 
                    product_name, 
                    quantity, 
                    price_text, 
                    subtotal_text
                )
            )

            self.rewrite_entry(self.quantity_entry, quantity)
            self.rewrite_entry(self.uniPrice_entry, price_text, True)
            self.rewrite_entry(self.subtotal_entry, subtotal_text, True)
        else:
            print("⚠️ Produto não encontrado!")

    def total_calculate(self):
        total_price = 0

        for item in self.sellList_treeview.get_children():
            values = self.sellList_treeview.item(item, "values")

            if values:
                subtotal = values[4]
                subtotal = float(subtotal.replace("R$", "").replace(",", "."))
                total_price += subtotal
        
        total_price_text = f"R$ {total_price:.2f}".replace(".", ",")

        self.rewrite_entry(self.total_price_entry, total_price_text, True)

    def barcode_entry_bind_enter(self, event=None):
        # Evento para Enter de barcode_entry (recupera item e soma no subtotal)
        barcode = self.barcode_entry.get().strip()

        self.get_item_by_barcode(barcode)
        self.total_calculate()

        self.barcode_entry.delete(0, tk.END)

        self.barcode_entry.focus_set()

    def sellList_frame_widget(self):
        self.sellList_treeview = ttk.Treeview(
            self.sellList_frame,
            style='sellList.Treeview', 
            height=3, 
            columns=("col1", "col2", "col3", "col4", "col5")
        )

        self.sellList_treeview.heading("#0", text="")
        self.sellList_treeview.heading("#1", text="Código")
        self.sellList_treeview.heading("#2", text="Item")
        self.sellList_treeview.heading("#3", text="Qnt")
        self.sellList_treeview.heading("#4", text="Preço")
        self.sellList_treeview.heading("#5", text="Subtotal")

        self.sellList_treeview.column("#0", width=0, stretch=False)
        self.sellList_treeview.column("#1", width=70, minwidth=70)
        self.sellList_treeview.column("#2", width=160, minwidth=160)
        self.sellList_treeview.column("#3", width=27, minwidth=27, anchor='center')
        self.sellList_treeview.column("#4", width=55, minwidth=44, anchor='e')
        self.sellList_treeview.column("#5", width=55, minwidth=44, anchor='e')

        self.sellList_treeview.bind('<Motion>', self.handle_column_resize)

        self.sellList_treeview.place(rely=0.001, relx=0.003, relheight=0.68, relwidth=0.985)

        self.sellList_scrollbar = ttk.Scrollbar(
            self.sellList_frame,
            orient='vertical'
        )
        self.sellList_treeview.configure(yscroll=self.sellList_scrollbar.set)
        self.sellList_scrollbar.place(rely=0.001, relx=0.989, relheight=0.68, relwidth=0.01)

        self.total_price_entry = ctk.CTkEntry(
            self.sellList_frame,
            corner_radius=20,
            bg_color=Colors.violetButton,
            text_color='gray',
            fg_color='white',
            justify='center',
            font=Fonts.quantityFont,
            
        )
        self.total_price_entry.insert(0, "R$ 0,00")
        self.total_price_entry.configure(state='readonly')
        self.total_price_entry.place(rely=0.78, relx=0.55, relheight=0.15, relwidth=0.44)

        self.total_price_label = ttk.Label(
            self.sellList_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Total:"
        )
        self.total_price_label.place(rely=0.733, relx=0.55)

        self.confirm_sell_button = ttk.Button(
            self.sellList_frame,
            text="Vender",
            style='ConfirmSell.TButton',
            padding=10,
            command= lambda: print("Venda efetuada")
        )
        self.confirm_sell_button.place(rely=0.78, relx=0.26, relheight=0.15, relwidth=0.28)

        self.cancel_sell_button = ttk.Button(
            self.sellList_frame,
            text="Estornar",
            style='CancelSell.TButton',
            padding=10,
            command= lambda: print("Venda cancelada")
        )
        self.cancel_sell_button.place(rely=0.78, relx=0.01, relheight=0.15, relwidth=0.24)

    def handle_column_resize(self, event):
        # impede o redimensionamento da coluna #0
        if self.sellList_treeview.identify_region(event.x, event.y) == "separator":
            # Obtém o identificador da coluna
            column = self.sellList_treeview.identify_column(event.x)
            
            # Se for a coluna #0, não permite o redimensionamento
            if column in ("#0"):
                return "break"

    def resize_controller(self):
        # Redimenciona dinamicamente o tamanho da fonte dos entrys de quantity_frame
        self.controller.bind_resizeFont_event(
            self,
            [self.quantity_entry, self.uniPrice_entry, self.subtotal_entry, self.total_price_entry],
            Fonts.quantityFont,
            20
        )

        # Redimenciona dinamicamente o tamanho da fonte do barcodeEntry
        self.controller.bind_resizeFont_event(
            self,
            [self.barcode_entry],
            Fonts.barcodeFont,
            30
        )

        self.controller.bind_resizeFont_event(
            self,
            [self.title],
            Fonts.screenTitleFont,
            15
        )

        self.controller.bind_resizeFont_event(
            self,
            [self.sellList_treeview],
            Fonts.treeviewHeadFont,
            60
        )

        self.controller.bind_resizeFont_event(
            self,
            [self.confirm_sell_button, self.cancel_sell_button],
            Fonts.sellsButtonFont,
            50
        )



