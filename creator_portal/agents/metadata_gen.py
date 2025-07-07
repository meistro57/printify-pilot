"""Metadata Generation Agent."""

from .blueprint_parser import Blueprint


def generate_metadata(bp: Blueprint) -> dict:
    """Generate simple title and description from blueprint."""
    title = (bp.intent[:30] if bp.intent else 'New Product').title()
    description = f"An awesome design about {bp.intent}."
    tags = bp.keywords
    return {
        'title': title,
        'description': description,
        'tags': tags
    }
