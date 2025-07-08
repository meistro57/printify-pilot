"""Design feedback loop via customer reviews."""

from typing import List, Dict

_REVIEWS: List[Dict[str, float | str]] = []


def add_review(product_id: str, review: str, rating: float | None = None) -> Dict[str, float | str]:
    """Store a review for a product with optional rating."""
    item: Dict[str, float | str] = {"product_id": product_id, "review": review}
    if rating is not None:
        item["rating"] = rating
    _REVIEWS.append(item)
    return item


def get_reviews(product_id: str) -> List[str]:
    """Return all reviews for the product."""
    return [r["review"] for r in _REVIEWS if r["product_id"] == product_id]


def average_rating(product_id: str) -> float:
    """Return the average rating for the product or 0.0 if none."""
    ratings = [float(r.get("rating", 0)) for r in _REVIEWS if r["product_id"] == product_id and "rating" in r]
    if not ratings:
        return 0.0
    return sum(ratings) / len(ratings)
