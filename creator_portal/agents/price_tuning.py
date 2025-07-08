"""Dynamic price tuning based on profit analysis."""

from typing import List

_HISTORY: List[float] = []


def record_sale(price: float, cost: float) -> None:
    """Log a sale to track profit margins."""
    profit = price - cost
    _HISTORY.append(profit)


def suggest_price(current_price: float) -> float:
    """Return a suggested price based on average profit."""
    if not _HISTORY:
        return current_price
    avg_profit = sum(_HISTORY) / len(_HISTORY)
    # Aim for 20% higher than avg profit margin
    return round(current_price + avg_profit * 0.2, 2)
