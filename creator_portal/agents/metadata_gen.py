"""Metadata Generation Agent."""

from .blueprint_parser import Blueprint
from typing import List

PERSONA_PREFIXES = {
    'mystic': 'Embrace the cosmic energy with',
    'witty': 'Add a dash of humor with',
    'minimalist': 'Clean lines meet simplicity in',
}

SEO_KEYWORDS = {
    'mug': ['coffee mug', 'ceramic mug', 'gift idea'],
    'shirt': ['t-shirt', 'cotton tee', 'fashion'],
}

TRANSLATIONS = {
    'es': 'Un diseño asombroso sobre',
    'fr': 'Un design incroyable sur',
}


def generate_metadata(bp: Blueprint, language: str = 'en', persona: str | None = None) -> dict:
    """Generate simple title and description from blueprint with persona and SEO."""
    title = (bp.intent[:30] if bp.intent else 'New Product').title()
    desc_base = 'An awesome design about'
    prefix = TRANSLATIONS.get(language, desc_base)
    description = f"{prefix} {bp.intent}."
    if persona and persona in PERSONA_PREFIXES:
        description = f"{PERSONA_PREFIXES[persona]} {bp.intent}."
    tags: List[str] = list(bp.keywords)
    seo_terms = SEO_KEYWORDS.get(bp.product_type or '', [])
    tags.extend(seo_terms)
    return {
        'title': title,
        'description': description,
        'tags': tags,
        'seo_keywords': seo_terms,
    }
