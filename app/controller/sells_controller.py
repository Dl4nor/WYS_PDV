import tkinter as tk
from models.db_storage import DBProducts
from controller.main_controller import mainController

class sellsController():
    def __init__(self):
        self.dbP = DBProducts()
        self.mController = mainController()

    def quantity_entry_bind_enter(self, parent, event=None):
        items = parent.sellList_treeview.get_children()

        if items:
            last_item_id = items[-1]
            values = parent.sellList_treeview.item(last_item_id, "values")

            if values:
                values_list = list(values)

                new_qnt = parent.quantity_entry.get().strip()
                new_subtotal = parent.subtotal_entry.get().strip()

                values_list[2] = new_qnt
                values_list[4] = new_subtotal

                parent.sellList_treeview.item(last_item_id, values=tuple(values_list))
                self.total_calculate(parent)

    def quantity_entry_bind_KeyRelease(self, parent, event=None):
        # Ação ao atualizar o preço
        price = float(parent.uniPrice_entry.get().replace("R$", "").replace(",", ".").strip())
        quantity_text = parent.quantity_entry.get().strip()

        if not quantity_text:
            quantity = 0
        else:
            quantity = int(parent.quantity_entry.get().strip())

        new_subtotal = price*quantity
        new_subtotal_text = f"R$ {new_subtotal:.2f}".replace(".", ",")

        self.mController.rewrite_entry(parent.subtotal_entry, new_subtotal_text, True)

    def get_item_by_barcode(self, parent, barcode):
        # Recupera os itens pelo código de barras e adiciona no treeview
        product = self.dbP.get_product_by_barcode(barcode)

        if product:
            barcode = product["barcode"]
            product_name = product["product_name"]
            quantity = 1
            price = product["price"]
            price_text = f"R$ {price:.2f}".replace(".", ",")
            subtotal = quantity * price
            subtotal_text = f"R$ {subtotal:.2f}".replace(".", ",")
            
            parent.sellList_treeview.insert("", tk.END, values=(
                    barcode, 
                    product_name, 
                    quantity, 
                    price_text, 
                    subtotal_text
                )
            )

            self.mController.rewrite_entry(parent.quantity_entry, quantity)
            self.mController.rewrite_entry(parent.uniPrice_entry, price_text, True)
            self.mController.rewrite_entry(parent.subtotal_entry, subtotal_text, True)
        else:
            print("⚠️ Produto não encontrado!")

    def total_calculate(self, parent):
        total_price = 0

        for item in parent.sellList_treeview.get_children():
            values = parent.sellList_treeview.item(item, "values")

            if values:
                subtotal = values[4]
                subtotal = float(subtotal.replace("R$", "").replace(",", "."))
                total_price += subtotal
        
        total_price_text = f"R$ {total_price:.2f}".replace(".", ",")

        self.mController.rewrite_entry(parent.total_price_entry, total_price_text, True)

    def barcode_entry_bind_enter(self, parent, event=None):
        # Evento para Enter de barcode_entry (recupera item e soma no subtotal)
        barcode = parent.barcode_entry.get().strip()

        self.get_item_by_barcode(parent, barcode)
        self.total_calculate(parent)

        parent.barcode_entry.delete(0, tk.END)

        parent.barcode_entry.focus_set()