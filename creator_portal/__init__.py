"""Creator Portal package init."""

from pathlib import Path
from .plugins import load_plugins

PLUGINS_DIR = Path(__file__).resolve().parent / 'plugins'
load_plugins(str(PLUGINS_DIR))
