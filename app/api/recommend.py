# app/api/recommend.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.qdrant_service import search

router = APIRouter()

class RecommendRequest(BaseModel):
    vector: List[float]

@router.post("/")
def recommend(req: RecommendRequest):
    return search(req.vector)