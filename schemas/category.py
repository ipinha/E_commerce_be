from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    
    name: str
    description: Optional[str] = None
    
class ShowCategory(CategoryBase):
    category_id:int
    class Config():
        orm_mode = True

