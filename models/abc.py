# from sqlalchemy import Column, Integer, DECIMAL, String, TIMESTAMP, ForeignKey
# from sqlalchemy.orm import relationship
# from database import Base
# import datetime








# class Payment(Base):
#     __tablename__ = "payments"

#     payment_id = Column(Integer, primary_key=True, index=True)
#     order_id = Column(Integer, ForeignKey("orders.order_id"))
#     amount = Column(DECIMAL(10, 2), nullable=False)
#     payment_method = Column(String(50))
#     payment_date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
#     status = Column(String(50), default="Pending")

#     order = relationship("Order", back_populates="payments")
