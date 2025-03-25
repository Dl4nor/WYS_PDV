from cx_Freeze import setup, Executable
from setuptools import find_packages
import winreg
import sys

def config_shortcut():
    shortcut_table = [
        (
            "DesktopShortcut",          # ID do atalho
            "DesktopFolder",            # Criar o atalho na Área de Trabalho
            "WYS PDV",                  # Nome do atalho
            "TARGETDIR",                # Diretório de destino para encontrar o executável
            "[TARGETDIR]WYS PDV.exe",   # Executável que o atalho vai abrir
            None,                       # Nenhum parâmetro adicional
            None,                       # Não há descrição extra
            None,                       # Ícone padrão ou personalizado se especificado
            None,                       # Ícone do índice, manter como None
            None,                       # Não há opção de hotkey
            None,
            "TARGETDIR",                # Diretório de destino do executável
        )
    ]
    return shortcut_table

def config_exe():
    # Configurações do executável
    executables = [
        Executable(
            script="app/main.py",  # Caminho para o arquivo principal do seu projeto
            base="Win32GUI",  # Para aplicativos GUI (remova para CLI)
            target_name="WYS PDV.exe",  # Nome do executável gerado
            icon="app/assets/icons/wys_real.ico",  # Caminho para o ícone
        )
    ]
    return executables

def config_setup(executables):

    shortcut = config_shortcut()

    # Configurações do setup
    setup(
        name="WYS PDV",
        version="1.0",
        description="Sistema PDV para minimercados",
        author="Seu Nome",
        options={
            "build_exe": {
                "packages": find_packages(),  # Dependências que devem ser incluídas
                "include_files": [
                    ("app/assets/", "assets/"),  # Inclua a pasta de ícones e imagens
                ],
                "optimize": 2,
            },
            "bdist_msi": {
                "data": {
                    "Shortcut": shortcut,
                },
            },
        },
        executables=executables,
    )

def add_deep_link(protocol):
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
                        f'"[TARGETDIR]WYS PDV.exe" "%1"')
        
        winreg.CloseKey(key)
        winreg.CloseKey(command_key)
        
        print(f"Deep link {protocol} registrado com sucesso!")
    except Exception as e:
        print(f"Erro ao registrar deep link: {e}")

if __name__ == "__main__":
    executables = config_exe()
    config_setup(executables)
    add_deep_link("wyspdv")
