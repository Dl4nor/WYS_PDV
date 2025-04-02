import winreg
import sys
import os

def add_deep_link(protocol, install_dir):
    try:
        # Caminho da chave de registro para protocolo personalizado
        key_path = fr"SOFTWARE\Classes\{protocol}"
        
        # Abrir (ou criar) a chave de registro
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        
        # Definir valores do protocolo
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f"URL:{protocol.capitalize()} Protocol")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
        
        # Definir comando para abrir a aplicação
        command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                    fr"SOFTWARE\Classes\{protocol}\shell\open\command")
        winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, 
                        f'"{install_dir}\\dist\\WYS PDV.exe" "%1"')
        
        winreg.CloseKey(key)
        winreg.CloseKey(command_key)
        
        print(f"Deep link {protocol} registrado com sucesso!")
        print(f"Caminho do DeepLink: {install_dir}\\WYS PDV.exe")
    except Exception as e:
        print(f"Erro ao registrar deep link: {e}")

if __name__ == "__main__":
    # O caminho de instalação do programa será passado como argumento
    if len(sys.argv) > 1:
        install_dir = sys.argv[1]  # O diretório de instalação
        install_dir = install_dir.strip('"')
        add_deep_link("wyspdv", install_dir)
