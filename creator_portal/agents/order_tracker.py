"""Order Tracking Agent."""

from typing import Dict, List


def get_order_statuses(order_ids: List[str]) -> Dict[str, str]:
    """Return dummy order statuses."""
    statuses = {}
    for oid in order_ids:
        statuses[oid] = 'processing'
    return statuses
