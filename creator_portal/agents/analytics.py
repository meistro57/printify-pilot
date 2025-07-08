"""Analytics Dashboard Agent."""

from typing import List, Dict
from io import StringIO
import csv


SAMPLE_DATA: List[Dict[str, int]] = [
    {"product": "Shirt", "views": 100, "sales": 10},
    {"product": "Mug", "views": 50, "sales": 5},
]


def get_analytics() -> List[Dict[str, int]]:
    """Return demo analytics data."""
    return SAMPLE_DATA


def export_csv(data: List[Dict[str, int]]) -> str:
    """Export analytics data as a CSV string."""
    if not data:
        return ""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()
