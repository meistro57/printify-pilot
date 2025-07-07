import requests
import json
import datetime
from config import PRINTIFY_API_KEY, BASE_URL

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}

# Fetch all shops linked to the Printify account
def get_shops():
    url = f"{BASE_URL}/shops.json"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching shops: {response.text}")
        return None

# Fetch all products from a given shop
def get_products(shop_id):
    url = f"{BASE_URL}/shops/{shop_id}/products.json"
    response = requests.get(url, headers=HEADERS)
    
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON response.")
        return None

    if response.status_code == 200 and "data" in data:
        return data["data"]  # Extract product list
    else:
        print(f"Unexpected API response structure: {data}")
        return None

# Save all shop and product data into a JSON file (WITH IMAGES)
def save_data(shops):
    structured_data = {
        "fetched_at": datetime.datetime.now().isoformat(),
        "shops": []
    }

    for shop in shops:
        shop_id = shop["id"]
        products = get_products(shop_id) or []

        structured_data["shops"].append({
            "id": shop_id,
            "title": shop["title"],
            "products": [
                {
                    "id": product.get("id", "N/A"),
                    "title": product.get("title", "Untitled Product"),
                    "description": product.get("description", "No description available").split("\n")[0],
                    "tags": product.get("tags", []),
                    "images": [image["src"] for image in product.get("images", [])],  # Extracting image URLs
                    "enabled_variants": [
                        {
                            "title": variant.get("title", "Unknown Variant"),
                            "price": variant.get("price", 0) / 100,
                            "stock": variant.get("quantity", 0)
                        }
                        for variant in product.get("variants", []) if variant.get("is_enabled", False)
                    ]
                }
                for product in products
            ]
        })

    with open("shop_products.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4)

    print("\n✅ Data saved to shop_products.json")

# Run the script
def main():
    print("Fetching shops...")
    shops = get_shops()

    if shops:
        save_data(shops)
    else:
        print("No shops found.")


if __name__ == "__main__":
    main()
