# phrase_utils.py – Phrase loading and AI review functions
import openai

# phrase_utils.py – Improved Phrase loading function
def load_phrases(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

def review_phrase(phrase, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Review this phrase for clarity and correctness: '{phrase}'"}]
    )
    review = response.choices[0].message.content
    return {'review': review, 'approved': 'approve' in review.lower()}
