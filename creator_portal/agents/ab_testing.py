"""A/B Testing Agent."""

from typing import List, Dict
from random import choice


def choose_variant(options: List[Dict[str, str]]) -> Dict[str, str]:
    """Return a randomly selected option as the winning variant."""
    if not options:
        raise ValueError('options must not be empty')
    return choice(options)
