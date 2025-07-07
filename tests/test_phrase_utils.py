import types
import sys
import os

# Ensure repository root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Insert dummy openai module before importing phrase_utils
openai_dummy = types.ModuleType('openai')
openai_dummy.ChatCompletion = types.SimpleNamespace(create=lambda **kwargs: types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content='Approve'))]))
sys.modules['openai'] = openai_dummy

from phrase_utils import load_phrases, review_phrase

class DummyOpenAI:
    def __init__(self):
        self.ChatCompletion = types.SimpleNamespace(create=self.create)
    def create(self, model, messages):
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content='Approve'))])

def test_load_phrases(tmp_path):
    text = """\n#comment\nfirst\nsecond\n   \n#another\nthird\n"""
    f = tmp_path / 'phrases.txt'
    f.write_text(text)
    assert load_phrases(str(f)) == ['first', 'second', 'third']

def test_review_phrase(monkeypatch):
    dummy = DummyOpenAI()
    monkeypatch.setattr('phrase_utils.openai', dummy)
    result = review_phrase('something', 'key')
    assert result['review'] == 'Approve'
    assert result['approved']
