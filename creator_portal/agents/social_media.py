"""Social Media Publishing Agent."""

from pathlib import Path
from datetime import datetime, timezone

LOG_PATH = Path(__file__).resolve().parents[1] / 'logs' / 'social_posts.log'
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def post_to_social(platform: str, content: str) -> dict:
    """Record a social media post to a log file."""
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = f"{timestamp}|{platform}|{content}\n"
    with LOG_PATH.open('a') as fh:
        fh.write(entry)
    return {'platform': platform, 'content': content, 'logged': True}
