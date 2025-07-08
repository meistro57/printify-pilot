"""Design feedback loop via customer reviews."""

from typing import List, Dict

_REVIEWS: List[Dict[str, str]] = []


def add_review(product_id: str, review: str) -> Dict[str, str]:
    """Store a review for a product."""
    item = {"product_id": product_id, "review": review}
    _REVIEWS.append(item)
    return item


def get_reviews(product_id: str) -> List[str]:
    """Return all reviews for the product."""
    return [r["review"] for r in _REVIEWS if r["product_id"] == product_id]
