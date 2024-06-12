from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    cart_id: int
    class Config:
        orm_mode = True

class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int
    class Config:
        orm_mode = True   

class CartItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    current_price: float
    cart_id: Optional[int] = None
    cart_item_id: Optional[int] = None

    class Config:
        orm_mode = True

class ShowCart(BaseModel):
    cart_id: int
    user_id: int
    items: List[CartItem]
