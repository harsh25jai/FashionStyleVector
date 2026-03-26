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
    top_occ = set(top.get("occasion", []))
    bottom_occ = set(bottom.get("occasion", []))
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

    # return top N
    return [item for _, item in scored_items[:limit]]


# 📦 Optional: format output (clean API response)
def format_recommendations(results: List[Any]):
    formatted = []

    for r in results:
        formatted.append({
            "id": r.id,
            "score": r.score,
            "payload": r.payload
        })

    return formatted

from app.services.qdrant_service import search


def get_candidates(vector, category: str):
    return search(vector, {"category": category})