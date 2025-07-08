import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from creator_portal.agents.analytics import get_analytics, export_csv
import creator_portal.agents.analytics as analytics
from creator_portal.agents.recommendations import design_recommendations
from creator_portal.agents.social_media import post_to_social
from creator_portal.agents.chat import add_message, get_messages
from creator_portal.agents.ab_testing import choose_variant
from creator_portal.agents.blueprint_parser import parse_blueprint
from creator_portal.agents.metadata_gen import generate_metadata
from creator_portal.agents.image_gen import generate_images
from creator_portal.agents.search import index_products, search_products, count_products
from creator_portal.agents.marketplace import upload_design, list_designs, delete_design
from creator_portal.agents.affiliate import generate_link, record_click, report
from creator_portal.agents.pricing import schedule_discount, list_schedules
from creator_portal.agents.import_tools import import_products
from creator_portal.agents.tax import calculate_tax
from creator_portal.agents.workflow import register_template, run_template, list_templates
from creator_portal.agents.voice_assistant import register_command, trigger
from creator_portal.agents.feedback import add_review, get_reviews, average_rating
from creator_portal.agents.price_tuning import record_sale, suggest_price
from creator_portal.agents.style_match import match_style
from creator_portal.agents.collection_generator import generate_collection
from datetime import datetime
from creator_portal.plugins import list_plugins
from creator_portal.tasks import create_product_task, celery_app
from creator_portal.agents.demand_forecasting import forecast_demand, propose_templates


def test_analytics_export():
    data = get_analytics()
    csv_text = export_csv(data)
    assert 'product' in csv_text
    assert csv_text.count('\n') >= 2


def test_average_sales():
    data = get_analytics()
    assert analytics.average_sales(data) == 7.5


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


def test_search_count():
    index_products([{'title': 'Sunset Tee', 'tags': ['retro']}])
    assert count_products('retro') >= 1


def test_plugins_loaded():
    assert 'sample_plugin' in list_plugins()


def test_celery_task(monkeypatch):
    celery_app.conf.task_always_eager = True
    res = create_product_task.delay('{"intent": "test"}').get()
    assert 'metadata' in res


def test_marketplace_upload_list():
    upload_design('design1', 'alice', 'http://example.com/img.png')
    assert list_designs()[0]['name'] == 'design1'


def test_marketplace_delete():
    upload_design('temp', 'bob', 'url')
    assert delete_design('temp')
    assert not any(d['name'] == 'temp' for d in list_designs())


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

def test_workflow_template():
    register_template('demo', [lambda: 'a', lambda: 'b'])
    assert run_template('demo') == ['a', 'b']


def test_workflow_list():
    assert 'demo' in list_templates()


def test_voice_assistant():
    register_command('start', lambda: 'ok')
    assert trigger('start') == 'ok'


def test_feedback_loop():
    add_review('p1', 'great', rating=4.0)
    assert get_reviews('p1')[0] == 'great'
    assert average_rating('p1') == 4.0


def test_price_tuning():
    record_sale(12.0, 5.0)
    record_sale(15.0, 5.0)
    new_price = suggest_price(10.0)
    assert new_price > 10.0


def test_style_match():
    results = match_style('retro')
    assert 'Sunset Tee' in results


def test_collection_generator():
    items = generate_collection(persona='gamer', items=2)
    assert len(items) == 2
    assert 'metadata' in items[0]
def test_demand_forecasting():
    niches = forecast_demand(top_n=2)
    assert len(niches) == 2
    templates = propose_templates(niches)
    assert len(templates) == 2
    assert 'intent' in templates[0]

