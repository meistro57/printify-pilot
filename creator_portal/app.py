"""FastAPI backend for the Creator Portal."""

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

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
    return create_product_from_blueprint(bp)


@app.post('/product/bulk_create')
def product_bulk_create(payload: BulkBlueprintPayload):
    results = []
    for item in payload.items:
        bp = parse_blueprint(item)
        results.append(create_product_from_blueprint(bp))
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


@app.post('/abtest/run')
def abtest_run(payload: ABTestPayload):
    return choose_variant(payload.options)


def main():
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
