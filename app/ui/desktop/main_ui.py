import os
import tkinter as tk
from tkinter import ttk

# Função principal para gerar uma janela

def main_window_create():
    
    # Craindo janela
    window = tk.Tk()
    window.title("Sistema WYS - PDV")
    window.geometry("800x600")

    # Caminho absoluto para o ícone
    script_dir = os.path.dirname(__file__)  # Diretório onde o script está
    icon_path = os.path.join(script_dir, "..", "..", "assets", "icons", "wys_t_icon.ico")
    icon_path = os.path.abspath(icon_path)  # Converte para caminho absoluto

    # Definir icone
    window.iconbitmap(icon_path)

    # Criar frame principal
    main_frame = ttk.Frame(window, padding=20)
    main_frame.pack(fill="both", expand=True)

    title = ttk.Label(
        main_frame,
        text="Bem-vindo ao WYS",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=10)

    # Adiciona botão
    exit_button = ttk.Button(
        main_frame,
        text="Abrir Tela de Vendas",
        command=lambda: print("Tela de vendas aberta!")
    )
    exit_button.pack(pady=10)

    window.mainloop()



