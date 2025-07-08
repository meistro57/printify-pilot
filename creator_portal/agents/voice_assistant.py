"""Simple voice assistant to trigger flows."""

from typing import Callable, Dict

_COMMANDS: Dict[str, Callable[[], str]] = {}


def register_command(phrase: str, func: Callable[[], str]) -> None:
    """Register a voice command."""
    _COMMANDS[phrase.lower()] = func


def trigger(phrase: str) -> str:
    """Trigger a registered command by phrase."""
    action = _COMMANDS.get(phrase.lower())
    if not action:
        return "unknown command"
    return action()
