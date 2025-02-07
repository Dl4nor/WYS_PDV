import os
import tkinter as tk
from tkinter import ttk
from app.utils.styles import *
from app.ui.desktop.home_ui import home_screen
from app.ui.desktop.sells_ui import sales_screen


class Aplication:
    def __init__(self):
        self.window = tk.Tk()
        self.style = ttk.Style()
        self.style_configure()
        self.window_create()
        self.icon_define()

        # Definindo o container onde ficarão as páginas
        self.container = ttk.Frame(self.window)
        self.container.pack(fill="both", expand=True)

        # Pilha de páginas
        self.screen_stack = []

        # Mostra a Home screen
        self.show_screen(home_screen)
        self.window.mainloop()

    def style_configure(self):
        # Definindo o tema de toda aplicação
        self.style.theme_use('alt')

        # Definindo o estilo dos MainFrame
        self.style.configure(
            'MainFrame.TFrame', 
            background=Colors.violetBackground
        )

        # Definindo o estilo do upperFrame
        self.style.configure(
            'UpperFrame.TFrame',
            background='#10002B'
        )

        # Definindo o estilo do MainBt
        self.style.configure(
            'MainBt.TButton', 
            background='#C77DFF', 
            foreground='black', 
            focuscolor='',
            font=Fonts.mainButtonFont
        )
        self.style.map(
            'MainBt.TButton',
            background=[('active', Colors.violetBackground)],
            foreground=[('active', 'black')]             
        )
        self.style.map(
            'Leave.MainBt.TButton',
            background=[('active', "#c05299")],
        )
        self.style.configure(
            'Back.TButton',
            background='#10002B',
            foreground='white',
            focuscolor='',
            borderwidth=0,
            relief="flat",
            font=Fonts.backButtonFont
        )
        self.style.map(
            'Back.TButton',
            background=[('active', '#240046')]
        )
        

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

        main_frame = ttk.Frame(parent, padding=20, style='MainFrame.TFrame')
        main_frame.pack(fill="both", expand=True)
        return main_frame
    
    def upper_frame_create(self, parent):
        # Cria barra acima com botão voltar

        upper_frame = ttk.Frame(parent, padding=0, height=20, style='UpperFrame.TFrame')
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

