from cx_Freeze import setup, Executable
from setuptools import find_packages

def config_shortcut():
    shortcut_table = [
        (
            "DesktopShortcut",          # ID do atalho
            "DesktopFolder",            # Criar o atalho na Área de Trabalho
            "WYS PDV",                  # Nome do atalho
            "TARGETDIR",                # Diretório de destino para encontrar o executável
            "[#WYS PDV.exe]",           # Executável que o atalho vai abrir
            None,                       # Nenhum parâmetro adicional
            "Atalho para WYS PDV",      # Não há descrição extra
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

def msi_options_config():
    shortcut = config_shortcut()

    msi_options = {
        "data": {
            "Shortcut": shortcut,
        },
    }
    return msi_options

def build_options_config():
    build_options = {
        "packages": find_packages(),  # Dependências que devem ser incluídas
        "include_files": [
            ("app/assets/", "assets/"),  # Inclua a pasta de ícones e imagens
        ],
        "optimize": 2,
    }

    return build_options

def config_setup(executables):

    msi_options = msi_options_config()
    build_options = build_options_config()

    # Configurações do setup
    setup(
        name="WYS PDV",
        version="1.0",
        description="Sistema PDV para minimercados",
        author="Seu Nome",
        options={
            "build_exe": build_options,
            "bdist_msi": msi_options,
        },
        executables=executables,
    )

if __name__ == "__main__":
    executables = config_exe()
    config_setup(executables)
