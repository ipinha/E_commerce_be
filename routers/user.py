from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models.user
import schemas
from database import get_db
import schemas.user
from hash import Hash



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


    