import pytest
from fastapi.testclient import TestClient

from main import app
from app.services.qdrant_service import init_collection
from scripts.seed_data import DATA

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def client():
    init_collection()
    with TestClient(app) as client:
        for item in DATA:
            resp = client.post("/products", json=item)
            assert resp.status_code == 200

        yield client

    # teardown
    init_collection()  # clean up data


def test_search_basic(client):
    res = client.post("/search", json={"query": "black polo tshirt"})

    assert res.status_code == 200
    data = res.json()

    assert "results" in data
    assert len(data["results"]) > 0


def test_search_fallback(client):
    res = client.post("/search", json={"query": "purple dragon hoodie"})

    assert res.status_code == 200
    data = res.json()

    # should fallback to vector
    assert data["mode"] in ["relaxed_1", "relaxed_2", "vector_only"]


def test_recommendation(client):
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

    res = client.post("/recommend", json={"item": top_item, "vector": [0.1] * 3072})

    assert res.status_code == 200
    data = res.json()

    assert len(data) > 0


def test_end_to_end(client):
    # search → pick → recommend

    search_response = client.post("/search", json={"query": "graphic tshirt"})
    assert search_response.status_code == 200
    search_res = search_response.json()

    assert len(search_res["results"]) > 0

    first_item = search_res["results"][0]["payload"]

    rec_res = client.post("/recommend", json={"item": first_item, "vector": [0.1] * 3072})
    assert rec_res.status_code == 200
