import re
from tkinter import ttk
import customtkinter as ctk

class Colors():
    violetBackground = '#E0AAFF'
    violetButton = '#9D4EDD'

class Fonts():
    mainTitleFont = ("Harlow Solid Italic", 54, "bold")
    screenTitleFont = ("Harlow Solid Italic", 44, "bold")

    infoTextFont = ('Georgia', 11, "italic")
    mainButtonFont = ('Georgia', 16, "bold")

    backButtonFont = ('Arial', 12, "bold")
    sellsButtonFont = backButtonFont
    treeviewHeadFont = backButtonFont
    productNameFont = ('Arial', 12, "normal")
    barcodeFont = ('Arial', 17, "bold")
    quantityFont = ('Arial', 16, "bold")

    treeviewTupleFont = ('Arial', 10, "")
    

    @staticmethod
    def resize_font(event, parent, widget, font, dividing):
        # Ajusta o tamanho da fonte com base no tamanho da janela

        new_font_size = parent.winfo_height() // dividing

        if isinstance(widget, ttk.Treeview):
            style = ttk.Style()
            style.configure(f'{widget.cget('style')}.Heading', font=(font[0], new_font_size, font[2]))
            style.configure(f'{widget.cget('style')}', font=(font[0], new_font_size, font[2]))
        elif isinstance(widget, ttk.Button):
            style = ttk.Style()
            style.configure(widget.cget('style'), font=(font[0], new_font_size, font[2]))
        else:
            widget.configure(font=(font[0], new_font_size, font[2]))

class ui_styles(): 
    def style_configure(parent):
        # Definindo o tema de toda aplicação
        parent.style.theme_use('alt')

        # Definindo o estilo dos MainFrame
        parent.style.configure(
            'MainFrame.TFrame', 
            background=Colors.violetBackground
        )

        # Definindo o estilo do upperFrame
        parent.style.configure(
            'UpperFrame.TFrame',
            background='#10002B',
        )

        # Definindo o estilo do BarcodeFrame
        parent.style.configure(
            'BarcodeFrame.TFrame',
            background=Colors.violetButton,
            borderwidth=5,
            relief='raised'
        )

        parent.style.configure(
            'BarcodeEntry.TEntry',
            padding=(10, 5)
        )

        # Definindo o estilo do SellListTreeview
        parent.style.configure(
            'sellList.Treeview',
            background=Colors.violetBackground,
            foreground='black',
            font=Fonts.treeviewTupleFont
        )
        parent.style.configure(
            'sellList.Treeview.Heading',
            background=Colors.violetBackground,
            foreground='black',
            font=Fonts.treeviewHeadFont
        )

        parent.style.map(
            'sellList.Treeview.Heading',
            background = [('selected', Colors.violetButton), ('active', Colors.violetButton)]
        )

        # Definindo o estilo do MainBt
        parent.style.configure(
            'MainBt.TButton', 
            background='#C77DFF', 
            foreground='black', 
            focuscolor='',
            font=Fonts.mainButtonFont
        )
        parent.style.map(
            'MainBt.TButton',
            background=[('active', Colors.violetBackground)],
            foreground=[('active', 'black')]             
        )

        # Definindo o estilo do LeaveBt
        parent.style.map(
            'Leave.MainBt.TButton',
            background=[('active', "#c05299")],
        )

        # Definindo o estilo do backBt
        parent.style.configure(
            'Back.TButton',
            background='#10002B',
            foreground='white',
            focuscolor='',
            borderwidth=0,
            relief="flat",
            font=Fonts.backButtonFont
        )

        parent.style.map(
            'Back.TButton',
            background=[('active', '#240046')]
        )

        # Definindo o estilo do ConfirmSellBt
        parent.style.configure(
            'ConfirmSell.TButton',
            background='#95d5b2',
            focuscolor='',
            font=Fonts.sellsButtonFont
        )

        parent.style.map(
            'ConfirmSell.TButton',
            background=[('active', '#b7e4c7')]
        )

        # Definindo o estilo do CancelSellBt
        parent.style.configure(
            'CancelSell.TButton',
            background='#df7373',
            focuscolor='',
            font=Fonts.sellsButtonFont
        )

        parent.style.map(
            'CancelSell.TButton',
            background=[('active', '#e39695')]
        )

        # Definindo o estilo do ClearBt
        parent.style.configure(
            'Clear.TButton',
            background='#C77DFF',
            focuscolor='',
            font=Fonts.sellsButtonFont
        )
        parent.style.map(
            'Clear.TButton',
            background=[('active', Colors.violetBackground)]
        )

class MonetaryEntry(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Valor numérico interno (em centavos)
        self._value = 0
        
        # Configura validação
        self.bind('<KeyRelease>', self._validate)
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
        
        # Inicializa com R$ 0,00
        self.insert(0, "R$ 0,00")
    
    def _validate(self, event):
        if event.char.isdigit() or event.keysym in ('BackSpace', 'Delete'):
            # Pega o texto atual removendo formatação
            current = self.get().replace('R$ ', '').replace('.', '').replace(',', '').replace(' ', '')
            
            # Remove zeros à esquerda
            if current:
                current = str(int(current))
            
            # Converte para centavos
            if current:
                value = int(current)
            else:
                value = 0
                
            # Atualiza valor interno
            self._value = value
            
            # Formata e exibe
            self._update_display()
            
        # Impede caracteres não numéricos
        return False
    
    def _update_display(self):
        # Converte centavos para reais
        reais = self._value / 100 if self._value else 0
        
        # Formata com R$, separador de milhares e 2 casas decimais
        texto = f"R$ {reais:,.2f}".replace(',', '@').replace('.', ',').replace('@', '.')
        
        # Atualiza display
        self.delete(0, 'end')
        self.insert(0, texto)
    
    def _on_focus_in(self, event):
        # Opcional: seleciona todo o texto ao receber foco
        self.select_range(0, 'end')
    
    def _on_focus_out(self, event):
        # Garante formatação correta ao perder foco
        self._update_display()
    
    def get_value(self):
        # Retorna o valor em centavos
        return self._value
    
    def set_value(self, centavos):
        # Define o valor em centavos
        self._value = centavos
        self._update_display()