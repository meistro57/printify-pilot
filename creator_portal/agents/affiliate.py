"""Affiliate link management."""

from typing import Dict
from uuid import uuid4

_LINKS: Dict[str, Dict[str, int]] = {}


def generate_link(product_id: str) -> str:
    """Return a unique affiliate link id."""
    link_id = str(uuid4())
    _LINKS[link_id] = {"product_id": product_id, "clicks": 0}
    return link_id


def record_click(link_id: str) -> None:
    """Increment click count for the given link."""
    if link_id in _LINKS:
        _LINKS[link_id]["clicks"] += 1


def report() -> Dict[str, Dict[str, int]]:
    """Return affiliate link statistics."""
    return dict(_LINKS)
