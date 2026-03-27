# app/services/qdrant_service.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.core.config import QDRANT_URL, COLLECTION_NAME

client = QdrantClient(url=QDRANT_URL)

def init_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )


def insert_product(product_id, vector, payload):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[{
            "id": product_id,
            "vector": vector,
            "payload": payload
        }]
    )


def search(vector, filters=None):
    return client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=5,
        query_filter=filters
    )