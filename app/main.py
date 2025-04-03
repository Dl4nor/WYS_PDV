import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import Application
from app.services.Socket_IPC import IPCSocket

if __name__ == "__main__":
    # Inicia o IPC antes de carregar o resto do app
    ipc = IPCSocket()
    ipc.run()

    Application()