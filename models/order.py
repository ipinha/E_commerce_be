from sqlalchemy import Column, Integer, DECIMAL, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    total = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(50), default="Pending")
    phone = Column(String(20))  
    address = Column(String(200))  

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")



class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

