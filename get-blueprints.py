import requests
import json
from config import PRINTIFY_API_KEY, BASE_URL

HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}

def get_blueprints():
    # Using the URL without a version prefix if confirmed to be correct
    url = f"{BASE_URL}/catalog/blueprints.json"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            blueprints = response.json()
            
            output_file = "blueprints_data.json"
            
            with open(output_file, 'w') as f:
                json.dump(blueprints, f, indent=4)
                
            print(f"Blueprints have been saved to {output_file}.")
        else:
            print(f"Failed to fetch blueprints. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print(f"An error occurred while making the request: {e}")

get_blueprints()
