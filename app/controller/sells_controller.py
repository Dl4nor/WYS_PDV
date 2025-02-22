import tkinter as tk
from models.db_storage import DBProducts
from controller.main_controller import mainController

class sellsController():
    def __init__(self):
        self.dbP = DBProducts()
        self.mController = mainController()

    def sellList_treeview_bind_TreeviewSelect(self, parent, event=None):
        # Evento ao clicar em um elemento de sellLsit_treeview

        selected_item = parent.sellList_treeview.selection()

        if selected_item:
            for item in selected_item:
                values = parent.sellList_treeview.item(item, "values")

                if values:
                    barcode = values[0]
                    product_name = values[1]
                    quantity = f"{values[2]}".replace(".", ",")
                    price = values[3]
                    subtotal = values[4]

                    self.mController.rewrite_entry(parent.barcode_entry, barcode)
                    self.mController.rewrite_entry(parent.product_name_entry, product_name, True)
                    self.mController.rewrite_entry(parent.quantity_entry, quantity)
                    self.mController.rewrite_entry(parent.uniPrice_entry, price, True)
                    self.mController.rewrite_entry(parent.subtotal_entry, subtotal, True)

    def quantity_entry_bind_enter(self, parent, event=None):

        barcode = parent.barcode_entry.get().strip()

        if barcode:
            items = parent.sellList_treeview.selection()
        else:
            items = parent.sellList_treeview.get_children()

        if items:
            last_item_id = items[-1]
            values = parent.sellList_treeview.item(last_item_id, "values")

            if values:
                values_list = list(values)
                price = float(values[3].replace("R$", "").replace(",", "."))

                new_qnt = float(parent.quantity_entry.get().replace(",", ".").strip())
                new_subtotal = new_qnt*price

                values_list[2] = f"{int(new_qnt) if new_qnt.is_integer() else new_qnt}"
                values_list[4] = f"R$ {new_subtotal:.2f}".replace(".", ",")

                parent.sellList_treeview.item(last_item_id, values=tuple(values_list))
                parent.barcode_entry.focus_set()
                parent.sellList_treeview.selection_remove(parent.sellList_treeview.selection())
                self.total_calculate(parent)
                self.clear_entries(parent)

    def quantity_entry_bind_KeyRelease(self, parent, event=None):
        # Ação ao atualizar o preço
        price = float(parent.uniPrice_entry.get().replace("R$", "").replace(",", ".").strip())
        quantity_text = parent.quantity_entry.get().strip()

        if not quantity_text:
            quantity = 0
        else:
            quantity = float(parent.quantity_entry.get().replace(",", ".").strip())

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
            self.mController.rewrite_entry(parent.product_name_entry, product_name, True)
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

    def clear_entries(self, parent):
        self.mController.rewrite_entry(parent.barcode_entry, "")
        self.mController.rewrite_entry(parent.quantity_entry, "")
        self.mController.rewrite_entry(parent.uniPrice_entry, "R$ 0,00", True)
        self.mController.rewrite_entry(parent.subtotal_entry, "R$ 0,00", True)
        self.mController.rewrite_entry(parent.product_name_entry, "Nome do produto", True)

    def cancel_sell_button_command(self, parent):
        # Estorna produto da lista de vendas
        selected_items = parent.sellList_treeview.selection()

        # Caso exista um item selecionado, estorna apenas ele
        if selected_items:
            for item in selected_items:
                parent.sellList_treeview.delete(item)

        # Caso não, estorna a lista completa
        else:
            parent.sellList_treeview.delete(*parent.sellList_treeview.get_children())
        
        parent.barcode_entry.focus_set()
        self.clear_entries(parent)
        self.total_calculate(parent)
