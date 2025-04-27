from ..models.db_storage import DBProducts
from ..utils.notifications import Notification
from ..controller.main_controller import mainController
from ..services.report_PDF import reportPDF
from ..models.db_report import DBReports
from tkinter import filedialog
from datetime import datetime
from PIL import Image, ImageTk
import sys
import fitz
import shutil
import os
import io

class reportController():
    def __init__(self):
        self.dbP = DBProducts()
        self.dbr = DBReports()
        self.mController = mainController()
        self.notf = Notification()
        self.pdf = reportPDF()
        self.xlsx_dir = self.get_xlsx_dir_path()
        self.month_map = {
            "Janeiro": "1", "Fevereiro": "2", "Março": "3", "Abril": "4",
            "Maio": "5", "Junho": "6", "Julho": "7", "Agosto": "8",
            "Setembro": "9", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
        }

    def clear_treeview(self, treeview):
        # Limpa a treeview antes d preencher

        for item in treeview.get_children():
            treeview.delete(item)

    def get_xlsx_dir_path(self):
        # Recupera o caminho completo de "fechamentos\"
        
        if getattr(sys, 'frozen', False):
            base_dir = os.path.join(os.environ["LOCALAPPDATA"], "WYS_PDV")
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        xlsx_dir = os.path.join(base_dir, f"fechamentos")
        os.makedirs(xlsx_dir, exist_ok=True)

        return xlsx_dir

    def search_reportFiles_by_date(self, month, year):
        # Procura os arquivos .xlsx de acordo com a data

        if month == "Mês":
            print("Mês não selecionado!")
            return

        result_paths = []

        if month == "Todos":
            # Verifica todas as pastas do ano
            for folder in os.listdir(self.xlsx_dir):
                if folder.endswith(f"- {year}"):
                    result_paths.append(os.path.join(self.xlsx_dir, folder))
        else:
            month_num = self.month_map.get(month)
            folder_name = f"{month_num} - {year}"
            full_path = os.path.join(self.xlsx_dir, folder_name)
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
        sellsDatetime = datetime.strptime(printDate.strip(), "%d / %m / %Y").date()
        data = self.dbr.search_d_sells_by_date(sellsDatetime)
        dic_data = self.transform_data_to_dict(data)
        self.pdf.create_report(dic_data, file_path, relType, storeName, printDate)

    def delete_temp(self, temp_path):
        # Deleta a pasta temp
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
            print("Pasta temp deletada")

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
    
    def move_report(self, origin_path):
        # Move o report da pasta temporária para odestino que o usuário escolher

        if not origin_path:
            return

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_name = os.path.basename(origin_path)

        final_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Todos os arquivos", "*.*")],
            title="Escolha onde salvar o relatório",
            initialdir=desktop,
            initialfile=file_name
        )

        if final_path:
            shutil.move(origin_path, final_path)
            print(f"Arquivo movido de: {origin_path}")
            print(f"Para: {final_path}")
            return final_path

    def bind_download_report_button(self, origin_path):
        # bind do botão "Baixar relatório" no report_ui

        file_path = self.move_report(origin_path)
        if file_path:
            self.pdf.print_report(file_path)
            temp_path = os.path.dirname(os.path.dirname(origin_path))
            self.delete_temp(temp_path)

    def get_tkimage_from_pdf(self, pdf_path, frame, page=0):
        # Retorna o tk_image do report_pdf

        doc = fitz.open(pdf_path)
        page = doc.load_page(page)

        # Renderiza a página como uma imagem
        pixmap = page.get_pixmap(dpi=150)  # Melhor qualidade que o padrão (72 dpi)

        # Converte o pixmap em imagem PIL
        img_bytes = pixmap.tobytes("ppm")  # PPM é imagem em memória compatível
        img = Image.open(io.BytesIO(img_bytes))
        doc.close()

        # Atualiza o frame para ter certeza que temos o tamanho correto
        frame.update_idletasks()
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()

        # Calcula escala proporcional
        img_width, img_height = img.size
        ratio = max(frame_width / img_width, frame_height / img_height)  # Usa max para dar zoom até preencher
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        # Redimensiona a imagem para caber no frame
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Converte para ImageTk
        tk_image = ImageTk.PhotoImage(img)

        return tk_image








    

    