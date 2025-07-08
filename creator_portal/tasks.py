from celery import Celery
from .agents.blueprint_parser import parse_blueprint
from .agents.product_creator import create_product_from_blueprint
from .configs.config import CELERY_BROKER_URL

celery_app = Celery('creator_portal', broker=CELERY_BROKER_URL)


@celery_app.task
def create_product_task(data: str) -> dict:
    bp = parse_blueprint(data)
    return create_product_from_blueprint(bp)
