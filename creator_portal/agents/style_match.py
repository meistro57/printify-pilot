"""Style match retrieval from successful Etsy sellers."""

from typing import List, Dict

_SUCCESSFUL_STYLES: List[Dict[str, str]] = [
    {"title": "Sunset Tee", "style": "retro"},
    {"title": "Galaxy Mug", "style": "space"},
]


def match_style(style: str) -> List[str]:
    """Return product titles that match the requested style."""
    return [p["title"] for p in _SUCCESSFUL_STYLES if p["style"] == style]
