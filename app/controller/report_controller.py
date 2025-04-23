from ..models.db_storage import DBProducts
from ..utils.styles import MonetaryEntry
from ..utils.notifications import Notification
from ..controller.main_controller import mainController
from ..services.OFoodF_API import OpenFoodFacts_API
import tkinter as tk
import winsound

class reportController():
    def __init__(self):
        self.dbP = DBProducts()
        self.mController = mainController()
        self.notf = Notification()

    def clear_treeview(self, treeview):
        for item in treeview.get_children():
            self.treeview.delete(item)

    def insert_founded_on_treeview(self, treeview, files):
        treeview.insert("", "end", text=files)
    
    




    

    