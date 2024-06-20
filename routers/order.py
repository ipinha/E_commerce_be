from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models.order
import schemas
from database import get_db
import schemas.order
from typing import List
from  oauth2 import get_current_user


router = APIRouter (
    tags=['Order'],
    prefix='/order'
)


@router.post('/create_order')
def new_order(order: schemas.order.OrderCreate, db : Session = Depends(get_db), current_user: schemas.authentication.TokenData = Depends(get_current_user)):
    user = db.query(models.user.User).filter(models.user.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_model = models.order.Order (
        user_id = user.user_id,
        total = order.total,
        name = order.name,
        status = order.status,
        phone = order.phone,
        address = order.address 
    )
    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    for item in order.order_items:
        new_oder_details = models.order.OrderItem (
            order_id = new_model.order_id,
            product_id = item.product_id,
            quantity = item.quantity,
            price = item.price
        )
        db.add(new_oder_details)

    db.commit()
    return new_model


@router.get('/orders', response_model=List[schemas.order.Order])
def get_user_orders(current_user: schemas.authentication.TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    orders = db.query(models.order.Order).filter(models.order.Order.user_id == user.user_id).all()
    return orders

@router.get('/orders/{order_id}', response_model=schemas.order.Order)
def get_order_by_id(order_id: int, current_user: schemas.authentication.TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    order = db.query(models.order.Order).filter(models.order.Order.order_id == order_id, models.order.Order.user_id == user.user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    
    return order

@router.put('/orders/{order_id}', response_model=schemas.order.Order)
def update_order_status(order_id: int, status: str, current_user: schemas.authentication.TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order = db.query(models.order.Order).filter(models.order.Order.order_id == order_id, models.order.Order.user_id == user.user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order