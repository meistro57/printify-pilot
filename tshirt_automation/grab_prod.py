# grab_prod.py
import requests
from config import PRINTIFY_API_KEY

BASE_URL = "https://api.printify.com/v1"

def get_products(shop_id):
    url = f"{BASE_URL}/shops/{shop_id}/products.json"
    
    headers = {
        'Authorization': f'Bearer {PRINTIFY_API_KEY}',
        'Content-Type': 'application/json;charset=utf-8',
        'User-Agent': 'PythonScript'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        products = response.json().get('data', [])
        for product in products:
            print(f"Product ID: {product['id']}, Name: {product['attributes']['name']}")
    else:
        print("Failed to fetch products")
        print(response.text)  # Print more details about the error

if __name__ == "__main__":
    shop_id = "your_shop_id_here"  # Replace with your actual Shop ID
    get_products(shop_id)
