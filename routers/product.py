from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models.product
import schemas
from database import get_db
import schemas.product
import schemas.user
from typing import List
from oauth2 import get_current_user

router = APIRouter(
    tags=['Product'],
    prefix='/product'
)


@router.get('/all', response_model=List[schemas.product.Product])
def show_all(db: Session = Depends(get_db)):
    products = db.query(models.product.Product).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No products found")
    return products


@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(product : schemas.product.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.product.Product(
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock,
        category_id = product.category_id,
        image_url = product.image_url

    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put('/update/{id}')
def update(id:int, product : schemas.product.ProductBase , db:Session = Depends(get_db), current_user: schemas.authentication.TokenData = Depends(get_current_user)):
    user = db.query(models.user.User).filter(models.user.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_admin:
        u_product = db.query(models.product.Product).filter(models.product.Product.product_id ==id).first()
        if not u_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"product with id {id} not found")
        
        for field, value in product.dict().items():
            setattr(u_product, field, value)
        db.commit()
        db.refresh(u_product)
        return {'cap nhat thanh cong'}


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, db: Session = Depends(get_db)):
    d_product = db.query(models.product.Product).filter(models.product.Product.product_id == id).first()
    if not d_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id {id} not found")
    db.delete(d_product)
    db.commit()
    return {"detail": "Deletion successful"}

@router.get('/show/{id}', response_model=schemas.product.Product, status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    product = db.query(models.product.Product).filter(models.product.Product.product_id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id {id} not found")
    return product

