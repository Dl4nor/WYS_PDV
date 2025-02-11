
class Colors():
    violetBackground = '#E0AAFF'
    violetButton = '#9D4EDD'

class Fonts():
    mainTitleFont = ("Harlow Solid Italic", 54, "bold")
    screenTitleFont = ("Harlow Solid Italic", 44, "bold")
    mainButtonFont = ('Georgia', 16, "bold")
    backButtonFont = ('Arial', 12, "bold")
    infoTextFont = ('Georgia', 11, "italic")
    barcodeFont = ('Arial', 17, "bold")
    quantityFont = ('Arial', 16, "bold")

    @staticmethod
    def resize_font(event, parent, widget, font, dividing):
        # Ajusta o tamanho da fonte com base no tamanho da janela

        new_font_size = parent.winfo_height() // dividing
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
        parent.style.map(
            'Leave.MainBt.TButton',
            background=[('active', "#c05299")],
        )
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