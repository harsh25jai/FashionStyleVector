# app/api/recommend.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.recommendation_service import recommend_outfit
from app.services.recommendation_service import get_candidates


router = APIRouter()

class RecommendRequest(BaseModel):
    vector: List[float]

@router.post("/")
def recommend(body: dict):
    top_item = body.get("item")
    vector = body.get("vector")

    candidates = get_candidates(vector, "bottomwear")

    results = recommend_outfit(top_item, candidates)

    return results