"""FastAPI backend for the Creator Portal."""

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from datetime import datetime

from .agents.blueprint_parser import Blueprint, parse_blueprint
from .agents.prompt_generator import generate_prompts
from .agents.metadata_gen import generate_metadata
from .agents.product_creator import create_product_from_blueprint
from .agents.assets import upload_asset
from .agents.order_tracker import get_order_statuses
from .agents.shipping import get_shipping_rates
from .agents.inventory import sync_inventory
from .agents.analytics import get_analytics, export_csv
from .agents.recommendations import design_recommendations
from .agents.social_media import post_to_social
from .agents.chat import add_message, get_messages
from .agents.ab_testing import choose_variant
from .agents.search import search_products, index_products
from .agents.marketplace import upload_design, list_designs
from .agents.affiliate import generate_link, record_click, report
from .agents.pricing import schedule_discount, list_schedules
from .agents.import_tools import import_products
from .agents.tax import calculate_tax
from .plugins import list_plugins
from .tasks import create_product_task, celery_app
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Creator Portal")


class BlueprintPayload(BaseModel):
    data: str


class BulkBlueprintPayload(BaseModel):
    items: list[str]


class MessagePayload(BaseModel):
    user: str
    text: str


class SocialPostPayload(BaseModel):
    platform: str
    content: str


class ABTestPayload(BaseModel):
    options: list[dict]


class OrdersPayload(BaseModel):
    order_ids: list[str]


class DesignPayload(BaseModel):
    name: str
    author: str
    url: str


class AffiliateLinkPayload(BaseModel):
    product_id: str


class AffiliateClickPayload(BaseModel):
    link_id: str


class DiscountPayload(BaseModel):
    product_id: str
    percent: float
    start: str
    end: str


class ImportPayload(BaseModel):
    platform: str
    items: list[dict]


class TaxPayload(BaseModel):
    amount: float
    region: str


@app.post('/blueprint/parse')
def blueprint_parse(payload: BlueprintPayload) -> Blueprint:
    return parse_blueprint(payload.data)


@app.post('/prompts/generate')
def prompts_generate(payload: BlueprintPayload):
    bp = parse_blueprint(payload.data)
    return generate_prompts(bp)


@app.post('/metadata/generate')
def metadata_generate(payload: BlueprintPayload):
    bp = parse_blueprint(payload.data)
    return generate_metadata(bp)


@app.post('/product/create')
def product_create(payload: BlueprintPayload):
    bp = parse_blueprint(payload.data)
    result = create_product_from_blueprint(bp)
    index_products([result['metadata']])
    return result


@app.post('/tasks/create_product')
def product_create_task(payload: BlueprintPayload):
    task = create_product_task.delay(payload.data)
    return {'task_id': task.id}


@app.post('/product/bulk_create')
def product_bulk_create(payload: BulkBlueprintPayload):
    results = []
    for item in payload.items:
        bp = parse_blueprint(item)
        res = create_product_from_blueprint(bp)
        results.append(res)
        index_products([res['metadata']])
    return results


@app.post('/assets/upload')
def asset_upload(file: UploadFile):
    path = upload_asset(file)
    return {'path': path}


@app.post('/orders/status')
def orders_status(payload: OrdersPayload):
    return get_order_statuses(payload.order_ids)


@app.get('/shipping/rates')
def shipping_rates(provider: str, destination: str):
    return get_shipping_rates(provider, destination)


@app.post('/inventory/sync')
def inventory_sync():
    return sync_inventory()


@app.get('/analytics/data')
def analytics_data():
    return get_analytics()


@app.get('/search/products')
def search_products_route(q: str):
    return search_products(q)


@app.post('/marketplace/upload')
def marketplace_upload(payload: DesignPayload):
    return upload_design(payload.name, payload.author, payload.url)


@app.get('/marketplace/list')
def marketplace_list():
    return list_designs()


@app.post('/affiliate/link')
def affiliate_link(payload: AffiliateLinkPayload):
    return {'link_id': generate_link(payload.product_id)}


@app.post('/affiliate/click')
def affiliate_click(payload: AffiliateClickPayload):
    record_click(payload.link_id)
    return {'ok': True}


@app.get('/affiliate/report')
def affiliate_report():
    return report()


@app.post('/pricing/schedule')
def pricing_schedule(payload: DiscountPayload):
    start = datetime.fromisoformat(payload.start)
    end = datetime.fromisoformat(payload.end)
    return schedule_discount(payload.product_id, payload.percent, start, end)


@app.get('/pricing/schedules')
def pricing_schedules():
    return list_schedules()


@app.post('/import/products')
def import_products_route(payload: ImportPayload):
    return import_products(payload.platform, payload.items)


@app.get('/tax/calc')
def tax_calc(amount: float, region: str):
    return {'tax': calculate_tax(amount, region)}


@app.get('/analytics/export', response_class=PlainTextResponse)
def analytics_export():
    return export_csv(get_analytics())


@app.get('/design/recommendations')
def design_recs(num: int = 3):
    return design_recommendations(num)


@app.post('/social/post')
def social_post(payload: SocialPostPayload):
    return post_to_social(payload.platform, payload.content)


@app.post('/chat/post')
def chat_post(payload: MessagePayload):
    return add_message(payload.user, payload.text)


@app.get('/chat/messages')
def chat_messages():
    return get_messages()


@app.get('/plugins/list')
def plugins_list():
    return list_plugins()


@app.post('/abtest/run')
def abtest_run(payload: ABTestPayload):
    return choose_variant(payload.options)


def main():
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
