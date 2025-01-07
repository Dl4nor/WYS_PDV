from cx_Freeze import setup, Executable

# Configurações do executável
executables = [
    Executable(
        script="app/main.py",  # Caminho para o arquivo principal do seu projeto
        base="Win32GUI",  # Para aplicativos GUI (remova para CLI)
        target_name="wys_pdv.exe",  # Nome do executável gerado
        icon="app/assets/icons/wys_icon.ico",  # Caminho para o ícone
    )
]

# Configurações do setup
setup(
    name="WYS PDV",
    version="1.0",
    description="Sistema PDV para minimercados",
    author="Seu Nome",
    options={
        "build_exe": {
            "packages": ["tkinter"],  # Dependências que devem ser incluídas
            "include_files": [
                "app/assets/",  # Inclua a pasta de ícones e imagens
            ],
        },
    },
    executables=executables,
)