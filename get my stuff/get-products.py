import requests
import json
from config import PRINTIFY_API_KEY

BASE_URL = "https://api.printify.com/v1"

def get_products(shop_id):
    url = f"{BASE_URL}/shops/{shop_id}/products.json"
    
    headers = {
        'Authorization': f'Bearer {PRINTIFY_API_KEY}',
        'Content-Type': 'application/json;charset=utf-8',
        'User-Agent': 'PythonScript'
    }
    
    products = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={'page': page})
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('data'):
                break
            products.extend(data['data'])
            page += 1  # Move to next page
        else:
            print(f"Failed to fetch products (Page {page})")
            print(response.text)
            break
    
    return products

def main():
    shop_id = "your_shop_id_here"  # Replace with your actual Shop ID
    products = get_products(shop_id)
    if products:
        with open("printify_products.json", "w") as f:
            json.dump(products, f, indent=4)
        print("Product data saved to printify_products.json")
    else:
        print("No products retrieved.")


if __name__ == "__main__":
    main()
