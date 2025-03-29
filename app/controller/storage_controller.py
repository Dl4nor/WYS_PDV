from ..models.db_storage import DBProducts
from ..utils.styles import MonetaryEntry
from ..controller.main_controller import mainController
from ..services.OFoodF_API import OpenFoodFacts_API
import tkinter as tk

class storageController():
    def __init__(self):
        self.dbP = DBProducts()
        self.mController = mainController()

    def barcode_entry_bind_enter(self, parent, event=None):
        # Função ao pressionar ENTER no barcode entry
        product_info = self.get_product_info(parent)
        barcode = product_info["barcode"]
        product = self.dbP.get_product_by_barcode(barcode)
        product_name = None
        if product:
            product_name = product["product_name"]
            price_text = f"R$ {product["price"]:.2f}".replace(".", ",")
        else:
            price_text = "R$ 0,00"

        if not product_name and barcode:
            product_name = OpenFoodFacts_API.search_pname_from_barcode(barcode)
        
        if not barcode:
            product_name = ""
        
        # Usando o índice correto para o insert
        parent.product_name_entry.delete("1.0", "end")  # Limpa o campo antes de inserir
        parent.product_name_entry.insert("1.0", product_name)  # Insere o nome do produto
        self.mController.rewrite_entry(parent.product_price_entry, price_text)

        parent.product_price_entry.focus_set()

    def entry_bind_KeyRelease(self, parent, event=None):
        # Função ao pressionar qualquer tecla no barcode entry
        self.get_searched_storage(parent)

    def storage_treeview_bind_doubleclick(self, parent, event=None):

        treeview = event.widget
        item = treeview.identify("item", event.x, event.y)

        if not item:
            # print("❗Nenhum item clicado!")
            return

        self.clear_entries(parent)
        parent.product_price_entry.delete(0, tk.END)
        parent.storage_treeview.selection()

        for n in parent.storage_treeview.selection():
            col1, col2, col3, col4 = parent.storage_treeview.item(n, "values")
            parent.barcode_entry.insert(tk.END, col2)
            parent.product_name_entry.insert("1.0", col3)
            parent.product_price_entry.insert(0, col4)

    def get_product_info(self, parent):
        # Recupera os dados das entrys
        barcode = parent.barcode_entry.get().strip()
        product_name = parent.product_name_entry.get("1.0", "end").strip()
        price_text = parent.product_price_entry.get().strip()

        price_text = MonetaryEntry.parse_price(price_text)

        try:
            price = float(price_text)
        except ValueError:
            # print("⚠️ Erro: O preço não é um número válido.")
            return None
        
        return {
            "barcode": barcode,
            "product_name": product_name,
            "price": price
        }
    
    def add_product_to_db(self, parent):
        # Adiciona um novo produto ao banco de dados
        product_info = self.get_product_info(parent)

        if not product_info["barcode"] or not product_info["product_name"]:
            return

        product = self.dbP.get_product_by_barcode(product_info["barcode"])
        if product:
            self.dbP.update_product(product_info)
            # print(f"✅ O produto '{product_info['product_name']}' foi atualizado com sucesso!")
        else:
            self.dbP.add_product(
                product_info["barcode"],
                product_info["product_name"],
                product_info["price"]
            )
            # print(f"✅ O produto '{product_info['product_name']}' foi adicionado com sucesso!")

        self.clear_entries(parent)
        self.get_storage_to_treeview(parent)
        parent.barcode_entry.focus_set()

    def delete_product_from_db(self, parent):
        # Deleta um produto do banco de dados
        product_info = self.get_product_info(parent)

        if not product_info["barcode"]:
            return

        self.dbP.delete_product(product_info["barcode"])

        self.clear_entries(parent)
        self.get_storage_to_treeview(parent)
        parent.barcode_entry.focus_set()

    def clear_entries(self, parent):
        parent.barcode_entry.delete(0, tk.END)
        parent.product_name_entry.delete("1.0", tk.END)
        parent.product_price_entry.set_value(0.0)

    def clear_button_click(self, parent):
        self.clear_entries(parent)
        self.get_storage_to_treeview(parent)
        parent.barcode_entry.focus_set()

    def get_searched_storage(self, parent):
        product_info = self.get_product_info(parent)
        barcode = f"{product_info['barcode']}%"
        product_name = f"{product_info['product_name']}%"

        parent.storage_treeview.delete(*parent.storage_treeview.get_children())

        product_name_list = self.dbP.search_product_by_name(product_name)
        product_barcode_list = self.dbP.search_product_by_barcode(barcode)
        product_list = list(set(product_barcode_list) & set(product_name_list))

        for i in product_list:
            price = i[3]
            i = (i[0], i[1], i[2], f"R$ {price:.2f}")
            parent.storage_treeview.insert("", tk.END, values=i)

    def get_storage_to_treeview(self, parent):

        parent.storage_treeview.delete(*parent.storage_treeview.get_children())

        products = self.dbP.get_all_products()

        for i in products:
            price = i[3]
            price_text = f"R$ {price:.2f}".replace(".", ",")
            i = (i[0], i[1], i[2], price_text)
            parent.storage_treeview.insert("", tk.END, values=i)