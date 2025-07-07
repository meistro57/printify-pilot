"""Product Creator Agent."""

from typing import List
from .metadata_gen import generate_metadata
from .image_gen import generate_images
from .prompt_generator import generate_prompts
from .blueprint_parser import Blueprint
from ..configs.config import PRINTIFY_API_KEY

# Placeholder using existing utils if available
try:
    from tshirt_automation.utils.printify_utils import upload_images_printify, create_product
except Exception:  # Module may not exist in tests
    upload_images_printify = None
    create_product = None


def create_product_from_blueprint(bp: Blueprint) -> dict:
    prompts = generate_prompts(bp)
    images = generate_images(prompts)
    metadata = generate_metadata(bp)

    result = {
        'prompts': prompts,
        'images': images,
        'metadata': metadata
    }

    if PRINTIFY_API_KEY and upload_images_printify and create_product:
        uploaded = upload_images_printify({'main': images[0]}, PRINTIFY_API_KEY)
        payload = create_product(metadata, uploaded, PRINTIFY_API_KEY)
        result['printify'] = payload
    return result
