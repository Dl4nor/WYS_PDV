import os
import psutil

class detectFiles():

    def is_file_open(self, file_path):
        # Verifica se o arquivo está aberto no Excel
        try:
            with open(file_path, "r+"):
                return False  # Se conseguir abrir, o arquivo NÃO está em uso
        except IOError:
            return True  # Se der erro, o arquivo está em uso

    def close_excel(self):
        # Encerra todos os processos do Excel
        for process in psutil.process_iter(attrs=["pid", "name"]):
            if "excel" in process.info["name"].lower():
                print(f"◯ Fechando Excel (PID: {process.info['pid']})...")
                process.kill()

    def wait_and_close_file(self, file_path):
        # Verifica se o arquivo está aberto e fecha o Excel se necessário
        if self.is_file_open(file_path):
            print("<!> O arquivo está aberto! Fechando o Excel...")
            self.close_excel()
        else:
            print("[✔] O arquivo está disponível para edição.")
    



