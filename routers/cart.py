from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import schemas.authentication
import schemas.cart
from  oauth2 import get_current_user
import schemas.user

router = APIRouter(
    tags=['Carts'],
    prefix='/cart'
)


@router.post('/add_to_cart')
def add_to_cart(request: schemas.cart.CartItemCreate, db: Session = Depends(get_db),current_user: schemas.authentication.TokenData = Depends(get_current_user)):
    user = db.query(models.user.User).filter(models.user.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    cart = db.query(models.cart.Cart).filter(models.cart.Cart.user_id == user.user_id).first()
    if not cart:
        cart = models.cart.Cart(
            user_id=user.user_id
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)
    cart_item = db.query(models.cart.CartItem).filter(
        models.cart.CartItem.cart_id == cart.cart_id,
        models.cart.CartItem.product_id == request.product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += request.quantity
    else:
        cart_item = models.cart.CartItem(
            cart_id=cart.cart_id,
            product_id=request.product_id,
            quantity=request.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    
    return {"message": "Item added to cart", "cart_item": cart_item}


@router.get('/cart', response_model=schemas.cart.ShowCart)
def get_cart(current_user: schemas.authentication.TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(models.cart.Cart).filter(models.cart.Cart.user_id == user.user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_items = db.query(models.cart.CartItem).filter(models.cart.CartItem.cart_id == cart.cart_id).all()
    cart_details = []
    for item in cart_items:
        product = db.query(models.product.Product).filter(models.product.Product.product_id== item.product_id).first()
        cart_details.append(schemas.cart.CartItem(
            product_id=item.product_id,
            product_name=product.name,
            quantity=item.quantity,
            current_price=product.price,
            cart_id=item.cart_id,
            cart_item_id=item.cart_item_id
        ))

    return schemas.cart.ShowCart(cart_id=cart.cart_id, user_id=user.user_id, items=cart_details)



@router.delete("/remove_from_cart/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db), current_user: schemas.authentication.TokenData = Depends(get_current_user)):
    user = db.query(models.user.User).filter(models.user.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    cart = db.query(models.cart.Cart).filter(models.cart.Cart.user_id == user.user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = db.query(models.cart.CartItem).filter(models.cart.CartItem.cart_item_id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if cart_item.cart_id != cart.cart_id:
        raise HTTPException(status_code=400, detail="Cart item does not belong to user's cart")

    db.delete(cart_item)
    db.commit()

    return {"message": "Cart item removed successfully"}
