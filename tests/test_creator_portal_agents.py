import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from creator_portal.agents.analytics import get_analytics, export_csv
from creator_portal.agents.recommendations import design_recommendations
from creator_portal.agents.social_media import post_to_social
from creator_portal.agents.chat import add_message, get_messages
from creator_portal.agents.ab_testing import choose_variant
from creator_portal.agents.blueprint_parser import parse_blueprint
from creator_portal.agents.metadata_gen import generate_metadata
from creator_portal.agents.image_gen import generate_images
from creator_portal.agents.search import index_products, search_products
from creator_portal.agents.marketplace import upload_design, list_designs
from creator_portal.agents.affiliate import generate_link, record_click, report
from creator_portal.agents.pricing import schedule_discount, list_schedules
from creator_portal.agents.import_tools import import_products
from creator_portal.agents.tax import calculate_tax
from datetime import datetime
from creator_portal.plugins import list_plugins
from creator_portal.tasks import create_product_task, celery_app


def test_analytics_export():
    data = get_analytics()
    csv_text = export_csv(data)
    assert 'product' in csv_text
    assert csv_text.count('\n') >= 2


def test_design_recommendations():
    recs = design_recommendations(2)
    assert len(recs) == 2


def test_social_media_post(tmp_path, monkeypatch):
    # Redirect log path to temp directory
    from creator_portal.agents import social_media as sm
    monkeypatch.setattr(sm, 'LOG_PATH', tmp_path / 'log.txt')
    result = sm.post_to_social('twitter', 'hello')
    assert result['logged']
    assert sm.LOG_PATH.exists()


def test_chat_messages():
    add_message('alice', 'hi')
    assert get_messages()[0]['user'] == 'alice'


def test_choose_variant():
    opts = [{'title': 'A'}, {'title': 'B'}]
    result = choose_variant(opts)
    assert result in opts


def test_generate_metadata_persona():
    bp_data = '{"intent": "cosmic fox mug", "product_type": "mug"}'
    bp = parse_blueprint(bp_data)
    meta = generate_metadata(bp, persona='mystic')
    assert 'seo_keywords' in meta and meta['seo_keywords']


def test_image_api_generation():
    images = generate_images(['test prompt'], use_api=True)
    assert images[0].startswith('https://')


def test_search_index():
    index_products([{'title': 'Cosmic Mug', 'tags': ['mug', 'cosmic']}])
    results = search_products('cosmic')
    assert results


def test_plugins_loaded():
    assert 'sample_plugin' in list_plugins()


def test_celery_task(monkeypatch):
    celery_app.conf.task_always_eager = True
    res = create_product_task.delay('{"intent": "test"}').get()
    assert 'metadata' in res


def test_marketplace_upload_list():
    upload_design('design1', 'alice', 'http://example.com/img.png')
    assert list_designs()[0]['name'] == 'design1'


def test_affiliate_flow():
    link = generate_link('prod123')
    record_click(link)
    assert report()[link]['clicks'] == 1


def test_pricing_schedule():
    item = schedule_discount('prod', 10.0, datetime.utcnow(), datetime.utcnow())
    assert item in list_schedules()


def test_import_products():
    data = [{'title': 'A'}, {'title': 'B'}]
    res = import_products('etsy', data)
    assert res[0]['platform'] == 'etsy'


def test_tax_calc():
    assert calculate_tax(100.0, 'us') == 7.0
