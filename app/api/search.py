from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_provider import get_ai_provider_cached
from app.services.qdrant_service import search

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

@router.post("")
def search_products(req: SearchRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query is required")
    
    try:
        ai = get_ai_provider_cached()

        parsed = ai.parse_query(req.query)
        embedding = ai.get_embedding(req.query)

        results, mode = smart_search(embedding, parsed)

        results = rerank(results, parsed)

        return {
            "query": req.query,
            "parsed": parsed,
            "mode": mode,
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

def smart_search(vector, parsed):
    # 1. strict
    results = search(vector, parsed)

    if results:
        return results, "strict"

    # 2. remove weakest filters (pattern/print first)
    relaxed = parsed.copy()
    relaxed.pop("pattern", None)
    relaxed.pop("print", None)

    results = search(vector, relaxed)
    if results:
        return results, "relaxed_1"

    # 3. only type/category
    minimal = {}
    if "type" in parsed:
        minimal["type"] = parsed["type"]
    if "category" in parsed:
        minimal["category"] = parsed["category"]

    results = search(vector, minimal)
    if results:
        return results, "relaxed_2"

    # 4. pure vector fallback
    results = search(vector, {})
    return results, "vector_only"

def rerank(results, parsed):
    scored = []

    for r in results:
        score = r.score
        payload = r.payload

        # boost exact matches
        for key, value in parsed.items():
            if payload.get(key) == value:
                score += 0.1

        # special boost for print/tag match
        if parsed.get("print") and parsed["print"] in payload.get("tags", []):
            score += 0.2

        scored.append((score, r))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [r for _, r in scored]