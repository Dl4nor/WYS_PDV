import os
from datetime import datetime, date
import pytz
import sqlite3
from services.Export_to_xlsx import exportToXlsx
from controller.sells_controller import sellsController
from app.models.db_controller import DBController

class DBSells():
    def __init__(self):
        self.db = DBController()
        self.sController = sellsController()
        self.expxlsx = exportToXlsx()
        
    def add_sell(self, parent):
        # Adiciona uma nova venda efetuada

        if not parent.sellList_treeview.get_children():
            print("⚠️ Nenhum item na venda!")
            return
        
        try:
            # Registra uma nova venda e recupera seu id
            self.db.connect()

            time_now = datetime.now(self.sController.brazil_tz).strftime("%Y-%m-%d %H:%M:%S")
            
            self.db.cursor.execute("""
                INSERT INTO tb_sells (sell_date)
                VALUES (?)
            """, (time_now, ))
            sell_id = self.db.cursor.lastrowid

            for item in parent.sellList_treeview.get_children():
                item_values = parent.sellList_treeview.item(item, 'values')
                barcode, _, quantity, _, total_price_text = item_values

                total_price = float(total_price_text.replace("R$", "").replace(",", "."))

                self.db.cursor.execute("""
                    SELECT id
                    FROM tb_storage
                    WHERE barcode = ? AND is_active = 1
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

            output_dir = f"Fechamentos/{date.today().month} - {date.today().year}/"
            output_file = os.path.join(output_dir, f"Vendas - {date.today()}.xlsx")

            # Criar diretório se não existir
            os.makedirs(output_dir, exist_ok=True)
            
            self.expxlsx.export_sale_to_excel(date.today(), output_file)