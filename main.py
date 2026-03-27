# main.py
from fastapi import FastAPI
from app.api import search, product, recommend
from app.services.qdrant_service import init_collection

app = FastAPI()

@app.on_event("startup")
def startup():
    init_collection()

app.include_router(product.router, prefix="/products")
app.include_router(search.router, prefix="/search")
app.include_router(recommend.router, prefix="/recommend")