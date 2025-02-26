import os
import tkinter as tk
import pytz
from utils.styles import *
from ctypes import windll, byref, c_int

class mainController():
    def __init__(self):
        # Pilha de páginas
        self.screen_stack = []
        self.window = None
        self.container = None
        self.brazil_tz = self.define_time_zone()

    def define_time_zone(self):
        brasil_tz = pytz.timezone("America/Sao_Paulo")
        return brasil_tz

    def set_window(self, window):
        self.window = window
    
    def set_container(self, container):
        self.container = container

    def icon_define(self):
        # Caminho absoluto para o ícone
        script_dir = os.path.dirname(__file__)  # Diretório onde o script está
        icon_path = os.path.join(script_dir, "..", "assets", "icons", "wys_t_icon.ico")
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

    def rewrite_entry(self, entry, text, isReadonly=False):
        if isReadonly:
            entry.configure(state='normal')
            entry.delete(0, tk.END)
            entry.insert(0, text)
            entry.configure(state='readonly')
        else:
            entry.delete(0, tk.END)
            entry.insert(0, text)

    def bind_resizeFont_event(self, parent, font):
        # Aplica a fonte inicial em todos os widgets
        self.resize_all_fonts(parent, font)

        # Evento <Configure> apenas na janela principal
        parent.bind('<Configure>', lambda e: self.resize_all_fonts(parent, font))

    def resize_all_fonts(self, parent, font):
        for widget, (font, dividing) in font.items():
            Fonts.resize_font(None, parent, widget, font, dividing)
