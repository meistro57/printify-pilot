# app.py – Main Flask application entry point
from flask import Flask, render_template, request, jsonify
import openai
import config
from utils.phrase_utils import load_phrases, review_phrase
from utils.image_utils import generate_text_images

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_phrases', methods=['GET'])
def load_phrases_route():
    phrases = load_phrases('tshirt_list.txt')
    return jsonify(phrases)

@app.route('/review_phrase', methods=['POST'])
def review_phrase_route():
    data = request.json
    phrase = data['phrase']
    
    openai.api_key = config.OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Review this phrase for clarity and correctness: '{phrase}'"}]
    )
    
    review_text = response.choices[0].message.content
    approved = "approve" in review_text.lower()
    suggestion = review_text if not approved else None

    return jsonify({"review": review_text, "approved": approved, "suggestion": suggestion})

@app.route('/generate_text_images', methods=['POST'])
def generate_text_images_route():
    data = request.json
    phrase = data['phrase']
    
    images = generate_text_images(phrase)
    
    return jsonify(images)

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
