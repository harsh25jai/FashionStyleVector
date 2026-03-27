import json
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

print("Imports loaded successfully.")

# Load environment variables
load_dotenv(override=True)

config_summary = {
    "OPENAI_API_KEY_present": bool(os.getenv("OPENAI_API_KEY")),
    "OPENAI_MODEL": os.getenv("OPENAI_MODEL"),
}

print("Config summary:", config_summary)

# Initialize FastAPI app
app = FastAPI(title="Fashion Product Search API")

# Mount the assets folder for static file serving
assets_path = Path(__file__).parent / "assets"
if assets_path.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")
    print(f"Assets folder mounted at /assets")
else:
    print("Warning: assets folder not found")

print()

# Fashion product data
products = [
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
        "image_description": "Yellow checked button-down shirt with full sleeves and chest pocket",
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
        "image_description": "Grey and brown checked button-down shirt with full sleeves and chest pocket",
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

print("Fashion product data loaded.")
print(f"Number of products: {len(products)}")
print()

# Chat model helper
def get_chat_model(provider: str):
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in .env")
        if not model:
            raise ValueError("OPENAI_MODEL is not set in .env")
        return ChatOpenAI(model=model, api_key=api_key)

    raise ValueError("provider must be 'openai' or 'ollama'")

provider = "openai"  # Change to "ollama" if you want to use Ollama.
llm = get_chat_model(provider)
print("Model ready.")
print()

# Product search prompt
search_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a fashion product search assistant. Given a user query and a list of products, identify which products best match the query. Return the matching product IDs as a JSON array.",
        ),
        (
            "human",
            """User query: {query}

            Available products:
            {products_list}

            Return ONLY a JSON array of matching product IDs. If no products match, return an empty array [].
            Example: ["id1", "id2"]""",
        ),
    ]
)

def search_products(query: str, base_url: str = "http://localhost:8000") -> list:
    """Search for products matching the user query and return matching product details."""
    # Format products list for the prompt
    products_list = json.dumps(
        [
            {
                "id": p["id"],
                "image_description": p["image_description"],
                "product_description": p["product_description"],
            }
            for p in products
        ],
        indent=2,
    )
    
    messages = search_prompt.format_messages(query=query, products_list=products_list)
    response = llm.invoke(messages)
    
    try:
        # Extract JSON array from response
        matching_ids = json.loads(response.content.strip())
        
        # Get full product details for matching IDs and add proper image URLs
        matching_products = []
        for p in products:
            if p["id"] in matching_ids:
                product_with_url = p.copy()
                product_with_url["image_url"] = f"{base_url}/assets/{p['image_url']}"
                matching_products.append(product_with_url)
        
        return matching_products
    except json.JSONDecodeError:
        return []

print("Product search helper ready.")
print()

# FastAPI endpoints

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Fashion Product Search API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search?query=your_search_query",
            "products": "/products",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/products")
async def get_all_products():
    """Get all products with proper image URLs."""
    base_url = "http://localhost:8000"
    products_with_urls = []
    for p in products:
        product_with_url = p.copy()
        product_with_url["image_url"] = f"{base_url}/assets/{p['image_url']}"
        products_with_urls.append(product_with_url)
    
    return {
        "total": len(products_with_urls),
        "products": products_with_urls
    }

@app.get("/search")
async def search(query: str):
    """Search for products by query.
    
    Example: /search?query=black+polo+tshirt
    """
    base_url = "http://localhost:8000"
    
    if not query or len(query.strip()) == 0:
        return JSONResponse(
            status_code=400,
            content={"error": "Query parameter is required and cannot be empty"}
        )
    
    print(f"Searching for: {query}")
    results = search_products(query, base_url)
    
    return {
        "query": query,
        "total_results": len(results),
        "products": results
    }

client = TestClient(app)


def call_search_api(payload: dict):
    response = client.get("/search", params=payload)
    print(f"Status: {response.status_code}")
    print(response.json())
    print("-" * 80)

def call_product_api(payload: dict):
    response = client.get("/products", params=payload)
    print(f"Status: {response.status_code}")
    print(response.json())
    print("-" * 80)

def call_health_api():
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    print(response.json())
    print("-" * 80)


print("Test client ready.")


call_search_api(
    {"query": "black polo t-shirt"}
)

call_search_api(
    {"query": "tshirt with motorcycle print"}
)

call_search_api(
    {"query": "rust tshirt with motorcycle print"}
)

call_search_api(
    {"query": "half sleeve red and blue polo with wrangler logo"}
)

call_search_api(
    {"query": "bottomwear with straight fit and mid-rise waist"}
)

call_search_api(
    {"query": "bottomwear for pink tshirt"}
)

call_search_api(
    {"query": "recommend only shirt for jeans"}
)

# call_health_api()

# call_product_api({})
# Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000