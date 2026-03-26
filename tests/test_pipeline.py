import requests

BASE_URL = "http://localhost:8000"


def test_search_basic():
    res = requests.post(f"{BASE_URL}/search", json={
        "query": "black polo tshirt"
    })

    assert res.status_code == 200
    data = res.json()

    assert "results" in data
    assert len(data["results"]) > 0


def test_search_fallback():
    res = requests.post(f"{BASE_URL}/search", json={
        "query": "purple dragon hoodie"
    })

    assert res.status_code == 200
    data = res.json()

    # should fallback to vector
    assert data["mode"] in ["relaxed_1", "relaxed_2", "vector_only"]


def test_recommendation():
    # simulate topwear
    top_item = {
        "category": "topwear",
        "color": "black",
        "pattern": "graphic",
        "fit": "regular",
        "occasion": ["casual"],
        "style_vectors": {
            "formality": 0.2,
            "boldness": 0.8,
            "sportiness": 0.3
        }
    }

    res = requests.post(f"{BASE_URL}/recommend", json={
        "item": top_item,
        "vector": [0.1] * 3072  # dummy vector
    })

    assert res.status_code == 200
    data = res.json()

    assert len(data) > 0


def test_end_to_end():
    # search → pick → recommend

    search_res = requests.post(f"{BASE_URL}/search", json={
        "query": "graphic tshirt"
    }).json()

    assert len(search_res["results"]) > 0

    first_item = search_res["results"][0]["payload"]

    rec_res = requests.post(f"{BASE_URL}/recommend", json={
        "item": first_item,
        "vector": [0.1] * 3072
    })

    assert rec_res.status_code == 200