from ..models.db_storage import DBProducts
from ..utils.styles import MonetaryEntry
from ..utils.notifications import Notification
from ..controller.main_controller import mainController
from ..services.OFoodF_API import OpenFoodFacts_API
import tkinter as tk
import winsound
import os

class reportController():
    def __init__(self):
        self.dbP = DBProducts()
        self.mController = mainController()
        self.notf = Notification()

    def clear_treeview(self, treeview):
        # Limpa a treeview antes d preencher

        for item in treeview.get_children():
            treeview.delete(item)

    # def insert_founded_on_treeview(self, treeview, files):
    #     # Insere os arquivos encontrados na treeview

    #     if files:
    #         for file in files:
    #             treeview.insert("", "end", text=file)
    #     else:
    #         return

    def search_reportFiles_by_date(self, month, year):
        # Procura os arquivos .xlsx de acordo com a data

        if month == "Mês":
            print("Mês não selecionado!")
            return
        
        month_map = {
            "Janeiro": "1", "Fevereiro": "2", "Março": "3", "Abril": "4",
            "Maio": "5", "Junho": "6", "Julho": "7", "Agosto": "8",
            "Setembro": "9", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
        }

        base_dir = f"fechamentos/"
        result_paths = []

        if month == "Todos":
            # Verifica todas as pastas do ano
            for folder in os.listdir(base_dir):
                if folder.endswith(f"- {year}"):
                    result_paths.append(os.path.join(base_dir, folder))
        else:
            month_num = month_map.get(month)
            folder_name = f"{month_num} - {year}"
            full_path = os.path.join(base_dir, folder_name)
            if os.path.exists(full_path):
                result_paths.append(full_path)

        return result_paths
    
    def bind_search_reports_button(self, treeview, day, month, year):
        # bind do botão "buscar" no report_ui

        self.clear_treeview(treeview)
        base_dirs = self.search_reportFiles_by_date(month, year)
        self.insert_folders(base_dirs, treeview, day)

    def insert_folders(self, base_paths, treeview, day):
        for folder_path in base_paths:
            folder_name = os.path.basename(folder_path)

            if os.path.isdir(folder_path):
                parent_id = treeview.insert("", "end", text=folder_name)

                for file in os.listdir(folder_path):
                    if file.endswith(".xlsx"):
                        if day == "Todos" or file.endswith(f"-{str(day).zfill(2)}.xlsx"):
                            treeview.insert(parent_id, "end", text=file.replace(".xlsx", ""))






    

    