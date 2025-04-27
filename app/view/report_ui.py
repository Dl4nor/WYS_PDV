from ..controller.report_controller import reportController
from ..utils.gnr_components import gnrComponents
from ..utils.styles import *
from ..models.db_sells import DBSells
from ..models.db_storage import DBProducts
from ..services.report_PDF import reportPDF
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import webbrowser
import calendar
import tempfile
import os

class report_screen(ttk.Frame):
    def __init__(self, parent, mController):
        super().__init__(parent)
        self.mController = mController  # Classe mainController
        self.rcontroller = reportController()

        self.Components = gnrComponents(self.mController)
        self.bdP = DBProducts()
        self.dbS = DBSells()
        self.pdf = reportPDF()

        self.Components.upper_frame_construct(self)
        self.main_frame = self.Components.main_frame_create(self)
        self.main_frame_widget()
        self.report_frame_create()
        self.report_frame_widgets()
        self.date_frame_create()
        self.date_frame_widgets()
        self.treeview_frame_create()
        self.treeview_frame_widgets()

        self.resize_controller()

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

        self.date_filter_frame = ttk.Frame(self, padding=5, style='BarcodeFrame.TFrame')
        self.date_filter_frame.place(rely=0.15, relx=0.72, relheight=0.15, relwidth=0.27)

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
        self.year_combobox.place(rely=0.25, relx=0.74, relheight=0.3, relwidth=0.25)
        self.year_combobox.bind("<<ComboboxSelected>>", lambda e: self._update_days_combobox())

        # Mês
        self.months = ["Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
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
        self.month_combobox.place(rely=0.25, relx=0.32, relheight=0.3, relwidth=0.43)
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
        self.day_combobox.place(rely=0.25, relx=0.01, relheight=0.3, relwidth=0.31)

    def _update_days_combobox(self):
        year = self.year_combobox.get()
        month = self.month_combobox.get()

        if year.isdigit() and month in self.months:
            month_index = self.months.index(month)
            if month_index>0:
                num_days = calendar.monthrange(int(year), month_index)[1]
                days = ["Todos"] + [str(day).zfill(2) for day in range(1, num_days + 1)]
                self.day_combobox.config(values=days)
            self.day_combobox.set("Todos")

    def on_date_combo_select(self):
        # Defini a fnção para quando uma combobox é selecionada

        for combobox in [self.month_combobox, self.year_combobox]:
            combobox.bind("<<ComboboxSelected>>", lambda e: (
                self._update_days_combobox(),
                self.rcontroller.bind_search_reports_button(
                    self.treeview_reports,
                    self.day_combobox.get(),
                    self.month_combobox.get(),
                    self.year_combobox.get()
                )
            )) 

        self.day_combobox.bind("<<ComboboxSelected>>", lambda e: self.rcontroller.bind_search_reports_button(
            self.treeview_reports,
            self.day_combobox.get(),
            self.month_combobox.get(),
            self.year_combobox.get()
        ))

    def date_frame_widgets(self):

        self.date_combo_create()
        self.on_date_combo_select()

        self.date_label = ttk.Label(
            self.date_filter_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Insira uma data"
        )
        self.date_label.place(relx=0.01, rely=0.01)

        self.date_search_button = ttk.Button(
            self.date_filter_frame,
            text="Buscar",
            style='Clear.TButton',
            padding=2,
            command= lambda: self.rcontroller.bind_search_reports_button(
                self.treeview_reports, 
                self.day_combobox.get(), 
                self.month_combobox.get(), 
                self.year_combobox.get()
            )
        )
        self.date_search_button.place(rely=0.6, relx=0.01, relheight=0.4, relwidth=0.98)
    
    def treeview_frame_create(self):
        # Cria o frame de Treeview

        self.treeview_frame = ttk.Frame(self, padding=5, style='BarcodeFrame.TFrame')
        self.treeview_frame.place(rely=0.31, relx=0.72, relheight=0.65, relwidth=0.27)

    def treeview_frame_widgets(self):
        # Cria os widgets da treeview

        self.treeview_reports = ttk.Treeview(
            self.treeview_frame,
            style='report.Treeview',
        )
        self.treeview_reports.heading("#0", text="Relatórios de Vendas")
        self.treeview_reports.place(rely=0.01, relx=0.01, relheight=0.55, relwidth=0.98)
        self.treeview_report_bind_config()
        self.rcontroller.bind_search_reports_button(self.treeview_reports, "Todos", "Todos", datetime.now().year)

        self.textbox_store_name = ctk.CTkEntry(
            self.treeview_frame,
            corner_radius=5,
            fg_color='white',
            text_color='black',
            bg_color=Colors.violetButton,
            state='normal',
            border_color="black",
            border_width=1,
            font=Fonts.storeNameFont,
        )
        self.textbox_store_name.place(rely=0.61, relx=0.01, relheight=0.09, relwidth=0.98)

        self.label_store_name = ttk.Label(
            self.treeview_frame,
            background=Colors.violetButton,
            foreground='black',
            font=Fonts.infoTextFont,
            text="Nome da loja:"
        )
        self.label_store_name.place(rely=0.57, relx=0.01)

        self.report_day_button = ttk.Button(
            self.treeview_frame,
            text="Gerar relatório diário",
            style='Clear.TButton',
            padding=2,
            command= lambda: (self.rcontroller.bind_daily_report_button(
                self.report_path, 
                self.textbox_store_name.get(),
                self.report_date
            ), self.update_report_frame_image())
        )
        self.report_day_button.place(rely=0.71, relx=0.01, relheight=0.08, relwidth=0.98)

        self.report_month_button = ttk.Button(
            self.treeview_frame,
            text="Gerar relatório mensal",
            style='Clear.TButton',
            padding=2,
            command= lambda: (self.rcontroller.bind_monthly_report_button(
                self.report_path,
                self.textbox_store_name.get(),
                self.report_date
            ), self.update_report_frame_image())
        )
        self.report_month_button.place(rely=0.8, relx=0.01, relheight=0.08, relwidth=0.98)
        
        self.report_download_button = ttk.Button(
            self.treeview_frame,
            text="Baixar relatório em PDF",
            style='ConfirmSell.TButton',
            padding=2,
            command= lambda: self.rcontroller.bind_download_report_button(self.report_path)
        )
        self.report_download_button.place(rely=0.9, relx=0.01, relheight=0.09, relwidth=0.98)
    
    def treeview_report_bind_config(self):
        # define o bind para selecionar uma tupla do treeview

        self.treeview_reports.bind("<<TreeviewSelect>>", lambda e: self._on_treeview_select(e))
        self.treeview_reports.bind("<Double-1>", lambda e: self._on_treeview_double_click(e))

    def _on_treeview_select(self, event):
        # Evento que aciona ao clicar em uma túpla da treeview
        
        tree = event.widget
        selected_item = tree.selection()

        if not selected_item:
            return

        item_id = selected_item[0]
        parent_id = tree.parent(item_id)
        item_text = tree.item(item_id, "text").replace(".xlsx", "").replace("Vendas - ", "")
        parent_text = tree.item(parent_id, "text")
        
        report_path = tempfile.gettempdir()
        report_path = os.path.join(report_path, "wys_reports")
        if parent_id != "":
            report_path += fr"\{parent_text}"
            os.makedirs(report_path, exist_ok=True)
            date = item_text.replace("Vendas - ", "").replace("-", " / ")
            report_path += fr"\Relatório do dia - {item_text}.pdf"
        else:
            report_path += fr"\{item_text}"
            os.makedirs(report_path, exist_ok=True)
            date = item_text.replace("-", " / ")
            report_path += fr"\Relatóio do mês - {item_text.replace(" - ", "-")}.pdf"
        
        self.report_path = report_path
        self.report_date = date

        print(f"rep_path: {self.report_path} --> rep_date: {self.report_date}")

    def _on_treeview_double_click(self, event):
        selected_item = self.treeview_reports.selection()
        if not selected_item:
            return
        
        item_text = self.treeview_reports.item(selected_item, "text")
        children = self.treeview_reports.get_children(selected_item)
        
        if children:
            return

        parent_item = self.treeview_reports.parent(selected_item)
        parent_text = self.treeview_reports.item(parent_item, "text")

        xlsx_path = os.path.join(self.rcontroller.xlsx_dir, parent_text, f"{item_text}.xlsx")

        if os.path.exists(xlsx_path):
            webbrowser.open(f'file:///{xlsx_path}')

        print(f"Arquivo xlsx em: {xlsx_path}")

    def report_frame_create(self):
        # Cria o frame de informações da atual venda

        self.report_frame = ttk.Frame(self, padding=10, style='BarcodeFrame.TFrame')
        self.report_frame.place(rely=0.15, relx=0.01, relheight=0.81, relwidth=0.7) 

    def report_frame_widgets(self):
        # Cria os widgets do report frame

        self.report_view_frame = ttk.Frame(self.report_frame, style='FrameWidget.TFrame')
        self.report_view_frame.place(rely=0.01, relx=0.01, relheight=0.98, relwidth=0.98)


    def update_report_frame_image(self):

        # Limpa o frame antes
        for widget in self.report_view_frame.winfo_children():
            widget.destroy()

        # Cria Canvas e Scrollbar vertical
        self.canvas = tk.Canvas(self.report_view_frame, highlightthickness=0)
        y_scroll = ttk.Scrollbar(self.report_view_frame, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=y_scroll.set)

        self.canvas.place(rely=0.01, relx=0.01, relheight=0.98, relwidth=0.98)
        y_scroll.pack(side="right", fill="y")

        self.tk_report = self.rcontroller.get_tkimage_from_pdf(self.report_path, self.report_view_frame)

        if self.tk_report:
            # Insere a imagem no Canvas
            self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_report)
            self.canvas.image = self.tk_report  # Mantém referência

            # Define o tamanho do scroll
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            # Habilita o scroll do mouse
            def _on_mousewheel(event):
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            self.canvas.bind("<MouseWheel>", _on_mousewheel)
        
            self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        if hasattr(self, "report_path") and hasattr(self, "canvas"):
            # Recarrega a imagem redimensionada no novo tamanho do Canvas
            self.tk_report = self.rcontroller.get_tkimage_from_pdf(self.report_path, self.report_view_frame)
            if self.tk_report:
                self.canvas.delete("all")
                self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_report)
                self.canvas.image = self.tk_report
                self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def resize_controller(self):
        self.mController.bind_resizeFont_event(
            self,
            {
                self.title: (Fonts.screenTitleFont, 15),
                self.year_combobox: (Fonts.reportTreeviewTupleFont, 52),
                self.month_combobox: (Fonts.reportTreeviewTupleFont, 52),
                self.day_combobox: (Fonts.reportTreeviewTupleFont, 52),
                self.date_search_button: (Fonts.sellsButtonFont, 50),
                self.report_day_button: (Fonts.sellsButtonFont, 50),
                self.report_month_button: (Fonts.sellsButtonFont, 50),
                self.report_download_button: (Fonts.sellsButtonFont, 50),
                self.treeview_reports: (Fonts.reportTreeviewTupleFont, 45),
                self.textbox_store_name: (Fonts.storeNameFont, 45)
            }
        )

    