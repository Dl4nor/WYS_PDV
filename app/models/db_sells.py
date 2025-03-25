from ..utils.detect_files import detectFiles
from ..services.Export_to_xlsx import exportToXlsx
from ..services.Pagbank_API import Pagbank_order_API
from ..controller.sells_controller import sellsController
from ..models.db_controller import DBController
import os
from datetime import datetime, date
import pytz
import sqlite3

class DBSells():
    def __init__(self):
        self.db = DBController()
        self.sController = sellsController()
        self.expxlsx = exportToXlsx()
        self.pagbank = Pagbank_order_API()
        self.files = detectFiles()
        
    def add_sell(self, parent):
        # Adiciona uma nova venda efetuada

        if not parent.sellList_treeview.get_children():
            print("⚠️ Nenhum item na venda!")
            return
        
        try:
            # Registra uma nova venda e recupera seu id
            sell_id = self.get_id_from_new_sell()
            self.insert_selled_items_to_db(parent, sell_id)
            print(f"✅ Nova venda registrada com sucesso! ID: {sell_id}")

            parent.sellList_treeview.delete(*parent.sellList_treeview.get_children())
        
            self.sController.clear_entries(parent)
            self.sController.total_calculate(parent)

        except sqlite3.Error as e:
            print(f"❌ Erro: Venda não cadastrada - {e}")
        finally:
            output_dir = f"Fechamentos/{date.today().month} - {date.today().year}/"
            output_file = os.path.join(output_dir, f"Vendas - {date.today()}.xlsx")

            self.files.wait_and_close_file(output_file)

            self.pagbank.post_create_order()

            # Criar diretório se não existir
            os.makedirs(output_dir, exist_ok=True)
            
            self.expxlsx.export_sale_to_excel(date.today(), output_file)

    def get_id_from_new_sell(self):
        # Insere um item na tabela tb_sells
        self.db.connect()

        time_now = datetime.now(self.sController.brazil_tz).strftime("%Y-%m-%d %H:%M:%S")

        self.db.cursor.execute("""
            INSERT INTO tb_sells (sell_date)
            VALUES (?)
        """, (time_now, ))
        sell_id = self.db.cursor.lastrowid
        self.db.commit()
        self.db.disconnect()

        return sell_id
    
    def insert_selled_items_to_db(self, parent, sell_id):
        # Insere todos os itens vendidos da treeview para tb_selled_items
        self.db.connect()

        for item in parent.sellList_treeview.get_children():
            item_values = parent.sellList_treeview.item(item, 'values')
            barcode, _, quantity, _, total_price_text = item_values

            total_price = float(total_price_text.replace("R$", "").replace(",", "."))

            product_id = self.get_pId_by_barcode(barcode)

            if product_id:
                self.db.cursor.execute("""
                    INSERT INTO tb_selled_items (sell_id, product_id, quantity, total_price)
                    VALUES (?, ?, ?, ?)
                """, (sell_id, product_id, int(quantity), float(total_price)))
            else:
                print(f"⚠️ Produto com código {barcode} não encontrado no banco de dados!")
        
        self.db.commit()
        self.db.disconnect()

    def get_pId_by_barcode(self, barcode):
        # Pega o ID do produto pelo código de barras

        self.db.cursor.execute("""
            SELECT id
            FROM tb_storage
            WHERE barcode = ? AND is_active = 1
        """, (barcode, ))
        product = self.db.cursor.fetchone()
        
        if product:
            product_id = product[0]
        else:
            product_id = None
        
        return product_id
