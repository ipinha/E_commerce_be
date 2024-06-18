from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models.user
import schemas
from database import get_db
import schemas.user
from hash import Hash
from  oauth2 import get_current_user



router = APIRouter (
    tags=['Users'],
    prefix='/user'
)


@router.post('/register')
def register(request : schemas.user.UserCreate,db :Session = Depends(get_db) ):
    new_user = models.user.User(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password),
        full_name = request.full_name,
        address = request.address,
        phone = request.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/role', response_model=dict)
def get_user_role(current_user: schemas.authentication.TokenData = Depends(get_current_user)):
    return {'isAdmin': current_user.is_admin}
    