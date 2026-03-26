from fastapi import APIRouter, HTTPException
from app.services.ai_provider import get_ai_provider
from app.services.qdrant_service import search

router = APIRouter()

def get_cached_ai():
    """Lazy initialization of AI provider on first use."""
    if not hasattr(get_cached_ai, '_instance'):
        get_cached_ai._instance = get_ai_provider()
    return get_cached_ai._instance

@router.post("")
def search_products(body: dict):
    query = body.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    ai = get_cached_ai()
    try:
        parsed = ai.parse_query(query)
        embedding = ai.get_embedding(query)
        results = search(embedding)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "parsed": parsed,
        "results": results
    }