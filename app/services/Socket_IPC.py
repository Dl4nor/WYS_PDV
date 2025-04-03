import socket
import threading
import sys
from urllib.parse import urlparse, parse_qs

class IPCSocket:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 65432
        self.server_socket = None

    def run(self):
        """Executa o processo de IPC: tenta enviar código ou inicia servidor"""
        if self.send_to_existing_instance(sys.argv[1] if len(sys.argv) > 1 else ""):
            sys.exit(0)  # Fecha nova instância se já houver outra rodando
        
        # Se não há outra instância, inicia o servidor
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()

        print("Iniciando o app...")

    def handle_client(self, client_socket):
        """Recebe dados do cliente e processa o código"""
        try:
            data = client_socket.recv(1024).decode()
            print(f"[OK] Codigo de autenticacao recebido: {data}")
        finally:
            client_socket.close()
            
            # Extrai o código do deep link
            parsed_url = urlparse(data)  # Analisa a URL
            params = parse_qs(parsed_url.query)  # Pega os parâmetros da query string

            code = params.get("code", [""])[0]  # Pega o valor do parâmetro "code"

            self.auth_code = code

            print(f"[OK] Código extraído: {code}")

    def start_server(self):
        """Cria e inicia o servidor para aceitar conexões"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print("[**] Servidor IPC rodando...")

            while True:
                client, _ = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client,)).start()
        except OSError as e:
            print(f"[X] Erro ao iniciar servidor IPC: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def send_to_existing_instance(self, code):
        """Tenta enviar o codigo para uma instancia já em execucao"""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, self.port))
            client.send(code.encode())
            client.close()
            print("[OK] Codigo enviado para a instancia ativa!")
            return True
        except ConnectionRefusedError:
            return False  # Nenhuma instância detectada

# Só executa se chamado diretamente, evitando execução acidental ao importar
if __name__ == "__main__":
    ipc = IPCSocket()
    ipc.run()
