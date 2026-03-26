# app/api/product.py
import textwrap
import re
from fastapi import APIRouter, HTTPException
from app.models.product_schema import Product
from app.services.ai_provider import get_ai_provider_cached
from app.services.qdrant_service import insert_product

router = APIRouter()

@router.post("/")
def add_product(product: Product):
    combined_text = textwrap.dedent(f"""
    {product.title}
    {product.product_description}
    {product.image_description}
    {' '.join(product.tags)}
    {product.category}
    {product.type} {product.color} {product.pattern or ''} {product.print or ''}
    """).strip()
    combined_text = re.sub(r'\s+', ' ', combined_text)

    try:
        ai = get_ai_provider_cached()
        embedding = ai.get_embedding(combined_text)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail="embedding service failed"
        ) from e
    
    try:
        insert_product(product.id, embedding, product.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="failed to insert product"
        ) from e

    return {"status": "inserted"}