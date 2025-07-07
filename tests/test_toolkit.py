import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from toolkit import MODULES

def test_known_commands():
    expected_keys = {'data-viewer', 'tshirt-automation', 'blueprint-review', 'product-reviewer', 'awakening-shirt', 'google-upload', 'fetch-products'}
    assert expected_keys == set(MODULES.keys())
