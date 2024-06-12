from sqlalchemy import Boolean, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    address = Column(Text)
    phone = Column(String(20))
    is_admin = Column(Boolean, default=False)
    carts = relationship("Cart", back_populates="user")
    # orders = relationship("Order", back_populates="user")
