import requests

class OpenFoodFacts_API():
    def search_pname_from_barcode(codigo_barras):
        url = f"https://world.openfoodfacts.org/api/v2/product/{codigo_barras}.json"
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()
            if 'product' in dados:
                nome_produto = dados['product'].get('product_name', 'Nome não encontrado')
                return nome_produto
            else:
                return "Produto não encontrado"
        else:
            return "Erro ao buscar o produto"