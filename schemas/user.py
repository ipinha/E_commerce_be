from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password:str