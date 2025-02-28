import os
import sqlite3
from app.models.db_controller import DBController

class DBProducts(): 

    def __init__(self):
        # Inicializa DBProducts
        self.db = DBController()

    def get_product_by_barcode(self, barcode):
        # Busca produto pelo código de barras
        self.db.connect()
        self.db.cursor.execute("""
            SELECT *
            FROM tb_storage
            WHERE barcode = ?
        """, (barcode,))

        product = self.db.cursor.fetchone()
        self.db.disconnect()
        return product
    
    def search_product_by_barcode(self, barcode):
        # procura produto pelo barcode
        self.db.connect()
        self.db.cursor.execute("""
            SELECT *
            FROM tb_storage
            WHERE barcode LIKE '%s' AND is_active = 1
            ORDER BY product_name ASC;
        """ % barcode)
        searchStorage = [tuple(row) for row in self.db.cursor.fetchall()]
        self.db.disconnect()
        return searchStorage

    def search_product_by_name(self, product_name):
        # Procura o produto pelo nome
        self.db.connect()
        self.db.cursor.execute("""
            SELECT *
            FROM tb_storage
            WHERE product_name LIKE '%s' AND is_active = 1
            ORDER BY product_name ASC;
        """ % product_name)
        searchStorage = [tuple(row) for row in self.db.cursor.fetchall()]
        self.db.disconnect()
        return searchStorage

    def get_all_products(self):
        # Retorna todos os produtos da loja
        self.db.connect()
        self.db.cursor.execute("""
            SELECT *
            FROM tb_storage
            WHERE is_active = 1
            ORDER BY product_name ASC;
        """)
        products = [tuple(row) for row in self.db.cursor.fetchall()]
        self.db.disconnect()
        return products

    def add_product(self, barcode, product_name, price):
        # Adiciona um novo produto ao estoque
        try:
            self.db.connect()
            self.db.cursor.execute("""
                INSERT INTO tb_storage (barcode, product_name, price)
                VALUES (?, ?, ?)
            """, (barcode, product_name, price))
            print(f"✅ Produto '{product_name}' cadastrado com sucesso!")

            self.db.commit()
            
        except sqlite3.IntegrityError:
            print("⚠️ Erro: Código de barras já cadastrado!")
        except sqlite3.Error as e:
            print(f"⚠️ Erro: {e}")
        finally:
            self.db.disconnect()

    def delete_product(self, barcode):
        # Deleta um produto do banco
        product = self.get_product_by_barcode(barcode)

        if not product:
            print(f"⚠️ Erro: Produto com código de barras '{barcode}' não encontrado!")
            return
        
        product_name = product["product_name"]

        try:
            self.db.connect()
            self.db.cursor.execute("""
                UPDATE tb_storage
                SET is_active = 0
                WHERE barcode = ?
            """, (barcode,))

            self.db.commit()
            print(f"🗑️ Produto '{product_name}' desativado com sucesso!")

        except sqlite3.Error as e:
            print(f"⚠️ Erro ao deletar o produto: {e}")
        finally:
            self.db.disconnect()

    def update_product(self, new_product):
        # Atualiza os dados de um produto

        barcode = new_product["barcode"]
        new_name = new_product["product_name"]
        new_price = new_product["price"]

        try:
            self.db.connect()
            self.db.cursor.execute("""
                UPDATE tb_storage
                SET product_name = ?, price = ?, is_active = 1
                WHERE barcode = ?
            """, (new_name, new_price, barcode))
            self.db.commit()
            print(f"✅ Produto '{new_name}' atualizado com sucesso!")

        except sqlite3.Error as e:
            print(f"⚠️ Erro ao atualizar o produto: {e}")
        finally:
            self.db.disconnect()