import os
import tkinter as tk
from utils.styles import *
from ctypes import windll, byref, c_int

class mainController():
    def __init__(self):
        # Pilha de páginas
        self.screen_stack = []
        self.window = None
        self.container = None

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

    def bind_resizeFont_event(self, parent, widgets, font, dividing):
        # Redimenciona o tamanho da fonte com evento <Mudar tamnho da janela>
        # Primeiro, define a fonte de acordo com o tamanho atual da tela
        for w in widgets:
            Fonts.resize_font(None, parent, w, font, dividing)

        # E caso a janela mude de tamanho, redimenciona de acordo com a altura
        for w in widgets:
            w.bind(
                '<Configure>', 
                lambda e, widget=w: Fonts.resize_font(
                    e,
                    parent,
                    widget, 
                    font,
                    dividing
                )
            )