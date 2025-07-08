"""Demand Forecasting Agent."""

from typing import List, Dict

# Sample market data representing sales volume by niche
_MARKET_DATA: List[Dict[str, int]] = [
    {"niche": "space art", "sales": 300},
    {"niche": "y2k aesthetic", "sales": 250},
    {"niche": "retro gaming", "sales": 200},
    {"niche": "minimalist yoga", "sales": 150},
]


def forecast_demand(top_n: int = 3) -> List[str]:
    """Return the top N niches by sales volume."""
    sorted_data = sorted(_MARKET_DATA, key=lambda d: d["sales"], reverse=True)
    return [item["niche"] for item in sorted_data[:top_n]]


def propose_templates(niches: List[str]) -> List[Dict[str, object]]:
    """Propose blueprint templates based on trending niches."""
    templates: List[Dict[str, object]] = []
    for niche in niches:
        keywords = niche.split()
        templates.append({
            "intent": f"{niche} design",
            "tone": "trend",
            "keywords": keywords,
        })
    return templates

