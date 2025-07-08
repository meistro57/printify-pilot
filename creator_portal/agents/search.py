"""Simple product search engine."""

from typing import List, Dict

PRODUCT_INDEX: List[Dict] = []


def index_products(products: List[Dict]) -> None:
    """Add products to the in-memory search index."""
    PRODUCT_INDEX.extend(products)


def search_products(term: str) -> List[Dict]:
    """Return products whose title or tags contain the search term."""
    term = term.lower()
    results = []
    for product in PRODUCT_INDEX:
        title = product.get('title', '').lower()
        tags = [t.lower() for t in product.get('tags', [])]
        if term in title or any(term in t for t in tags):
            results.append(product)
    return results
