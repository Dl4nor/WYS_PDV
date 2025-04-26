from ..models.db_controller import DBController
import sqlite3

class DBReports():
    def __init__(self):
        self.db = DBController()

    def search_d_sells_by_date(self, date):
        # procura prdutos e vendas pela data de venda
        self.db.connect()
        self.db.cursor.execute("""
            SELECT 
                p.id, 
                p.product_name, 
                p.barcode, 
                SUM(si.quantity) as totalQnt,
                ROUND(SUM(si.total_price) / SUM(si.quantity), 2) AS uniPrice, 
                SUM(si.total_price) AS totalPrice 
            FROM tb_storage AS p
            JOIN tb_selled_items AS si ON p.id = si.product_id
            JOIN tb_sells AS s ON si.sell_id = s.id
            WHERE DATE(s.sell_date) = ?
            GROUP BY p.id, p.product_name, p.barcode
            ORDER BY totalPrice DESC;
        """, (date,))
        searchSales = self.db.cursor.fetchall()
        self.db.disconnect()

        return searchSales

    def search_m_sells_by_date(self, date):
        # procura prdutos e vendas pela data de venda
        self.db.connect()
        self.db.cursor.execute("""
            SELECT 
                p.id, 
                p.product_name, 
                p.barcode, 
                SUM(si.quantity) as totalQnt,
                ROUND(SUM(si.total_price) / SUM(si.quantity), 2) AS uniPrice, 
                SUM(si.total_price) AS totalPrice 
            FROM tb_storage AS p
            JOIN tb_selled_items AS si ON p.id = si.product_id
            JOIN tb_sells AS s ON si.sell_id = s.id
            WHERE strftime('%Y-%m', s.sell_date) = ?
            GROUP BY p.id, p.product_name, p.barcode
            ORDER BY totalPrice DESC;
        """, (date,))
        searchSales = self.db.cursor.fetchall()
        self.db.disconnect()

        return searchSales