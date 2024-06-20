from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    total: float
    status: Optional[str] = "Pending"
    name:Optional[str]
    phone: Optional[str]
    address: Optional[str]
    order_items: List[OrderItemCreate]


class Order(OrderCreate):
    order_id: int

    class Config:
        orm_mode = True