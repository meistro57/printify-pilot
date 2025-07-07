"""Metadata Generation Agent."""

from .blueprint_parser import Blueprint

TRANSLATIONS = {
    'es': 'Un diseño asombroso sobre',
    'fr': 'Un design incroyable sur',
}


def generate_metadata(bp: Blueprint, language: str = 'en') -> dict:
    """Generate simple title and description from blueprint."""
    title = (bp.intent[:30] if bp.intent else 'New Product').title()
    desc_base = 'An awesome design about'
    prefix = TRANSLATIONS.get(language, desc_base)
    description = f"{prefix} {bp.intent}."
    tags = bp.keywords
    return {
        'title': title,
        'description': description,
        'tags': tags
    }
