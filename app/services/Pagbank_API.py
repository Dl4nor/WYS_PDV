'''
from ..models.db_controller import DBController
import requests
from datetime import date
import webbrowser

myToken = "cd49f263-8563-4cd6-ad24-ba9206f009946a1d16ac48d5a49654e8073c6608548f74b5-1d62-4e84-a840-3baf49ab691b"

class Pagbank_order_API():
    def __init__(self):
        self.db = DBController()

    def generate_pagbank_order_data(self):
        # Converte os itens da venda para o formato de dicionário

        # Estrutura básica de uma request
        order_data = {
            "customer": {
                "name": "Cliente", # Nome do cliente
                "email": "cliente@email.com",
                "tax_id": "12345678909" # CPF ou CNPJ do cliente
            },
            "reference_id": None,
            "items": [],
            "qr_codes": [{
                "amount": { "value": None }
            }]
        }

        items = self.get_last_selled_items()

        if not items:
            print("<!> Nenhuma venda encontrada para gerar o pedido!")
            return None

        sell_id = items[0][0]
        order_data["reference_id"] = str(sell_id)
        total_value = 0

        for _, _, product_name, quantity, total_price in items:
            total_price_cent = int(total_price * 100)  # Convertendo para centavos
            total_value += total_price_cent

            order_data["items"].append({
                "name": product_name,
                "quantity": quantity,
                "unit_amount": total_price_cent // quantity  # Preço unitário em centavos
            })
        
        order_data["qr_codes"][0]["amount"]["value"] = total_value

        return order_data

    def post_create_order(self):
        # Envia o pedido para a API do PagBank.

        url = "https://sandbox.api.pagseguro.com/orders"  # Para produção, altere para o endpoint real

        headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {myToken}",  # Token de autenticação
            "content-type": "application/json"
        }

        # Gera os dados do pedido
        order_data = self.generate_pagbank_order_data()

        try:
            response = requests.post(url, json=order_data, headers=headers)
            response_data = response.json()

            if response.status_code == 201:
                print("[OK] Pedido criado com sucesso!")
                print(response_data)
                return response_data  # Retorna os dados do pedido, incluindo ID e links

            else:
                print(f"[X] Erro ao criar pedido: {response_data}")
                return None

        except requests.RequestException as e:
            print(f"[X] Erro na requisição: {e}")
            return None

    def get_last_selled_items(self):
        # Recupera os itens da última venda registrada no banco de dados.

        self.db.connect()
        
        self.db.cursor.execute("""
            SELECT si.sell_id, s.barcode, s.product_name, SUM(si.quantity), SUM(si.total_price)
            FROM tb_storage s
            JOIN tb_selled_items si ON(si.product_id = s.id)
            WHERE si.sell_id = (
                SELECT id
                FROM tb_sells
                WHERE DATE(sell_date) = ?
                ORDER BY sell_date DESC
                LIMIT 1
            )
            GROUP BY si.sell_id, s.barcode, s.product_name
            ORDER BY s.product_name ASC
        """, (date.today(), ))

        items = self.db.cursor.fetchall()
        self.db.disconnect()

        return items

class Pagbank_account_API():
    def __init__(self):
        # response = self.post_create_application()

        self.AUTH_URL = "https://connect.sandbox.pagseguro.uol.com.br/oauth2/authorize"
        self.CLIENT_ID = "0962d187-8758-42e6-b6df-2d82d31cfb77"
        self.REDIRECT_URI = "https://wys-webserver.netlify.app/callback"
        self.CLIENT_SECRET = "0e639639-7eef-42cb-bceb-03f72a434558"
        self.SCOPE = "payments.read"

    def get_auth_link_to_oauth2(self):

        auth_link = f"{self.AUTH_URL}?response_type=code&client_id={self.CLIENT_ID}&redirect_uri={self.REDIRECT_URI}&scope={self.SCOPE}"

        return auth_link
    
    def get_access_token(self, code):
        url = "https://sandbox.api.pagseguro.com/oauth2/token"

        payload = {
            "grant_type": "authorization_code",
            "redirect_uri": self.REDIRECT_URI,
            "code": code
        }
        headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {myToken}",
            "X_CLIENT_ID": self.CLIENT_ID,
            "X_CLIENT_SECRET": self.CLIENT_SECRET,
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.text)
    
    """
    def post_create_application(self):
        # Cria uma aplicação, para poder utilizar dados do usuário Pagbank

        url = "https://sandbox.api.pagseguro.com/oauth2/application"

        payload = {
            "name": "WYS",
            "site": "https://wys-webserver.netlify.app",
            "redirect_uri": "https://wys-webserver.netlify.app/callback",
            "description": "Descrição da aplicação"
        }
        headers = {
            "accept": "*/*",
            "Authorization": myToken,
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.text)

        return response.json()
    """
    
'''