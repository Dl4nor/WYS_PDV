from controller.main_controller import mainController
import tkinter
from tkinter import ttk
import customtkinter as ctk

class gnrComponents():

    def __init__(self, controller):
        self.mController = controller # Recupera mainController

    def main_frame_create(self, parent):
        # Criar frame principal

        main_frame = ttk.Frame(parent, style='MainFrame.TFrame')
        main_frame.pack(fill="both", expand=True)
        return main_frame
    
    def upper_frame_create(self, parent):
        # Cria barra acima com botão voltar

        upper_frame = ttk.Frame(parent, style='UpperFrame.TFrame')
        upper_frame.pack(fill='x')
        return upper_frame 
    
    def upper_frame_widget(self, upper_frame):
        # Criar botão de voltar
        self.back_bt = ttk.Button(
            upper_frame,
            text="<",
            width=2,
            style='Back.TButton',
            command= self.mController.go_back
        )
        self.back_bt.pack(side="left", padx=1)

    def upper_frame_construct(self, parent):
        if len(self.mController.screen_stack) > 0:
            upper_frame = self.upper_frame_create(parent)
            self.upper_frame_widget(upper_frame)
