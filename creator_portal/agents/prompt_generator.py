"""Image Prompt Generator Agent."""

from typing import List
from .blueprint_parser import Blueprint

STYLE_TOKENS = {
    'vibe': ['cosmic', 'retro', 'minimal'],
    'symbol': ['fox', 'galaxy', 'sun'],
    'mod': ['vibrant', 'muted', 'high contrast'],
    'scene': ['portrait', 'landscape', 'abstract']
}


def generate_prompts(bp: Blueprint, num_variations: int = 5) -> List[str]:
    """Generate simple text prompts from a blueprint."""
    base = bp.intent or 'artwork'
    prompts = []
    for i in range(num_variations):
        vibe = STYLE_TOKENS['vibe'][i % len(STYLE_TOKENS['vibe'])]
        symbol = STYLE_TOKENS['symbol'][i % len(STYLE_TOKENS['symbol'])]
        mod = STYLE_TOKENS['mod'][i % len(STYLE_TOKENS['mod'])]
        scene = STYLE_TOKENS['scene'][i % len(STYLE_TOKENS['scene'])]
        prompts.append(f"{base} {vibe} {symbol} {mod} {scene}")
    return prompts
