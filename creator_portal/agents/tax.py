"""Simple regional tax calculation."""

from typing import Dict

_TAX_RATES: Dict[str, float] = {
    "us": 0.07,
    "eu": 0.20,
    "uk": 0.19,
}


def calculate_tax(amount: float, region: str) -> float:
    """Return the taxed amount for the region."""
    rate = _TAX_RATES.get(region.lower(), 0.0)
    return round(amount * rate, 2)
