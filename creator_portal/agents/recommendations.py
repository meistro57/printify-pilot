"""AI-driven design recommendations."""

from typing import List
from random import choice

STYLES = ["cosmic", "vintage", "minimal", "pop art"]
SUBJECTS = ["fox", "owl", "mountain", "wave"]


def design_recommendations(num: int = 3) -> List[str]:
    """Return dummy design recommendations."""
    recs = []
    for _ in range(num):
        style = choice(STYLES)
        subject = choice(SUBJECTS)
        recs.append(f"{style} {subject}")
    return recs
