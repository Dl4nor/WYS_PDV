import os
import tkinter as tk
from tkinter import ttk
from app.utils.styles import *
from app.ui.desktop.home_ui import home_screen
from app.ui.desktop.sells_ui import sales_screen
from ctypes import windll, byref, c_int



class Aplication:
    def __init__(self):
        
        self.window = tk.Tk()
        self.style = ttk.Style()
        ui_styles.style_configure(self)
        self.window_create()
        self.icon_define()

        # Ativa o modo escuro da barra de título (Windows 10 e 11)
        self.enable_dark_mode()

        # Definindo o container onde ficarão as páginas
        self.container = ttk.Frame(self.window)
        self.container.pack(fill="both", expand=True)

        # Pilha de páginas
        self.screen_stack = []

        # Mostra a Home screen
        self.show_screen(home_screen)
        self.window.mainloop()


    def window_create(self):
        # Criando janela
        self.window.title("Sistema WYS - PDV")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.maxsize(width=1920, height=1080)
        self.window.minsize(width=800, height=600)

    def icon_define(self):
        # Caminho absoluto para o ícone
        script_dir = os.path.dirname(__file__)  # Diretório onde o script está
        icon_path = os.path.join(script_dir, "..", "..", "assets", "icons", "wys_t_icon.ico")
        icon_path = os.path.abspath(icon_path)  # Converte para caminho absoluto

        # Definir icone
        self.window.iconbitmap(icon_path)

    def enable_dark_mode(self): # O importante é que funciona
        try:
            hwnd = windll.user32.GetParent(self.window.winfo_id())

            # Tentando aplicar para as diferentes versões do Windows
            USE_DARK_MODE = 20  # Código do DarkMode para Windows 10 1809 e superior
            DARK_MODE = c_int(1) # Ativa o modo escuro (1 = ON)

            result = windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                USE_DARK_MODE,
                byref(DARK_MODE),
                4
            )

            # Caso o primeiro valor não funcione, tenta o valor alternativo
            if result != 0:
                USE_DARK_MODE = 19  # Código do DarkMode para versões anteriores
                windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    USE_DARK_MODE,
                    byref(DARK_MODE),
                    4
                )
        except Exception as e:
            print(f"Falha ao ativar o modo escuro: {e}")

    def show_screen(self, screen_class):
        ## Exibe nova tela e esconde a anterior
        
        # Se existe uma tela visível, empilha o histórico
        if self.screen_stack:
            self.screen_stack[-1].pack_forget()

        # Cria uma nova janela e adiciona na pilha
        new_screen = screen_class(self.container, self)
        new_screen.pack(fill="both", expand=True)
        self.screen_stack.append(new_screen)

    def go_back(self):
        # Volta para a tela anterior

        if len(self.screen_stack) > 1:
            # Remove a tela da frente
            self.screen_stack.pop().pack_forget()

            # Mostra a tela anterior
            self.screen_stack[-1].pack(fill="both", expand=True)

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
            command= self.go_back
        )
        self.back_bt.pack(side="left", padx=1)

    def upper_frame_construct(self, parent):
        if len(self.screen_stack) > 0:
            upper_frame = self.upper_frame_create(parent)
            self.upper_frame_widget(upper_frame)

