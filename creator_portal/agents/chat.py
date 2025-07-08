"""In-app Chat Support Agent."""

from typing import List, Dict

MESSAGES: List[Dict[str, str]] = []


def add_message(user: str, text: str) -> Dict[str, str]:
    entry = {'user': user, 'text': text}
    MESSAGES.append(entry)
    return entry


def get_messages() -> List[Dict[str, str]]:
    return MESSAGES
