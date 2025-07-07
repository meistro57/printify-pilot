# printify_utils.py – Printify API integration
import requests

def upload_images_printify(images, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    uploaded_ids = {}
    for key, path in images.items():
        files = {'file': open(path, 'rb')}
        response = requests.post("https://api.printify.com/v1/uploads/images.json", headers=headers, files=files)
        uploaded_ids[key] = response.json()['id']
    return uploaded_ids

def create_product(details, image_ids, api_key):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "title": details['title'],
        "description": details['description'],
        "tags": details['tags'],
        "variants": [
            {"color": "light", "image_id": image_ids['black']},
            {"color": "dark", "image_id": image_ids['white']}
        ]
    }
    response = requests.post("https://api.printify.com/v1/shops/YOUR_SHOP_ID/products.json", headers=headers, json=data)
    return response.json()
