import importlib
import os
import sys
import pytest


def reload_config():
    if 'config' in sys.modules:
        del sys.modules['config']
    return importlib.import_module('config')


def test_require_missing(monkeypatch):
    monkeypatch.delenv('PRINTIFY_API_KEY', raising=False)
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    cfg = reload_config()
    with pytest.raises(cfg.ConfigError):
        cfg.require()


def test_require_present(monkeypatch):
    monkeypatch.setenv('PRINTIFY_API_KEY', 'key')
    monkeypatch.setenv('OPENAI_API_KEY', 'key')
    cfg = reload_config()
    cfg.require()  # should not raise
