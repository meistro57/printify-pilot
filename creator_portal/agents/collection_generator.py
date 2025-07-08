"""Merch collection generator agent."""

from typing import List, Optional

from .blueprint_parser import Blueprint
from .prompt_generator import generate_prompts
from .metadata_gen import generate_metadata

SEASONAL_COLLECTIONS = {
    'summer': ['sunset vibes', 'tropical waves', 'beach party'],
    'winter': ['snowflake dream', 'cozy cabin', 'mountain retreat'],
    'spring': ['floral bloom', 'fresh rain', 'garden walk'],
    'fall': ['harvest moon', 'pumpkin spice', 'autumn leaves'],
}

PERSONA_STYLES = {
    'gamer': ['pixel hero', 'retro console', 'high score'],
    'spiritual': ['chakra flow', 'mystic mandala', 'awakening mind'],
    'minimalist': ['simple line art', 'monochrome shapes', 'clean geometry'],
}


def generate_collection(persona: Optional[str] = None,
                         event: Optional[str] = None,
                         items: int = 3) -> List[dict]:
    """Generate a small merch collection based on persona or event."""
    themes: List[str] = []
    if persona and persona in PERSONA_STYLES:
        themes = PERSONA_STYLES[persona]
    elif event and event in SEASONAL_COLLECTIONS:
        themes = SEASONAL_COLLECTIONS[event]

    if not themes:
        themes = ['abstract vibe']

    results = []
    for theme in themes[:items]:
        bp = Blueprint(intent=theme, product_type='shirt')
        prompt = generate_prompts(bp, num_variations=1)[0]
        metadata = generate_metadata(bp)
        results.append({'theme': theme, 'prompt': prompt, 'metadata': metadata})
    return results
