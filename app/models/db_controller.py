import os
import sqlite3
import sys

class DBController():

    def __init__(self, db_name="bd_wyspdv.sqlite"):
        # Inicializa o db_controller
        if getattr(sys, 'frozen', False):
            base_dir = os.path.join(os.environ["LOCALAPPDATA"], "WYS_PDV")
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)  # Cria a pasta apenas se não existir

        self.db_name = os.path.join(base_dir, db_name)
        self.conn = None
        self.cursor = None

        self.tables_contruct()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor(); print("[✔] Conectando ao banco...")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print("◯ Desconectando do banco...")

    def commit(self):
        if self.conn:
            self.conn.commit()

    def tables_contruct(self):
        # Criando as tabela
        try:
            self.connect()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_storage(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode         TEXT UNIQUE NOT NULL,
                    product_name    TEXT NOT NULL,
                    price           REAL NOT NULL DEFAULT 0.0,
                    is_active       INTEGER NOT NULL DEFAULT 1
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_sells(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    sell_date       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_selled_items(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    sell_id         INTEGER NOT NULL,
                    product_id      INTEGER NOT NULL,
                    quantity        INTEGER NOT NULL DEFAULT 1,
                    total_price     REAL NOT NULL DEFAULT 0.0,
                    FOREIGN KEY (sell_id) REFERENCES tb_sells(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES tb_storage(id)             
                )
            """)
            self.commit()
            print("[✔] Tabelas verificadas/criadas com sucesso")
        
        except sqlite3.Error as e:
            print(f"<!> Erro ao criar tabelas: {e}")
        
        finally:
            self.disconnect()

    
    