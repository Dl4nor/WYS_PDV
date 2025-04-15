from ..controller.storage_controller import storageController
from ..utils.styles import *
from ..utils.gnr_components import gnrComponents
from ..models.db_storage import DBProducts
from tkinter import ttk
import customtkinter as ctk

class storage_screen(ttk.Frame):
    def __init__(self, parent, mController):
        super().__init__(parent)
        self.dbP = DBProducts()
        self.Components = gnrComponents(mController)
        self.controller = storageController()
        self.mController = mController # Classe mainController

        self.Components.upper_frame_construct(self)
        self.main_frame = self.Components.main_frame_create(self)
        self.main_frame_widget()

        self.barcode_frame_create()
        self.barcode_frame_widget()
        self.storage_frame_create()
        self.storage_frame_widget()
        self.infoProduct_frame_create()
        self.infoProduct_frame_widget()

        self.controller.get_storage_to_treeview(self)

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

        self.barcode_entry.bind("<Return>", lambda event: self.controller.barcode_entry_bind_enter(self, event))
        self.barcode_entry.bind("<KeyRelease>", lambda event: self.controller.entry_bind_KeyRelease(self, event))

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
        self.storage_treeview.column("#2", width=115, minwidth=115, stretch=False, anchor="w")
        self.storage_treeview.column("#3", width=160, minwidth=160, anchor="w")
        self.storage_treeview.column("#4", width=100, minwidth=100, stretch=False, anchor='w')

        self.storage_treeview.bind('<Motion>', self.handle_column_resize)
        self.storage_treeview.bind('<Double-1>', lambda event: self.controller.storage_treeview_bind_doubleclick(self, event))

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
        self.product_name_entry.bind("<KeyRelease>", lambda event: self.controller.entry_bind_KeyRelease(self, event))

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
            command= lambda: self.controller.add_product_to_db(self)
        )
        self.add_product_button.place(rely=0.83, relx=0.0, relheight=0.08, relwidth=1)

        # Criando botão de adicionar produtos
        self.clear_entry_button = ttk.Button(
            self.infoProduct_frame,
            text="Limpar",
            style='Clear.TButton',
            padding=5,
            command= lambda: self.controller.clear_button_click(self)
        )
        self.clear_entry_button.place(rely=0.92, relx=0.0, relheight=0.08, relwidth=0.65)

        # Criando botão de excluir produtos
        self.delete_product_button = ttk.Button(
            self.infoProduct_frame,
            text="Excluir",
            style='CancelSell.TButton',
            padding=5,
            command= lambda: self.controller.delete_product_from_db(self)
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
        self.mController.bind_resizeFont_event(
            self,
            {
                self.title: (Fonts.screenTitleFont, 15),
                self.barcode_entry: (Fonts.barcodeFont, 30),
                self.barcode_label: (Fonts.infoTextFont, 60),
                self.delete_product_button: (Fonts.sellsButtonFont, 55),
                self.add_product_button: (Fonts.sellsButtonFont, 55),
                self.clear_entry_button: (Fonts.sellsButtonFont, 55),
                self.product_price_entry: (Fonts.quantityFont, 20),
                self.product_name_entry: (Fonts.productNameFont, 35),
                self.storage_treeview: (Fonts.treeviewTupleFont, 60),
            }
        )
