from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

import schemas, database, models
from database import get_db
from hash import Hash
from JWTtoken import create_access_token, verify_token
from  oauth2 import get_current_user
router = APIRouter(
    tags=['Authentication']
)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
    

    access_token = create_access_token(data={"sub": user.email, "is_admin": user.is_admin})
    return {'access_token': access_token, 'token_type': "bearer"}



    