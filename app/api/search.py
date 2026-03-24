# app/api/search.py
from fastapi import APIRouter
from app.services.ai_provider import get_ai_provider
from app.services.qdrant_service import search

router = APIRouter()
ai = get_ai_provider()

@router.post("/")
def search_products(body: dict):
    query = body.get("query")

    parsed = ai.parse_query(query)

    embedding = ai.get_embedding(query)

    results = search(embedding)

    return {
        "parsed": parsed,
        "results": results
    }