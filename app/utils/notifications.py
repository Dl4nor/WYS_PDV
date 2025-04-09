import customtkinter as ctk
from PIL import Image, ImageTk
from ..utils.styles import *

class Notification():

    window = None  # variável de classe para guardar a window principal

    @classmethod
    def set_window(cls, window):
        cls.window = window.winfo_toplevel()

    def __init__(self):
        self.main_toplevel = Notification.window

    def show_notification(self, img_path):
        notif = ctk.CTkToplevel(self.main_toplevel)
        notif.overrideredirect(True)
        notif.attributes("-topmost", True)
        notif.attributes("-alpha", 1.0)
        notif.configure(fg_color=Colors.violetBackground)

        screen_width = self.main_toplevel.winfo_width()

        # Carrega a imagem com PIL
        image = Image.open(img_path)
        original_width, original_height = image.size

        img_width = int(screen_width*0.20)
        aspect_ratio = original_height / original_width
        img_height = int(img_width * aspect_ratio)

        # CTkImage para suporte HiDPI
        self.ctk_image = ctk.CTkImage(light_image=image, size=(img_width, img_height))

        # Exibe a imagem como label
        img_label = ctk.CTkLabel(master=notif, image=self.ctk_image, text="")
        img_label.pack()

        # Posicionamento inicial (fora da tela)
        start_y = self.main_toplevel.winfo_y() - original_height
        end_y = self.main_toplevel.winfo_y() + 85
        x = self.main_toplevel.winfo_x() + self.main_toplevel.winfo_width() - int(img_width*1.28)

        notif.geometry(f"{img_width}x{img_height}+{x}+{start_y}")

        # Animação slide_in
        def slide_in(y=start_y):
            if y < end_y:
                notif.geometry(f"{img_width}x{img_height}+{x}+{y}")
                notif.after(10, lambda: slide_in(y + 10))
            else:
                notif.geometry(f"{img_width}x{img_height}+{x}+{end_y}")
                notif.after(1500, fade_out)

        # Fade-out
        def fade_out(alpha=1.0):
            alpha -= 0.05
            if alpha > 0:
                notif.attributes("-alpha", alpha)
                notif.after(25, lambda: fade_out(alpha))
            else:
                notif.destroy()

        slide_in()
