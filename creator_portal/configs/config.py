from pathlib import Path
import sys

# Reuse project root config
ROOT_CONFIG = Path(__file__).resolve().parents[2] / 'config.py'
if ROOT_CONFIG.exists():
    sys.path.append(str(ROOT_CONFIG.parent))
    from config import PRINTIFY_API_KEY, BASE_URL, OPENAI_API_KEY
else:
    PRINTIFY_API_KEY = ''
    BASE_URL = 'https://api.printify.com/v1'
    OPENAI_API_KEY = ''
