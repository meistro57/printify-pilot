"""Discount scheduling agent."""

from typing import List, Dict
from datetime import datetime

_SCHEDULED: List[Dict[str, str]] = []


def schedule_discount(product_id: str, percent: float, start: datetime, end: datetime) -> Dict[str, str]:
    """Schedule a price discount."""
    item = {
        "product_id": product_id,
        "percent": percent,
        "start": start.isoformat(),
        "end": end.isoformat(),
    }
    _SCHEDULED.append(item)
    return item


def list_schedules() -> List[Dict[str, str]]:
    """Return all scheduled discounts."""
    return list(_SCHEDULED)
