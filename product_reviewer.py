import requests
import json
import time
import openai
from config import PRINTIFY_API_KEY, BASE_URL, OPENAI_API_KEY

# OpenAI Setup
openai.api_key = OPENAI_API_KEY

# Headers for Printify API
HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}

# Fetch all shops
def get_shops():
    url = f"{BASE_URL}/shops.json"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

# Fetch all products from a shop
def get_products(shop_id):
    url = f"{BASE_URL}/shops/{shop_id}/products.json"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get("data", []) if response.status_code == 200 else None

# Evaluate and improve product descriptions
def evaluate_description(title, description):
    prompt = f"""
    You are an expert eCommerce product description editor.
    Your task is to analyze and refine descriptions for T-shirts and apparel.
    
    **Instructions:**
    1. Keep the original intent but make it more engaging, compelling, and optimized for sales.
    2. Do NOT change the product type (this is a T-shirt, NOT a book, mug, etc.).
    3. Keep descriptions concise yet impactful (2-4 sentences max).
    4. Maintain the theme of the original description.
    5. If the description is already good, reply only with "GOOD". Otherwise, provide an improved version.

    **Product Title:** {title}
    **Current Description:** {description}

    Your response:
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert product description editor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    ai_response = response.choices[0].message.content.strip()

    # Check if AI made a mistake (e.g., called a T-shirt a book)
    if "book" in ai_response.lower() or "mug" in ai_response.lower():
        print("⚠️ AI made a mistake! Retrying...")
        return evaluate_description(title, description)  # Re-run AI evaluation

    return ai_response

# Update product description on Printify
def update_product_description(shop_id, product_id, new_description):
    url = f"{BASE_URL}/shops/{shop_id}/products/{product_id}.json"
    payload = {"description": new_description}
    response = requests.put(url, headers=HEADERS, json=payload)

    return response.status_code == 200

# Main execution
def main():
    print("Fetching shops...")
    shops = get_shops()

    if not shops:
        print("No shops found. Exiting.")
        exit()

    for shop in shops:
        shop_id = shop["id"]
        print(f"\nFetching products for Shop ID: {shop_id} ({shop['title']})...")
        products = get_products(shop_id)

        if not products:
            print("No products found.")
            continue

        for product in products:
            product_id = product.get("id")
            title = product.get("title", "Untitled Product")
            description = product.get("description", "No description available")

            print(f"\n🔹 Evaluating: {title} (ID: {product_id})")
            ai_response = evaluate_description(title, description)

            if ai_response == "GOOD":
                print("✅ Description is already good. Skipping.")
                continue

            print("\n⚠️ Suggested New Description:")
            print(ai_response)

            user_input = input("\nApprove new description? (yes/no/exit): ").strip().lower()

            if user_input == "yes":
                print("Updating description...")
                success = update_product_description(shop_id, product_id, ai_response)

                if success:
                    print("✅ Update successful!")
                else:
                    print("❌ Failed to update product.")

            elif user_input == "exit":
                print("Exiting process.")
                exit()

            else:
                print("⏩ Skipping product.")

            time.sleep(2)  # Pause to avoid rate limits


if __name__ == "__main__":
    main()
