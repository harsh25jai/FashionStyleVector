import requests

BASE_URL = "http://localhost:8000/products"

DATA = [  # shortened here, use your full dataset
    {
        "id": "WMTS103193_1.webp",
        "image_url": "WMTS103193_1.webp",
        "image_description": "Dark grey solid polo t-shirt with contrast collar trim, half sleeves, worn with blue jeans",
        "product_description": "Wrangler men's 100% cotton solid polo neck t-shirt"
    },
    {
        "id": "WMJN006775_1.jpg",
        "image_url": "WMJN006775_1.jpg",
        "image_description": "Dark blue skinny fit jeans with light fade and rolled hems",
        "product_description": "Wrangler men's skinny fit jeans"
    }
]

def seed():
    for item in DATA:
        res = requests.post(BASE_URL, json=item)
        print(item["id"], res.status_code, res.json())

if __name__ == "__main__":
    seed()