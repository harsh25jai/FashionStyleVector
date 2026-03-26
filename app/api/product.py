# app/api/product.py
import textwrap
import re
from fastapi import APIRouter, HTTPException
from app.models.product_schema import Product
from app.services.ai_provider import get_ai_provider_cached
from app.services.qdrant_service import insert_product

router = APIRouter()

@router.post("")
def add_product(body: dict):
    id_value = body.get("id")
    if not id_value or not str(id_value).strip():
        raise HTTPException(400, "id required")

    image_desc = body.get("image_description")
    product_desc = body.get("product_description", "")

    if not image_desc:
        raise HTTPException(400, "image_description required")

    try:
        ai = get_ai_provider_cached()

        # 🔥 AI extraction
        structured = ai.extract_attributes(image_desc, product_desc)

        if isinstance(structured, str):
            import json
            structured = json.loads(structured)
        
        if "category" not in structured:
            raise HTTPException(500, "AI extraction failed")
        
        # merge base fields
        payload = {
            "id": id_value,
            "image_url": body.get("image_url"),
            "image_description": image_desc,
            "product_description": product_desc,
            **structured
        }

        # embedding text
        combined_text = f"""
        {payload.get('title')}
        {payload.get('product_description')}
        {payload.get('image_description')}
        {' '.join(payload.get('tags', []))}
        {payload.get('category')} {payload.get('type')} {payload.get('color')}
        {payload.get('pattern')} {payload.get('print')}
        """

        embedding = ai.get_embedding(combined_text)

        insert_product(payload["id"], embedding, payload)

        return {"status": "inserted", "payload": payload}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e