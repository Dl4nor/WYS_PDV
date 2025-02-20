import os
from datetime import datetime
import pytz
import sqlite3
from controller.sells_controller import sellsController
from app.models.db_controller import DBController

class DBSells():
    def __init__(self):
        self.db = DBController()
        self.sController = sellsController()
        
    def add_sell(self, parent):
        # Adiciona uma nova venda efetuada

        if not parent.sellList_treeview.get_children():
            print("⚠️ Nenhum item na venda!")
            return
        
        try:
            # Registra uma nova venda e recupera seu id
            self.db.connect()

            brasil_tz = pytz.timezone("America/Sao_Paulo")
            brasil_now = datetime.now(brasil_tz).strftime("%Y-%m-%d %H:%M:%S")
            
            self.db.cursor.execute("""
                INSERT INTO tb_sells (sell_date)
                VALUES (?)
            """, (brasil_now, ))
            sell_id = self.db.cursor.lastrowid

            for item in parent.sellList_treeview.get_children():
                item_values = parent.sellList_treeview.item(item, 'values')
                barcode, _, quantity, _, total_price_text = item_values

                total_price = float(total_price_text.replace("R$", "").replace(",", "."))

                self.db.cursor.execute("""
                    SELECT id
                    FROM tb_storage
                    WHERE barcode = ?
                """, (barcode, ))
                product = self.db.cursor.fetchone()

                if product:
                    product_id = product[0]

                    self.db.cursor.execute("""
                        INSERT INTO tb_selled_items (sell_id, product_id, quantity, total_price)
                        VALUES (?, ?, ?, ?)
                    """, (sell_id, product_id, int(quantity), float(total_price)))
                else:
                    print(f"⚠️ Produto com código {barcode} não encontrado no banco de dados!")

            self.db.commit()
            print(f"✅ Nova venda registrada com sucesso! ID: {sell_id}")

            parent.sellList_treeview.delete(*parent.sellList_treeview.get_children())
            self.sController.clear_entries(parent)
            self.sController.total_calculate(parent)

        except sqlite3.Error as e:
            print(f"❌ Erro: Venda não cadastrada - {e}")
        finally:
            self.db.disconnect()