"""Blueprint Parser Agent.
Parses blueprint text or JSON into structured product data."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
import json

@dataclass
class Blueprint:
    intent: str
    tone: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    variant_notes: Optional[str] = None
    product_type: Optional[str] = None
    language: str = "en"


def parse_blueprint(data: str) -> Blueprint:
    """Parse a blueprint from text or JSON."""
    try:
        payload = json.loads(data)
        intent = payload.get("intent", "")
        tone = payload.get("tone")
        keywords = payload.get("keywords", [])
        variant_notes = payload.get("variant_notes")
        product_type = payload.get("product_type")
        language = payload.get("language", "en")
    except json.JSONDecodeError:
        # Fallback simple text parser
        intent = data.strip()
        tone = None
        keywords = []
        variant_notes = None
        product_type = None
        language = "en"
    return Blueprint(intent=intent, tone=tone, keywords=keywords,
                     variant_notes=variant_notes, product_type=product_type,
                     language=language)
