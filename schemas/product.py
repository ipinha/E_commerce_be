from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    class Config:
        orm_mode = True

class Product(ProductBase):
    class Config:
        orm_mode = True
