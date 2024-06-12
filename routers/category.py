from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models.category
import schemas
from database import get_db
import schemas.category
from typing import List



router = APIRouter (
    tags=['Category'],
    prefix='/category'
)

@router.get('/all',response_model=List[schemas.category.ShowCategory])
def show_all(db:Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No categories found")
    return categories


@router.post('/create', )
def create(category: schemas.category.CategoryBase, db : Session = Depends(get_db)):
    new_category = models.category.Category(
        name = category.name,
        description = category.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.put('/update/{id}', status_code=status.HTTP_201_CREATED)
def update(id : int, category : schemas.category.CategoryBase, db:Session = Depends(get_db) ):
    u_category = db.query(models.category.Category).filter(models.category.Category.category_id == id).first()
    if not u_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"category with id {id} not found")
    u_category.name = category.name
    u_category.description = category.description
    db.commit()
    db.refresh(u_category)
    return {'cap nhat thanh cong'}

@router.get('/show/{id}', response_model=schemas.category.ShowCategory, status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    category = db.query(models.category.Category).filter(models.category.Category.category_id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id {id} not found")
    return category


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, db: Session = Depends(get_db)):
    d_category = db.query(models.Category).filter(models.Category.category_id == id).first()
    if not d_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id {id} not found")
    db.delete(d_category)
    db.commit()
    return {"detail": "Deletion successful"}