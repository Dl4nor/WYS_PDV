import winreg
import sys
import os

class WYS_WebServer_API():
    def register_protocol_handler():
        # Registra o protocolo personalizado 'meupdv://' no Windows

        try:
            # Caminho para o executável do seu aplicativo
            app_path = os.path.abspath(sys.argv[0])
            
            # Registra o protocolo
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "meupdv") as key:
                winreg.SetValue(key, "", winreg.REG_SZ, "URL:MeuPDV Protocol")
                winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
                
                with winreg.CreateKey(key, r"shell\open\command") as cmd_key:
                    winreg.SetValue(cmd_key, "", winreg.REG_SZ, f'"{app_path}" "%1"')
            
            # print("Protocolo registrado com sucesso!")
        except Exception as e:
            print(f"Erro ao registrar protocolo: {e}")

    def handle_protocol_args():
        # Processa argumentos de linha de comando para protocolo personalizado

        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg.startswith("meupdv://auth?code="):
                # Extrair o código de autorização
                code = arg.replace("meupdv://auth?code=", "")
                # print(f"Código de autorização recebido: {code}")
                # Aqui você usaria o código no seu aplicativo
                return code
        return None