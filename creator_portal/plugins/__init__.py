"""Simple plugin loader."""

from importlib import util
from pathlib import Path

PLUGINS = {}


def load_plugins(directory: str) -> None:
    """Load all plugin modules from the given directory."""
    for path in Path(directory).glob('*.py'):
        if path.name == '__init__.py':
            continue
        spec = util.spec_from_file_location(path.stem, path)
        if spec and spec.loader:
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            PLUGINS[path.stem] = module


def list_plugins() -> list[str]:
    return list(PLUGINS.keys())
