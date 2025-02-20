import requests

class OpenFoodFacts_API():
    def search_pname_from_barcode(barcode):
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        response = requests.get(url)

        if response.status_code == 200:
            datas = response.json()
            if 'product' in datas:
                product_name = datas['product'].get('product_name', 'Nome não encontrado')
                return product_name
            else:
                return None
        else:
            return None