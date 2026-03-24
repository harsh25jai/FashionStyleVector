# app/api/recommend.py
from fastapi import APIRouter
from app.services.qdrant_service import search

router = APIRouter()

@router.post("/")
def recommend(body: dict):
    vector = body.get("vector")
    return search(vector)