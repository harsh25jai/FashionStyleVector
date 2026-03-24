# app/models/product_schema.py
from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    id: str
    title: str
    image_url: str
    product_description: str
    image_description: str

    type: str
    category: str

    color: str
    pattern: Optional[str]
    print: Optional[str]

    tags: List[str]