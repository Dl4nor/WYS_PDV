from ..models.db_controller import DBController
import sqlite3

class DBReports():
    def __init__(self):
        self.db = DBController()

    # def search_sell_by_date(self, barcode):
    #     # procura produto pelo barcode
    #     self.db.connect()
    #     self.db.cursor.execute("""
    #         SELECT *
    #         FROM tb_storage
    #         WHERE barcode LIKE '%s' AND is_active = 1
    #         ORDER BY product_name ASC;
    #     """ % barcode)
    #     searchStorage = [tuple(row) for row in self.db.cursor.fetchall()]
    #     self.db.disconnect()
    #     return searchStorage