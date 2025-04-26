from ..models.db_storage import DBProducts
from ..utils.notifications import Notification
from ..controller.main_controller import mainController
from ..services.report_PDF import reportPDF
from ..models.db_report import DBReports
from datetime import datetime
import os

class reportController():
    def __init__(self):
        self.dbP = DBProducts()
        self.dbr = DBReports()
        self.mController = mainController()
        self.notf = Notification()
        self.pdf = reportPDF()
        self.month_map = {
            "Janeiro": "1", "Fevereiro": "2", "Março": "3", "Abril": "4",
            "Maio": "5", "Junho": "6", "Julho": "7", "Agosto": "8",
            "Setembro": "9", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
        }

    def clear_treeview(self, treeview):
        # Limpa a treeview antes d preencher

        for item in treeview.get_children():
            treeview.delete(item)

    def search_reportFiles_by_date(self, month, year):
        # Procura os arquivos .xlsx de acordo com a data

        if month == "Mês":
            print("Mês não selecionado!")
            return

        base_dir = f"fechamentos/"
        result_paths = []

        if month == "Todos":
            # Verifica todas as pastas do ano
            for folder in os.listdir(base_dir):
                if folder.endswith(f"- {year}"):
                    result_paths.append(os.path.join(base_dir, folder))
        else:
            month_num = self.month_map.get(month)
            folder_name = f"{month_num} - {year}"
            full_path = os.path.join(base_dir, folder_name)
            if os.path.exists(full_path):
                result_paths.append(full_path)

        return result_paths

    def insert_folders(self, base_paths, treeview, day):
        # Insere os diretórios na treeview

        for folder_path in base_paths:
            folder_name = os.path.basename(folder_path)

            if os.path.isdir(folder_path):
                parent_id = treeview.insert("", "end", text=folder_name)

                for file in os.listdir(folder_path):
                    if file.endswith(".xlsx"):
                        if day == "Todos" or file.endswith(f"-{str(day).zfill(2)}.xlsx"):
                            treeview.insert(parent_id, "end", text=file.replace(".xlsx", ""))

    def bind_search_reports_button(self, treeview, day, month, year):
        # bind do botão "buscar" no report_ui

        self.clear_treeview(treeview)
        base_dirs = self.search_reportFiles_by_date(month, year)
        self.insert_folders(base_dirs, treeview, day)

    def bind_daily_report_button(self, file_path, storeName, printDate):
        # bind do botão "Gerar relatório diário" no report_ui

        if not printDate:
            return
        
        relType = "dia"
        sellsDatetime = datetime.strptime(printDate.strip(), "%Y / %m / %d").date()
        data = self.dbr.search_d_sells_by_date(sellsDatetime)
        dic_data = self.transform_data_to_dict(data)
        self.pdf.create_report(dic_data, file_path, relType, storeName, printDate)

    def bind_monthly_report_button(self, file_path, storeName, printDate):
        # bind do botão "Gerar relatório diário" no report_ui

        if not printDate:
            return
        
        relType = "mês"
        sellsDatetime = datetime.strptime(printDate.strip(), "%m / %Y").date()
        sellsMonthYear = sellsDatetime.strftime("%Y-%m")
        data = self.dbr.search_m_sells_by_date(sellsMonthYear)
        dic_data = self.transform_data_to_dict(data)
        self.pdf.create_report(dic_data, file_path, relType, storeName, printDate)

    def transform_data_to_dict(self, vec_data):
        # Tranforma o vetor data (retornado do SELECT) em um dicionário

        dic_data = []

        for row in vec_data:
            dic_data.append({
                "id": row[0],
                "nome": row[1],
                "codigo_barras": row[2],
                "qtd": row[3],
                "preco_unit": row[4],
                "preco_total": row[5]
            })
        
        return dic_data
            






    

    