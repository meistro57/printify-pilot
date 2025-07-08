"""User-contributed design marketplace."""

from typing import List, Dict

# In-memory marketplace store
_DESIGNS: List[Dict[str, str]] = []


def upload_design(name: str, author: str, url: str) -> Dict[str, str]:
    """Add a design to the marketplace."""
    design = {"name": name, "author": author, "url": url}
    _DESIGNS.append(design)
    return design


def list_designs() -> List[Dict[str, str]]:
    """Return all uploaded designs."""
    return list(_DESIGNS)


def delete_design(name: str) -> bool:
    """Remove a design by name. Returns True if deleted."""
    for i, design in enumerate(_DESIGNS):
        if design.get("name") == name:
            del _DESIGNS[i]
            return True
    return False
