from ..controller.sells_controller import sellsController
from ..utils.gnr_components import gnrComponents
from ..utils.styles import *
from ..models.db_sells import DBSells
from ..models.db_storage import DBProducts
from datetime import datetime
import calendar
import os
from tkinter import ttk
import customtkinter as ctk
import winsound

class report_screen(ttk.Frame):
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
        self.report_frame_create()
        self.date_frame_create()
        self.date_frame_widgets()
        self.treeview_frame_create()
        self.treeview_frame_widgets()


        # self.barcode_frame_widget()
        # self.quantity_frame_create()
        # self.quantity_frame_widgets()
        # self.shortcut_frame_create()
        # self.shortcut_frame_widget()
        # self.sellList_frame_create()
        # self.sellList_frame_widget()
        # self.product_name_frame_create()
        # self.product_name_frame_widget()
        # #
        # self.resize_controller()

    def main_frame_widget(self):
        # Criar título
        self.title = ttk.Label(
            self.main_frame,
            text="Wys >> Relatórios",
            font=Fonts.screenTitleFont,
            justify='center',
            background=Colors.violetBackground
        )
        self.title.pack(side='top', anchor='n')
    
    def date_frame_create(self):
        # Cria o frame de informações da atual venda

        self.date_filter_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.date_filter_frame.place(rely=0.15, relx=0.72, relheight=0.2, relwidth=0.27)

    def date_combo_create(self):
        # Ano
        years = [str(year) for year in range(2020, datetime.now().year + 1)]
        self.year_combobox = ttk.Combobox(
            self.date_filter_frame, 
            values=years, 
            state="readonly", 
            width=10,
            style='date.TCombobox',
            font=Fonts.reportTreeviewTupleFont
        )
        self.year_combobox.set(str(datetime.now().year))
        self.year_combobox.place(rely=0.3, relx=0.64, relheight=0.3, relwidth=0.35)
        self.year_combobox.bind("<<ComboboxSelected>>", lambda e: self._update_days_combobox())

        # Mês
        self.months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                       "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.month_combobox = ttk.Combobox(
            self.date_filter_frame, 
            values=self.months, 
            state="readonly", 
            width=10,
            style='date.TCombobox',
            font=Fonts.reportTreeviewTupleFont
        )
        self.month_combobox.set("Mês")
        self.month_combobox.place(rely=0.3, relx=0.23, relheight=0.3, relwidth=0.4)
        self.month_combobox.bind("<<ComboboxSelected>>", lambda e: self._update_days_combobox())

        # Dia
        self.day_combobox = ttk.Combobox(
            self.date_filter_frame, 
            values=["Todos"], 
            state="readonly", 
            width=5,
            style='date.TCombobox',
            font=Fonts.reportTreeviewTupleFont
        )
        self.day_combobox.set("Dia")
        self.day_combobox.place(rely=0.3, relx=0.01, relheight=0.3, relwidth=0.21)

    def _update_days_combobox(self):
        year = self.year_combobox.get()
        month = self.month_combobox.get()

        if year.isdigit() and month in self.months:
            month_index = self.months.index(month) + 1
            num_days = calendar.monthrange(int(year), month_index)[1]
            days = ["Todos"] + [str(day).zfill(2) for day in range(1, num_days + 1)]
            self.day_combobox.config(values=days)
            self.day_combobox.set("Todos")
    
    def date_frame_widgets(self):

        self.date_combo_create()

        self.date_label = ttk.Label(
            self.date_filter_frame,
            background=Colors.violetButton,
            foreground='lightgray',
            font=Fonts.infoTextFont,
            text="Insira uma data"
        )
        self.date_label.place(relx=0.01, rely=0.022)
    
    def treeview_frame_create(self):
        # Cria o frame de Treeview

        self.treeview_frame = ttk.Frame(self, padding=5, style='BarcodeFrame.TFrame')
        self.treeview_frame.place(rely=0.36, relx=0.72, relheight=0.6, relwidth=0.27)

    def treeview_frame_widgets(self):
        # Cria os widgets da treeview

        self.treeview_reports = ttk.Treeview(
            self.treeview_frame,
            style='report.Treeview',
        )
        self.treeview_reports.heading("#0", text="Relatórios de Vendas")
        self.treeview_reports.place(rely=0.01, relx=0.01, relheight=0.63, relwidth=0.98)
        self.insert_folders(r"Fechamentos")

        self.report_day_button = ttk.Button(
            self.treeview_frame,
            text="Relatório diário",
            style='Clear.TButton',
            padding=5,
            command= lambda: print("aaa")
        )
        self.report_day_button.place(rely=0.65, relx=0.01, relheight=0.1, relwidth=0.98)

        self.report_month_button = ttk.Button(
            self.treeview_frame,
            text="Relatório mensal",
            style='Clear.TButton',
            padding=5,
            command= lambda: print("aaa")
        )
        self.report_month_button.place(rely=0.76, relx=0.01, relheight=0.1, relwidth=0.98)
        
        self.report_download_button = ttk.Button(
            self.treeview_frame,
            text="Baixar relatório",
            style='ConfirmSell.TButton',
            padding=5,
            command= lambda: print("aaa")
        )
        self.report_download_button.place(rely=0.89, relx=0.01, relheight=0.1, relwidth=0.98)

    def insert_folders(self, base_path):
        for folder in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder)
            if os.path.isdir(folder_path):
                # Adiciona o mês/ano como pasta principal
                parent_id = self.treeview_reports.insert("", "end", text=folder)

                # Adiciona os arquivos .xlsx como filhos
                for file in os.listdir(folder_path):
                    if file.endswith(".xlsx"):
                        self.treeview_reports.insert(parent_id, "end", text=f"{file.replace('.xlsx', '')}")

    def report_frame_create(self):
        # Cria o frame de informações da atual venda

        self.report_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.report_frame.place(rely=0.15, relx=0.01, relheight=0.81, relwidth=0.7)  

    