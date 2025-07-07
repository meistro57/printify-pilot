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

app = FastAPI(title="Creator Portal")


class BlueprintPayload(BaseModel):
    data: str


class BulkBlueprintPayload(BaseModel):
    items: list[str]


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


def main():
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
