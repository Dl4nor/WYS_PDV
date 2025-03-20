import os
from flask import Flask, request, redirect

app = Flask(__name__)

# Rota inicial de autorização
@app.route('/')
def home():
    return redirect('https://connect.sandbox.pagseguro.uol.com.br/oauth2/authorize?client_id=355cf1c5-a1a0-4cfb-80dd-f6b265c9e818&response_type=code&redirect_uri=https://8d6f-2804-10f8-4330-c800-cd09-3109-ce45-795.ngrok-free.app/callback&scope=payments.read')

# Rota para capturar o código de autorização
@app.route('/callback')
def callback():
    authorization_code = request.args.get('code')
    if authorization_code:
        return f'Código de autorização recebido: {authorization_code}'
    return 'Erro: Código de autorização não encontrado!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Heroku define a PORT automaticamente
    app.run(host='0.0.0.0', port=port)
