import requests
import time
import uuid

BASE_URL = "http://localhost:8000/products"

DATA = [
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMTS103193_1.webp",
    "image_description": "Dark grey solid polo t-shirt with contrast collar trim, half sleeves, worn with blue jeans",
    "product_description": "Wrangler men's 100% cotton solid polo neck t-shirt, regular fit, breathable fabric, suitable for casual outdoor wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMSH008409_1.webp",
    "image_description": "Black solid full sleeve button-down shirt with collar, worn with blue jeans",
    "product_description": "Wrangler men's 100% cotton solid shirt, regular fit, full sleeves, versatile casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMSS009251_1.webp",
    "image_description": "Rust orange graphic sweatshirt with Wrangler logo, motorcycle print and crew neck, full sleeves",
    "product_description": "Wrangler men's 100% cotton graphic sweatshirt, regular fit, crew neck, full sleeves, soft and breathable casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMSS009250_1.webp",
    "image_description": "Dark grey graphic sweatshirt with Wrangler logo, motorcycle print and crew neck, full sleeves",
    "product_description": "Wrangler men's 100% cotton graphic sweatshirt, regular fit, crew neck, full sleeves, soft and breathable casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMSS009210_1.webp",
    "image_description": "Black solid crew neck sweatshirt with subtle Wrangler logo on chest, full sleeves",
    "product_description": "Wrangler men's 100% cotton solid sweatshirt, regular fit, crew neck, full sleeves, minimalist and comfortable casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMSH006696_1.jpg",
    "image_description": "Yellow checked button-down shirt with full sleeves and chest pocket, worn over a white t-shirt with light blue jeans",
    "product_description": "Wrangler men's checked shirt made from 76% cotton and 24% linen, regular fit, full sleeves, button closure, lightweight and breathable casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMTS006399_1.jpg",
    "image_description": "Red and blue colorblock polo t-shirt with white collar, half sleeves and Wrangler logo patches on chest",
    "product_description": "Wrangler men's 100% cotton colorblock polo t-shirt, relaxed fit, drop shoulder sleeves, button placket, comfortable casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMSH004519_1.webp",
    "image_description": "Grey and brown checked button-down shirt with full sleeves and chest pocket, worn over a white t-shirt with blue jeans",
    "product_description": "Wrangler men's cotton checked shirt, slim fit, full sleeves, cutaway collar, button closure, casual everyday wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMTS005564_1.webp",
    "image_description": "Black solid polo t-shirt with yellow and white contrast collar, half sleeves and small logo on chest",
    "product_description": "Wrangler men's cotton solid polo t-shirt, regular fit, half sleeves, contrast collar design, comfortable casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMTS005562_1.webp",
    "image_description": "Light pink solid polo t-shirt with black and white tipped collar and sleeve edges, half sleeves, worn with blue jeans",
    "product_description": "Wrangler men's cotton solid polo t-shirt, regular fit, half sleeves, contrast tipping on collar and sleeves, comfortable casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMTR007949_1.webp",
    "image_description": "Olive green solid trousers with straight fit and mid-rise waist, worn with white sneakers",
    "product_description": "Wrangler men's 100% cotton solid trousers, regular fit, mid-rise waist, comfortable and breathable casual wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMJN006775_1.jpg",
    "image_description": "Dark blue skinny fit jeans with light fade and rolled hems, low-rise waist, worn with white sneakers",
    "product_description": "Wrangler men's jeans made from 98% cotton and 2% spandex, skinny fit, low rise waist, five-pocket style, dark wash with light fade, comfortable stretch denim"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMJN006765_1.webp",
    "image_description": "Black slim fit jeans with clean look and rolled hems, low-rise waist, worn with black high-top shoes",
    "product_description": "Wrangler men's jeans made from cotton, polyester and spandex blend, slim tapered fit, low rise waist, five-pocket style, clean dark wash, flexible and comfortable wear"
  },
  {
    "id": str(uuid.uuid4()),
    "image_url": "WMJN004833_1.jpg",
    "image_description": "Light grey slim fit jeans with clean look and subtle fade, low-rise waist, worn with black sneakers",
    "product_description": "Wrangler men's jeans made from 98% cotton and 2% elastane, slim fit, low rise waist, five-pocket style, light grey wash with subtle fade, comfortable stretch denim"
  }
]

def seed():
    for item in DATA:
        attempt = 0
        max_attempts = 3
        res = None

        while attempt < max_attempts:
            attempt += 1
            try:
                res = requests.post(BASE_URL, json=item, timeout=5)
                break
            except (requests.ReadTimeout, requests.ConnectionError) as exc:
                print(f"WARNING: attempt {attempt}/{max_attempts} for {item['id']} failed: {exc}")
                if attempt >= max_attempts:
                    print(f"ERROR: request failed for {item['id']} after {max_attempts} attempts")
                    raise
                else:
                    time.sleep(1)
            except requests.RequestException as exc:
                print(f"ERROR: request failed for {item['id']}: {exc}")
                raise

        if res is None:
            raise RuntimeError(f"No response for item {item['id']}")

        if not res.ok:
            print(f"ERROR: seed failed for {item['id']} status={res.status_code} response={res.text}")
            res.raise_for_status()

        try:
            data = res.json()
        except ValueError as exc:
            print(f"ERROR: invalid JSON for {item['id']}: {exc}")
            raise

        print(item["id"], res.status_code, data)

    print("\n\nSeeding completed.")

if __name__ == "__main__":
    seed()