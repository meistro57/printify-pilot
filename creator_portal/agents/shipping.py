"""Shipping Provider Integration Agent."""

from typing import Dict


def get_shipping_rates(provider: str, destination: str) -> Dict[str, float]:
    """Return dummy shipping rates for a provider."""
    return {
        'provider': provider,
        'destination': destination,
        'rate': 4.99,
    }
