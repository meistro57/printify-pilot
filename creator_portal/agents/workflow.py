"""Workflow automation templates for repetitive tasks."""

from typing import Dict, List, Callable

_TEMPLATES: Dict[str, List[Callable[..., str]]] = {}


def register_template(name: str, steps: List[Callable[..., str]]) -> None:
    """Register a workflow template."""
    _TEMPLATES[name] = steps


def run_template(name: str) -> List[str]:
    """Execute a registered workflow template and return step results."""
    steps = _TEMPLATES.get(name, [])
    results: List[str] = []
    for step in steps:
        results.append(step())
    return results


def list_templates() -> List[str]:
    """Return the names of all registered templates."""
    return list(_TEMPLATES.keys())
