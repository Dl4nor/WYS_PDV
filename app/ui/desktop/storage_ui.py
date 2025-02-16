import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from app.utils.styles import *
from app.utils.OFoodF_API import OpenFoodFacts_API
from app.models.db_storage import DBProducts

class storage_screen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.dbP = DBProducts()
        self.controller = controller # Classe application

        controller.upper_frame_construct(self)
        self.main_frame = controller.main_frame_create(self)
        self.main_frame_widget()
        self.barcode_frame_create()
        self.barcode_frame_widget()
        self.storage_frame_create()
        self.storage_frame_widget()
        self.infoProduct_frame_create()
        self.infoProduct_frame_widget()
        self.get_storage_to_treeview()

        self.resize_controller()

    def main_frame_widget(self):
        # Criar título
        self.title = ttk.Label(
            self.main_frame,
            text="Wys >> Produtos",
            font=Fonts.screenTitleFont,
            justify='center',
            background=Colors.violetBackground
        )
        self.title.pack(side='top', anchor='n')

    def barcode_entry_bind_enter(self, event=None):
        # Função ao pressionar ENTER no barcode entry
        product_info = self.get_product_info()
        barcode = product_info["barcode"]
        product = self.dbP.get_product_by_barcode(barcode)
        product_name = None
        if product:
            product_name = product["product_name"]

        if not product_name and barcode:
            product_name = OpenFoodFacts_API.search_pname_from_barcode(barcode)
        
        if not barcode:
            product_name = ""
        
        # Usando o índice correto para o insert
        self.product_name_entry.delete("1.0", "end")  # Limpa o campo antes de inserir
        self.product_name_entry.insert("1.0", product_name)  # Insere o nome do produto

        self.product_price_entry.focus_set()
        self.get_searched_storage()

    def storage_treeview_bind_doubleclick(self, event=None):
        self.clear_entries()
        self.product_price_entry.delete(0, tk.END)
        self.storage_treeview.selection()

        for n in self.storage_treeview.selection():
            col1, col2, col3, col4 = self.storage_treeview.item(n, "values")
            self.barcode_entry.insert(tk.END, col2)
            self.product_name_entry.insert("1.0", col3)
            self.product_price_entry.insert(0, col4)

    def barcode_frame_create(self):
        # Cria o frame do código de barras

        self.barcode_frame = ttk.Frame(self, padding=10, takefocus=1, style='BarcodeFrame.TFrame')
        self.barcode_frame.place(relx=0.05, rely=0.15, relwidth=0.6, relheight=0.15)

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

    def storage_frame_create(self):
        # Cria o frame de informações da atual venda

        self.storage_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.storage_frame.place(rely=0.31, relx=0.05, relheight=0.6, relwidth=0.6)  

    def storage_frame_widget(self):
        self.storage_treeview = ttk.Treeview(
            self.storage_frame,
            style='sellList.Treeview', 
            height=3, 
            columns=("col1", "col2", "col3", "col4")
        )

        self.storage_treeview.heading("#0", text="")
        self.storage_treeview.heading('#1', text="id")
        self.storage_treeview.heading("#2", text="Código")
        self.storage_treeview.heading("#3", text="Item")
        self.storage_treeview.heading("#4", text="Preço")

        self.storage_treeview.column("#0", width=0, stretch=False)
        self.storage_treeview.column("#1", width=60, minwidth=60, stretch=False, anchor="center")
        self.storage_treeview.column("#2", width=100, minwidth=100, stretch=False, anchor="w")
        self.storage_treeview.column("#3", width=160, minwidth=160, anchor="w")
        self.storage_treeview.column("#4", width=120, minwidth=120, stretch=False, anchor="w")

        self.storage_treeview.bind('<Motion>', self.handle_column_resize)
        self.storage_treeview.bind('<Double-1>', self.storage_treeview_bind_doubleclick)

        self.storage_treeview.place(rely=0.001, relx=0.003, relheight=0.998, relwidth=0.985)

        self.storage_scrollbar = ttk.Scrollbar(
            self.storage_frame,
            orient='vertical'
        )
        self.storage_treeview.configure(yscroll=self.storage_scrollbar.set)
        self.storage_scrollbar.place(rely=0.001, relx=0.989, relheight=0.998, relwidth=0.01) 
        
    def infoProduct_frame_create(self):
        # Cria o frame de informações sobre o produto selecionado

        self.infoProduct_frame = ttk.Frame(self, padding=15, style='BarcodeFrame.TFrame')
        self.infoProduct_frame.place(rely=0.15, relx=0.66, relheight=0.76, relwidth=0.29)

    def get_product_info(self):
        # Recupera os dados das entrys
        barcode = self.barcode_entry.get().strip()
        product_name = self.product_name_entry.get("1.0", "end").strip()
        price_text = self.product_price_entry.get().strip()

        price_text = MonetaryEntry.parse_price(price_text)

        try:
            price = float(price_text)
        except ValueError:
            print("⚠️ Erro: O preço não é um número válido.")
            return None
        
        # if not barcode or not product_name:
        #     print("⚠️ Erro: Código de barras e nome do produto são obrigatórios!")
        #     return None

        return {
            "barcode": barcode,
            "product_name": product_name,
            "price": price
        }

    def add_product_to_db(self):
        # Adiciona um novo produto ao banco de dados
        product_info = self.get_product_info()

        if not product_info["barcode"] or not product_info["product_name"]:
            return

        product = self.dbP.get_product_by_barcode(product_info["barcode"])
        if product:
            self.dbP.update_product(product_info)
            print(f"✅ O produto '{product_info['product_name']}' foi atualizado com sucesso!")
        else:
            self.dbP.add_product(
                product_info["barcode"],
                product_info["product_name"],
                product_info["price"]
            )
            print(f"✅ O produto '{product_info['product_name']}' foi adicionado com sucesso!")

        self.clear_entries()
        self.get_storage_to_treeview()

    def delete_product_from_db(self):
        # Deleta um produto do banco de dados
        product_info = self.get_product_info()

        if not product_info["barcode"]:
            return

        self.dbP.delete_product(
            product_info["barcode"]
        )
        print(f"🗑️ O produto '{product_info['product_name']}' foi deletado com sucesso!")

        self.clear_entries()
        self.get_storage_to_treeview()

    def clear_entries(self):
        self.barcode_entry.delete(0, tk.END)
        self.product_name_entry.delete("1.0", tk.END)
        self.product_price_entry.set_value(0.0)

    def get_searched_storage(self):
        product_info = self.get_product_info()
        barcode = f"{product_info['barcode']}%"

        self.storage_treeview.delete(*self.storage_treeview.get_children())

        product_list = self.dbP.search_product(barcode)

        for i in product_list:
            self.storage_treeview.insert("", tk.END, values=i)

    def get_storage_to_treeview(self):

        self.storage_treeview.delete(*self.storage_treeview.get_children())

        products = self.dbP.get_all_products()

        for i in products:
            price = i[3]
            i = (i[0], i[1], i[2], f"R$ {price}")
            self.storage_treeview.insert("", tk.END, values=i)
        

    def infoProduct_frame_widget(self):
        # Cria os widgets para o frame infoProduct

        # Cria o entry de preço unitário
        self.product_price_entry = MonetaryEntry(
            self.infoProduct_frame,
            corner_radius=20,
            fg_color='white',
            text_color='black',
            bg_color=Colors.violetButton,
            justify='right',
            state='normal',
            font=Fonts.quantityFont,
        )
        self.product_price_entry.place(rely=0.04, relx=0.0, relheight=0.15, relwidth=1)

        self.product_price_label = ttk.Label(
            self.infoProduct_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Preço unitário:"
        )
        self.product_price_label.place(rely=0.0, relx=0.0)

        self.product_name_entry = ctk.CTkTextbox(
            self.infoProduct_frame,
            corner_radius=5,
            fg_color='white',
            text_color='black',
            bg_color=Colors.violetButton,
            state='normal',
            border_color="black",
            border_width=1,
            font=Fonts.productNameFont,
            wrap="word" 
        )
        self.product_name_entry.place(rely=0.25, relx=0.0, relheight=0.15, relwidth=1)

        self.product_name_label = ttk.Label(
            self.infoProduct_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Nome do produto:"
        )
        self.product_name_label.place(rely=0.21, relx=0.0)

        self.add_product_button = ttk.Button(
            self.infoProduct_frame,
            text="Adicionar produto",
            style='ConfirmSell.TButton',
            padding=5,
            command= self.add_product_to_db
        )
        self.add_product_button.place(rely=0.83, relx=0.0, relheight=0.08, relwidth=1)

        # Criando botão de adicionar produtos
        self.clear_entry_button = ttk.Button(
            self.infoProduct_frame,
            text="Limpar",
            style='Clear.TButton',
            padding=5,
            command= self.clear_entries
        )
        self.clear_entry_button.place(rely=0.92, relx=0.0, relheight=0.08, relwidth=0.65)

        # Criando botão de excluir produtos
        self.delete_product_button = ttk.Button(
            self.infoProduct_frame,
            text="Excluir",
            style='CancelSell.TButton',
            padding=5,
            command= self.delete_product_from_db
        )
        self.delete_product_button.place(rely=0.92, relx=0.66, relheight=0.08, relwidth=0.34)


    def handle_column_resize(self, event):
        # impede o redimensionamento da coluna #0
        if self.storage_treeview.identify_region(event.x, event.y) == "separator":
            # Obtém o identificador da coluna
            column = self.storage_treeview.identify_column(event.x)
            
            # Se for a coluna #0, não permite o redimensionamento
            if column in ("#0"):
                return "break"

    def resize_controller(self):
        # Redimenciona dinamicamente o tamanho da fonte dos entrys de quantity_frame
        self.controller.bind_resizeFont_event(
            self,
            [self.title],
            Fonts.screenTitleFont,
            15
        )

        self.controller.bind_resizeFont_event(
            self,
            [self.barcode_entry],
            Fonts.barcodeFont,
            30
        )

        self.controller.bind_resizeFont_event(
            self,
            [self.delete_product_button, self.add_product_button, self.clear_entry_button],
            Fonts.sellsButtonFont,
            55
        )

        self.controller.bind_resizeFont_event(
            self,
            [self.product_price_entry],
            Fonts.quantityFont,
            20
        )

        self.controller.bind_resizeFont_event(
            self,
            [self.product_name_entry],
            Fonts.productNameFont,
            35
        )