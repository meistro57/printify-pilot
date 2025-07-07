from flask import Flask, send_from_directory, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "shop_products.json"
EXPORT_FILE = "selected_products.json"

def load_data():
    """Load product data from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"shops": [], "fetched_at": "N/A"}

@app.route("/")
def index():
    """Serve the compiled frontend."""
    return send_from_directory("webpack-app/dist", "index.html")


@app.route("/<path:path>")
def static_files(path):
    """Serve static files from the webpack build."""
    return send_from_directory("webpack-app/dist", path)

@app.route("/data")
def get_data():
    """Provide JSON data to the frontend."""
    return jsonify(load_data())

@app.route("/export", methods=["POST"])
def export_selected():
    """Export selected products with full details and ensure file integrity."""
    data = request.json
    selected_items = data.get("selectedProducts", [])

    if not selected_items:
        print("❌ No products selected.")
        return jsonify({"error": "No products selected"}), 400

    full_data = load_data()
    selected_products = []

    # Debugging: Print all available product IDs in the system
    all_product_ids = {product["id"] for shop in full_data["shops"] for product in shop["products"]}
    print(f"🔎 Available Product IDs: {all_product_ids}")

    print(f"🔍 Selected Items: {selected_items}")

    for shop in full_data["shops"]:
        for product in shop["products"]:
            for selected in selected_items:
                if product["id"] == selected["productId"] and shop["id"] == selected["shopId"]:
                    print(f"✅ Matched: {product['title']} (ID: {product['id']})")
                    selected_products.append(product)

    if not selected_products:
        print("⚠️ No matching products found! Double-check the IDs.")

    try:
        with open(EXPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(selected_products, f, indent=4)
        print(f"📁 Exported {len(selected_products)} products to {EXPORT_FILE}")
    except Exception as e:
        print(f"❌ Error writing to file: {e}")
        return jsonify({"error": "Failed to write file"}), 500

    return jsonify({"message": "Export successful!", "count": len(selected_products)})


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
