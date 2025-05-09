from ..controller.sells_controller import sellsController
from ..utils.gnr_components import gnrComponents
from ..utils.styles import *
from ..models.db_sells import DBSells
from ..models.db_storage import DBProducts
from tkinter import ttk
import customtkinter as ctk

class sales_screen(ttk.Frame):
    def __init__(self, parent, mController):
        super().__init__(parent)
        self.mController = mController  # Classe mainController
        self.controller = sellsController()

        self.Components = gnrComponents(self.mController)
        self.bdP = DBProducts()
        self.dbS = DBSells()

        self.Components.upper_frame_construct(self)
        self.main_frame = self.Components.main_frame_create(self)
        self.main_frame_widget()
        self.barcode_frame_create()
        self.barcode_frame_widget()
        self.quantity_frame_create()
        self.quantity_frame_widgets()
        self.shortcut_frame_create()
        self.shortcut_frame_widget()
        self.sellList_frame_create()
        self.sellList_frame_widget()
        self.product_name_frame_create()
        self.product_name_frame_widget()
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

        self.bind_all("<F2>", lambda e: self.controller.cancel_sell_button_command(self))
        self.bind_all("<F3>", lambda e: self.dbS.add_sell(self))

    def barcode_frame_create(self):
        # Cria o frame do código de barras

        self.barcode_frame = ttk.Frame(self, padding=10, takefocus=1, style='BarcodeFrame.TFrame')
        self.barcode_frame.place(relx=0.01, rely=0.15, relwidth=0.5, relheight=0.15)

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
            text="Insira o código de barras. Em seguida, tecle [ ENTER ]"
        )
        self.barcode_label.place(relx=0.01, rely=0.022)

        self.barcode_entry.bind(
            "<Return>", 
            lambda event: self.controller.barcode_entry_bind_enter(self, event)
        )

    def quantity_frame_create(self):
        # Cria o frame de quantidade do produto vendido

        self.quantity_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.quantity_frame.place(rely=0.31, relx=0.01, relheight=0.49, relwidth=0.25)

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
        self.quantity_entry.place(rely=0.05, relx=0.04, relheight=0.22, relwidth=0.92)
        self.quantity_entry.bind(
            "<Return>", 
            lambda event: self.controller.quantity_entry_bind_enter(self, event)
        )
        self.quantity_entry.bind(
            "<KeyRelease>", 
            lambda event: self.controller.quantity_entry_bind_KeyRelease(self, event)
        )

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
        self.uniPrice_entry.place(rely=0.365, relx=0.04, relheight=0.22, relwidth=0.92)

        self.uniPrice_label = ttk.Label(
            self.quantity_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Preço unitário:"
        )
        self.uniPrice_label.place(rely=0.315, relx=0.04)

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
        self.subtotal_entry.place(rely=0.680, relx=0.04, relheight=0.22, relwidth=0.92)

        self.subtotal_label = ttk.Label(
            self.quantity_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="SUBTOTAL:"
        )
        self.subtotal_label.place(rely=0.63, relx=0.04)

    def shortcut_frame_create(self):
        # Cria o frame de menu de atalhos

        self.shortcut_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.shortcut_frame.place(rely=0.31, relx=0.27, relheight=0.49, relwidth=0.24)

    def shortcut_frame_widget(self):
        # Cria os labels do frame de atalhos

        self.help_label = ttk.Label(
            self.shortcut_frame,
            background=Colors.violetButton,
            foreground='lightgray',
            font=Fonts.shortcutFont,
            text=
            "F1 - Ajuda\n\n"
            "F2 - Cancelar venda\n\n"
            "F3 - Confirmar venda\n\n",
        )
        self.help_label.pack(padx=0.5)

    def sellList_frame_create(self):
        # Cria o frame de informações da atual venda

        self.sellList_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.sellList_frame.place(rely=0.15, relx=0.52, relheight=0.65, relwidth=0.47) 

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
        self.sellList_treeview.column("#1", width=0, minwidth=0, stretch=False)
        self.sellList_treeview.column("#2", width=160, minwidth=160)
        self.sellList_treeview.column("#3", width=27, minwidth=27, anchor='center')
        self.sellList_treeview.column("#4", width=55, minwidth=44, anchor='e')
        self.sellList_treeview.column("#5", width=55, minwidth=44, anchor='e')

        self.sellList_treeview.bind(
            '<Motion>', 
            self.handle_column_resize
        )
        self.sellList_treeview.bind(
            '<<TreeviewSelect>>', 
            lambda event: self.controller.sellList_treeview_bind_TreeviewSelect(self, event)
        )

        self.sellList_treeview.place(rely=0.001, relx=0.003, relheight=0.78, relwidth=0.985)

        self.sellList_scrollbar = ttk.Scrollbar(
            self.sellList_frame,
            orient='vertical'
        )
        self.sellList_treeview.configure(yscroll=self.sellList_scrollbar.set)
        self.sellList_scrollbar.place(rely=0.001, relx=0.989, relheight=0.78, relwidth=0.01)

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
        self.total_price_entry.place(rely=0.84, relx=0.55, relheight=0.15, relwidth=0.44)

        self.total_price_label = ttk.Label(
            self.sellList_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Total:"
        )
        self.total_price_label.place(rely=0.793, relx=0.55)

        self.confirm_sell_button = ttk.Button(
            self.sellList_frame,
            text="Vender",
            style='ConfirmSell.TButton',
            padding=10,
            command= lambda: self.dbS.add_sell(self)
        )
        self.confirm_sell_button.place(rely=0.84, relx=0.26, relheight=0.15, relwidth=0.28)

        self.cancel_sell_button = ttk.Button(
            self.sellList_frame,
            text="Estornar",
            style='CancelSell.TButton',
            padding=10,
            command= lambda: self.controller.cancel_sell_button_command(self)
        )
        self.cancel_sell_button.place(rely=0.84, relx=0.01, relheight=0.15, relwidth=0.24)

    def product_name_frame_create(self):
        # Cria o frame de informações da atual venda

        self.product_name_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.product_name_frame.place(rely=0.81, relx=0.01, relheight=0.15, relwidth=0.98)

    def product_name_frame_widget(self):
        # Cria o widget do pName_frame

        self.product_name_entry = ctk.CTkEntry(
            self.product_name_frame,
            corner_radius=20,
            fg_color='white',
            bg_color=Colors.violetButton,
            text_color='gray',
            justify='center',
            state='normal',
            font=('Arial', 54, 'bold'),
        )
        self.product_name_entry.insert(0, "Nome do produto")
        self.product_name_entry.configure(state='readonly')
        self.product_name_entry.place(rely=0.01, relx=0.001, relheight=0.98, relwidth=0.99)

    def handle_column_resize(self, event):
        # impede o redimensionamento da coluna #0
        if self.sellList_treeview.identify_region(event.x, event.y) == "separator":
            # Obtém o identificador da coluna
            column = self.sellList_treeview.identify_column(event.x)
            
            # Se for a coluna #0, não permite o redimensionamento
            if column in ("#0"):
                return "break"

    def resize_controller(self):
        self.mController.bind_resizeFont_event(
            self,
            {
                self.quantity_entry: (Fonts.quantityFont, 25),
                self.uniPrice_entry: (Fonts.quantityFont, 25),
                self.subtotal_entry: (Fonts.quantityFont, 25),
                self.total_price_entry: (Fonts.quantityFont, 25),
                self.barcode_entry: (Fonts.barcodeFont, 30),
                self.barcode_label: (Fonts.infoTextFont, 60),
                self.title: (Fonts.screenTitleFont, 15),
                self.sellList_treeview: (Fonts.treeviewHeadFont, 60),
                self.confirm_sell_button: (Fonts.sellsButtonFont, 60),
                self.cancel_sell_button: (Fonts.sellsButtonFont, 60),
                self.help_label: (Fonts.shortcutFont, 51),
            }
        )
