"""Tools for importing data from other platforms."""

from typing import List, Dict


def import_products(platform: str, items: List[Dict]) -> List[Dict]:
    """Pretend to convert competitor data into our format."""
    converted = []
    for item in items:
        converted.append({
            "title": item.get("title", ""),
            "platform": platform,
        })
    return converted
