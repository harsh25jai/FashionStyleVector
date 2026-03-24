# app/api/product.py
from fastapi import APIRouter
from app.models.product_schema import Product
from app.services.ai_provider import get_ai_provider
from app.services.qdrant_service import insert_product

router = APIRouter()
ai = get_ai_provider()

@router.post("/")
def add_product(product: Product):
    combined_text = f"""
    {product.title}
    {product.product_description}
    {product.image_description}
    {' '.join(product.tags)}
    {product.type} {product.color} {product.pattern or ''} {product.print or ''}
    """

    embedding = ai.get_embedding(combined_text)

    insert_product(product.id, embedding, product.dict())

    return {"status": "inserted"}