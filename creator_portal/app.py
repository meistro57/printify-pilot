"""FastAPI backend for the Creator Portal."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agents.blueprint_parser import Blueprint, parse_blueprint
from .agents.prompt_generator import generate_prompts
from .agents.metadata_gen import generate_metadata
from .agents.product_creator import create_product_from_blueprint

app = FastAPI(title="Creator Portal")


class BlueprintPayload(BaseModel):
    data: str


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


def main():
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
