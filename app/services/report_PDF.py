from ..utils.styles import Fonts
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from datetime import datetime
import webbrowser
import os

class reportPDF():
    def __init__(self):
        self.width, self.height = A4
        self.relfont = Fonts.relfont
    
    def  create_report(self, data, file_path, relType, storeName, sells_date):
        # Relatóio simulado, apresentado ao usuário em tela antes de ser baixado
        """
        dados: lista de dicionários com as chaves:
            - id, nome, codigo_barras, qtd, preco_unit, preco_total
        """

        today = datetime.now().strftime("%d/%m/%Y")
        now = datetime.now().strftime("%H:%M:%S")

        c = canvas.Canvas(file_path, pagesize=A4)

        # Cabeçalho
        c.setFont(f"{self.relfont}-Roman", 10)
        c.drawString(30, self.height - 30, "WYS PDV")
        c.drawCentredString(self.width / 2, self.height - 30, "www.wyspdv.com.br")
        c.drawRightString(self.width - 30, self.height - 30, f"{today} - {now}")
        c.line(30, self.height - 32, self.width - 30, self.height - 32)

        c.setFont(f"{self.relfont}-Bold", 18)
        c.drawCentredString(self.width / 2, self.height - 60, "Relatório de vendas")

        c.setFont(f"{self.relfont}-Bold", 14)
        c.drawCentredString(self.width / 2, self.height - 74, f"{storeName}")
        c.drawCentredString(self.width / 2, self.height - 90, sells_date)

        # Cabeçalho da tabela
        c.line(30, self.height - 123, self.width - 30, self.height - 123)

        c.setFont(f"{self.relfont}-Bold", 12)
        c.drawCentredString(self.width / 2, self.height - 135, f"Total de vendas do {relType}")

        c.setFont(f"{self.relfont}-Bold", 10)
        y = self.height - 150
        c.drawString(30, y, "ID")
        c.drawString(60, y, "Nome do produto")
        c.drawString(250, y, "Código de barras")
        c.drawString(370, y, "QTD.")
        c.drawString(415, y, "Valor unit.")
        c.drawString(505, y, "Valor total")

        c.line(30, y - 2, self.width - 30, y - 2)

        # Linhas de produtos
        c.setFont(f"{self.relfont}-Roman", 10)
        y -= 20
        total = 0
        for item in data:
            c.drawString(30, y, str(item["id"]))
            c.drawString(60, y, item["nome"][:30])  # Limita o nome
            c.drawString(250, y, str(item["codigo_barras"]))
            c.drawRightString(390, y, str(item["qtd"]))
            c.drawRightString(460, y, f"R$ {item['preco_unit']:.2f}".replace(".", ","))
            c.drawRightString(550, y, f"R$ {item['preco_total']:.2f}".replace(".", ","))

            total += item["preco_total"]
            y -= 20
            if y < 50:
                c.showPage()
                y = self.height - 50

        c.line(30, y + 10, self.width - 30, y + 10)

        # Total
        c.setFont(f"{self.relfont}-Bold", 12)
        c.drawRightString(560, y - 10, f"TOTAL     R$ {total:.2f}".replace(".", ","))

        c.save()
        self.print_report(file_path)
        print(f"Relatório gerado em: {file_path}")

    def print_report(self, file_path):
        # Printa o relatório na tela após criado

        pathRep = os.path.abspath(f"./{file_path}")
        webbrowser.open(pathRep)