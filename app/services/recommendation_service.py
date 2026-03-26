from typing import List, Dict, Any


# 🎯 Core compatibility scoring
def is_compatible(top: Dict[str, Any], bottom: Dict[str, Any]) -> float:
    score = 0.0

    # 1. Category pairing (must-have)
    if top.get("category") == "topwear" and bottom.get("category") == "bottomwear":
        score += 2.0

    # 2. Color contrast (avoid same color outfits)
    if top.get("color") and bottom.get("color"):
        if top["color"] != bottom["color"]:
            score += 1.0
        else:
            score -= 0.5

    # 3. Pattern balance
    top_pattern = top.get("pattern")
    bottom_pattern = bottom.get("pattern")

    if top_pattern == "graphic" and bottom_pattern == "solid":
        score += 2.0
    elif top_pattern == "solid" and bottom_pattern == "solid":
        score += 1.0
    elif top_pattern == "graphic" and bottom_pattern == "graphic":
        score -= 1.0  # too noisy

    # 4. Fit balance
    if top.get("fit") == "oversized" and bottom.get("fit") == "slim":
        score += 1.0
    elif top.get("fit") == bottom.get("fit"):
        score += 0.5

    # 5. Occasion match
    # Guard against occasion being None or a string
    top_occasion = top.get("occasion", [])
    if top_occasion is None:
        top_occasion = []
    elif isinstance(top_occasion, str):
        top_occasion = [top_occasion]
    top_occ = set(top_occasion)

    bottom_occasion = bottom.get("occasion", [])
    if bottom_occasion is None:
        bottom_occasion = []
    elif isinstance(bottom_occasion, str):
        bottom_occasion = [bottom_occasion]
    bottom_occ = set(bottom_occasion)

    if top_occ and bottom_occ and top_occ.intersection(bottom_occ):
        score += 1.0

    # 6. Style vector similarity
    top_style = top.get("style_vectors", {})
    bottom_style = bottom.get("style_vectors", {})

    if top_style and bottom_style:
        diff = sum(
            abs(top_style.get(k, 0) - bottom_style.get(k, 0))
            for k in ["formality", "boldness", "sportiness"]
        )
        score += max(0, 2.0 - diff)  # closer → better

    return score


# 🔍 Combine vector score + compatibility score
def combine_scores(vector_score: float, compatibility_score: float) -> float:
    return vector_score + (0.2 * compatibility_score)


# 🧠 Main recommendation logic
def recommend_outfit(
    top_item: Dict[str, Any],
    candidates: List[Any],  # Qdrant results
    limit: int = 5
):
    scored_items = []

    for item in candidates:
        payload = item.payload or {}

        compatibility_score = is_compatible(top_item, payload)

        final_score = combine_scores(item.score, compatibility_score)

        scored_items.append((final_score, item))

    # sort descending
    scored_items.sort(key=lambda x: x[0], reverse=True)

    # return top N with final_score preserved
    top_items = scored_items[:limit]
    # Attach final_score to each item for downstream use
    for final_score, item in top_items:
        item.final_score = final_score
    return [item for _, item in top_items]


# 📦 Optional: format output (clean API response)
def format_recommendations(results: List[Any]):
    formatted = []

    for r in results:
        # Use final_score if available (from recommend_outfit reranking), otherwise fall back to vector score
        score = getattr(r, 'final_score', r.score)
        formatted.append({
            "id": r.id,
            "score": score,
            "payload": r.payload
        })

    return formatted

from app.services.qdrant_service import search
from qdrant_client.models import Filter, FieldCondition, MatchValue


def get_candidates(vector, category: str):
    # Build proper Qdrant Filter instead of plain dict
    category_filter = Filter(
        must=[FieldCondition(key="category", match=MatchValue(value=category))]
    )
    return search(vector, category_filter)