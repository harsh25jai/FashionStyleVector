from fastapi import APIRouter, HTTPException
from app.services.ai_provider import get_ai_provider
from app.services.qdrant_service import search

router = APIRouter()
ai = get_ai_provider()

@router.post("")
def search_products(body: dict):
    try:
        query = body.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")

        parsed = ai.parse_query(query)
        embedding = ai.get_embedding(query)

        results = search(embedding)

        return {
            "parsed": parsed,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))