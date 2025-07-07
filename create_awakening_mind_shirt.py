import requests
import json
import openai
from PIL import Image, ImageDraw, ImageFont
from config import PRINTIFY_API_KEY, BASE_URL, OPENAI_API_KEY

# OpenAI Setup
openai.api_key = OPENAI_API_KEY

# Headers for Printify API
HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}

# 🏪 Get Printify Shop ID
def get_shop_id():
    url = f"{BASE_URL}/shops.json"
    response = requests.get(url, headers=HEADERS)
    shops = response.json()
    if response.status_code == 200 and shops:
        return shops[0]["id"]  # Use first available shop
    return None

# 🎨 Generate a Text-Based Image for the T-Shirt
def create_text_image(text, output_path="design.png"):
    width, height = 2400, 3200  # Printify standard resolution
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 200)  # Adjust size for visibility
    except IOError:
        font = ImageFont.load_default()  # Use default font if custom font fails
    
    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    draw.text(position, text, font=font, fill="black")
    image.save(output_path)
    return output_path

# 📤 Upload Image to Printify
def upload_image(image_path):
    headers = {"Authorization": f"Bearer {PRINTIFY_API_KEY}"}
    
    with open(image_path, "rb") as file:
        response = requests.post(f"{BASE_URL}/uploads/images.json", headers=headers, files={"file": file})
    
    if response.status_code == 200:
        image_data = response.json()
        return image_data["id"]
    else:
        print("❌ Image upload failed:", response.text)
        return None

# 🤖 AI Generates an Original Awakening Mind T-Shirt Quote
def generate_awakening_mind_quote():
    prompt = """
    You are creating a powerful and thought-provoking T-shirt design for the Awakening Mind collection.
    Your goal is to inspire deep thinking, self-awareness, and spiritual growth.
    
    - Keep it short (4-10 words).
    - It should be catchy, deep, and original.
    - Avoid generic clichés, make it truly unique.

    Example ideas:
    - "Consciousness is the New Currency"
    - "Decode Reality, Expand Awareness"
    - "Your Frequency Shapes Your Reality"

    Generate 3 unique T-shirt sayings:
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a creative thinker designing T-shirt slogans."},
                  {"role": "user", "content": prompt}],
        temperature=0.8
    )

    return response.choices[0].message.content.strip().split("\n")

# 🛒 Create the Printify Product
def create_printify_product(shop_id, title, description, image_id):
    url = f"{BASE_URL}/shops/{shop_id}/products.json"
    
    product_data = {
        "title": title,
        "description": description,
        "blueprint_id": 31,  # Replace with a real blueprint ID
        "print_provider_id": 1,  # Replace with real provider ID
        "variants": [
            {"id": 9155, "price": 1999, "is_enabled": True},  # Replace with real variant ID
            {"id": 9156, "price": 2199, "is_enabled": True}
        ],
        "print_areas": [
            {
                "variant_ids": [9155, 9156],  # Use actual variant IDs
                "place": "front",
                "images": [
                    {
                        "id": image_id,  # Use the uploaded text image
                        "x": 0.5,
                        "y": 0.5,
                        "scale": 1,
                        "angle": 0
                    }
                ],
                "placeholders": [
                    {
                        "position": "front",
                        "height": 1800,  # Example dimensions
                        "width": 2400
                    }
                ]
            }
        ],
        "images": [image_id]  # Use the uploaded image for display
    }

    response = requests.post(url, headers=HEADERS, json=product_data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to create product. Response: {response.text}")
        return None

# 🚀 Publish the Product
def publish_product(shop_id, product_id):
    url = f"{BASE_URL}/shops/{shop_id}/products/{product_id}/publish.json"
    payload = {
        "title": True,
        "description": True,
        "images": True,
        "variants": True,
        "tags": True,
        "categories": True
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.status_code == 200

# 🚦 MAIN EXECUTION 🚦
def main():
    print("Fetching Printify Shop ID...")
    shop_id = get_shop_id()

    if not shop_id:
        print("❌ No shop found! Exiting.")
        exit()

    print("\n💡 Generating original Awakening Mind T-shirt ideas...")
    shirt_sayings = generate_awakening_mind_quote()

    for i, saying in enumerate(shirt_sayings, 1):
        print(f"{i}. {saying}")

    choice = input("\nChoose a T-shirt quote (1-3) or type 'new' to generate again: ").strip()

    if choice.lower() == "new":
        shirt_sayings = generate_awakening_mind_quote()
        for i, saying in enumerate(shirt_sayings, 1):
            print(f"{i}. {saying}")
        choice = input("\nChoose a T-shirt quote (1-3): ").strip()

    try:
        chosen_saying = shirt_sayings[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ Invalid choice. Exiting.")
        exit()

    title = chosen_saying
    description = f"This exclusive Awakening Mind T-shirt features the phrase '{chosen_saying}'. A bold statement for those who see beyond the illusion. Made for seekers, visionaries, and awakened minds."

    print(f"\n🖼️ Generating text-based design for '{title}'...")
    image_path = create_text_image(chosen_saying)

    print("\n📤 Uploading design to Printify...")
    image_id = upload_image(image_path)

    if not image_id:
        print("❌ Image upload failed. Cannot create product.")
        exit()

    print(f"\n🛠️ Creating T-shirt: '{title}' with image ID: {image_id}...")
    new_product = create_printify_product(shop_id, title, description, image_id)

    if new_product and "id" in new_product:
        product_id = new_product["id"]
        print(f"✅ T-shirt '{title}' created successfully! (ID: {product_id})")

        confirm_publish = input("\nDo you want to publish this product? (yes/no): ").strip().lower()
        if confirm_publish == "yes":
            if publish_product(shop_id, product_id):
                print("🚀 Product published successfully!")
            else:
                print("❌ Failed to publish product.")
        else:
            print("📌 Product saved as draft.")
    else:
        print("❌ Failed to create product.")


if __name__ == "__main__":
    main()
