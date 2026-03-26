# app/api/product.py
from fastapi import APIRouter, HTTPException
from app.models.product_schema import Product
from app.services.ai_provider import get_ai_provider
from app.services.qdrant_service import insert_product

router = APIRouter()

def get_cached_ai():
    """Lazy initialization of AI provider on first use."""
    if not hasattr(get_cached_ai, '_instance'):
        get_cached_ai._instance = get_ai_provider()
    return get_cached_ai._instance

@router.post("/")
def add_product(product: Product):
    combined_text = f"""
    {product.title}
    {product.product_description}
    {product.image_description}
    {' '.join(product.tags)}
    {product.category}
    {product.type} {product.color} {product.pattern or ''} {product.print or ''}
    """

    try:
        ai = get_cached_ai()
        embedding = ai.get_embedding(combined_text)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail="embedding service failed"
        )
    
    try:
        insert_product(product.id, embedding, product.dict())
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="failed to insert product"
        )

    return {"status": "inserted"}