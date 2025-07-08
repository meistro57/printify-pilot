from __future__ import annotations

import os
from pathlib import Path
import sys

# Reuse project root config
ROOT_CONFIG = Path(__file__).resolve().parents[2] / 'config.py'
if ROOT_CONFIG.exists():
    sys.path.append(str(ROOT_CONFIG.parent))
    from config import PRINTIFY_API_KEY, BASE_URL, OPENAI_API_KEY, require
    CELERY_BROKER_URL = getattr(sys.modules['config'], 'CELERY_BROKER_URL', os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'))
else:
    PRINTIFY_API_KEY = os.getenv('PRINTIFY_API_KEY', '')
    BASE_URL = os.getenv('BASE_URL', 'https://api.printify.com/v1')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    def require(keys: list[str] | None = None) -> None:
        missing = [k for k in (keys or ["PRINTIFY_API_KEY", "OPENAI_API_KEY"]) if not globals().get(k)]
        if missing:
            joined = ", ".join(missing)
            raise ValueError(f"Missing required config values: {joined}")
