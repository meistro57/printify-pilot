"""Image Generation Agent."""

from typing import List
from pathlib import Path
from urllib.parse import quote_plus


def _generate_image_api(prompt: str) -> str:
    """Return a URL to a dummy image generated via HTTP request."""
    url = f"https://dummyimage.com/512x512/000/fff.png&text={quote_plus(prompt)}"
    return url


def generate_images(prompts: List[str], use_api: bool = False) -> List[str]:
    """Generate images locally or via a simple API."""
    paths: List[str] = []
    if use_api:
        for prompt in prompts:
            paths.append(_generate_image_api(prompt))
        return paths

    out_dir = Path(__file__).resolve().parents[1] / 'images/temp'
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, prompt in enumerate(prompts):
        path = out_dir / f'image_{i}.png'
        path.touch()
        paths.append(str(path))
    return paths
