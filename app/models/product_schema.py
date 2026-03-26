# app/models/product_schema.py
from pydantic import BaseModel, Field
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
    pattern: Optional[str] = Field(default=None)
    print: Optional[str] = Field(default=None)

    tags: List[str]